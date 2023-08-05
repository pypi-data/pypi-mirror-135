#!/usr/bin/env python3
################################################################################
#
# spec_extract_diffuse.py
# ----------------------
# Perl script: spec_extract_diffuse.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import spec_extract_diffuse

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'Ha_map_fits', 'segmentation_diffuse_fits',
                     'output_rss_fits']
    __optional__ = ['lower_limit']
    __def_optional__ = {'lower_limit': 0}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'Ha_map_fits': str,
                               'segmentation_diffuse_fits': str, 'output_rss_fits': str}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' CUBE.fits Ha_map.fits diffuse.fits OUTPUT.RSS.FITS [LOWER_LIMIT]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    spec_extract_diffuse(pa.input_fits, pa.Ha_map_fits, pa.segmentation_diffuse_fits,
                         pa.output_rss_fits, pa.lower_limit)
