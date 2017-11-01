"""
Main entry point for zippy
"""

import os
import argparse
import logging
from zippy import parser, inserter, connector


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
        'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        'datefmt': '%m-%d %H:%M:%S'
    }

    if args.output:
        log_args['filename'] = args.output
        log_args['filemode'] = 'w'

    logging.basicConfig(**log_args)


def main():
    args = get_args()
    init_logging(args)

    engine = connector.connect(args.username, args.password, args.database)
    connector.setup(engine)

    # add index of choice
    # do lookup

    logging.info('That\'s all, folks!')

if __name__ == '__main__':
    main()
