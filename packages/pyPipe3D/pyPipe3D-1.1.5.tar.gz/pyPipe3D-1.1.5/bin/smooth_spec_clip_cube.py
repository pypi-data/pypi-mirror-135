#!/usr/bin/env python3
################################################################################
#
# smooth_spec_clip_cube.py
# ----------------------
# Perl script: smooth_spec_clip_cube.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.tools import smooth_spec_clip_cube

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_cube_fits', 'output_cube_fits', 'width', 'nsigma', 'nxmin', 'nxmax']
    __optional__ = []
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_cube_fits': str, 'output_cube_fits': str,
                               'width': int, 'nxmin': int, 'nxmax': int}
    __conv_func_optional__ = {}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' input_spec.cube.fits output_spec.cube.fits WIDTH NSIGMA NXMIN NXMAX'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    cube__wyx, h_out = get_data_from_fits(args.input_cube_fits, header=True)
    output_data__wyx = smooth_spec_clip_cube(cube__wyx, args.width, args.nsigma, args.nxmin, args.nxmax)
    array_to_fits(filename=args.output_cube_fits, arr=output_data__wyx, header=h_out, overwrite=True)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # parsed_args = ReadArgumentsLocal()
    # # sys.exit()
    # smooth_spec_clip_cube(parsed_args.input_cube_fits, parsed_args.output_cube_fits,
    #                       parsed_args.width, parsed_args.nsigma,
    #                       parsed_args.nxmin, parsed_args.nxmax)
