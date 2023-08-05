#!/usr/bin/env python3
################################################################################
#
# get_SN_cube.py
# ----------------------
# Perl script: get_SN_cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits
from pyFIT3D.common.io import get_data_from_fits
from pyFIT3D.common.io import get_wave_from_header
from pyFIT3D.common.tools import get_SN_cube

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_cube_fits', 'output_SN_map', 'output_signal_map', 'output_noise_map']
    __optional__ = ['w_minmax']
    __def_optional__ = {'w_minmax': '0,0'}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_cube_fits': str, 'output_SN_map': str,
                               'output_signal_map': str, 'output_noise_map': str}
    __conv_func_optional__ = {'w_minmax': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' input_cube.fits SN_map.fits signalmap.fits noisemap.fits [WMIN,WMAX]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        if self.w_minmax is not None:
            self.parse_wavelength()

    def parse_wavelength(self):
        wminmax = self.w_minmax.split(',')
        if len(wminmax) == 2:
            self.wmin = eval(wminmax[0])
            self.wmax = eval(wminmax[1])

def main(args):
    # read data
    org_cube__wyx, h = get_data_from_fits(args.input_cube_fits, header=True)

    # create wavelength array
    wave__w = get_wave_from_header(h, wave_axis=3)

    SN__yx, mean_flux__yx, sigma_flux__yx = get_SN_cube(org_cube__wyx, wave__w, args.wmin, args.wmax)

    array_to_fits(filename=args.output_SN_map, arr=SN__yx, overwrite=True)
    array_to_fits(filename=args.output_signal_map, arr=mean_flux__yx, overwrite=True)
    array_to_fits(filename=args.output_noise_map, arr=sigma_flux__yx, overwrite=True)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
