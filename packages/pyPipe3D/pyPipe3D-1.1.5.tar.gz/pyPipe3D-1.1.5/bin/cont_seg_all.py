#!/usr/bin/env python3
################################################################################
#
# cont_seg_all_SN.py
# ----------------------
# Perl script: cont_seg_all_SN.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import cont_seg_all

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['signal_fits', 'flux_limit_peak', 'max_dist_peak', 'frac_peak', 'min_flux',
                     'segmentation_fits', 'diffuse_mask_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'signal_fits': str, 'segmentation_fits': str, 'diffuse_mask_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' Ha_map.fits FLUX_LIMIT_PEAK MAX_DIST_PEAK FRAC_PEAK MIN_FLUX SEGFILE.fits DIFFUSE_MASK.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    # sys.exit()
    cont_seg_all(parsed_args.signal_fits, parsed_args.flux_limit_peak,
                 parsed_args.max_dist_peak, parsed_args.frac_peak, parsed_args.min_flux,
                 parsed_args.segmentation_fits, parsed_args.diffuse_mask_fits)
