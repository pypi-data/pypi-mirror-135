#!/usr/bin/env python3
################################################################################
#
# csv_to_map.seg.py
# ----------------------
# Perl script: csv_to_map.seg.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import csv_to_map_seg

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['csvfile', 'column', 'seg_file_fits', 'map_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'csvfile': str, 'seg_file_fits': str,
                               'map_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' CSVFILE column seg_file.fits map.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    csvfile = parsed_args.csvfile
    column = int(parsed_args.column)
    seg_file_fits = parsed_args.seg_file_fits
    map_fits = parsed_args.map_fits
    csv_to_map_seg(csvfile, column, seg_file_fits, map_fits)
