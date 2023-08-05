#!/usr/bin/env python3
################################################################################
#
# spec_extract_cube_error.py
# ----------------------
# Perl script: spec_extract_cube_error.pl
#
################################################################################

# System imports
import sys
import numpy as np
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.tools import spec_extract_cube_error

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'segmentation_fits', 'output_rss_fits']
    __optional__ = ['output_diffuse_fits']
    __def_optional__ = {'output_diffuse_fits': 'diffuse.fits'}
    __arg_names__ = __mandatory__  + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'segmentation_fits': str, 'output_rss_fits': str}
    __conv_func_optional__ = {'output_diffuse_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' INPUT.CUBE.fits SEGMENTATION.fits OUTPUT.RSS.FITS'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    diffuse_output = 'diffuse.fits' if args.diffuse_output is None else args.diffuse_output
    # read cube
    _, h = get_data_from_fits(args.input_fits, header=True)
    error__wyx = get_data_from_fits(args.input_fits, extension=1)
    nw, ny, nx = error__wyx.shape
    # read segmentation
    seg__yx = get_data_from_fits(args.segmentation_fits)
    ns = seg__yx.max().astype('int')
    nys, nxs = seg__yx.shape

    if (nx > nxs) or (ny > nys):
        print(f'{basename(sys.argv[0])}: Dimensions does not match ({nx},{ny}) != ({nxs},{nys})')
        # XXX: deal function returns in all tools
        sys.exit()

    out_data__sw, inv_seg__yx, x, y, npt = spec_extract_cube_error(error__wyx, seg__yx)

    h_set = {'CRVAL1': h['CRVAL3'], 'CDELT1': h['CDELT3'], 'CRPIX1': h['CRPIX3']}
    array_to_fits(args.output_rss_fits, out_data__sw, header=h_set, overwrite=True)

    size = np.sqrt(nx**2+ny**2)/(2*ns)
    output_rss_txt = args.output_rss_fits.replace('fits', 'pt.txt')
    with open(output_rss_txt, 'w') as f:
        output_header = f'C {size} {size} 0'
        print(output_header, file=f)
        # output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
        np.savetxt(f, list(zip(list(range(ns)), x/npt, y/npt, [1]*ns)),
                   fmt=['%d'] + 2*['%.18g'] + ['%d'], delimiter=' ')
    print(f'{args.output_rss_fits} and {output_rss_txt} created')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # pa = ReadArgumentsLocal()
    # spec_extract_cube_error(pa.input_fits, pa.segmentation_fits, pa.output_rss_fits)
