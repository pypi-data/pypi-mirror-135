#!/usr/bin/env python3
import sys
from os import getcwd
from os.path import basename, splitext

from pyFIT3D.common.io import readFileArgumentParser
from pyFIT3D.common.io import create_ConfigAutoSSP_from_lists
from pyFIT3D.common.io import create_emission_lines_file_from_list
from pyFIT3D.common.gas_tools import detect_create_ConfigEmissionModel
from pyFIT3D.common.io import create_emission_lines_mask_file_from_list

def parse_arguments(default_args_file=None):
    """
    Parse the command line args.

    With fromfile_pidxrefix_chars=@ we can read and parse command line args
    inside a file with @file.txt.
    default args inside default_args_file
    """
    default_args = {
        'sigma_guess': 2.5,
        'nsearch': 1,
        'peak_threshold': 2,
        'dmin': 2,
        'plot': 0,
        'sort_by_flux': False,
        'output_path': getcwd(),
        'crossmatch_list_filename': None,
        'crossmatch_absdmax_AA': 6,
    }

    help_args = {
        'filename': 'Spectrum file.',
        'nconf': 'It will divide the spectrum in nconf chunks to generate nconf ConfigEmissionModel files.',
        'redshift': 'Used to correct the peaks detected to write the ConfigEmissionModel and also to compare the detected peaks with a crossmatch list when required.',
        'sigma_guess': 'Sigma guess to the emission line fit config.',
        'nsearch': 'A peak will have the highest flux around the interval (in pixels): (peak - nsearch, peak + nsearch)',
        'peak_threshold': 'Defines the standard deviation multiplicative factor for the probable peak threshold calculation,',
        'dmin': 'Defines the minimal distance between peaks (in pixels).',
        'plot': '0 = no plot | 1 = plot in screen | 2 = plot to file',
        'output_path': 'Output path to write config and masks files.',
        'sort_by_flux': 'Creates the ConfigEmissionModel file sorted by the flux peak (descending order).',
        'crossmatch_list_filename': 'A file with a list of known emission lines rest-frame central wavelengths to compare and match the detected peaks.',
        'crossmatch_absdmax_AA': 'Maximal absolute distance in Angstrom to identify a emission line when using a crossmatch list file.',
    }

    parser = readFileArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument('--sigma_guess', '-S', metavar='FLOAT', type=float, default=default_args['sigma_guess'], help=help_args['sigma_guess'])
    parser.add_argument('--nsearch', '-N', metavar='INT', type=int, default=default_args['nsearch'], help=help_args['nsearch'])
    parser.add_argument('--peak_threshold', '-t', metavar='FLOAT', type=float, default=default_args['peak_threshold'], help=help_args['peak_threshold'])
    parser.add_argument('--dmin', '-d', metavar='INT', type=int, default=default_args['dmin'], help=help_args['dmin'])
    parser.add_argument('--crossmatch_absdmax_AA', metavar='INT', type=int, default=default_args['crossmatch_absdmax_AA'], help=help_args['crossmatch_absdmax_AA'])
    parser.add_argument('--output_path', '-O', metavar='OUTPUT_PATH', type=str, default=default_args['output_path'], help=help_args['output_path'])
    parser.add_argument('--crossmatch_list_filename', '-C', metavar='OUTPUT_PATH', type=str, default=default_args['crossmatch_list_filename'], help=help_args['crossmatch_list_filename'])
    parser.add_argument('--plot', '-p', type=int, choices=[0, 1, 2], help=help_args['plot'])
    parser.add_argument('--sort_by_flux', action='store_true', default=default_args['sort_by_flux'], help=help_args['sort_by_flux'])

    # positional args
    parser.add_argument('filename', metavar='SPECFILE', type=str, help=help_args['filename'])
    parser.add_argument('nconf', metavar='NCONF', type=int, help=help_args['nconf'])
    parser.add_argument('redshift', metavar='REDSHIFT', type=float, help=help_args['redshift'])

    parser.add_argument('--verbose', '-v', action='count', default=0)

    args_list = sys.argv[1:]
    # if exists file default.args, load default args
    if default_args_file is not None and isfile(default_args_file):
        args_list.insert(0, '@%s' % default_args_file)
    args = parser.parse_args(args=args_list)
    # TREAT ARGUMENTS HERE
    return args

def retrieve_spec(filename):
    from pyFIT3D.common.io import read_spectra
    # TODO READ CUBE AND FITS RSS
    _fname, _ext = splitext(filename)
    if _ext == '.fits' or ((_ext == '.gz') and (_fname[:-4] == 'fits')):
        print('Not implemented yed. TODO: read RSS and CUBE FITS')
    else:
        wl__w, f__w, _ = read_spectra(filename)
    return wl__w, f__w

def main(args):
    wave, flux = retrieve_spec(args.filename)
    r = detect_create_ConfigEmissionModel(wave, flux, redshift=args.redshift,
                                          sigma_guess=args.sigma_guess,
                                          chunks=args.nconf,
                                          peak_find_nsearch=args.nsearch,
                                          peak_find_threshold=args.peak_threshold,
                                          peak_find_dmin=args.dmin,
                                          flux_boundaries_fact=None,
                                          sigma_boundaries_fact=None,
                                          v0_boundaries_add=None,
                                          polynomial_order=None,
                                          polynomial_coeff_guess=None,
                                          polynomial_coeff_boundaries=None,
                                          plot=args.plot,
                                          output_path=args.output_path,
                                          sort_by_flux=args.sort_by_flux,
                                          crossmatch_list_filename=args.crossmatch_list_filename,
                                          crossmatch_absdmax_AA=args.crossmatch_absdmax_AA,
                                          verbose=args.verbose)
    config_filenames, wl_chunks, wave_peaks_tot, wave_peaks_tot_corr = r
    create_emission_lines_file_from_list(wave_peaks_tot, output_path=args.output_path)
    create_emission_lines_mask_file_from_list(wave_peaks_tot_corr, eline_half_range=8*args.sigma_guess, output_path=args.output_path)
    create_ConfigAutoSSP_from_lists(wl_chunks, config_filenames, output_path=args.output_path)

if __name__ == '__main__':
    # main(ReadArgumentsLocal())
    main(parse_arguments())





# list_eml = []
# list_eml_assoc = []
# list_eml_ind_assoc = []
# for w in wref:
#     absdist = np.abs(w - wl)
#     _where = np.where(absdist < 6)[0]
#     # while _where.size > 0:
#     tmp_wl = copy(wl)
#     tmp_ind_wl = np.arange(wl.size)
#     tmp_wl = tmp_wl.tolist()
#     tmp_ind_wl = tmp_ind_wl.tolist()
#     if _where.size > 0:
#         print(w, _where.size)
#         if _where.size == 1:
#             i_assoc = _where[0]
#             wl_assoc = wl[i_assoc]
#             print('w=', w, 'i_assoc=',i_assoc, 'wl_assoc=', wl_assoc)
#         else:
#             _iSwhere = np.argsort(absdist[_where])
#             #print(_where, absdist[_where], _iSwhere, absdist[_where[_iSwhere]])
#             #print(_where[_iSwhere[0]])
#             i_assoc = _where[_iSwhere[0]]
#             print('w=', w, 'i_assoc=',i_assoc, 'wl_assoc=', wl[i_assoc])
#         if w in list_eml:
#             i_list_eml = list_eml.index(w)
#             _prev_wl_assoc = wl[i_list_eml]
#             _prev_dist = np.abs(w - _prev_wl_assoc)
#             _dist = np.abs(w - wl_assoc)
#             print(_prev_dist, _dist)
#         else:
#             list_eml.append(w)
#             list_eml_assoc.append(wl_assoc)
#             list_eml_ind_assoc.append(i_assoc)
