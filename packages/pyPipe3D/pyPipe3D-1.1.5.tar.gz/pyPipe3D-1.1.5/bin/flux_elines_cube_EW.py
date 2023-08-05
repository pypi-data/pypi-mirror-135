#!/usr/bin/env python3
################################################################################
#
# flux_elines_cube_EW.py
# ----------------------
# Perl script: flux_elines_cube_EW.pl
#
################################################################################

### Local imports
import sys
import numpy as np
from astropy.io import fits
from os.path import basename
from copy import deepcopy as copy

from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.constants import __FWHM_to_sigma__
from pyFIT3D.common.tools import flux_elines_cube_EW

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['cube_fits', 'emission_lines_txt', 'output_fits',
                     'vel_map_fits',  'FWHM_map_sigma_inst']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'cube_fits': str, 'emission_lines_txt': str,
                               'output_fits': str, 'vel_map_fits': str,
                               'FWHM_map_sigma_inst': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' CUBE.fits,e_CUBE.fits,N_MC,CONT_CUBE.fits'
    usage_msg_tmp3 = ' emission_lines.txt output.fits VEL_map.fits'
    usage_msg_tmp4 = ' FWHM_map.fits[sigma_inst]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2 + usage_msg_tmp3 + \
        usage_msg_tmp4

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self._parse_filenames()

    def _parse_filenames(self):
        self.e_cube_fits = None
        self.n_mc = 1
        self.cont_cube_fits = None
        self.min_flux = None # Check if it is used.
        cube_fits_args = self.cube_fits.split(',')
        # print(cube_fits_args)
        if "," in self.cube_fits:
            self.cube_fits = cube_fits_args[0]
            self.e_cube_fits = cube_fits_args[1]
            self.n_mc = int(cube_fits_args[2])
            self.cont_cube_fits = cube_fits_args[3]

def main(args):
    input_e_cube = args.e_cube_fits
    input_cont_cube = args.cont_cube_fits
    guided_sigma = args.FWHM_map_sigma_inst
    input_cube_data, input_cube_header = get_data_from_fits(args.cube_fits, header=True)
    if input_e_cube is not None:
        # print("Reading Error cube")
        if "[1]" in input_e_cube:
            input_e_cube=input_e_cube.replace('[1]','')
        e_cube = fits.open(input_e_cube)
        if len(e_cube) > 1:
            input_e_cube_data = copy(e_cube[1].data)
        else:
            input_e_cube_data = copy(e_cube[0].data)
    if input_cont_cube is not None:
        # print("Reading cont cube")
        input_cont_cube_data = get_data_from_fits(input_cont_cube)
    gmap = get_data_from_fits(args.vel_map_fits)
    if "fit" in guided_sigma:
        # print("guided_sigma is a file")
        s_gmap = get_data_from_fits(guided_sigma)*__FWHM_to_sigma__
    else:
        s_gmap = float(guided_sigma)
    out, input_cube_header = flux_elines_cube_EW(input_cube_data, input_cube_header,
                                                 args.n_mc, args.emission_lines_txt, gmap, s_gmap,
                                                 input_e_cube_data, input_cont_cube_data)
    array_to_fits(args.output_fits, out, header=input_cube_header,
                  overwrite=True, sort_dict_header=False)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # parsed_args = ReadArgumentsLocal()
    # input_cube = parsed_args.cube_fits
    # input_e_cube = parsed_args.e_cube_fits
    # n_mc = int(parsed_args.n_mc)
    # input_cont_cube = parsed_args.cont_cube_fits
    # elines_list = parsed_args.emission_lines_txt
    # guided_map = parsed_args.vel_map_fits
    # guided_sigma = parsed_args.FWHM_map_sigma_inst
    # output = parsed_args.output_fits
    # flux_elines_cube_EW(input_cube, input_e_cube, n_mc, input_cont_cube, elines_list,
    #                     guided_map, guided_sigma, output)
