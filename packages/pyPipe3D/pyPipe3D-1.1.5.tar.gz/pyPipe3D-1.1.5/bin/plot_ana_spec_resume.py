#!/usr/bin/env python3
import os
import sys
import errno
import itertools
import numpy as np
import pandas as pd
from os.path import basename, isfile, dirname, join

import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['legend.numpoints'] = 1
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(context='paper', style='ticks', palette='colorblind', color_codes=True,
        font_scale=1.5)

from pyFIT3D.common.auto_ssp_tools import ConfigAutoSSP
from pyFIT3D.common.gas_tools import read_fit_elines_output
from pyFIT3D.common.io import trim_waves, sel_waves, print_verbose
from pyFIT3D.common.io import ReadArguments, readFileArgumentParser
from pyFIT3D.common.io import get_data_from_fits, get_wave_from_header
from pyFIT3D.common.constants import __c__, __mask_elines_window__
from pyFIT3D.common.constants import _MODELS_ELINE_PAR, __sigma_to_FWHM__

__solar_metallicity__ = 0.019

latex_ppi = 72.0

latex_column_width_pt = 240.0
latex_column_width = latex_column_width_pt/latex_ppi

latex_text_width_pt = 504.0
latex_text_width = latex_text_width_pt/latex_ppi

golden_mean = 0.5 * (1. + 5**0.5)
aspect = 1/golden_mean

def parse_arguments(default_args_file=None):
    default_args = {
        'mask_list': None,
        'elines_mask_file': None,
        'img_suffix': 'pdf',
        'dpi': 300,
        'cmap': 'Blues',
        'wl_range': [3800, 6850],
        'fraction': False,
        'instrumental_dispersion': None,
        'block': False,
    }

    help_args = {
        'fraction': 'Display coeffs in fractions instead percent.',
        'block': 'Block image at the end waiting for the user to close the window.',
    }

    parser = readFileArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--mask_list', metavar='FILE', type=str,
                        default=default_args['mask_list'])
    parser.add_argument('--elines_mask_file', metavar='FILE', type=str,
                        default=default_args['elines_mask_file'])
    parser.add_argument('--img_suffix', '-i', metavar='IMG_SUFFIX', type=str,
                        default=default_args['img_suffix'])
    parser.add_argument('--dpi', metavar='INT', type=int, default=default_args['dpi'])
    parser.add_argument('--cmap', metavar='COLORMAP', type=str,
                        default=default_args['cmap'])
    parser.add_argument('--wl_range', nargs=2, metavar='INT', type=int)
    parser.add_argument('--fraction', action='store_true',
                        default=default_args['fraction'], help=help_args['fraction'])
    parser.add_argument('--block', action='store_true', default=default_args['block'],
                        help=help_args['block'])
    parser.add_argument('--instrumental_dispersion', '-d', metavar='FLOAT', type=float,
                        default=default_args['instrumental_dispersion'])
    # positional arguments
    parser.add_argument('out_file', metavar='OUT_FILE', type=str)
    parser.add_argument('--verbose', '-v', action='count', default=0)

    args_list = sys.argv[1:]
    # if exists file default.args, load default args
    if default_args_file is not None and isfile(default_args_file):
        args_list.insert(0, '@%s' % default_args_file)
    args = parser.parse_args(args=args_list)
    # TREAT ARGUMENTS HERE
    # parse filenames
    dname = os.path.dirname(args.out_file)
    if dname:
        _bn = basename(args.out_file)
    else:
        _bn =args.out_file

    args.out_file_fit = join(dname, 'output.' + _bn + '.fits')
    if not isfile(args.out_file_fit):
        args.out_file_fit += '.gz'
    args.out_file_elines = join(dname, 'elines_' + _bn)
    args.out_file_elines = 'elines_' + args.out_file
    args.out_file_coeffs = join(dname, 'coeffs_' + _bn)
    for _f in [args.out_file, args.out_file_fit, args.out_file_coeffs]:
        if not isfile(_f):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), _f)
    return args

def plot_output_resume(wl, spec__tw, output_results, coeffs, masks, e_masks,
                       el_wl_fit, wl_range=[3800, 6850], cmap='Blues',
                       vmin=0.1, vmax=50, sigma_unit='km/s', percent=True):
    fmt = '.1f' if percent else '.3f'
    wlmsk = np.ones_like(wl, dtype='bool')
    if wl_range is not None:
        wlmsk = trim_waves(wl, wl_range)
    else:
        wl_range = [wl.min(), wl.max()]

    f = plt.figure()
    width = 2*latex_text_width
    f.set_size_inches(width, 0.7*width*aspect)

    gs = f.add_gridspec(3,4)
    ax_sp = f.add_subplot(gs[:2, :3])
    ax = f.add_subplot(gs[2, :])

    ax_lw = f.add_subplot(gs[:2, 3])
    ax_lw.set_axis_off()

    msg = r'$\chi^2$ = %6.2f' % output_results[0]
    msg += '\n'
    msg += r'RMS Flux = %6.2f' % output_results[13]
    msg += '\n'
    msg += '\n'
    msg += r'sys vel = %6.2f +/- %.2f km/s' % (output_results[7]*__c__, output_results[8]*__c__)
    msg += '\n'
    msg += r'$\sigma^\star$ = %6.2f +/- %0.2f' % (output_results[9], output_results[10])
    msg += sigma_unit
    msg += '\n'
    msg += r'${\rm A}_{\rm V}^\star$ = %6.2f +/- %0.2f' % (output_results[5], output_results[6])
    msg += '\n'
    msg += '\n'
    msg += r'$\left< \log {\rm t^\star} \right>_{\rm L}$ = %6.2f +/- %0.2f Gyr' % (output_results[1], output_results[2])
    msg += '\n'
    msg += r'$\left< \log {\rm Z}^\star \right>_{\rm L}$ = %6.2f +/- %0.2f [Z/H]' % (output_results[3], output_results[4])
    msg += '\n'
    msg += r'$\left< \log {\rm t^\star} \right>_{\rm M}$ = %6.2f +/- %0.2f Gyr' % (output_results[15], output_results[16])
    msg += '\n'
    msg += r'$\left< \log {\rm Z}^\star \right>_{\rm M}$ = %6.2f +/- %0.2f [Z/H]' % (output_results[17], output_results[18])
    # msg += '\n'
    # msg += r'$\log {\rm M}/{\rm M}$ = %6.2f' % output_results[-2]

    ax_lw.text(0.02, 0.9, msg, transform=ax_lw.transAxes, ha='left', va='top', fontsize=13)

    in_spec = spec__tw[0][wlmsk]
    out_spec = spec__tw[1][wlmsk]
    out_spec_joint = spec__tw[2][wlmsk]

    res = in_spec - out_spec
    wl = wl[wlmsk]
    ax_sp.set_ylabel('Flux [$10^{-16}$ erg/s/cm$^2$]')
    ax_sp.set_xlabel('wavelength [\AA]')
    ax_sp.plot(wl, in_spec, '-k', lw=3)
    ax_sp.plot(wl, out_spec, '-y', lw=0.7)
    ax_sp.plot(wl, (in_spec - out_spec), '-r', lw=1)

    if masks is not None:
        _ = [ax_sp.axvspan(msk[0], msk[1], alpha=0.3, color='gray') for msk in masks if msk[0] < wl_range[1]]
    if e_masks is not None:
        for msk in e_masks:
            l, r = msk
            if r > wl_range[1]:
                r = wl_range[1]
            if l > wl_range[0]:
                ax_sp.axvspan(l, r, alpha=0.2, color='blue')

    # Plot EL
    _ = [ax_sp.axvline(x=wlc, color='k', ls='--') for wlc in el_wl_fit]

    # COEFFS HEATMAP
    pwei, met_weights, age_weights = calc_weights(coeffs)
    pwei = pwei.T
    pwei.sort_index(axis='index', ascending=False, inplace=True)
    sns.heatmap((pwei / pwei.values.sum() * 100 if percent else pwei), cmap=cmap,
                center=None, vmin=vmin, vmax=vmax, square=False, linewidths=1.0,
                linecolor='w', annot=True, fmt=fmt, annot_kws={'fontsize':12},
                cbar=False, ax=ax,
                xticklabels=list(map(lambda v: '$%5.2f$'%v, np.log10(pwei.columns*1e9))),
                yticklabels=list(map(lambda v: '$%5.2f$'%v, pwei.index)))

    ax.set_xlabel(r'$\log {\rm t}^\star$ [yr]')
    ax.set_ylabel(r'$\log {\rm Z}^\star$ [${\rm Z}/{\rm Z}_\odot$]')
    ax_sp.set_xlim(wl_range)
    f.tight_layout()
    return f

def calc_weights(df):
    """Return the pivot matrix with coefficients and the
    marginal weights in age and metallicity"""
    coeffs = df.pivot_table(index="AGE", columns="MET", values="COEFF")

    met = coeffs.columns.values

    met_weights = coeffs / coeffs.sum(axis="columns", skipna=True).values[:,None]
    met_weights = met_weights.values[:,:,None].transpose(0,2,1)

    age_weights = coeffs.sum(axis="columns", skipna=True)
    age_weights /= np.nansum(age_weights)
    age_weights = age_weights.values[None,:]

    return coeffs, met_weights, age_weights

def read_masks(mask_list=None, elines_mask_file=None, redshift=0, sigma_mean=1,
               eline_half_range=None, verbose=0):
    masks = None
    e_w = None
    e_masks = None
    if mask_list is not None:
        if isfile(mask_list):
            masks = np.loadtxt(mask_list)
        else:
            print(f'{basename(sys.argv[0])}: {mask_list}: mask list file not found')
            mask_list = None
    else:
        print(f'{basename(sys.argv[0])}: no mask list file')
        # read elines mask
    if elines_mask_file is not None:
        if isfile(elines_mask_file):
            e_w = np.loadtxt(elines_mask_file, usecols=(0))
        else:
            print(f'{basename(sys.argv[0])}: {elines_mask_file}: emission lines mask file not found')
            elines_mask_file = None
    else:
        print(f'{basename(sys.argv[0])}: no elines mask file')

    z_fact = 1 + redshift
    eline_half_range = __mask_elines_window__ if eline_half_range is None else eline_half_range
    if e_w is not None:
        e_masks = np.empty((e_w.size, 2), dtype=np.float)
        eline_half_range *= sigma_mean
        if eline_half_range < 4:
            eline_half_range = 4
        e_masks[:,0] = e_w*z_fact - eline_half_range
        e_masks[:,1] = e_w*z_fact + eline_half_range
        e_masks = e_masks
        print_verbose(f'- Update emission line masks: ', verbose=verbose, level=2)
        print_verbose(e_masks, verbose=verbose, level=2)
        # if needed a complete mask:
    return masks, e_masks

def main(args):
    # read spec
    spec__tw, h = get_data_from_fits(args.out_file_fit, header=True)
    wl = get_wave_from_header(h)
    # read props
    props = np.loadtxt(args.out_file, delimiter=',', unpack=True)
    # read coeffs
    df = pd.read_csv(args.out_file_coeffs, sep='\t', usecols=[0, 1, 2, 3],
                     comment='#', names=['ID', 'AGE', 'MET', 'COEFF'],
                     header=None)
    idx = np.lexsort((df.MET, df.AGE))
    df = df.iloc[idx]
    df.MET = df.MET.apply(lambda x: np.log10(x/__solar_metallicity__))
    coeffs = df.reset_index(drop=True)

    if args.instrumental_dispersion is not None:
        sigma_unit = 'km/s'
        sigma_mean = np.sqrt(args.instrumental_dispersion**2 + (5000*props[9]/__c__)**2)
    else:
        sigma_unit = r'\AA'
        sigma_mean = props[9]

    # # generate list of the central wavelengths of fitted emission lines
    el_wl_fit = []
    # cf = ConfigAutoSSP(args.config_file)
    # for elcf in cf.systems_config:
    #     n_wl_fit = np.sum([
    #         elcf.check_par_fit('eline', a) for a in range(len(_MODELS_ELINE_PAR))
    #     ])
    #     for i, mt in enumerate(elcf.model_types):
    #         if ((mt == 'eline') and n_wl_fit):
    #             el_wl_fit.append(elcf.guess[i][_MODELS_ELINE_PAR['central_wavelength']]*(1+props[7]))
    if isfile(args.out_file_elines):
        _, _, output_systems = read_fit_elines_output(args.out_file_elines)
        el_wl_fit = sorted(itertools.chain(*[_s['central_wavelength'] for _s in output_systems]))

    # create masks ranges
    masks, e_masks = read_masks(mask_list=args.mask_list,
                                elines_mask_file=args.elines_mask_file,
                                redshift=props[7], sigma_mean=sigma_mean,
                                verbose=args.verbose)

    f = plot_output_resume(wl, spec__tw, props, coeffs, masks, e_masks, el_wl_fit,
                           wl_range=args.wl_range, cmap=args.cmap, vmin=0.1, vmax=50,
                           percent=not args.fraction)
    f.savefig(f'ana_spec_{basename(args.out_file)}.{args.img_suffix}', dpi=args.dpi)
    plt.show(block=args.block)
    plt.close(f)

if __name__ == '__main__':
    main(parse_arguments())
