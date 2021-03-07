from __future__ import with_statement, print_function, division, unicode_literals 

import sys 
import os.path as op 
from functools import wraps 
import datetime 
from datetime import timedelta 
from collections import defaultdict, namedtuple 
from zipfile import ZipFile 
from io import BytesIO 
from decimal import Decimal 

# If the Python version is less than 3 then we import a different set of dependencies
if sys.version_info[0] < 3:
    range = xrange 
    from itertools import izip as zip 
    from urllib2 import urlopen 

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()
else: 
# for Python 3 
    from urllib.request import urlopen 

    def iteritems(d):
        return d.items()

    def itervalues(d):
        return d.values()

_DIRNAME = op.realpath(op.dirname(__file__))
CURRENCY_FILE = op.join(_DIRNAME, 'eurofxref-hist.zip')
ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'
SINGLE_DAY_ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip'

# this namedtuple is used as a range for the currency price where first_date is the startprice and last_date is the end price
Bounds = namedtuple('Bounds', 'first_date last_date') 

__all__ = ['CurrencyConverter',
            'S3CurrencyConverter',
            'RateNotFoundError',
            'ECB_URL',
            'SINGLE_DAY_ECB_URL']

def memoize(function):
    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args not in memo:
            memo[args] = function(*args)
        return memo[args]
    return wrapper 

@memoize 
def list_dates_between(first_date, last_date):
    """Returns all dates from first to last included."""
    return [first_date + timedelta(days=n)
            for n in range(1 + (last_date - first_date).days)]

@memoize 
def parse_date(s):
    """Fast %Y-%m-%d parsing."""
    try: 
        return datetime.date(int(s[:4]), int(s[5:7]), int(s[8:10]))
    except ValueError: # other accepted format using in one-day data set 
        return datetime.datetime.strptime(s, '%d %B %Y').date()

def get_lines_from_zip(zip_str):
    zip_file = ZipFile(BytesIO(zip_str)) # unzips file and reads it 
    for name in zip_file.namelist():
        for line in zip_file.read(name).decode('utf-8').splitlines():
            yield line 


class RateNotFoundError(Exception):
    """Custom exception when data is missing inn the rates file."""
    pass 

class CurrencyConverter(object):
    """
    At init, load the historic currencies since 1999 from the ECB. 
    The rates are EUR foreign exchange reference rates:

    Date,USB,JPY,BGN,CYP,CZK,...
    2018-02-23,1.2345,123.8,2.8495,N/A,27.435,...
    2018-01-12,1.4325,...

    ``_rates`` is a dictionary with:
    * currencies is keys 
    * {date: rate, ...} as values 

    ``currencies`` is a set of all available currencies.
    ``bounds`` is a dict if first and last date available per currency.
    """
    # this is the default constructor that will assign the below values 
    # as default for var1 = CurrencyConverter() 
    def __init__(self, 
                 currency_file=CURRENCY_FILE,
                 fallback_on_wrong_date=False,
                 fallback_on_missing_rate=False,
                 fallback_on_missing_rate_method="linear_interpolation",
                 ref_currency='EUR',
                 na_values=frozenset(['', 'N/A']),
                 decimal=False, 
                 verbose=False):
        """
        Instantiate a CurrencyConverter. 

        :param str currency_file: Path to the source data. Can be a local path, 
            or an URL starting with 'http://' or 'https://'. Defaults to the 
            European Central Bank historial rates file included in the package.
        
        :param bool fallback_on_wrong_date: Set to False (default) to raise a RateNotFoundError 
        when dates are requested outside the data's range.
        Set to True to extrapolate rates for dates outside the source data's 
        range. The extrapolation is done by falling back to the first or last data point, for dates before and after the data's range, 
        respectively. 

        :param bool fallback_on_missing_rate: Set to True to linearly interpolate missing rates by 
        their two closed valid rates. This only affects dates within the source data's range. Default false. 

        :param bool fallback_on_missing_rate_method: Choose the fallback on missing rate method. Default 
        is "linear_interpolation", also available is "last_known". 
        
        :param str ref_currency: Three-letter currency code for the currency 
        that the source data is oriented towards. This is EUR for the default
        European Central Bank data, and so the default is 'EUR'. 

        :param iterable na_values: What to interpret as missing values in the source data. 

        :param decimal: Set to True to use decimal. Decimal internally, this will slow the loading time but will allow exact conversions

        :param verbose: Set to True to print what is going on under the hood. 
        """
        # Global options 
        # example instantiation of self._rates = [[date(1), date(2), date(3)], [date(4), date(5), date(6)]] where each array in the 2d array represents a currency
        # each rate in self._rates has a date
        self.fallback_on_wrong_date = fallback_on_wrong_date
        self.fallback_on_missing_rate = fallback_on_missing_rate 
        self.fallback_on_missing_rate_method = fallback_on_missing_rate_method 
        self.ref_currency = ref_currency 
        self.na_values = na_values 
        self.cast = Decimal if decimal else float 
        self.verbose = verbose 

        # Will be filled once the file is loaded 
        self._rates = None 
        self.bounds = None 
        self.currencies = None 

        if currency_file is not None: # if currency file arg is passed, pass the file to load_file function
            self.load_file(currency_file)

    def load_file(self, currency_file):
        """
        To be subclassed if alternate methods of loading data
        """
        if currency_file.startswith(('http://', 'https://')):
            content = urlopen(currency_file).read() # if file is a url then open it with urlopen() and read page contents
        else:
            with open(currency_file, 'rb') as f:
                content = f.read() # if a local file is passed then just read it 

        if currency_file.endswith('.zip'):
            self.load_lines(get_lines_from_zip(content)) # if it is zip file then get the lines from that zip file(by calling that specific function) then call load_lines function to process those lines 
        else:
            self.load_lines(content.decode('utf-8').splitlines()) # else then split lines using splitlines() and pass that data to load_lines()

    def load_lines(self, lines):
        _rates = self._rates = defaultdict(dict)
        na_values = self.na_values 
        cast = self.cast 

        lines = iter(lines)
        header = next(lines).strip().split(',')[1:]

        for line in lines:
            line = line.strip().split(',')
            date = parse_date(line[0])
            for currency, rate in zip(header, line[1:]):
                currency = currency.strip()
                if rate not in na_values and currency: # if rate not in values frozenset then skip the empty currency
                    _rates[currency][date] = cast(rate)

            self.currencies = set(self._rates) | set([self.ref_currency])
            self._compute_bounds()

            for currency in sorted(self._rates):
                self._set_missing_to_none(currency) # this function fills missing rates of a currency with the closed available ones 
                if self.fallback_on_missing_rate: # if fallback_on_missing_rate == True then use appropriate method 
                    method = self.fallback_on_missing_rate_method
                    if method == "linear_interpolation":
                        self._use_linear_interpolation(currency)
                    elif method == "last_known":
                        self._use_last_known(currency)
                    else:
                        # if fallback method is not either of the two above then throw ValueError 
                        raise ValueError("Unknown fallback method {0!r}".format(method))


    def _compute_bounds(self):
        # self.bounds is a dict with entries in format:
        # key = currency name
        # value = (first_date, last_date)
        self.bounds = dict((currency, Bounds(min(r), max(r)))
                            # the value of self.bounds is a namedtuple where first date is in [0] and last date is in [1] positions
                            for currency, r in iteritems(self._rates)) 
                            # here currency is the key, r is the value
                            
        # this changing the value of self.bounds from ('first_date last_date') 
        # to b.first_date and b.last_date where b is the value
        self.bounds[self.ref_currency] = Bounds(
            min(b.first_date for b in itervalues(self.bounds)),
            max(b.last_date for b in itervalues(self.bounds))
        )

    def _set_missing_to_none(self, currency):
        """ 
        This function fills missing rates of a currency with the closed 
        available ones.
        """
        # the value of _rates dict which is in format: ('first_date last_date') will be assigned to rates variable 
        rates = self._rates[currency]
        # extracting first_date and last_date from self.bounds's value which is a named tuple with values ('first_date last_date')
        first_date, last_date = self.bounds[currency]

        for date in list_dates_between(first_date, last_date):
            if date not in rates:
                # if the list of dates inbetween first and last date are not the first_date or last_date values in rates then 
                # each date in that list of dates will be added to rates along with a value of None 
                rates[date] = None 

        if self.verbose:
            # if in verbose mode then print out all the missing rates to sysout
            missing = len([r for r in itervalues(rates) if r is None]) # for each value in rates if a value is empty(None) then add it to an array, finally count the length of the array to get the total # of missing rates 
            if missing:
                print('{0}: {1} missing rates from {2} to {3} ({4} days)').format(
                    currency, missing, first_date, last_date,
                    1 + (last_date - first_date).days) 

    def _use_linear_interpolation(self, currency):
        """
        Fill missing rates of a currency.

        This is done by linear interpolation of the two closed available rates
        (which is the first method of calculating missing rates).
        :param str currency: The currency to fill missing rates for.
        """
        rates = self._rates[currency]
        
        # tmp will store the closest rates forward and backward 
        tmp = defaultdict(lambda: [None, None]) # default value for this dict would be array containing [None, None]

        for date in sorted(rates):
            rate = rates[date]
            if rate is not None:
                # for every date in rates, if date is not null then current date iteration would be the closest_date 
                # and distribution would be set/reset to 0 
                closest_rate = rate 
                dist = 0
            else:
                # if date is null then distribution is incremented +1 and that date key is added to tmp(defaultdict) and given the value of [closest_date, dist value]
                dist += 1
                tmp[date][0] = closest_rate, dist 

        for date in sorted(rates, reverse=True):
            # iterating thru sorted rates, assign each value to rate var, if rate is not null then closest_rate is give rate's value
            # and dist is set/reset to 0 
            rate = rates[date]
            if rate is not None:
                closest_rate = rate 
                dist = 0 
            else: 
            # if rate is null then dist is incremented by 1 and new key/value pair(key=date, value=[closest_rate, dist])) is added to tmp dict 
                dist += 1
                tmp[date][1] = closest_rate, dist 

        for date in sorted(tmp):
            (r0, d0), (r1, d1) = tmp[date] # (r0, d0) is a tuple 
            rates[date] = (r0 * d1 + r1 * d0) / (d0 + d1) # using a formula to calculate the missing rate value for date keys with empty values 
            if self.verbose:
                print(('{0}: filling {1} missing rate using {2} ({3}d old) and'
                       '{4} ({5}d later)').format(currency, date, r0, d0, r1, d1))
                    
    def _use_last_known(self, currency):
        """
        Fill missing rates of a currency

        This is done by using the last known rate(which is the second method for calculating missing rates).
        :param str currency: The currency to file missing rates for. 
        """
        rates = self._rates[currency]

        for date in sorted(rates):
            rate = rates[date]
            if rate is not None:
                # iterate thru the sorted rates, if rates value is not null then assign that value to last_rate and assign date(which is the key) to last_date var 
                last_rate, last_date = rate, date 
            else:
                # if rates value is null then assign the last_rate to that key 
                rates[date] = last_rate 
                if self.verbose: 
                    print('{0}: filling {1} missing rate using {2} from {3}'.format(
                        currency, date, last_rate, last_date))

    def _get_rate(self, currency, date):
        """
        Get a rate for a give currency and date. 
        :param datetime.date date: the value for the currency param
        
        >>> from datetime import date 
        >>> c = CurrencyConverter()
        >>> c._get_rate('USD', date=date(2014, 3, 28)) 
        1.375... # this is the currency rate for USD currency for date(2014, 3, 28) in the EUR stock market 
        # if no value is found in self._rates dict then AssertionError is raised(see below)
        >>> c._get_rate('BGN', date=date(2010, 11, 21))
        Traceback (most recent call last):
        RateNotFoundError: BGN has no rate for 2010-11-21
        """
        if currency == self.ref_currency:
            # if the passed currency is the same as the reference currency then no conversion is needed so return 1
            return self.cast('1')
        if date not in self._rates[currency]:
            # if date is not in self._rates then assign the first_date and last_date in self.bounds to first_date and last_date variables 
            first_date, last_date = self.bounds[currency]

            if not self.fallback_on_wrong_date: 
                # if self.fallback_on_wrong is false then throw RateNotFoundError
                raise RateNotFoundError('{0} not in {1} bounds {2}/{3}'.format(
                    date, currency, first_date, last_date))

            if date < first_date:
                # if when self.fallback_on_wrong is true and current date in self._rates is before first_date(from self.bounds)
                # then fallback_date should be the first_date
                fallback_date = first_date 
            elif date > last_date: 
                # if current date is after last_date(from self.bounds) then fallback_date should be the last_date 
                fallback_date = last_date 
            else: 
                # this means this date is not in self.rates and in between the first and last dates in self.bounds 
                # which is not possible so throw an AssertionError to indicate bug in the code 
                raise AssertionError('Should never happen, bug in the code!')

            if self.verbose:
                print(r'/!\ {0} not in {1} bounds {2}/{3}, falling back to {4}'.format(
                    date, currency, first_date, last_date, fallback_date 
                ))
            # assign fallback_date to current date iteration
            date = fallback_date 
        # find the fallback_date in the self._rates dictionary 
        rate = self._rates[currency][date]
        if rate is None:
            # if fallback_date is not found in self._rates  
            # then throw RateNotFoundError
            raise RateNotFoundError('{0} has no rate for {1}'.format(currency, date))
        # if the fallback_rate is found in self._rates 
        # then return that rate 
        return rate 

    def convert(self, amount, currency, new_currency='EUR', date=None):
        """
        Convert amount from a currency to another one.

        :param float amount: The amount of `currency` to convert. 
        :param str currency: The currency to convert from.
        :param str new_currency: The currency to convert to.    
        :param datetime.date date: Use the conversion rate of this date. If this 
            is not given, the most recent rate is used.
        :return: The value of `amount` in `new_currency`
        :retype: float 

        >>> from datetime import date 
        >>> c = CurrencyConverter()
        >>> c.convert(100, 'EUR', 'USD', date=date(2014, 3, 28))
        137.5...
        >>> c.convert(100, 'USD', date=date(2010, 11, 21))
        72.67...
        >>> c.convert(100, 'BGN', date=date(2010, 11, 21))
        Traceback (most recent call last):
        RateNotFoundError: BGN has no rate for 2010-11-21
        """
        for c in currency, new_currency: 
            if c not in self.currencies:
                # if either currency or new_currency is not in self.currencies  
                # then throw ValueError
                raise ValueError('{0} is not a supported currency'.format(c))
        
        if date is None: 
            # if date is null 
            # then get the latest date in self.bounds 
            date = self.bounds[currency].last_date 
        else:
            try:
                # date is of type datetime so we use date.date() to 
                # get the date in string form 
                date = date.date() # fallback if input was a datetime object 
            except AttributeError:
                pass 

        # getting the currency rate for that specific date 
        # for both input and output currencies 
        # self._get_rate will throw RateNotFoundError if a rate was not found for that specific date
        r0 = self._get_rate(currency, date)
        r1 = self._get_rate(new_currency, date)
        # the formula for currency conversion is:
        # = ((amount) / (rate #1 * rate #2))
        return self.cast(amount) / r0 * r1 

class S3CurrencyConverter(CurrencyConverter):
    """
    Load the ECB CSV file from an S3 key instead of from a local file.
    The first argument should be an instance of boto.s3.key.Key (or any other
    object that provides a get_contents_as_string() method which returns the 
    CSV file as a string).
    """
    def __init__(self, currency_file, **kwargs):
        """
        Make currency_file a required attribute
        """
        super(S3CurrencyConverter, self).__init__(currency_file, **kwargs)

    def load_file(self, currency_file):
        lines = currency_file.get_contents_as_string().splitlines()
        self.load_lines(lines)

    






        




            