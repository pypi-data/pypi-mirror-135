#!/usr/bin/env python3
# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import call_cmnd

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['command']
    __optional__ = ['logfile', 'verbose']
    __def_optional__ = {'verbose': True}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'command': str}
    __conv_func_optional__ = {'logfile': str, 'verbose': bool}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' "COMMAND" [LOGFILE] [VERBOSE=0/1]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    # pa stands for parsed arguments
    pa = ReadArgumentsLocal()
    call_cmnd(pa.command, pa.logfile, pa.verbose)
