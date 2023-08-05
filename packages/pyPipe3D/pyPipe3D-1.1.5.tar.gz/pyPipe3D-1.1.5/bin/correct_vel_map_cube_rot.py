#!/usr/bin/env python3
################################################################################
#
# correct_vel_map_cube_rot.py
# ----------------------
# Perl script: correct_vel_map_cube_rot.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import correct_vel_map_cube_rot

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'velocity_map_fits', 'output_fits']
    __optional__ = ['final_velocity']
    __def_optional__ = {'final_velocity': 0}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'velocity_map_fits': str, 'output_fits': str}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' CUBE.fits Ha_map.fits diffuse.fits OUTPUT.RSS.FITS [LOWER_LIMIT]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    correct_vel_map_cube_rot(pa.input_fits, pa.velocity_map_fits, pa.output_fits, pa.final_velocity)
