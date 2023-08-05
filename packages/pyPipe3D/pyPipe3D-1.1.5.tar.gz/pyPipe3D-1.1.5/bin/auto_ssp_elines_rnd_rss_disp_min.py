#!/usr/bin/env python3
import sys
import numpy as np
from os.path import basename
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.auto_ssp_tools import auto_ssp_elines_rnd_rss

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for the SSP models fit scripts.

    To add an argument to the script:
        Argument name in `__mandatory__` or `__optional__` list.
        Argument conversion function in `__mandatory_conv_func___` or `__optional_conv_func___` list.
        Argument default value (if not mandatory) in `__def_optional__`
    """
    # class static configuration:
    # arguments names and conversion string to number functions
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['spec_file', 'ssp_files', 'out_file', 'mask_list', 'config_file', 'plot']
    __optional__ = ['min', 'max', 'w_min', 'w_max', 'elines_mask_file', 'input_redshift', 'delta_redshift', 'min_redshift', 'max_redshift', 'input_sigma', 'delta_sigma', 'min_sigma', 'max_sigma', 'input_AV', 'delta_AV', 'min_AV', 'max_AV']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)
    # default values of optional arguments following __optional__ order
    __def_optional__ = {'input_redshift': 0}

    # parse functions
    __conv_func_mandatory__ = {'spec_file': str, 'ssp_files': str, 'out_file': str, 'mask_list': str, 'config_file': str}
    __conv_func_optional__ = {'elines_mask_file': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    # usage message
    __usage_msg__ = 'USE: {} SPEC1.RSS.fits[,ERROR.RSS.fits] SSP_SFH.fits,SSP_KIN.fits OUTFILE MASK_LIST CONFIG_FILE PLOT'.format(__script_name__)
    __usage_msg__ += ' [min max] [wmin[,wmin2]] [wmax[,wmax2]] [redshift_elines_to_mask] [input_redshift delta_redshift min_redshift max_redshift]'
    __usage_msg__ += ' [input_sigma delta_sigma min_sigma max_sigma] [input_AV delta_AV min_AV max_AV] \n'
    __usage_msg__ += 'CONFIG_FILE:\n'
    __usage_msg__ += 'redshift delta_redshift min_redshift max_redshift\n'
    __usage_msg__ += 'sigma delta_sigma min_sigma max_sigma (Angstroms)\n'
    __usage_msg__ += 'AV delta_AV min_AV max_AV [Same range for all - magnitudes ]\n'
    __usage_msg__ += 'N_SYSTEMS\n'
    __usage_msg__ += '(1) START_W END_W MASK_FILE CONFIG_FILE NPOLY MASK_FILE_POLY\n'
    __usage_msg__ += '...\n'
    __usage_msg__ += '(N) START_W END_W MASK_FILE CONFIG_FILE NPOLY MASK_FILE_POLY\n'
    __usage_msg__ += 'MIN_DELTA_CHISQ MAX_NITER CUT_MEDIAN_FLUX\n'
    __usage_msg__ += 'start_w_peak end_w_peak\n'
    __usage_msg__ += 'wavelength_to_norm width_AA new_back_templates.fits\n'

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self._parse()

    def _parse(self):
        self.error_file = None
        spec_file_args = self.spec_file.split(',')
        if len(spec_file_args) == 2:
            self.spec_file = spec_file_args[0]
            self.error_file = spec_file_args[1]
        print(f'ef={self.error_file} sp={self.spec_file}')
        if self.w_min is None:
            self.w_min = -np.inf
        if self.w_max is None:
            self.w_max = np.inf
        self.nl_w_min = self.w_min
        self.nl_w_max = self.w_max
        if isinstance(self.w_min, tuple):
            w_min = self.w_min[0]
            nl_w_min = self.w_min[1]
            self.nl_w_min = nl_w_min
            self.w_min = w_min
        if isinstance(self.w_max, tuple):
            w_max = self.w_max[0]
            nl_w_max = self.w_max[1]
            self.nl_w_max = nl_w_max
            self.w_max = w_max
        self._parse_ssp_sigma_inst()
        self._final_check()

    def _final_check(self):
        self.redef = 0
        if self.min is not None and self.max is not None:
            self.redef = 1
        if self.w_min is not None and self.w_max is not None:
            self.redef = 2
        self.redshift_set = None
        if ((self.input_redshift is not None) and (self.delta_redshift is not None)
            and (self.min_redshift is not None) and (self.max_redshift is not None)):
            self.redshift_set = [self.input_redshift, self.delta_redshift,
                                 self.min_redshift, self.max_redshift]
        self.sigma_set = None
        if ((self.input_sigma is not None) and (self.delta_sigma is not None)
            and (self.min_sigma is not None) and (self.max_sigma is not None)):
            self.sigma_set = [self.input_sigma, self.delta_sigma,
                              self.min_sigma, self.max_sigma]
        self.AV_set = None
        if ((self.input_AV is not None) and (self.delta_AV is not None)
            and (self.min_AV is not None) and (self.max_AV is not None)):
            self.AV_set = [self.input_AV, self.delta_AV,
                              self.min_AV, self.max_AV]

    def _parse_ssp_sigma_inst(self):
        # parse SSP_SFH.fits,SSP_KIN.fits,sigma_inst argument
        ssp_args = self.ssp_files.split(',')
        n = len(ssp_args)
        self.ssp_file = ssp_args[0]
        self.ssp_nl_fit_file = ssp_args[0]
        if n > 1:
            self.ssp_nl_fit_file = ssp_args[1]
        print(f'sspnlf={self.ssp_nl_fit_file} sspf={self.ssp_file}')

if __name__ == '__main__':
    pa = ReadArgumentsLocal()
    auto_ssp_elines_rnd_rss(
        spec_file=pa.spec_file,
        error_file=pa.error_file,
        ssp_file=pa.ssp_file,
        ssp_nl_fit_file=pa.ssp_nl_fit_file,
        out_file=pa.out_file,
        config_file=pa.config_file,
        mask_list=pa.mask_list,
        elines_mask_file=pa.elines_mask_file,
        sigma_inst=None,
        min=pa.min, max=pa.max,
        w_min=pa.w_min, w_max=pa.w_max,
        nl_w_min=pa.nl_w_min, nl_w_max=pa.nl_w_max,
        plot=pa.plot,
        input_redshift=pa.input_redshift, delta_redshift=pa.delta_redshift, min_redshift=pa.min_redshift, max_redshift=pa.max_redshift,
        input_sigma=pa.input_sigma, delta_sigma=pa.delta_sigma, min_sigma=pa.min_sigma, max_sigma=pa.max_sigma,
        input_AV=pa.input_AV, delta_AV=pa.delta_AV, min_AV=pa.min_AV, max_AV=pa.max_AV,
        is_guided_sigma=True
    )
