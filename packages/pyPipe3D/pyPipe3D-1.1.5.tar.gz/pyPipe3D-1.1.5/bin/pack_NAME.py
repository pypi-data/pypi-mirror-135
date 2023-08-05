#!/usr/bin/env python3
################################################################################
#
# pack_NAME.py
# ----------------------
# Perl script: pack_NAME.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import pack_NAME

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['name']
    __optional__ = ['ssp_pack_filename', 'elines_pack_filename', 'sfh_pack_filename']
    __def_optional__ = {
        'ssp_pack_filename': '../legacy/pack_CS_inst_disp.csv',
        'elines_pack_filename': '../legacy/pack_elines_v1.5.csv',
        'sfh_pack_filename': '../legacy/pack_SFH.csv'
    }
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'name': str}
    __conv_func_optional__ = {'ssp_pack_filename': str, 'elines_pack_filename': str, 'sfh_pack_filename': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' NAME [SSP_PACK] [ELINES_PACK] [SFH_PACK]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

if __name__ == '__main__':
    # pa stands for parsed arguments
    pa = ReadArgumentsLocal()
    pack_NAME(pa.name, pa.ssp_pack_filename, pa.elines_pack_filename, pa.sfh_pack_filename)
