#!/usr/bin/env python3
import sys
import numpy as np
from os.path import basename, isfile
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.gas_tools import kin_rss_elines

np.set_printoptions(precision=4, suppress=True, linewidth=200)

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for script that fits the emission-lines of a RSS FITS.

    To add an argument to the script:
        Argument name in `__mandatory__` or `__optional__` list.
        Argument conversion function in `__mandatory_conv_func___` or `__optional_conv_func___` list.
        Argument default value (if not mandatory) in `__def_optional__`
    """
    # class static configuration:
    # arguments names and conversion string to number functions
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['spec_file', 'config_file', 'mask_file', 'w_min', 'w_max', 'out_file']
    __optional__ = ['n_MC', 'n_loops', 'plot', 'scale_ini', 'guided', 'memo', 'prefix']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    # default values of optional arguments with __optional__ as keys
    __def_optional__ = {
        'n_MC': 50, 'n_loops': 15, 'plot': 0, 'scale_ini': 0.15, 'guided': 0, 'memo': 0,
        # 'out_file': 'out.fit_spectra',
        # 'out_mod_res_final': __script_name__.replace('.py', '.out')
    }

    # parse functions
    __conv_func_mandatory__ = {'spec_file': str, 'config_file': str, 'mask_file': str, 'out_file': str}
    __conv_func_optional__ = {'prefix': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    # usage message
    __usage_msg__ = 'usage: {} SPECTRUM_FILE[,ERROR_FILE] CONFIG MASK_LIST W_MIN W_MAX OUTFILE'.format(__script_name__)
    __usage_msg__ += ' [N_MC={:d}]'.format(__def_optional__['n_MC'])
    __usage_msg__ += ' [N_LOOPS={:d}]]'.format(__def_optional__['n_loops'])
    __usage_msg__ += ' [PLOT] [SCALE_INI={:.2f}]'.format(__def_optional__['scale_ini'])
    __usage_msg__ += ' [guided] [MEMO=0/1]'
    # __usage_msg__ += ' [OUTPUT_FILENAME] [OUTPUT_MOD_RES_FILENAME]'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self.redefine_max = 0
        self._parse_filenames()

    def _parse_filenames(self):
        self.error_file = None
        spec_file_args = self.spec_file.split(',')
        if len(spec_file_args) == 2:
            self.spec_file = spec_file_args[0]
            self.error_file = spec_file_args[1]

if __name__ == "__main__":
    # parse arguments
    pa = ReadArgumentsLocal()
    kin_rss_elines(spec_file=pa.spec_file, config_file=pa.config_file, guided=pa.guided,
                   w_min=pa.w_min, w_max=pa.w_max, out_file=pa.out_file, mask_file=pa.mask_file,
                   error_file=pa.error_file, n_MC=pa.n_MC, n_loops=pa.n_loops, plot=pa.plot,
                   scale_ini=pa.scale_ini, memo=pa.memo, run_mode='RND',
                   prefix=pa.prefix, seed=None)
