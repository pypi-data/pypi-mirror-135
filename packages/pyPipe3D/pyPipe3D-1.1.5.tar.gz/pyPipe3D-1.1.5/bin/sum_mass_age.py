#!/usr/bin/env python3
################################################################################
#
# sum_mass_age.py
# ----------------------
# Perl script: sum_mass_age.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import sum_mass_age

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['name']
    __optional__ = ['output_csv_filename']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'name': str}
    __conv_func_optional__ = {'output_csv_filename': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' NAME [OUTPUT.csv]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    # pa stands for parsed arguments
    pa = ReadArgumentsLocal()
    sum_mass_age(pa.name, pa.output_csv_filename)
