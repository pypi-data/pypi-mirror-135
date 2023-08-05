#!/usr/bin/env python3
################################################################################
#
# spec_extract_cube.py
# ----------------------
# Perl script: spec_extract_cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import spec_extract_cube

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'segmentation_fits', 'output_rss_fits']
    __optional__ = ['output_diffuse_fits']
    __def_optional__ = {'output_diffuse_fits': 'diffuse.fits'}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'segmentation_fits': str, 'output_rss_fits': str}
    __conv_func_optional__ = {'output_diffuse_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' INPUT.CUBE.fits SEGMENTATION.fits OUTPUT.RSS.FITS [DIFFUSE_OUTPUT]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    spec_extract_cube(pa.input_fits, pa.segmentation_fits,
                      pa.output_rss_fits, pa.output_diffuse_fits)
