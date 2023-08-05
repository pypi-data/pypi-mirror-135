#!/usr/bin/env python3
################################################################################
#
# map_auto_ssp_rnd.seg.py
# ----------------------
# Perl script: map_auto_ssp_rnd.seg.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import map_auto_ssp_rnd_seg

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input', 'segmentation_fits', 'output_prefix']
    __optional__ = ['inst_disp', 'central_wavelength']
    __def_optional__ = {'central_wavelength': 4275, 'inst_disp': 2.45}
    __arg_names__ = __mandatory__  + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input': str, 'segmentation_fits': str, 'output_prefix': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' elines_OUT seg_file.fits PREFIX_OUT [DISP_INST] [WAVE_NORM]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    map_auto_ssp_rnd_seg(pa.input, pa.segmentation_fits, pa.output_prefix,
                         pa.inst_disp, pa.central_wavelength)  #, pa.auto_ssp_config)
