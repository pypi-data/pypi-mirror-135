#!/usr/bin/env python3
################################################################################
#
# get_index_output_auto_ssp_elines_rnd_rss_outFIT3D.py
# ----------------------
# Perl script: get_index_output_auto_ssp_elines_rnd_rss_outFIT3D.pl
#
################################################################################

# System imports
import io
import sys
import numpy as np
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.tools import get_index
from pyFIT3D.common.constants import __indices__
from pyFIT3D.common.io import get_data_from_fits, get_wave_from_header

def parse_value(x):
    try:
        _x = eval(x)
    except (NameError, SyntaxError):
        _x = str(x)
    return _x

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['input_fits', 'n_sim', 'input_auto_ssp_rss_output']
    __optional__ = ['plot', 'output_file']
    __def_optional = {'plot': 0, 'output_file': 'none'}
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'input_fits': str, 'n_sim': eval, 'input_auto_ssp_rss_output': str}
    __conv_func_optional__ = {'plot': parse_value, 'output_file': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' output_auto_ssp_elines_several.RSS.cube.fits NSIM auto_ssp.rss.out [PLOT] [OUTPUT_FILE]'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        # self._parse_filenames()

def main(args):
    output_file = args.output_file
    clf = False
    if output_file is not None:
        if isinstance(output_file, io.TextIOWrapper):
            f = output_file
        else:
            clf = True
            f = open(output_file, 'w')
    else:
        f = sys.stdout
    redshift__s = np.loadtxt(args.input_auto_ssp_rss_output, usecols=7, delimiter=',')
    flux__tsw, h = get_data_from_fits(args.input_fits, header=True)
    flux_ssp__sw = flux__tsw[0] - flux__tsw[3]
    res__sw = flux__tsw[4]
    plot = 0 if args.plot is None else args.plot
    indices = get_index(get_wave_from_header(h, 1),
                        flux_ssp__sw, res__sw,
                        redshift__s, args.n_sim, plot)
    names__i = list(__indices__.keys())
    for i_s in range(res__sw.shape[0]):
        for i in range(len(names__i)):
            name = names__i[i]
            print(f'{name}', end=' ', file=f)
            EW_now = indices[name]['EW'][i_s]
            s_EW_now = indices[name]['sigma_EW'][i_s]
            print(f' {EW_now} {s_EW_now}', end=' ', file=f)
        SN = indices['SN'][i_s]
        e_SN = indices['e_SN'][i_s]
        print(f'SN  {SN} {e_SN}', file=f)
    if clf:
        f.close()

if __name__ == '__main__':
    # pa stands for parsed arguments
    main(ReadArgumentsLocal())
    # pa =
    # get_index_output_auto_ssp_elines_rnd_rss_outFIT3D(pa.input_fits, pa.n_sim,
    #                                                   pa.input_auto_ssp_rss_output, pa.plot)
