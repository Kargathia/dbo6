"""
Parses input file or DB, and inserts created values
"""

import sys


def parse_headers(fpath, encoding=None):
    """Interprets the first line of a document as its headers.
    Splits them, and returns them as string array"""
    with open(fpath, encoding=encoding) as f:
        return (f.readline()
                .strip()
                .replace('"', '')
                .split(','))


def parse_data(fpath, headers, firstline=1, lastline=None, encoding=None):
    if not isinstance(firstline, int) or firstline <= 0:
        firstline = 1

    with open(fpath, encoding=encoding) as f:
        # skip through file until the firstline is reached
        for _ in range(firstline - 1):
            next(f)

        # yield line as dict, headers as keys
        line_num = firstline

        # iterate over remainder
        for line in f:
            vals = line.strip().replace('"', '').split(',')
            yield line_num, {k: v for k, v in zip(headers, vals)}

            line_num += 1
            if lastline and line_num > lastline:
                break
