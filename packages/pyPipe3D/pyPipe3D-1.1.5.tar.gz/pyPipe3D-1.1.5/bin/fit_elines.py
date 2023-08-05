#!/usr/bin/env python3
import sys
import numpy as np
from os.path import basename
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.gas_tools import fit_elines

np.set_printoptions(precision=4, suppress=True, linewidth=200)

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for the emission-lines fit scripts.

    To add an argument to the script:
        Argument name in `__mandatory__` or `__optional__` list.
        Argument conversion function in `__mandatory_conv_func___` or `__optional_conv_func___` list.
        Argument default value (if not mandatory) in `__def_optional__`
    """
    # class static configuration:
    # arguments names and conversion string to number functions
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['spec_file', 'config_file', 'mask_file', 'w_min', 'w_max']
    __optional__ = [
        'redefine_max', 'n_MC', 'n_loops', 'plot', 'scale_ini', 'out_file',
        'out_mod_res_final'
    ]
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    # default values of optional arguments with __optional__ as keys
    __def_optional__ = {
        'redefine_max': '0', 'n_MC': '50', 'n_loops': '15', 'plot': '0', 'scale_ini': '0.15',
        # 'out_file': __script_name__.replace('.py', '.out'),
        # 'out_mod_res_final': 'out.fit_spectra'
        'out_file': 'out.fit_spectra',
        'out_mod_res_final': __script_name__.replace('.py', '.out'),
    }

    # parse functions
    __conv_func_mandatory__ = {'spec_file': str, 'config_file': str, 'mask_file': str}
    __conv_func_optional__ = {'out_file': str, 'out_mod_res_final': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    # usage message
    __usage_msg__ = 'usage: {} SPECTRUM_FILE CONFIG MASK_LIST W_MIN W_MAX'.format(__script_name__)
    __usage_msg__ += ' [REDEFINE_MAX] [N_MC={:d}]'.format(eval(__def_optional__['n_MC']))
    __usage_msg__ += ' [N_LOOPS={:d}]]'.format(eval(__def_optional__['n_loops']))
    __usage_msg__ += ' [PLOT] [SCALE_INI={:.2f}]'.format(eval(__def_optional__['scale_ini']))
    __usage_msg__ += ' [OUTPUT_FILENAME] [OUTPUT_MOD_RES_FILENAME]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)

#############################################################################
################################## BEGIN ####################################
#############################################################################
if __name__ == '__main__':
    # read arguments
    pa = ReadArgumentsLocal()
    fit_elines(spec_file=pa.spec_file, config_file=pa.config_file, mask_file=pa.mask_file,
               w_min=pa.w_min, w_max=pa.w_max, redefine_max=pa.redefine_max,
               n_MC=pa.n_MC, n_loops=pa.n_loops, plot=pa.plot, scale_ini=pa.scale_ini,
               out_file=pa.out_file, out_mod_res_final=pa.out_mod_res_final,
               run_mode='both', seed=None, check_stats=False)
