#!/usr/bin/env python3
################################################################################
#
# get_Ha.py
# ----------------------
# Perl script: get_Ha.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import get_Ha

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'redshift', 'output_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'output_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' INPUT_CUBE.fits redshift map_Ha.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    get_Ha(pa.input_fits, pa.redshift, pa.output_fits)
