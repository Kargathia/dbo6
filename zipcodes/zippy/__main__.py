"""
Main entry point for zippy
"""

import os
import argparse
import logging
from zippy import parser, inserter, connector


def set_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('csv_file',
                           help='The CSV file containing the ZipCode Database')
    argparser.add_argument('--database',
                           help='The Postgres database name. Default = zippy',
                           default='zippy')
    argparser.add_argument('--username',
                           help='The database user name. Default = postgres',
                           default='postgres')
    argparser.add_argument('--password',
                           help='The database password. Default = root',
                           default='root')
    argparser.add_argument('--recreate',
                           help='Drop and recreate the database. Default = false',
                           type=bool,
                           default=False)
    argparser.add_argument('--startline',
                           help='The first line to be inserted. Default = 2',
                           default=2,
                           type=int)
    argparser.add_argument('--endline',
                           help='The last line to be inserted. Default = None',
                           default=None,
                           type=int)
    argparser.add_argument('--batchsize',
                           help='Insertion batch size(lines). Default = 1000',
                           default=1000,
                           type=int)
    argparser.add_argument('--encoding',
                           help='Data file encoding. Default = utf-8-sig',
                           default='utf-8-sig')
    argparser.add_argument('--output',
                           help='Log output file. Default = stdout',
                           default='')
    return argparser


def init_logging(args):
    log_args = {
        'level': logging.INFO,
        'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        'datefmt': '%m-%d %H:%M:%S'
    }

    if args.output:
        log_args['filename'] = args.output

    logging.basicConfig(**log_args)


def main():
    args = set_args().parse_args()
    fpath = os.path.abspath(args.csv_file)
    init_logging(args)

    headers = parser.parse_headers(fpath, args.encoding)
    engine = connector.connect(args.username, args.password, args.database)

    if args.recreate:
        logging.info('Dropping and recreating database')
        connector.recreate_database(engine)
    connector.setup(engine)

    for line_num, vals in parser.parse_data(
            fpath,
            headers,
            firstline=args.startline,
            lastline=args.endline,
            encoding=args.encoding):
        try:
            with connector.session_scope() as session:
                inserter.insert(session, vals)
                if line_num % args.batchsize == 0:
                    logging.info('processed line {}'.format(line_num))
        except Exception as ex:
            logging.error('error reading line {}'.format(line_num))
            logging.exception(ex, exc_info=False)

    logging.info('That\'s all, folks!')

if __name__ == '__main__':
    main()
