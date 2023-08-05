#!/usr/bin/env python3
################################################################################
#
# read_img_header.py
# ----------------------
# Perl script: read_img_header.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import read_img_header

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'header']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'header': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' FILE.FITS HEADER'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self._parse_cards()

    def _parse_cards(self):
        self.header_cards = self.header.split(',')

if __name__ == '__main__':
    # pa stands for parsed arguments
    pa = ReadArgumentsLocal()
    read_img_header(pa.input_fits, pa.header_cards)
