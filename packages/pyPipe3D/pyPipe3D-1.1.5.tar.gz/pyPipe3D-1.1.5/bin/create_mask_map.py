#!/usr/bin/env python3
################################################################################
#
# create_mask_map.py
# ----------------------
# Perl script: create_mask_map.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import create_mask_map

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['map_fits', 'cut', 'mask_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'map_fits': str,
                               'mask_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' map.fits cut mask.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    map_fits = parsed_args.map_fits
    cut = parsed_args.cut
    mask_fits = parsed_args.mask_fits
    create_mask_map(map_fits, cut, mask_fits)
