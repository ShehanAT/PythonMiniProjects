import sys 
import argparse 

from .currency_converter import CurrencyConverter, CURRENCY_FILE, parse_date

if sys.version_info[0] < 3:
    from itertools import izip_longest as zip_longest 
else:
    from itertools import zip_longest 


def grouper(iterable, n, fillvalue=None)
    """Group iterable by n elements 

    >>> for t in group('abcdefg', 3, fillvalue='x'):
    ...  print(''.join(t))

    abc 
    def 
    gxx
    """
    return list(zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('amount', type=float)
    parser.add_argument('currency')

    parser.add_argument(
        '-t', '--to',
        help='target currency, default is %(default)s',
        default='EUR'
    )

    parser.add_argument(
        '-d', '--date',
        help='date of rate, with format %%Y-%%m-%%d',
        default=None 
    )

    parser.add_argument(
        '-v', '--verbose',
        help=('display available currencies, use twice (-vv) to'
              'also display details of missing rates completion'),
        action='count',
        default=0)
    
    parser.add_argument(
        '--decimal',
        help='use decimal.Decimal internally',
        action='store_true'
    )

    args = parser.parse_args()

    c = CurrencyConverter(currency_file=args.file,
                          fallback_on_wrong_date=True,
                          fallback_on_missing_rate=True,
                          decimal=args.decimal,
                          verbose=args.verbose > 1)
    currencies = sorted(c.currencies)

    if args.verbose:
        print('{0} available currencies:'.format(len(currencies)))
        for group in grouper(currencies, 10, fillvalue=''):
            print(' '.join(group))
        print('')

        currencies.sort(key=lambda u: c.bounds[u].last_date, reverse=True)
        currencies.sort(key=lambda u: c.bounds[u].first_date)
        
    