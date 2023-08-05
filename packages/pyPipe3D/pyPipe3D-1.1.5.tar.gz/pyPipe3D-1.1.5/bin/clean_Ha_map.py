#!/usr/bin/env python3
################################################################################
#
# clean_Ha_map.py
# ----------------------
# Perl script: clean_Ha_map.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits, get_data_from_fits
from pyFIT3D.common.tools import clean_Ha_map

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input1_fits', 'input2_fits',]
    __optional__ = ['max_vel', 'min_vel']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __def_optional__ = {'max_vel': '1e12', 'min_vel': '0'}
    __conv_func_mandatory__ = {'input1_fits': str, 'input2_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' INPUT1.FITS INPUT2.FITS [MAX_VEL] [MIN_VEL]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

def main(args):
    v__yx, h1 = get_data_from_fits(args.input1_fits, header=True)
    mask__yx, h2 = get_data_from_fits(args.input2_fits, header=True)
    v__yx, mask__yx = clean_Ha_map(v__yx, mask__yx, args.max_vel, args.min_vel)
    array_to_fits(args.input1_fits, v__yx, overwrite=True, header=h1)
    array_to_fits(args.input2_fits, mask__yx, overwrite=True, header=h2)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # parsed_args = ReadArgumentsLocal()
    # in1_file = parsed_args.input1_fits
    # in2_file = parsed_args.input2_fits
    # max_vel = parsed_args.max_vel
    # min_vel = parsed_args.min_vel
    # clean_Ha_map(in1_file, in2_file, max_vel, min_vel)
