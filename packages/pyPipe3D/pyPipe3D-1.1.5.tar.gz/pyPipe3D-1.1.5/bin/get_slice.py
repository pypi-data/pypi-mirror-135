#!/usr/bin/env python3
################################################################################
#
# get_slice.py
# ----------------------
# Perl script: get_slice.pl
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
from pyFIT3D.common.tools import get_slice

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_cube_fits', 'prefix', 'conf_file']
    __optional__ = []
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_cube_fits': str, 'prefix': str, 'conf_file': str}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' INPUT_CUBE.fits PREFIX CONF_FILE\n'
    __usage_msg__ += 'CONF_FILE: NAME START_W END_W'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    data__wyx, h = get_data_from_fits(args.input_cube_fits, header=True)
    wave__w = get_wave_from_header(h, wave_axis=3)
    slices = get_slice(data__wyx, wave__w, args.prefix, args.conf_file)
    if len(slices) > 0:
        for k, v in slices.items():
            if v is not None:
                fname = f'{k}.fits'
                array_to_fits(fname, v, overwrite=True)
                print(f'{fname} saved')
            else:
                s_w, e_w = k.split('_')[-2:]
                print(f'section ({s_w}, {e_w}) out of margins')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # parsed_args.input_cube_fits, parsed_args.prefix, parsed_args.conf_file)
