#!/usr/bin/env python3
# System imports
import sys
import itertools
import numpy as np
from os.path import basename
from copy import deepcopy as copy

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits, get_data_from_fits
from pyFIT3D.common.tools import clean_map

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input1_fits', 'input2_fits',]
    __optional__ = ['max_vel', 'min_vel', 'output_fits']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __def_optional__ = {'max_vel': 1e12, 'min_vel': 0}
    __conv_func_mandatory__ = {'input1_fits': str, 'input2_fits': str}
    __conv_func_optional__ = {'output_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' INPUT_CUBE.FITS VELOCITY.FITS [MAX_VEL] [MIN_VEL] [OUTPUT_CUBE_NAME]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

# from pyFIT3D.common.stats import _STATS_POS, pdl_stats
#
# def clean_cubes_map(in1_file, in2_file, max_vel, min_vel):
#     a_in1, h1 = get_data_from_fits(in1_file, header=True)
#     a_in2, h2 = get_data_from_fits(in2_file, header=True)
#     nz, ny, nx = a_in1.shape
#     mask_a_in2 = np.full((ny,nx), True, dtype=bool)
#     mask = (a_in2 > max_vel) | (a_in2<min_vel)
#     mask_a_in2[mask] = 0
#     for iyx in itertools.product(range(ny),range(nx)):
#         iy, ix = iyx
#         if (iy > 2) & (iy < (ny - 2)) & (ix > 2) & (ix < (nx - 2)):
#             if mask_a_in2[iy, ix] == 0:
#                 iy0 = iy - 1
#                 iy1 = iy + 2
#                 ix0 = ix - 1
#                 ix1 = ix + 2
#                 val = a_in1[:,iy0:iy1, ix0:ix1]
#                 val[~np.isfinite(val)] = 0
#                 val_vel = mask_a_in2[iy0:iy1, ix0:ix1]
#                 mask_vel = val_vel[val_vel>0]
#                 if mask_vel.sum() > 5:
#                     for iz in range(nz):
#                         val_z=a_in1[iz,iy0:iy1, ix0:ix1]
#                         val_z=val_z[val_vel>0]
#                         st_val_z = pdl_stats(val_z)
#                         a_in1[iz,iy, ix] = st_val_z[_STATS_POS['median']]
#     for iyx in itertools.product(range(ny),range(nx)):
#         iy, ix = iyx
#         if (iy > 2) & (iy < (ny - 2)) & (ix > 2) & (ix < (nx - 2)):
#             if a_in2[iy, ix] <= 0:
#                 iy0 = iy - 1
#                 iy1 = iy + 2
#                 ix0 = ix - 1
#                 ix1 = ix + 2
#                 val = a_in1[:,iy0:iy1, ix0:ix1]
#                 val[~np.isfinite(val)] = 0
#                 val_vel = mask_a_in2[iy0:iy1, ix0:ix1]
#                 mask_vel = val_vel[val_vel>0]
#                 if mask_vel.sum() > 5:
#                     for iz in range(nz):
#                         val_z=a_in1[iz,iy0:iy1, ix0:ix1]
#                         val_z=val_z[val_vel>0]
#                         st_val_z = pdl_stats(val_z)
#                         a_in1[iz,iy, ix] = st_val_z[_STATS_POS['median']]
#     array_to_fits(in1_file, a_in1, overwrite=True, header=h1)

def main(args):
    cube__zyx, h = get_data_from_fits(args.input1_fits, header=True)
    vel__yx = get_data_from_fits(args.input2_fits)
    nz = cube__zyx.shape[0]
    for iz in range(nz):
        print(f'cube map id: {iz}')
        map__yx = copy(cube__zyx[iz])
        cube__zyx[iz] = clean_map(map__yx, vel__yx,
                                  max_vel=args.max_vel, min_vel=args.min_vel)
    output_fits = args.input1_fits
    if args.output_fits is not None:
        output_fits = args.output_fits
    array_to_fits(output_fits, cube__zyx, overwrite=True, header=h)

if __name__ == '__main__':
    # pa = ReadArgumentsLocal()
    # clean_cubes_map(pa.input1_fits, pa.input2_fits, max_vel=pa.max_vel, min_vel=pa.min_vel)
    main(ReadArgumentsLocal(verbose=True))
