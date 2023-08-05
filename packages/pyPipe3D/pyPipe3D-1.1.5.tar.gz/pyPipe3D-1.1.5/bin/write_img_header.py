#!/usr/bin/env python3
################################################################################
#
# write_img_header.py
# ----------------------
# Perl script: write_img_header.pl
#
################################################################################

# System imports
import sys
import warnings
from os.path import basename
from astropy.io.fits.verify import VerifyWarning

# Local imports
from pyFIT3D.common.io import ReadArguments, write_img_header

warnings.simplefilter('ignore', category=VerifyWarning)

def parse_value(x):
    try:
        _x = eval(x)
    except (NameError, SyntaxError):
        _x = str(x)
    return _x

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_cube_fits', 'keyword', 'value']
    __optional__ = ['comment', 'before', 'after', 'output_fits']
    __def_optional__ = {}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_cube_fits': str, 'keyword': str, 'value': parse_value}
    __conv_func_optional__ = {'comment': str, 'before': str, 'after': str, 'output_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' input_cube.fits KEYWORD VALUE [COMMENT] [BEFORE] [AFTER] [OUTPUT_FITS]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

if __name__ == '__main__':
    parsed_args = ReadArgumentsLocal()
    write_img_header(parsed_args.input_cube_fits, parsed_args.keyword, parsed_args.value,
                     comment=parsed_args.comment,
                     before=parsed_args.before,
                     after=parsed_args.after,
                     output=parsed_args.output_fits,
                     overwrite=True)
