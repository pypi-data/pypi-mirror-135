#!/usr/bin/env python3
###############################################################################
#
# vel_eline_spec.py
# ----------------------
# Perl script: vel_eline_spec.pl
#
###############################################################################

### Local imports
import sys
import numpy as np
from astropy.io import fits
from os.path import basename

from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits, get_data_from_fits, trim_waves
# from pyFIT3D.common.tools import vel_eline_spec
from pyFIT3D.common.tools import vel_eline

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['spec', 'nsearch', 'imin',
                     'output_file','wave_ref', 'dev']
    __optional__ = ['wmin', 'wmax']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __def_optional__ = {'wmax': '0', 'wmin': '1e12'}
    __conv_func_mandatory__ = {'spec': str,
                               'output_file': str,
                               }
    __conv_func_optional__ = {'dev':str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' spec.txt nsearch LIMIT(% max)'
    usage_msg_tmp3 = ' OUTPUT_FILE WAVE_REF DEV [WMIN WMAX]\n'
    usage_msg_tmp4 = 'OUTPUT: spec.txt,npeak,vel\n'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2 + usage_msg_tmp3 + \
            usage_msg_tmp4

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

def main(args):
    wave = np.genfromtxt(args.spec, usecols=[1])
    flux = np.genfromtxt(args.spec, usecols=[2])
    mask_wave = trim_waves(wave, [args.wmin, args.wmax])
    wave = wave[mask_wave]
    flux = flux[mask_wave]
    vel, _, npeaks = vel_eline(flux, wave, args.nsearch, args.imin, args.wave_ref)
    clf = False
    if (args.output_file is None) or (args.output_file == 'junk'):
        f = sys.stdout
    else:
        clf = True
        f = open(args.output_file, 'w')
    print("{},{},{}".format(args.spec, npeaks, vel), file=f)
    if clf:
        f.close()

if __name__ == '__main__':
    main(ReadArgumentsLocal(verbose=True))
    # parsed_args = ReadArgumentsLocal()
    # spec = parsed_args.spec
    # nsearch = parsed_args.nsearch
    # imin = parsed_args.imin
    # prefix_out = parsed_args.prefix_out
    # wave_ref = parsed_args.wave_ref
    # dev = parsed_args.dev
    # wmin = parsed_args.wmin
    # wmax = parsed_args.wmax
    # vel_eline_spec(spec, nsearch, imin, prefix_out, wave_ref, wmin, wmax, dev)
    # ./vel_eline_spec.py /home/espinosa/tmp/spec_UGC12250_40_34.txt 1 0.3 vel_Ha.UGC12250 6562.8 1 6670 6750
