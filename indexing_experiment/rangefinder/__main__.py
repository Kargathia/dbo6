"""
Main entry point for zippy
"""

import os
import argparse
import logging
import timeit
from rangefinder import connector, indexer, finder


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
    argparser.add_argument('-i', '--index',
                           help='Used index type')
    argparser.add_argument('-d', '--drop_index',
                           help='Drop index if exists. Default = false',
                           action='store_true')
    argparser.add_argument('--closest',
                           help='Time finding closest lat/long to Amsterdam',
                           action='store_true')
    argparser.add_argument('-r', '--repeats',
                           help='Number of times query is repeated',
                           type=int,
                           default=1)
    return argparser.parse_args()


def init_logging(args):
    log_args = {
        'level': logging.DEBUG,
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

    with connector.session_scope() as session:
        indexer.add_extension(session)

    if args.drop_index or args.index:
        with connector.session_scope() as session:
            logging.info('dropping index...')
            indexer.drop_index(session)

    with connector.session_scope() as session:
        if args.index:
            logging.info('adding {} index...'.format(args.index))
            indexer.add_index(engine, args.index)

        if args.closest:
            logging.info('finding closest...')
            duration = timeit.timeit(lambda: finder.find_closest(
                session, 52.3667, 4.9000, limit=100), number=args.repeats)
            avg = duration / args.repeats
            logging.info(
                'Finding closest to Amsterdam(52.3667, 4.9000) took {} seconds avg'.format(avg))

    logging.info('That\'s all, folks!')


if __name__ == '__main__':
    main()
