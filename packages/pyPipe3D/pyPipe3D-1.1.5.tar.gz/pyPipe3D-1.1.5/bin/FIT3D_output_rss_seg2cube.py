#!/usr/bin/env python3
################################################################################
#
# FIT3D_output_rss_seg2cube.py
# ----------------------
# Perl script: FIT3D_output_rss_seg2cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.tools import rss_seg2cube

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'n_out', 'segmentation_fits', 'output_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'segmentation_fits': str, 'output_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' INPUT.FITS OUTPUT.FITS X_WIDTH Y_WIDTH'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

def main(args):
    rss__sw, h = get_data_from_fits(args.input_fits, header=True)
    wave_axis = 1
    crval = h[f'CRVAL{wave_axis}']
    cdelt = h[f'CDELT{wave_axis}']
    crpix = h[f'CRPIX{wave_axis}']
    seg__yx = get_data_from_fits(args.segmentation_fits)
    cube__wyx = rss_seg2cube(rss__sw[args.n_out], seg__yx)
    # write cube
    h_set = {'CRVAL3': crval, 'CDELT3': cdelt, 'CRPIX3': crpix}
    array_to_fits(args.output_fits, cube__wyx, header=h_set, overwrite=True)
    print(f'{args.output_fits} created')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # pa stands for parsed arguments
    # FIT3D_output_rss_seg2cube(pa.input_fits, pa.n_out, pa.segmentation_fits, pa.output_fits)
