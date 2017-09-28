"""
Main entry point for zippy
"""

import os
import argparse
import logging
import json
from dbfaker import connector, data_mapper
from pprint import pprint


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--database',
                           help='The Postgres database name. Default = zippy',
                           default='zippy')
    argparser.add_argument('--username',
                           help='The database user name. Default = postgres',
                           default='postgres')
    argparser.add_argument('--password',
                           help='The database password. Default = root',
                           default='root')
    argparser.add_argument('--output',
                           help='Log output file. Default = stdout',
                           default='')
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
    logging.info(json.dumps(data_mapper.map_base(base), indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
