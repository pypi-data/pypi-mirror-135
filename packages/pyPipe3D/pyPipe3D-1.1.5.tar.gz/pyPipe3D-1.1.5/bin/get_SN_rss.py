#!/usr/bin/env python3
################################################################################
#
# get_SN_rss.py
# ----------------------
# Perl script: get_SN_rss.pl
#
################################################################################

# System imports
import sys
import numpy as np
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import array_to_fits
from pyFIT3D.common.io import get_data_from_fits
from pyFIT3D.common.io import get_wave_from_header
from pyFIT3D.common.tools import get_SN_rss

class ReadArgumentsLocal(ReadArguments):
    """
    Local argument parser
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_rss_fits', 'output']
    __optional__ = ['w_minmax']
    __def_optional__ = {'w_minmax': '0,0'}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_rss_fits': str, 'output': str}
    __conv_func_optional__ = {'w_minmax': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    __usage_msg__ = f'USE: {__script_name__}'
    __usage_msg__ += ' input_rss.fits out_values.csv [WMIN,WMAX]'

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
    org_rss__sw, h = get_data_from_fits(args.input_rss_fits, header=True)

    # create wavelength array
    wave__w = get_wave_from_header(h, wave_axis=1)

    SN__s, mean_flux__s, sigma_flux__s = get_SN_rss(org_rss__sw, wave__w, args.wmin, args.wmax)

    with open(args.output, 'w') as f:
        output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
        np.savetxt(f, list(zip(list(range(SN__s.size)), SN__s, mean_flux__s, sigma_flux__s)),
                   fmt=['%d'] + 3*['%.18g'], header=output_header, delimiter=',')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
