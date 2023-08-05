#!/usr/bin/env python3
################################################################################
#
# vel_eline_cube.py
# ----------------------
# Perl script: vel_eline_cube.pl
#
################################################################################

### Local imports
import sys
import itertools
import numpy as np
from os.path import basename

from pyFIT3D.common.io import ReadArguments, get_wave_from_header
from pyFIT3D.common.io import array_to_fits, get_data_from_fits, trim_waves
# from pyFIT3D.common.tools import vel_eline_cube
from pyFIT3D.common.tools import vel_eline

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['cube_fits', 'nsearch', 'imin',
                     'prefix_out','wave_ref', 'plot']
    __optional__ = ['wmin', 'wmax']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __def_optional__ = {'wmax': '0', 'wmin': '1e12'}
    __conv_func_mandatory__ = {'cube_fits': str,
                               'prefix_out': str,
                               }
    __conv_func_optional__ = {'plot': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' CUBE.fits nsearch LIMIT(% max)'
    usage_msg_tmp3 = ' PREFIX_OUT WAVE_REF DEV [WMIN WMAX]\n'
    usage_msg_tmp4 = 'OUTPUT: PREFIX_OUT.vel_map.fits\n'
    usage_msg_tmp5 = 'OUTPUT: PREFIX_OUT.mask_map.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2 + usage_msg_tmp3 + \
            usage_msg_tmp4 + usage_msg_tmp5

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    map_outfile = args.prefix_out + ".vel_map.fits"
    mask_outfile = args.prefix_out + ".mask_map.fits"
    data_in, h = get_data_from_fits(args.cube_fits, header=True)
    nz, ny, nx = data_in.shape
    map_out = np.zeros((ny, nx))
    mask_out = np.zeros((ny, nx))
    wave = get_wave_from_header(h, wave_axis=3)
    mask_wave = trim_waves(wave, [args.wmin, args.wmax])
    # wave = np.array([crval3 + cdelt3 * k for k in np.arange(nz)])
    # mask_wave = (wave > wmin) & (wave < wmax)
    wave = wave[mask_wave]
    # print(wave[mask_wave])
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        # if (ix == 26) & (iy == 44):
        flux = data_in[:, iy, ix]
        flux = flux[mask_wave]
        vel, mask, npeaks = vel_eline(flux, wave, args.nsearch, args.imin, args.wave_ref, set_first_peak=False)
        map_out[iy, ix] = vel
        mask_out[iy, ix] = mask
        print("{}/{}".format(ix, nx))
    h_set = {
        # 'NAXIS': 2,
        # 'NAXIS1': nx,
        # 'NAXIS2': ny,
        'COMMENT': 'vel_eline_cube result',
        'WMIN': args.wmin,
        'WMAX': args.wmax,
        'WREF': args.wave_ref,
        'FILENAME': map_outfile,
    }
    array_to_fits(map_outfile, map_out, header=h_set, overwrite=True)
    h_set['FILENAME'] = mask_outfile
    array_to_fits(mask_outfile, mask_out, header=h_set, overwrite=True)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # parsed_args = ReadArgumentsLocal()
    # cube_fits = parsed_args.cube_fits
    # nsearch = parsed_args.nsearch
    # imin = parsed_args.imin
    # prefix_out = parsed_args.prefix_out
    # wave_ref = parsed_args.wave_ref
    # plot = parsed_args.plot
    # wmin = parsed_args.wmin
    # wmax = parsed_args.wmax
    # vel_eline_cube(cube_fits, nsearch, imin, prefix_out, wave_ref, plot, wmin, wmax)
    # ./vel_eline_cube.py /home/espinosa/tmp/GAS.UGC12250.cube.fits.gz 1 0.3 vel_Ha.UGC12250 6562.8 dev 6670 6750
