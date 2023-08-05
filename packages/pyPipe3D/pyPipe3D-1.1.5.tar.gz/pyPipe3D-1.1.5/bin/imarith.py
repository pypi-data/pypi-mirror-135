#!/usr/bin/env python3
################################################################################
#
# imarith.py
# ----------------------
# Perl script: imarith.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import imarith

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input1_fits', 'operator', 'input2_fits', 'output_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input1_fits': str, 'operator': str,
                               'input2_fits': str, 'output_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' INPUT1.FITS OPERATOR(+,-,?,*) INPUT2.FITS OUTPUT.FITS'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    in1_file = parsed_args.input1_fits
    operator = parsed_args.operator
    in2_file = parsed_args.input2_fits
    out_file = parsed_args.output_fits
    imarith(in1_file, operator, in2_file, out_file)
