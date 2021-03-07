import sys 
import argparse 
from currency_converter import CurrencyConverter, CURRENCY_FILE, parse_date

if sys.version_info[0] < 3:
    from itertools import izip_longest as zip_longest 
else:
    from itertools import zip_longest 


def grouper(iterable, n, fillvalue=None):
    """Group iterable by n elements 

    >>> for t in group('abcdefg', 3, fillvalue='x'):
    ...  print(''.join(t))

    abc 
    def 
    gxx
    """
    return list(zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue))


def main(): # this is the main function in Python 

    # this is the command line input formatter
    # where arg1=amount, arg2=currency are mandatory
    parser = argparse.ArgumentParser()
    parser.add_argument('amount', type=float)
    parser.add_argument('currency')

    # all added args are optional  
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

    parser.add_argument(
        '-f', '--file',
        help='change currency file used, default is %(default)s',
        default=CURRENCY_FILE)

    # parse the recieve cmd args and store them in variable args 
    args = parser.parse_args()
    
    c = CurrencyConverter(currency_file=args.file,
                          fallback_on_wrong_date=True,
                          fallback_on_missing_rate=True,
                          decimal=args.decimal,
                          verbose=args.verbose > 1)
    currencies = sorted(c.currencies)

    if args.verbose:
        # if user passes verbose arg
        # then print out all available currencies 
        print('{0} available currencies:'.format(len(currencies)))
        for group in grouper(currencies, 10, fillvalue=''):
            print(' '.join(group))
        print('')
        # sort the currencies in the list by last date then reverse that order
        # then sort the currencies by first date
        currencies.sort(key=lambda u: c.bounds[u].last_date, reverse=True)
        currencies.sort(key=lambda u: c.bounds[u].first_date)
        for currency in currencies:
            first_date, last_date = c.bounds[currency]
            # printing the bounds of each currency in format:
            # USD: from 02/12/2021 to 02/28/2021 (16 days)
            print('{0}: from {1} to {2} ({3} days)'.format(
                currency, first_date, last_date,
                1 + (last_date - first_date).days))
        print('')

    if args.currency not in c.currencies:
        # if a currency provided in the args was not found in c.currencies 
        # then print out a message saying so 
        print(r'/!\ "{0}" is not in available currencies:'.format(args.currency))
        for group in grouper(currencies, 10, fillvalue=''):
            print(''.join(group))
        exit(1)

    if args.date is not None:
        # parse the date if it is provided in args 
        date = parse_date(args.date)
    else:
        # if date is not in args then use the value of last date of that specific 
        # currency in the c.bound dict and assign it to variable date 
        date = c.bounds[args.currency].last_date 

    # new_amount variable is the result of converting the amount 
    # from currency A to currency B based on the date provided 
    new_amount = c.convert(amount=args.amount,
                            currency=args.currency,
                            new_currency=args.to,
                            date=date)

    # print out the results of new_amount 
    print('{0:.3f} {1} = {2:.3f} {3} on {4}'.format(
        args.amount,
        args.currency,
        new_amount,
        args.to,
        date))    
    
if __name__ == '__main__':
    main() 