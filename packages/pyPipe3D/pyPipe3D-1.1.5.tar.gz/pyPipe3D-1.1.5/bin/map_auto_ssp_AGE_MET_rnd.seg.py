#!/usr/bin/env python3
################################################################################
#
# map_auto_ssp_AGE_MET_rnd.seg.py
# ----------------------
# Perl script: map_auto_ssp_AGE_MET_rnd.seg.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import map_auto_ssp_AGE_MET_rnd_seg

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input', 'segmentation_fits', 'output_prefix', 'central_wavelength', 'inst_disp']
    # __optional__ = ['output_diffuse_fits']
    # __def_optional__ = {'output_diffuse_fits': 'diffuse.fits'}
    __arg_names__ = __mandatory__  # + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input': str, 'segmentation_fits': str, 'output_prefix': str}
    # __conv_func_optional__ = {'output_diffuse_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    # __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' auto_ssp.out seg_file.fits PREFIX_OUT WAVE_CEN INST_DISP'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    map_auto_ssp_AGE_MET_rnd_seg(pa.input, pa.segmentation_fits, pa.output_prefix,
                                 pa.central_wavelength, pa.inst_disp)
