"""
Main entry point for zippy
"""

import os
import argparse
import logging
from foodgenerator import generator


def get_args():
    argparser = argparse.ArgumentParser()
    # argparser.add_argument('csv_file',
    #                        help='The CSV file containing the ZipCode Database')
    argparser.add_argument('-u', '--url',
                           help='The URL where the Stock application is hosted. Optional.',
                           default='')
    argparser.add_argument('-n', '--number',
                           help='Number of products that should be generated. Default = 100',
                           type=int,
                           default=100)
    argparser.add_argument('-i', '--install',
                           help='Install the node JS library. Default = False',
                           action='store_true',
                           default=False)
    argparser.add_argument('-q', '--quiet',
                           help='Don\'t log output. Default = False',
                           action='store_true',
                           default=False)
    argparser.add_argument('-o', '--output',
                           help='Log output file. Default = stdout',
                           default='')
    argparser.add_argument('-c', '--categories',
                           nargs='+',
                           help='set custom set of categories')
    return argparser.parse_args()


def init_logging(args):
    log_args = {
        'level': logging.INFO,
        'format': '%(message)s',
    }

    if args.output:
        log_args['filename'] = args.output
        log_args['filemode'] = 'w'

    logging.basicConfig(**log_args)


def main():
    args = get_args()
    init_logging(args)

    if args.output:
        args.quiet = False

    if args.install:
        generator.install_lib()

    for product in generator.generate_products(args.number, args.categories):
        if not args.quiet:
            logging.info(product)
        if args.url:
            generator.call_api(args.url, product)


if __name__ == '__main__':
    main()
