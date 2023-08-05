#!/usr/bin/env python3
################################################################################
#
# pack_results_name.py
# ----------------------
# Perl script: pack_results_name.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import pack_results_name

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['name', 'pack_filename', 'prefix']
    __def_optional__ = {}
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'name': str, 'pack_filename': str, 'prefix': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' NAME pack_CS.csv PREFIX'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    # pa stands for parsed arguments
    pa = ReadArgumentsLocal()
    pack_results_name(pa.name, pa.pack_filename, pa.prefix)
