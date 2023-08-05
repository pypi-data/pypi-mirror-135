#!/usr/bin/env python3
################################################################################
#
# rss_seg2cube.py
# ----------------------
# Perl script: rss_seg2cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits, get_data_from_fits, get_wave_from_header
from pyFIT3D.common.tools import rss_seg2cube

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_rss_fits', 'segmentation_fits', 'output_cube_fits']
    __optional__ = []
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_rss_fits': str, 'segmentation_fits': str,
                               'output_cube_fits': str}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' INPUT_RSS.fits SEGMENTATION.fits OUTPUT.CUBE.fits'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    rss__sw, h = get_data_from_fits(args.input_rss_fits, header=True)
    wave_axis = 1
    crval = h[f'CRVAL{wave_axis}']
    cdelt = h[f'CDELT{wave_axis}']
    crpix = h[f'CRPIX{wave_axis}']
    seg__yx = get_data_from_fits(args.segmentation_fits)
    cube__wyx = rss_seg2cube(rss__sw, seg__yx)
    # write cube
    h_set = {'CRVAL3': crval, 'CDELT3': cdelt, 'CRPIX3': crpix}
    array_to_fits(args.output_cube_fits, cube__wyx, header=h_set, overwrite=True)
    print(f'{args.output_cube_fits} created')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # rss_seg2cube(parsed_args.input_rss_fits, parsed_args.segmentation_fits, parsed_args.output_cube_fits)
