#!/usr/bin/env python3
################################################################################
#
# get_SN_cube.py
# ----------------------
# Perl script: get_SN_cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename
from copy import deepcopy as copy

### Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import img2spec_e

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'ny', 'output']
    __optional__ = []
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'ny': int, 'output': str}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' INPUT_FILE.fits NY OUTPUT_FILE.txt'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    img2spec_e(parsed_args.input_fits, parsed_args.ny, parsed_args.output)
