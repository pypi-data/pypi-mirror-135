#!/usr/bin/env python3
import sys
import numpy as np
from os.path import basename, isfile
from pyFIT3D.common.io import ReadArguments, readFileArgumentParser
from pyFIT3D.common.auto_ssp_tools import auto_ssp_spec
from pyFIT3D.common.constants import __selected_R_V__, __selected_extlaw__
# from auto_ssp_elines_rnd_sigma_inst import ReadArgumentsLocal

# def debug_var(debug_mode=False, **kwargs):
#     pref = kwargs.pop('pref', '>>>')
#     verbose_level = kwargs.pop('verbose_level', 0)
#     pref = '\t' * verbose_level + pref
#     if debug_mode:
#         for kw, vw in kwargs.items():
#             if isinstance(vw, dict):
#                 print('%s') % pref, kw
#                 for k, v in vw.items():
#                     print('\t%s' % pref, k, ':\t', v)
#             else:
#                 print('%s' % pref, '%s:\t' % kw, vw)
#
# def parse_old_arguments(append_args=None):
#     # create new scheme
#     oa = ReadArgumentsLocal()
#     new_argv = f'{sys.argv[0]} --error_file {oa.error_file} --nl_ssp_models_file {oa.ssp_nl_fit_file}'
#     new_argv += f' --out_file {oa.out_file} --mask_list {oa.mask_list} --elines_mask_file {oa.elines_mask_file}'
#     new_argv += f' --instrumental_dispersion {oa.sigma_inst} --min_flux_plot {oa.min} --max_flux_plot {oa.max}'
#     new_argv += f' --wl_range {oa.w_min} {oa.w_max} --nl_wl_range {oa.nl_w_min} {oa.nl_w_max} --plot {oa.plot}'
#     new_argv += f' --redshift_set {oa.input_redshift} {oa.delta_redshift} {oa.min_redshift} {oa.max_redshift}'
#     new_argv += f' --losvd_set {oa.input_sigma} {oa.delta_sigma} {oa.min_sigma} {oa.max_sigma}'
#     new_argv += f' --AV_set {oa.input_AV} {oa.delta_AV} {oa.min_AV} {oa.max_AV}'
#     if append_args is not None:
#         for k, v in append_args.items():
#             new_argv += f' {k} {v}'
#     new_argv += f' {oa.spec_file} {oa.ssp_file} {oa.config_file}'
#     return new_argv.split()

def parse_arguments(default_args_file=None):
    """
    Parse the command line args.

    With fromfile_pidxrefix_chars=@ we can read and parse command line args
    inside a file with @file.txt.
    default args inside default_args_file
    """
    default_args = {
        'error_file': None, 'error_flux_variance': False, 'single_ssp': False,
        'nl_ssp_models_file': None, 'out_file': 'auto_ssp.out',
        'mask_list': None, 'elines_mask_file': None,
        'plot': 0,  # TODO: 'plot': False, 'plot_to_file': '',
        'min_flux_plot': None, 'max_flux_plot': None,
        'instrumental_dispersion': None, 'wl_range': None, 'nl_wl_range': None,
        'redshift_set': None, 'losvd_set': None, 'AV_set': None,
        'fit_sigma_nnls': False, 'no_eml_fit': False, 'sigma_in_AA': False,
        'losvd_rnd_medres_merit': False,
        'extlaw': __selected_extlaw__, 'R_V': __selected_R_V__,
    }

    help_args = {
        'spec_file': 'A file containing the spectrum information (columns should be: ID WAVELENGTH FLUX [ERROR_FLUX])',
        'error_file': 'An optional file with the error (std-dev) of the obseved spectrum',
        'ssp_models_file': 'Stellar population synthesis models. For more information about ssp_models file see README.txt.',
        'nl_ssp_models_file': 'Stellar population models used for the fit of the non-linear parameters (redshift, sigma and AV). If not used, the program uses SSP_MODELS_FILE by default',
        'config_file': 'Auto-SSP config file',
        'mask_list': 'Rest-frame wavelength ranges to be masked',
        'elines_mask_file': 'File with rest-frame emission lines central wavelength masked during the non-linear fit and stellar population synthesis',
        'out_file': 'The output parameters file. Also will set the filename prefix for other produced files',
        'instrumental_dispersion': 'The instrumental dispersion of the observed spectra. Unit in Angstroms.',
        'min_flux_plot': 'Used when plot != 0. Set the min flux used in plots',
        'max_flux_plot': 'Used when plot != 0. Set the max flux used in plots',
        'wl_range': 'Stellar population synthesis wavelength range',
        'nl_wl_range': 'Non-linear parameters fit wavelength range (only used in redshift and sigma fit)',
        'plot': '0 = no plot | 1 = plot in screen | 2 = plot to file',
        # TODO: 'plot_to_file': 'All plots to files.'
        'redshift_set': 'Redshift fit setup. The inputs are GUESS DELTA MIN MAX',
        'losvd_set': 'Line-of-sight velocity dispersion fit setup. The inputs are in the same way as the redshift fit setup. The used unit is Angstrom when --sigma_in_AA active, otherwise in km/s.',
        'AV_set': 'Dust extinction parameter fit setup. The inputs are in the same way as the redshift fit setup. The used unit is mag.',
        'no_eml_fit': 'Do not perform the emission lines fit',
        'sigma_in_AA': 'Set the line-of-sight velocity dispersion unit as Angstroms',
        'error_flux_variance': 'Treat the optional ERROR_FLUX column of spec_file as variance',
        'force_seed': 'Force the seed of the random number generator',
        'fit_sigma_nnls': 'Fit sigma using non-negative least squares (faster but less precise)',
        'single_ssp': 'Run the stellar population synthesis looking for a single SSP as an answer',
        'losvd_rnd_medres_merit': 'When using the default losvd fit, uses the median of the residual spectrum (obs - mod) instead the Chi-squared as the merit function',
        'R_V': 'R_V extinction factor: R_V=A_V/E(B-V)',
        'extlaw': 'Extinction law used. Cardelli, Clayton & Mathis (CCM) or Calzetti (CAL)',
    }

    parser = readFileArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument('--error_file', metavar='FILE', type=str, default=default_args['error_file'], help=help_args['error_file'])
    parser.add_argument('-n','--nl_ssp_models_file', metavar='FILE', type=str, default=default_args['nl_ssp_models_file'], help=help_args['nl_ssp_models_file'])
    parser.add_argument('--mask_list', metavar='FILE', type=str, default=default_args['mask_list'], help=help_args['mask_list'])
    parser.add_argument('--elines_mask_file', metavar='FILE', type=str, default=default_args['elines_mask_file'], help=help_args['elines_mask_file'])
    parser.add_argument('--out_file', '-o', metavar='FILE', type=str, default=default_args['out_file'], help=help_args['out_file'])
    parser.add_argument('--instrumental_dispersion', '-d', metavar='FLOAT', type=float, default=default_args['instrumental_dispersion'], help=help_args['instrumental_dispersion'])
    parser.add_argument('--min_flux_plot', metavar='FLOAT', type=float, default=default_args['min_flux_plot'], help=help_args['min_flux_plot'])
    parser.add_argument('--max_flux_plot', metavar='FLOAT', type=float, default=default_args['max_flux_plot'], help=help_args['max_flux_plot'])
    parser.add_argument('--wl_range', nargs=2, metavar='INT', type=int, help=help_args['wl_range'])
    parser.add_argument('--nl_wl_range', nargs=2, metavar='INT', type=int, help=help_args['nl_wl_range'])
    parser.add_argument('--force_seed', metavar='INT', help=help_args['force_seed'])
    parser.add_argument('--R_V', metavar='FLOAT', type=float, default=default_args['R_V'], help=help_args['R_V'])
    parser.add_argument('--extlaw', type=str, choices=['CCM', 'CAL'], default=default_args['extlaw'], help=help_args['extlaw'])
    # TODO: plot to file
    parser.add_argument('--plot', '-p', type=int, choices=[0, 1, 2], help=help_args['plot'])
    # parser.add_argument('--plot', '-p', action='store_true', default=default_args['plot'], help=help_args['plot'])
    # parser.add_argument('--plot_to_file', metavar='FILE_PREFIX', type=str, default=default_args['plot_to_file'], help=help_args['plot_to_file'])
    parser.add_argument('--redshift_set', '-R', type=float, nargs=4, metavar='FLOAT', help=help_args['redshift_set'])
    parser.add_argument('--losvd_set', '-S', type=float, nargs=4, metavar='FLOAT', help=help_args['losvd_set'])
    parser.add_argument('--AV_set', '-A', type=float, nargs=4, metavar='FLOAT', help=help_args['AV_set'])
    parser.add_argument('--single_ssp', action='store_true', default=default_args['single_ssp'], help=help_args['single_ssp'])
    parser.add_argument('--no_eml_fit', action='store_true', default=default_args['no_eml_fit'], help=help_args['no_eml_fit'])
    parser.add_argument('--sigma_in_AA', action='store_true', default=default_args['sigma_in_AA'], help=help_args['sigma_in_AA'])
    parser.add_argument('--error_flux_variance', action='store_true', default=default_args['error_flux_variance'], help=help_args['error_flux_variance'])
    parser.add_argument('--fit_sigma_nnls', action='store_true', default=default_args['fit_sigma_nnls'], help=help_args['fit_sigma_nnls'])
    parser.add_argument('--losvd_rnd_medres_merit', action='store_true', default=default_args['losvd_rnd_medres_merit'], help=help_args['losvd_rnd_medres_merit'])

    # positional arguments
    parser.add_argument('spec_file', metavar='SPEC_FILE', type=str, help=help_args['spec_file'])
    parser.add_argument('ssp_models_file', metavar='SSP_MODELS_FILE', type=str, help=help_args['ssp_models_file'])
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=str, help=help_args['config_file'])

    parser.add_argument('--verbose', '-v', action='count', default=0)

    args_list = sys.argv[1:]
    # if exists file default.args, load default args
    if default_args_file is not None and isfile(default_args_file):
        args_list.insert(0, '@%s' % default_args_file)
    args = parser.parse_args(args=args_list)
    # TREAT ARGUMENTS HERE
    print(f'ef={args.error_file} sp={args.spec_file}')
    print(f'sspnlf={args.nl_ssp_models_file} sspf={args.ssp_models_file}')
    return args

if __name__ == '__main__':
    # already in new format
    # if len(sys.argv) > 1 and (not (sys.argv[1].startswith('-') or sys.argv[1].startswith('@'))):
    #     sys.argv = parse_old_arguments()
    #     for i, arg in enumerate(sys.argv):
    #         print(i, arg)
    pa = parse_arguments()
    # debug_var(True, parsed_arguments=pa)
    # sys.exit()

    # pa = ReadArgumentsLocal()
    auto_ssp_spec(
        spec_file=pa.spec_file,
        ssp_models_file=pa.ssp_models_file,
        config_file=pa.config_file,
        out_file=pa.out_file,

        error_file=pa.error_file,
        nl_ssp_models_file=pa.nl_ssp_models_file,
        mask_list=pa.mask_list, elines_mask_file=pa.elines_mask_file,
        instrumental_dispersion=pa.instrumental_dispersion,
        wl_range=pa.wl_range, nl_wl_range=pa.nl_wl_range,
        plot=pa.plot, min=pa.min_flux_plot, max=pa.max_flux_plot,

        redshift_set=pa.redshift_set, losvd_set=pa.losvd_set, AV_set=pa.AV_set,

        fit_gas=(not pa.no_eml_fit),
        variance_error_column=pa.error_flux_variance,
        fit_sigma_rnd=(not pa.fit_sigma_nnls),
        seed=pa.force_seed,
        single_ssp=pa.single_ssp,
        losvd_rnd_medres_merit=pa.losvd_rnd_medres_merit,

        verbose=pa.verbose,

        # TODO: this option need to be implemented in StPopSynt class
        losvd_in_AA=pa.sigma_in_AA,
        R_V=pa.R_V, extlaw=pa.extlaw,
    )
