#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os

from common import progname

desc = '''
Manages music libraries with metadata in M-TAGS format.
Written with love by Zachary Murray (dremelofdeath).
'''

__foobar2000_default_cover_patterns = [
    'front.jpg',
    'cover.jpg',
    '%filename%.jpg',
    '%album%.jpg',
    'folder.jpg',
]

__aggressive_cover_patterns = [
    os.path.join(os.pardir, 'override.png'),
    os.path.join(os.pardir, 'override.jpg'),
    os.path.join(os.pardir, 'front.png'),
    os.path.join(os.pardir, 'cover.png'),
    os.path.join(os.pardir, '%filename%.png'),
    os.path.join(os.pardir, '%album%.png'),
    os.path.join(os.pardir, 'folder.png'),
    os.path.join(os.pardir, '%artist% - %album%.png'),
    os.path.join(os.pardir, 'front.jpg'),
    os.path.join(os.pardir, 'cover.jpg'),
    os.path.join(os.pardir, '%filename%.jpg'),
    os.path.join(os.pardir, '%album%.jpg'),
    os.path.join(os.pardir, 'folder.jpg'),
    os.path.join(os.pardir, 'front.jpeg'),
    os.path.join(os.pardir, 'cover.jpeg'),
    os.path.join(os.pardir, 'folder.jpeg'),
    os.path.join(os.pardir, '%artist% - %album%.jpg'),
    os.path.join(os.pardir, '%artist% - %album%.jpeg'),
    'override.png',
    'override.jpg',
    'override.jpeg',
    'front.png',
    'front.jpg',
    'cover.png',
    'cover.jpg',
    '%filename%.png',
    '%filename%.jpg',
    '%album%.png',
    '%album%.jpg',
    'folder.png',
    'folder.jpg',
    os.path.join('artwork', 'front.png'),
    os.path.join('artwork', 'front.jpg'),
    '00 %album%.png',
    '00 %album%.jpg',
    '%album% - front.png',
    '%album% - front.jpg',
    '%album% - cover.png',
    '%album% - cover.jpg',
    '%artist% - %album% - front.png',
    '%artist% - %album% - front.jpg',
    '%artist% - %album% - cover.png',
    '%artist% - %album% - cover.jpg',
    'front.jpeg',
    'cover.jpeg',
    'folder.jpeg',
    os.path.join('artwork', 'front.jpeg'),
    '00 %album%.jpeg',
    '%album% - front.jpeg',
    '%album% - cover.jpeg',
    '%artist% - %album% - front.jpeg',
    '%artist% - %album% - cover.jpeg',
    '%artist% - %album%.jpg',
    '%artist% - %album%.jpeg',
    '%artist% - %album%.png',
    'folder*.jpg',
    'FOLDER*.jpg',
]

parser = argparse.ArgumentParser(prog=progname, description=desc)

cmd_parser = parser.add_subparsers(title='supported operations', dest='cmd')

shared_cmd_parser = argparse.ArgumentParser(add_help=False)

shared_cmd_parser.add_argument('--limit',
    default=-1,
    help='stop processing records after the specified number of tracks',
    type=int,
)

copy_cmd_parser=cmd_parser.add_parser('copy',
    help='copy all referenced files found in metadata',
    parents=[shared_cmd_parser],
)

copy_cmd_parser.add_argument('--to',
    help='pattern that specifies the destination for file operations',
    required=True,
)

copy_cmd_parser.add_argument('--dry-run',
    action='store_true',
    dest='dry_run',
    help="don't actually copy anything, just show what would happen",
)
copy_cmd_parser.set_defaults(dry_run=False)

copy_cmd_parser.add_argument('--write-mtags',
    action='store_true',
    dest='write_mtags',
    help='write a new M-TAGS file in each leaf directory created',
)
copy_cmd_parser.set_defaults(write_mtags=False)

copy_cmd_cover_search=copy_cmd_parser.add_mutually_exclusive_group()

copy_cmd_cover_search.add_argument('--include-covers',
    dest='include_covers',
    nargs='+',
    help='patterns to copy front cover art for each tag file found',
    metavar='PATTERN',
)

copy_cmd_cover_search.add_argument('--include-covers-default',
    action='store_const',
    dest='include_covers',
    const=__foobar2000_default_cover_patterns,
    help='same as --include-covers, but use the foobar2000 default patterns',
)

copy_cmd_cover_search.add_argument('--include-covers-aggressive',
    action='store_const',
    dest='include_covers',
    const=__aggressive_cover_patterns,
    help='same as --include-covers, but aggressively find cover art to copy',
)

copy_cmd_parser.set_defaults(include_covers=False)

copy_cmd_parser.add_argument('--cover-name',
    dest='cover_name',
    default='front',
    help='filename of the found cover art, without extension (default: front)',
    metavar='NAME',
)

copy_cmd_parser.add_argument('--per-track-cover-search',
    action='store_true',
    dest='per_track_cover_search',
    help='aggressively search each track for cover art (EXTREMELY SLOW!)',
)
copy_cmd_parser.set_defaults(per_track_cover_search=False)

copy_cmd_parser.add_argument('-q', '--quiet',
    action='store_true',
    dest='quiet',
    help="don't print anything but errors while performing the operation",
)
copy_cmd_parser.set_defaults(quiet=False)

list_cmd_parser=cmd_parser.add_parser('list',
    help='print out all found tracks',
    parents=[shared_cmd_parser],
)

list_cmd_parser.add_argument('--display',
    default='%artist% - %title%',
    help='pattern used to format output when listing tracks',
    metavar='PATTERN',
)

list_cmd_output_filter=list_cmd_parser.add_mutually_exclusive_group()

list_cmd_output_filter.add_argument('--startswith',
    default=False,
    help='display only output that starts with the specified pattern',
    metavar='PATTERN',
)

list_cmd_output_filter.add_argument('--equals',
    default=False,
    help='display only output that matches the specified pattern exactly',
    metavar='PATTERN',
)

list_cmd_output_filter.add_argument('--contains',
    default=False,
    help='display only output that contains the specified pattern',
    metavar='PATTERN',
)

list_cmd_parser.add_argument('--unique',
    action='store_true',
    default=False,
    help='only print each uniquely formatted line once',
)

parser.add_argument('--tagsfile',
    default='!.tags',
    help='the filename of the target tags files in subdirectories (!.tags)',
)

parser.add_argument('--case-sensitive',
    action='store_true',
    dest='case_sensitive',
    help='force variable resolution to instead be case-sensitive',
)
parser.set_defaults(case_sensitive=False)

parser.add_argument('--disable-magic',
    action='store_false',
    dest='magic',
    help='prevent variable resolution from searching multiple fields',
)
parser.set_defaults(magic=True)

args = parser.parse_args()

