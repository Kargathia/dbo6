"""
Main entry point for zippy
"""

import os
import argparse
import logging
import json
from dbfaker import connector, data_mapper, filler
from pprint import pformat


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--database',
                           help='The Postgres database name. Default = zippy_tester.',
                           default='zippy_tester')
    argparser.add_argument('--username',
                           help='The database user name. Default = postgres.',
                           default='postgres')
    argparser.add_argument('--password',
                           help='The database password. Default = root.',
                           default='root')
    argparser.add_argument('--output',
                           help='Log output file. Default = stdout.',
                           default='')
    argparser.add_argument('--input',
                           help='Custom input specification file (json). Optional.',
                           default='')
    argparser.add_argument('--fill',
                           help='Generate dummy data, and insert it. Default = False',
                           default=False,
                           action='store_true')
    return argparser.parse_args()


def init_logging(args):
    log_args = {
        'level': logging.INFO,
        'format': '%(message)s'
    }

    if args.output:
        log_args['filename'] = args.output
        log_args['filemode'] = 'w'

    logging.basicConfig(**log_args)


def main():
    args = get_args()
    init_logging(args)

    engine, base = connector.startup(args.username, args.password, args.database)

    if args.input and not args.fill:
        logging.warning('Input is specified without --fill: nothing will happen')

    spec = None
    if args.input:
        with open(args.input) as f:
            spec = json.load(f)
    else:
        spec = data_mapper.map_base(base)
        logging.info(json.dumps(spec, indent=4, sort_keys=True))

    if args.fill:
        logging.info(pformat(spec))
        filler.fill_database(engine, base, spec)


if __name__ == '__main__':
    main()
