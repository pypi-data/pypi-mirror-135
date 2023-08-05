#!/usr/bin/env python3
################################################################################
#
# radial_sum_cube_e.py
# ----------------------
# Perl script: radial_sum_cube_e.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.tools import radial_sum_cube_e

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_cube_fits', 'delta_R', 'x0', 'y0', 'output_rss_fits']
    __optional__ = ['plot']
    __def_optional__ = {'plot': '0', 'badpixel_mask_extension': 3, 'badpixel_mask_value': 1}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_cube_fits': str, 'output_rss_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' CUBE.fits Delta_R X_C Y_C OUTPUT.RSS.fits [PLOT] [BADPIXEL_MASK] [BADPIXEL_VALUE]\n'
    __usage_msg__ += 'It will use images coordinates: 0,nx 0,ny'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    e_output_rss_fits = f'e_{args.output_rss_fits}'
    weight_output_rss_fits = f'weight.{args.output_rss_fits}'
    cube__wyx, h, n_ext = get_data_from_fits(args.input_cube_fits, header=True, return_n_extensions=True)
    crval = h['CRVAL3']
    cdelt = h['CDELT3']
    crpix = h['CRPIX3']
    input_mask = None
    input_error = None
    if h['EXTEND']:
        input_error = get_data_from_fits(args.input_cube_fits, extension=1)
        if (args.badpixel_mask_extension is not None) and (n_ext > 3):
            input_mask = get_data_from_fits(args.input_cube_fits, extension=args.badpixel_mask_extension)
            if args.badpixel_mask_value != 1:
                _tmp_input_mask = np.ones_like(input_mask)
                _tmp_input_mask[input_mask != args.badpixel_mask_value] = 0
                input_mask = _tmp_input_mask
    r = radial_sum_cube_e(cube__wyx, args.delta_R, args.x0, args.y0,
                          input_mask=input_mask, input_error=input_error)
    output__rw, e_output__rw, mask_output__rw = r
    h_set = {'CRVAL1': crval, 'CDELT1': cdelt, 'CRPIX1': crpix}
    array_to_fits(args.output_rss_fits, output__rw, header=h_set, overwrite=True)
    array_to_fits(e_output_rss_fits, e_output__rw, header=h_set, overwrite=True)
    array_to_fits(weight_output_rss_fits, mask_output__rw, header=h_set, overwrite=True)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # pa =
    # radial_sum_cube_e(pa.input_cube_fits, pa.delta_R, pa.x0, pa.y0, pa.output_rss_fits, pa.plot)
