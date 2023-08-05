#!/usr/bin/env python3
import os
import sys
import gzip
import glob
import shutil
import itertools
import numpy as np
import configparser
from os import makedirs, remove
from copy import deepcopy as copy
from os.path import basename, isfile
from scipy.ndimage import median_filter
from contextlib import redirect_stdout, redirect_stderr

from pyFIT3D.common.io import ReadArguments, print_done, print_block_init
from pyFIT3D.common.io import get_data_from_fits, get_wave_from_header, print_time
from pyFIT3D.common.io import trim_waves, output_spectra, remove_isfile, write_img_header
from pyFIT3D.common.tools import imarith, get_slice, clean_nan
from pyFIT3D.common.tools import smooth_spec_clip_cube, map_auto_ssp_rnd_seg
from pyFIT3D.common.tools import flux_elines_cube_EW, pack_NAME, sum_mass_age
from pyFIT3D.common.tools import spec_extract_cube_mean, spec_extract_cube_error
from pyFIT3D.common.tools import radial_sum_cube_e, cont_seg_all_SN, rss_seg2cube
# from pyFIT3D.common.tools import get_index_output_auto_ssp_elines_rnd_rss_outFIT3D
from pyFIT3D.common.tools import get_index
from pyFIT3D.common.tools import read_img_header, redshift_config
from pyFIT3D.common.tools import index_seg_cube, clean_Ha_map, med2df, array_to_fits
from pyFIT3D.common.tools import vel_eline, SN_map_seg, get_SN_cube, get_SN_rss
from pyFIT3D.common.auto_ssp_tools import ConfigAutoSSP
from pyFIT3D.common.auto_ssp_tools import auto_ssp_elines_rnd_rss_main
from pyFIT3D.common.auto_ssp_tools import auto_ssp_elines_single_main, dump_rss_output
from pyFIT3D.common.gas_tools import kin_cube_elines_main, output_emission_lines_parameters
from pyFIT3D.common.gas_tools import output_emission_lines_spectra, create_emission_lines_parameters
from pyFIT3D.common.constants import __selected_R_V__, __selected_extlaw__, __n_Monte_Carlo__
from pyFIT3D.common.constants import __c__, __Ha_central_wl__, _MODELS_ELINE_PAR
from pyFIT3D.common.constants import __FWHM_to_sigma__, __sigma_to_FWHM__, __indices__

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])

    __mandatory__ = ['name', 'config_file']
    __optional__ = ['redshift', 'x0', 'y0']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)

    __conv_func_mandatory__ = {'name': str, 'config_file': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' NAME CONFIG_FILE'
    usage_msg_tmp3 = ' [REDSHIFT] [X0] [Y0]'
    usage_msg_tmp4 = '\nCONFIG_FILE is mandatory but defaults to ana_single.ini'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2 + usage_msg_tmp3
    __usage_msg__ += usage_msg_tmp4

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self._parse()

    def _parse(self):
        if self.config_file is None:
            self.config_file = 'ana_single.ini'
        if not isfile(self.config_file):
            print(f'{self.__script_name__}: {self.config_file}: not found')
            sys.exit()

# EL: TODO
def get_redshift_from_file(filename):
    z = None
    if filename is None:
        return None
    # if isfile(filename):
    #     Read the file FILENAME and get redshift.
    return z

# XXX: EADL
#   It should be called mask_regions_brighter_than_center()
def mask_stars_in_FoV(name, V__yx, msk__yx, x0=None, y0=None, mask_val=0):
    time_ini_loc = print_block_init('Mask stars in FoV...')
    ny, nx = V__yx.shape
    ix0 = int(nx*.5) if x0 is None else x0
    iy0 = int(ny*.5) if y0 is None else y0
    V_msk__yx = np.ones_like(msk__yx)
    V_msk__yx[msk__yx == 2] = 0
    # look for stars in the field
    ix0, iy0 = int(nx*.5), int(ny*.5)
    val0 = V__yx[iy0, ix0]
    max_dist = 0.15*np.sqrt(nx**2 + ny**2)
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        val = V__yx[iy, ix]
        dist = np.sqrt((ix - ix0)**2 + (iy - iy0)**2)
        if (val > val0) & (dist > max_dist):
            nx0 = ix - 3
            nx1 = ix + 3
            ny0 = iy - 3
            ny1 = iy + 3
            # img border control
            nx0 = 0 if nx0 < 0 else nx0
            ny0 = 0 if ny0 < 0 else ny0
            nx1 = nx - 1 if nx1 > (nx - 1) else nx1
            ny1 = ny - 1 if ny1 > (ny - 1) else ny1
            # mask region
            for iixy in itertools.product(range(nx0, nx1),range(ny0, ny1)):
                iix, iiy = iixy
                V_msk__yx[iiy, iix] = mask_val
    print_done(time_ini=time_ini_loc)
    return V_msk__yx

def collapse_badpixels_mask(mask__wyx, threshold_fraction=1, mask_value=1):
    """
    Performs the bad pixels mask collapse, i.e., generates a 2D map from a 3D
    (wavelengths, y, x) masking spaxels with a fraction of masked pixels equal
    or above `threshold`.

    Parameters
    ----------
    mask__wyx : array like
        Bad pixels mask cube (3 dimensions, NWAVE, NY, NX).

    threshold_fraction : float
        Sets the threshold to be considered a bad spaxel, i.e. spaxels with a
        fraction of masked pixels equal or above this threshold will be masked.
        threshold = NWAVE * threshold_fraction.

    Returns
    -------
    array like
        2D bad spaxels map.
    """
    nw, ny, nx = mask__wyx.shape
    threshold = nw*threshold_fraction
    badspaxels__yx = np.zeros((ny, nx), dtype=mask__wyx.dtype)
    badpixels_total__yx = mask__wyx.sum(axis=0)
    badspaxels__yx[badpixels_total__yx/nw >= threshold] == 1
    return badspaxels__yx

def ana_single(name, input_config, force_z=None, x0=None, y0=None):
    config = input_config['general']
    config_single = input_config['general_single_analysis']
    config_seg = input_config['cube_segmentation']
    config_elines = input_config['emission_lines']
    config_pack = input_config['pack']

    plot = config.getint('plot', 0)
    save_aux_files = config.getboolean('save_aux_files', True)
    dir_conf = config.get('dir_conf', '../legacy')
    dir_out = config.get('dir_out', '../out')
    dir_datacubes_out = config.get('dir_datacubes_out', '../out')
    inst_disp = config.getfloat('instrumental_dispersion')

    ##########################################################################
    # Load datacube
    #
    time_ini_loc = print_block_init('Loading datacube and calculating signal-to-noise...')
    cube_filename = config['cube_filename'].replace('NAME', name)
    org_cube__wyx, org_h, n_ext = get_data_from_fits(cube_filename, header=True, return_n_extensions=True)
    h_set_rss = {'CRVAL1': org_h['CRVAL3'], 'CDELT1': org_h['CDELT3'], 'CRPIX1': org_h['CRPIX3']}
    h_set_cube = {'CRVAL3': org_h['CRVAL3'], 'CDELT3': org_h['CDELT3'], 'CRPIX3': org_h['CRPIX3']}
    med_vel = org_h.get('MED_VEL')
    org_badpix__wyx = None
    org_error__wyx = None
    org_badspaxels__yx = None
    if org_h['EXTEND']:
        org_error__wyx = get_data_from_fits(cube_filename, extension=1)
        badpix_ext = config.getint('badpix_extension', None)
        if badpix_ext is not None:
            badpix_val = config.getint('badpix_value', 1)
            org_badpix__wyx = get_data_from_fits(cube_filename, extension=badpix_ext)
            if badpix_val != 1:
                _tmp_org_badpix__wyx = np.ones_like(org_badpix__wyx)
                _tmp_org_badpix__wyx[org_badpix__wyx != badpix_val] = 0
                org_badpix__wyx = _tmp_org_badpix__wyx
            badpix_coll_threshold_frac = config.getfloat('badpix_coll_threshold_fraction', 0.5)
            badpix_outmask_value = config.getint('badpix_outmask_value', 1)
            org_badspaxels__yx = collapse_badpixels_mask(org_badpix__wyx,
                                                         threshold_fraction=badpix_coll_threshold_frac,
                                                         mask_value=badpix_outmask_value)
        else:
            print('# Unable to find a bad pixels extension on cube: ', flush=True)
            print('# - missing bad pixels spectra', flush=True)
            print('# - bad spaxels mask disable', flush=True)
    else:
        print('# Unable to find an EXTEND key on cube: ', flush=True)
        print('# - missing error spectra', flush=True)
        print('# - missing bad pixels spectra', flush=True)
        print('# - bad spaxels mask disable', flush=True)

    # original wavelength
    org_wave__w = get_wave_from_header(org_h, wave_axis=3)

    # Signal-to-noise information
    print('# -----=> get_SN_cube()', flush=True)
    SN__yx, signal__yx, noise__yx = get_SN_cube(copy(org_cube__wyx), org_wave__w)
    if save_aux_files:
        with open(f'SYS_VEL_NOW_{name}', 'w') as f:
            print(f'{cube_filename} {med_vel}', file=f)
        SN_map_filename = f'map_SN.{name}.fits.gz'
        signal_map_filename = f'signal.{name}.fits.gz'
        noise_map_filename =  f'noise.{name}.fits.gz'
        array_to_fits(SN_map_filename, SN__yx, overwrite=True)
        array_to_fits(signal_map_filename, signal__yx, overwrite=True)
        array_to_fits(noise_map_filename, noise__yx, overwrite=True)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # pseudo V-band slice
    time_ini_loc = print_block_init('Creating pseudo V-band map...')
    slice_prefix = f'img_{name}'
    slice_config = config.get('slice_config_file')

    # get_slice(cube_filename, slice_prefix, slice_config)
    print('# -----=> get_slice()', flush=True)
    slices = get_slice(copy(org_cube__wyx), org_wave__w, slice_prefix, slice_config)
    V_img_slice_key = f'{slice_prefix}_V_4500_5500'  #.fits'
    if save_aux_files:
        V_slice_filename = f'{slice_prefix}_V_4500_5500.fits'
        array_to_fits(V_slice_filename, slices[V_img_slice_key], overwrite=True)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Creating mask
    #
    V__yx = copy(slices[V_img_slice_key])
    ny, nx = V__yx.shape
    nx1, ny1 = nx, ny
    # V__yx = get_data_from_fits(tmp_img_filename)
    msk__yx = np.zeros_like(V__yx)
    # EL: deprecated - MaNGA v1.4 mask
    msk_filename = config.get('spatial_mask_file', None)
    if msk_filename is not None:
        msk_filename = msk_filename.replace('NAME', name)
        if isfile(msk_filename):
            msk__yx = get_data_from_fits(msk_filename)
            ny1, nx1 = msk__yx.shape
    print(f'# Dimensions = {nx},{ny},{nx1},{ny1}')
    # mask_val = 1 means that this is not used
    mask_stars = config.getboolean('mask_stars', False)  #config.getint('mask_stars', 1)
    mask_val = 1
    if mask_stars:
        mask_val = 0
    V_msk__yx = mask_stars_in_FoV(name, copy(V__yx), msk__yx, mask_val=mask_val)
    if save_aux_files:
        msk_filename = f'{name}.mask.fits'
        array_to_fits(msk_filename, V_msk__yx, overwrite=True)
    # Appending badpix mask V_msk__yx: if some spaxel has only bad pixels,
    # this spaxel should be masked.
    if org_badspaxels__yx is not None:
        V_msk__yx[org_badspaxels__yx == 1] = 0
        if save_aux_files:
            msk_filename = f'{name}.mask.nobadspaxels.fits'
            array_to_fits(msk_filename, V_msk__yx, overwrite=True)
    ##########################################################################

    ##########################################################################
    # Central spectrum integrated spectrum
    #
    # pseudo V-band map
    time_ini_loc = print_block_init('Analyzing central and integrated spectra...')
    if x0 is None:
        x0 = config_single.getfloat('x0', None)
    if y0 is None:
        y0 = config_single.getfloat('y0', None)
    if x0 is None or y0 is None:
        nx0 = int(nx*.33)
        nx1 = int(nx*2*.33)
        ny0 = int(ny*.33)
        ny1 = int(ny*2*.33)
        iy, ix = np.indices(V__yx.shape)
        iy = iy[ny0:ny1, nx0:nx1]
        ix = ix[ny0:ny1, nx0:nx1]
        sel = V_msk__yx[ny0:ny1, nx0:nx1] != 2
        V_slice = copy(V__yx[ny0:ny1, nx0:nx1][sel])
        __V = V_slice**5
        _s = __V.sum()
        x0 = ix[sel].dot(__V)/_s
        y0 = iy[sel].dot(__V)/_s
    # clean_nan(V_img_filename, badval=-1)
    V__yx[np.isnan(V__yx)] = -1
    print(f'# x0:{x0} y0:{y0}')

    # creating spectra (central and integrated)
    print('# -----=> radial_sum_cube_e()', flush=True)
    # radial_sum_cube_e(cube_filename, delta_R=2.5, x0=x0, y0=y0, output_rss_fits=radial_sum_cube_filename)

    # (EADL) To think:
    # radial_sum_cube_e() do not consider V-band mask (which inlcudes masked
    # stars in the field), only a bad pixels mask (input_mask). The spatial mask
    # should also be processed by radial_sum_cube_e() function.
    r = radial_sum_cube_e(copy(org_cube__wyx), x0=x0, y0=y0,
                          delta_R=config_single.getfloat('radial_sum_cube_delta_R', 2.5),
                          input_mask=org_badpix__wyx, input_error=org_error__wyx)
    output__rw, e_output__rw, mask_output__rw = r

    print('# -----=> img2spec_e() central spectrum', flush=True)
    # img2spec_e(radial_sum_cube_filename, 0, cen_spec_filename)
    f_cen__w = copy(output__rw[0])
    f_cen__w[~np.isfinite(f_cen__w)] = 0
    sqrt_f_cen__w = np.sqrt(np.abs(f_cen__w))
    e_f_cen__w = copy(e_output__rw[0])
    e_f_cen__w[~np.isfinite(e_f_cen__w)] = 1e12
    e_f_cen__w = np.where(e_f_cen__w > sqrt_f_cen__w, sqrt_f_cen__w, e_f_cen__w)

    print('# -----=> img2spec_e() integrated spectrum', flush=True)
    # img2spec_e(radial_sum_cube_filename, 5, int_spec_filename)
    f_int__w = copy(output__rw[5])
    f_int__w[~np.isfinite(f_int__w)] = 0
    sqrt_f_int__w = np.sqrt(np.abs(f_int__w))
    e_f_int__w = copy(e_output__rw[5])
    e_f_int__w[~np.isfinite(e_f_int__w)] = 1e12
    e_f_int__w = np.where(e_f_int__w > sqrt_f_int__w, sqrt_f_int__w, e_f_int__w)

    # Needed final files
    cen_spec_filename = config_single.get('cen_spec_filename', None)
    cen_spec_filename = f'{name}.spec_5.txt' if cen_spec_filename is None else cen_spec_filename.replace('NAME', name)
    output_spectra(org_wave__w, [f_cen__w, e_f_cen__w], cen_spec_filename)
    int_spec_filename = config_single.get('int_spec_filename', None)
    int_spec_filename = f'{name}.spec_30.txt' if int_spec_filename is None else int_spec_filename.replace('NAME', name)
    output_spectra(org_wave__w, [f_int__w, e_f_int__w], int_spec_filename)

    if save_aux_files:
        radial_sum_cube_filename = f'rad.{name}.rss.fits'
        e_radial_sum_cube_filename = f'e_{radial_sum_cube_filename}'
        weight_radial_sum_cube_filename = f'weight.{radial_sum_cube_filename}'
        array_to_fits(radial_sum_cube_filename, output__rw, header=h_set_rss, overwrite=True)
        array_to_fits(e_radial_sum_cube_filename, e_output__rw, header=h_set_rss, overwrite=True)
        array_to_fits(weight_radial_sum_cube_filename, mask_output__rw, header=h_set_rss, overwrite=True)

    # define redshift range
    ############################################################################
    # (EADL): To think: This entire block has not been used.
    ############################################################################
    ############################################################################
    # print('# -----=> vel_eline_spec()', flush=True)
    # # npeaks, vel = vel_eline_spec(cen_spec_filename, 2, 0.7, 'junk', 3728, 3800, 4000, output_file=f'vel_eline_spec.{name}.txt')
    # w_min = config_single.getint('vel_eline_min_wavelength', 3800)
    # w_max = config_single.getint('vel_eline_max_wavelength', 4000)
    # wave_ref = config_single.getfloat('vel_eline_reference_wavelength', 3728)
    # nsearch = config_single.getint('vel_eline_nsearch', 2)
    # imin = config_single.getfloat('vel_eline_imin', 0.7)
    # sel__w = trim_waves(org_wave__w, [w_min, w_max])
    # vel, _, npeaks = vel_eline(f_cen__w[sel__w], org_wave__w[sel__w], nsearch=nsearch, imin=imin, wave_ref=wave_ref)
    # if npeaks == 1:
    #     red = vel/__c__
    #     red_f = 300/__c__
    #     min_red = red - red_f
    #     min_red = red + red_f
    # else:
    #     # EL: not used in MaNGA I supose, because else is just rewritten
    #     # below, in NSA redshift if.
    #     red = 0.02
    #     min_red = 0.0045
    #     max_red = 0.032
    ############################################################################
    if force_z is None:
        force_z = config_single.getfloat('force_redshift', None)
    # (EADL) TODO: Create a parser to read a redshift file (^NAME\tXXXX$ probable format)
    # if force_z is None:
    #     force_z = get_redshift_from_file(config_single.get('redshift_file', None))
    # print(force_z)
    if (force_z is not None) and (force_z > 0):
        red = force_z
        red_hr_kms = config_single.getfloat('redshift_half_range', 600)
        red_f = red_hr_kms/__c__
        min_red = red - red_f
        max_red = red + red_f
        d_red = 0.2*red_hr_kms/__c__
        print(f'# USING FORCED REDSHIFT')
    else:
        red = config_single.getfloat('input_redshift', 0.02)
        min_red = config_single.getfloat('min_redshift', -0.001)
        max_red = config_single.getfloat('max_redshift', 0.2)
        d_red = config_single.getfloat('delta_redshift_kms', 300)/__c__
    print(f'# redshift = {red:.8f} - min = {min_red:.8f} - max = {max_red:.8f} - delta = {d_red:.8f}')

    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd(): Analyzing central spectrum...')
    tmp_cf = input_config['cen_auto_ssp_no_lines']
    auto_ssp_output_filename = tmp_cf.get('output_filename', 'auto_ssp_Z.NAME.cen.out').replace('NAME', name)
    remove_isfile(auto_ssp_output_filename)
    auto_ssp_output_elines_filename = 'elines_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_elines_filename)
    auto_ssp_output_coeffs_filename = 'coeffs_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_output_filename + '.fits'
    remove_isfile(auto_ssp_output_fits_filename)
    w_min = tmp_cf.getint('min_wavelength', 3800)
    w_max = tmp_cf.getint('max_wavelength', 7000)
    nl_w_min = tmp_cf.getint('nonlinear_min_wavelength', 3850)
    nl_w_max = tmp_cf.getint('nonlinear_max_wavelength', 4700)
    cf, SPS = auto_ssp_elines_single_main(
        copy(org_wave__w), copy(f_cen__w), copy(e_f_cen__w), tmp_cf.get('models_file'),
        tmp_cf.get('config_file'), auto_ssp_output_filename,
        ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
        mask_list=tmp_cf.get('mask_file', None),
        elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
        min=None, max=None, w_min=w_min, w_max=w_max,
        nl_w_min=nl_w_min, nl_w_max=nl_w_max,
        input_redshift=red, delta_redshift=d_red,
        min_redshift=min_red, max_redshift=max_red,
        input_sigma=tmp_cf.getfloat('input_sigma'), delta_sigma=tmp_cf.getfloat('delta_sigma'),
        min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=tmp_cf.getfloat('max_sigma'),
        input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
        min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
        R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
        fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
        fit_gas=False,
    )
    SPS.output_gas_emission(filename=auto_ssp_output_elines_filename)
    SPS.output_fits(filename=auto_ssp_output_fits_filename)
    SPS.output_coeffs_MC(filename=auto_ssp_output_coeffs_filename)
    SPS.output(filename=auto_ssp_output_filename, block_plot=False)
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd(): DONE!')

    # data = np.genfromtxt(auto_ssp_output_filename, usecols=[7,9], delimiter=',',
    #                      dtype=[('redshift', 'float'), ('disp', 'float')])
    # red = data['redshift']
    # disp_max = 1.5*data['disp']

    # read redshift and dispersion from auto_ssp output
    red = SPS.best_redshift
    disp_max = 1.5*SPS.best_sigma

    # ###################################################################
    # # A faster way to derive the redshift #############################
    # ###################################################################
    # # This entire block can replace the previous
    # # auto_ssp_elines_single_main() call.
    # ##################################
    # # Do not perform SPS, only fits redshift and sigma
    # # also do not produce output files
    # ###################################################################
    # from pyFIT3D.modelling.stellar import StPopSynt
    # tmp_cf = input_config['cen_auto_ssp_no_lines']
    # sigma_set = [
    #     tmp_cf.getfloat('input_sigma'), tmp_cf.getfloat('delta_sigma'),
    #     tmp_cf.getfloat('min_sigma'), tmp_cf.getfloat('max_sigma')
    # ]
    # redshift_set = [red, d_red, min_red, max_red]
    # # do not fit AV
    # AV_set = [tmp_cf.getfloat('input_AV'), 0, 0, 0]
    # cf = ConfigAutoSSP(tmp_cf.get('config_file'), redshift_set=redshift_set, sigma_set=sigma_set, AV_set=AV_set)
    # w_min = tmp_cf.getint('min_wavelength', 3800)
    # w_max = tmp_cf.getint('max_wavelength', 7000)
    # nl_w_min = tmp_cf.getint('nonlinear_min_wavelength', 3850)
    # nl_w_max = tmp_cf.getint('nonlinear_max_wavelength', 4700)
    # ssp_nl_fit_file=,
    # mask_list=tmp_cf.get('mask_file', None),
    # elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
    # SPS = StPopSynt(config=cf, wavelength=copy(org_wave__w),
    #                 flux=copy(f_cen__w), eflux=copy(e_f_cen__w),
    #                 mask_list=tmp_cf.get('mask_file', None),
    #                 elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
    #                 ssp_file=tmp_cf.get('models_file'),
    #                 ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
    #                 w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
    #                 R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'),
    #                 sigma_inst=None, out_file=None, fit_gas=False, plot=plot)
    # msg_cut = f' - cut value: {cf.CUT_MEDIAN_FLUX:6.4f}'
    # if cf.CUT_MEDIAN_FLUX == 0:
    #     msg_cut = ' - Warning: no cut (CUT_MEDIAN_FLUX = 0)'
    # print(f'-> median raw flux = {SPS.median_flux:6.4f}{msg_cut}')
    # SPS.cut = False
    # if SPS.median_flux > cf.CUT_MEDIAN_FLUX:  # and (median_flux > cf.ABS_MIN):
    #     # redshift
    #     SPS.non_linear_fit(is_guided_sigma, fit_sigma_rnd=fit_sigma_rnd)
    #     red = SPS.best_redshift
    #     disp_max = 1.5*SPS.best_sigma
    # else:
    #     # max sigma is in AA -> km/s using 5000 A as reference wl
    #     disp_max = tmp_cf.getfloat('max_sigma')*5000/__c__
    # ###################################################################

    red_f = 300/__c__
    min_red = red - red_f
    max_red = red + red_f
    d_red = 0.1*red_f
    vel = red*__c__
    print(f'# Redshift = {red:.8f} - Vel = {vel:.8f}')

    # fix redshift at config file
    config_file = f'auto.{name}.config'
    print('# -----=> redshift_config()', flush=True)
    redshift_config(
        input_config=input_config['auto_ssp_config'].get('strong'),
        redshift=red, output_config=config_file
    )
    # Analyze central spectrum with no mask
    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd(): Analyzing central spectrum with instrumental sigma (no mask)...')
    tmp_cf = input_config['cen_auto_ssp_inst_disp']
    w_min = w_min*(1 + red)
    w_max = w_max*(1 + red)
    nl_w_min = nl_w_min*(1 + red)
    nl_w_max = nl_w_max*(1 + red)
    auto_ssp_output_filename = tmp_cf.get('no_mask_output_filename', 'auto_ssp_no_mask.NAME.cen.out').replace('NAME', name)
    remove_isfile(auto_ssp_output_filename)
    auto_ssp_output_elines_filename = 'elines_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_elines_filename)
    auto_ssp_output_coeffs_filename = 'coeffs_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_output_filename + '.fits'
    remove_isfile(auto_ssp_output_fits_filename)
    cf, SPS = auto_ssp_elines_single_main(
        wavelength=copy(org_wave__w), flux=copy(f_cen__w), eflux=copy(e_f_cen__w),
        ssp_file=tmp_cf.get('models_file'),
        ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
        config_file=config_file,
        out_file=auto_ssp_output_filename,
        sigma_inst=tmp_cf.getfloat('instrumental_dispersion'),
        mask_list=None, elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
        min=-3, max=50, w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
        input_redshift=red, delta_redshift=0, min_redshift=min_red, max_redshift=max_red,
        input_sigma=tmp_cf.getfloat('input_sigma'), delta_sigma=tmp_cf.getfloat('delta_sigma'),
        min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=tmp_cf.getfloat('max_sigma'),
        input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
        min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
        R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
        fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
    )
    SPS.output_gas_emission(filename=auto_ssp_output_elines_filename)
    SPS.output_fits(filename=auto_ssp_output_fits_filename)
    SPS.output_coeffs_MC(filename=auto_ssp_output_coeffs_filename)
    SPS.output(filename=auto_ssp_output_filename, block_plot=False)
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd(): DONE!')

    # Analyze central spectrum with mask
    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd(): Analyzing central spectrum with instrumental sigma...')
    auto_ssp_output_filename = tmp_cf.get('output_filename', 'auto_ssp.NAME.cen.out').replace('NAME', name)
    remove_isfile(auto_ssp_output_filename)
    auto_ssp_output_elines_filename = 'elines_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_elines_filename)
    auto_ssp_output_coeffs_filename = 'coeffs_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_output_filename + '.fits'
    remove_isfile(auto_ssp_output_fits_filename)
    cf, SPS = auto_ssp_elines_single_main(
        wavelength=copy(org_wave__w), flux=copy(f_cen__w), eflux=copy(e_f_cen__w),
        ssp_file=tmp_cf.get('models_file'),
        ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
        config_file=config_file,
        out_file=auto_ssp_output_filename,
        sigma_inst=tmp_cf.getfloat('instrumental_dispersion'),
        mask_list=tmp_cf.get('mask_file', None),
        elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
        min=-3, max=50, w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
        input_redshift=red, delta_redshift=0, min_redshift=min_red, max_redshift=max_red,
        input_sigma=tmp_cf.getfloat('input_sigma'), delta_sigma=tmp_cf.getfloat('delta_sigma'),
        min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=tmp_cf.getfloat('max_sigma'),
        input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
        min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
        R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
        fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
    )
    SPS.output_gas_emission(filename=auto_ssp_output_elines_filename)
    SPS.output_fits(filename=auto_ssp_output_fits_filename)
    SPS.output_coeffs_MC(filename=auto_ssp_output_coeffs_filename)
    SPS.output(filename=auto_ssp_output_filename, block_plot=False)
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd(): DONE!')

    # Analyze integrated spectrum
    # data = np.genfromtxt(auto_ssp_output_filename, usecols=[9], delimiter=',',
    #                      dtype=[('disp', 'float')])
    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd(): Analyzing integrated spectrum with instrumental sigma...')
    tmp_cf = input_config['int_auto_ssp_inst_disp']
    sigma = SPS.best_sigma
    max_sigma = sigma + 30
    guess_sigma = sigma
    print(f'# Max sigma:{max_sigma:.8f} - Guess sigma:{guess_sigma:.8f}')
    guess_sigma = 30
    auto_ssp_output_filename = tmp_cf.get('output_filename', 'auto_ssp.NAME.int.out').replace('NAME', name)
    remove_isfile(auto_ssp_output_filename)
    auto_ssp_output_elines_filename = 'elines_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_elines_filename)
    auto_ssp_output_coeffs_filename = 'coeffs_' + auto_ssp_output_filename
    remove_isfile(auto_ssp_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_output_filename + '.fits'
    remove_isfile(auto_ssp_output_fits_filename)
    cf, SPS = auto_ssp_elines_single_main(
        wavelength=copy(org_wave__w), flux=copy(f_int__w), eflux=copy(e_f_int__w),
        ssp_file=tmp_cf.get('models_file'),
        ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
        config_file=config_file,
        out_file=auto_ssp_output_filename,
        sigma_inst=tmp_cf.getfloat('instrumental_dispersion'),
        mask_list=tmp_cf.get('mask_file', None),
        elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
        min=-3, max=50, w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
        input_redshift=red, delta_redshift=d_red, min_redshift=min_red, max_redshift=max_red,
        input_sigma=guess_sigma, delta_sigma=tmp_cf.getfloat('delta_sigma'),
        min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=max_sigma,
        input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
        min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
        R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
        fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
    )
    SPS.output_gas_emission(filename=auto_ssp_output_elines_filename)
    SPS.output_fits(filename=auto_ssp_output_fits_filename)
    SPS.output_coeffs_MC(filename=auto_ssp_output_coeffs_filename)
    SPS.output(filename=auto_ssp_output_filename, block_plot=False)
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd(): DONE!')
    print_done(time_ini=time_ini_loc, message='Central and integrated analysis DONE!')
    ##########################################################################

    ##########################################################################
    # FoV segmentation (RSS build)
    #
    time_ini_loc = print_block_init('FoV segmentation (RSS build)...')
    print('# -----=> med2df()', flush=True)
    # med2df(input_fits=V_img_filename,
    #        x_width=2, y_width=2,
    #        output_fits=filt_V_img_filename)
    # imarith(filt_V_img_filename, '*', msk_filename, filt_V_img_filename)
    filt_V__yx = median_filter(V__yx, size=(2, 2), mode='reflect')
    mV__yx = filt_V__yx*V_msk__yx
    ########
    # (EADL)
    #    NOTE: config[general_single_analysis][pseudo_V_band_file] usage is
    #    deprecated.
    _tmp_V_img_filename = config_single.get('pseudo_V_band_file', 'NAME.V.fits')
    ########
    V_img_filename = config_seg.get('pseudo_V_band_file', _tmp_V_img_filename).replace('NAME', name)
    array_to_fits(V_img_filename, mV__yx, overwrite=True)

    # Segmentation map from signal and noise maps
    print('# -----=> cont_seg_all_SN()', flush=True)
    flux_limit_peak = config_seg.getfloat('flux_limit_peak', 0.001)
    target_SN = config_seg.getfloat('target_SN', 50)
    min_SN = config_seg.getfloat('min_SN', 1)
    frac_peak = config_seg.getfloat('frac_peak', 0.85)
    min_flux = config_seg.getfloat('min_flux', 0.001)
    seg_map__yx, dmask_map__yx = cont_seg_all_SN(copy(signal__yx), copy(noise__yx),
                                                 flux_limit_peak=flux_limit_peak,
                                                 target_SN=target_SN, min_SN=min_SN,
                                                 frac_peak=frac_peak, min_flux=min_flux)

    # Do not get stucked due to bad data.
    if (seg_map__yx.sum() == 0) or (dmask_map__yx.sum() == (nx*ny)):
        print(f'{basename(sys.argv[0])}: cont_seg_all_SN: no segmentation. Stopping analysis.')
        return

    # mask based in SN < 1
    mask_map__yx = (SN__yx > min_SN).astype(int)
    # extract segmented spectra

    print('# -----=> spec_extract_cube_mean()', flush=True)
    # spec_extract_cube_mean(cube_filename, cont_seg_filename, cont_seg_rss_filename)
    org_rss__sw, _, _x_mean, _y_mean, npt_mean = spec_extract_cube_mean(copy(org_cube__wyx), seg_map__yx, badpix__wyx=org_badpix__wyx)
    ns = org_rss__sw.shape[0]

    print('# -----=> spec_extract_cube_error()', flush=True)
    # spec_extract_cube_error(cube_filename, cont_seg_filename, e_cont_seg_rss_filename)
    org_e_rss__sw, inv_seg__yx, _x_error, _y_error, npt_error = spec_extract_cube_error(copy(org_error__wyx), seg_map__yx,
                                                                                        badpix__wyx=org_badpix__wyx,
                                                                                        fov_selection__yx=mV__yx.astype('bool'))
    # org_rss__sw, h_org_rss = get_data_from_fits(cont_seg_rss_filename, header=True)
    # wave_rss__w = get_wave_from_header(h_org_rss, wave_axis=1)
    wave_rss__w = copy(org_wave__w)

    # get signal to noise from RSS
    print('# -----=> get_SN_rss()', flush=True)
    SN__s, signal__s, noise__s = get_SN_rss(copy(org_rss__sw), wave_rss__w)
    # output SN rss file

    # CSV to FITS
    print('# -----=> csv_to_map_seg()', flush=True)
    # csv_to_map_seg(output_SN_rss_csv_filename, 1, cont_seg_filename, output_SN_rss_fits_filename)
    SN_rss__yx, norm_SN_rss__yx, area_rss__yx = SN_map_seg(copy(SN__s), seg_map__yx)

    # RSS SEG to Cube
    print('# -----=> rss_seg2cube()', flush=True)
    cube__wyx = rss_seg2cube(org_rss__sw, seg_map__yx)

    # get pseudo V-band slice
    print('# -----=> get_slice()', flush=True)
    slice_prefix = f'SEG_img_{name}'
    slices = get_slice(copy(cube__wyx), wave_rss__w, slice_prefix, slice_config)
    k = list(slices.keys())[0]
    V_slice__yx = slices[k]
    V_slice__yx[np.isnan(V_slice__yx)] = -1
    scale_seg__yx = mV__yx/V_slice__yx

    # Needed final files
    cont_seg_filename = config_seg.get('cont_seg_file', f'cont_seg.NAME.fits').replace('NAME', name)
    array_to_fits(cont_seg_filename, seg_map__yx, overwrite=True)
    scale_seg_filename = config_seg.get('scale_seg_file', f'scale.seg.NAME.fits').replace('NAME', name)
    array_to_fits(scale_seg_filename, scale_seg__yx, overwrite=True)
    SN_mask_map_filename = f'mask.{name}.V.fits'
    array_to_fits(SN_mask_map_filename, mask_map__yx, overwrite=True)

    if save_aux_files:
        filt_V_img_filename = f'm{V_img_filename}'
        array_to_fits(filt_V_img_filename, mV__yx, overwrite=True)
        diffuse_seg_filename = f'DMASK.{name}.fits'
        array_to_fits(diffuse_seg_filename, dmask_map__yx, overwrite=True)
        cont_seg_rss_filename = f'CS.{name}.RSS.fits'
        array_to_fits(cont_seg_rss_filename, org_rss__sw, header=h_set_rss, overwrite=True)
        size = np.sqrt(nx**2+ny**2)/(2*ns)
        output_rss_txt = cont_seg_rss_filename.replace('fits', 'pt.txt')
        with open(output_rss_txt, 'w') as f:
            output_header = f'C {size} {size} 0'
            print(output_header, file=f)
            # output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
            np.savetxt(f, list(zip(list(range(ns)), _x_mean/npt_mean, _y_mean/npt_mean, [1]*ns)),
                       fmt=['%d'] + 2*['%.18g'] + ['%d'], delimiter=' ')
        print(f'# {cont_seg_rss_filename} and {output_rss_txt} created')
        e_cont_seg_rss_filename = f'e_{cont_seg_rss_filename}'
        array_to_fits(e_cont_seg_rss_filename, org_e_rss__sw, header=h_set_rss, overwrite=True)
        size = np.sqrt(nx**2+ny**2)/(2*ns)
        output_rss_txt = e_cont_seg_rss_filename.replace('fits', 'pt.txt')
        with open(output_rss_txt, 'w') as f:
            output_header = f'C {size} {size} 0'
            print(output_header, file=f)
            # output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
            np.savetxt(f, list(zip(list(range(ns)), _x_error/npt_error, _y_error/npt_error, [1]*ns)),
                       fmt=['%d'] + 2*['%.18g'] + ['%d'], delimiter=' ')
        print(f'# {e_cont_seg_rss_filename} and {output_rss_txt} created')
        output_SN_rss_csv_filename = f'SN_{name}.CS.rss.csv'
        with open(output_SN_rss_csv_filename, 'w') as f:
            output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
            np.savetxt(f, list(zip(list(range(SN__s.size)), SN__s, signal__s, noise__s)),
                       fmt=['%d'] + 3*['%.18g'], header=output_header, delimiter=',')
        output_SN_rss_fits_filename = f'SN_{name}.CS.fits'
        output_norm_SN_rss_fits_filename = f'norm_{output_SN_rss_fits_filename}'
        output_area_rss_fits_filename = f'area_{output_SN_rss_fits_filename}'
        array_to_fits(output_SN_rss_fits_filename, SN_rss__yx, overwrite=True)
        array_to_fits(output_norm_SN_rss_fits_filename, norm_SN_rss__yx, overwrite=True)
        array_to_fits(output_area_rss_fits_filename, area_rss__yx, overwrite=True)
        seg_cube_filename = f'SEG.cube.{name}.fits'
        array_to_fits(seg_cube_filename, cube__wyx, header=h_set_cube, overwrite=True)
        seg_img_filename = f'SEG_img_{name}.fits'
        array_to_fits(seg_img_filename, V_slice__yx, overwrite=True)

    print_done(time_ini=time_ini_loc, message='FoV segmentation DONE!')
    ##########################################################################

    if config.getboolean('debug', False):
        return

    ##########################################################################
    # Begin RSS analysis
    #
    #
    time_ini_loc = print_block_init('RSS analysis...')
    # RSS analysis with sigma guided (disp_min)
    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd_rss(): Analyzing RSS with guided sigma...')
    tmp_cf = input_config['auto_ssp_rss_sigma_guided']
    auto_ssp_rss_output_filename = tmp_cf.get('output_filename', 'auto_ssp.CS_few.NAME.rss.out').replace('NAME', name)
    remove_isfile(auto_ssp_rss_output_filename)
    auto_ssp_rss_output_elines_filename = 'elines_' + auto_ssp_rss_output_filename
    remove_isfile(auto_ssp_rss_output_elines_filename)
    auto_ssp_rss_output_coeffs_filename = 'coeffs_' + auto_ssp_rss_output_filename
    remove_isfile(auto_ssp_rss_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_rss_output_filename + '.fits.gz'
    remove_isfile(auto_ssp_output_fits_filename)
    with open(auto_ssp_rss_output_elines_filename,"w") as elines_out, open(auto_ssp_rss_output_coeffs_filename,"w") as coeffs_out, open(auto_ssp_rss_output_filename,"w") as summary_out:
        r = auto_ssp_elines_rnd_rss_main(
            wavelength=copy(org_wave__w), rss_flux=copy(org_rss__sw), rss_eflux=copy(org_e_rss__sw),
            output_files=(elines_out,coeffs_out,summary_out),
            ssp_file=tmp_cf.get('models_file'),
            ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
            sigma_inst=tmp_cf.getfloat('instrumental_dispersion'),
            out_file=auto_ssp_rss_output_filename,
            config_file=config_file,
            mask_list=tmp_cf.get('mask_file', None),
            elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
            min=-2, max=5, w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
            input_redshift=red, delta_redshift=d_red, min_redshift=min_red, max_redshift=max_red,
            input_sigma=guess_sigma, delta_sigma=tmp_cf.getfloat('delta_sigma'),
            min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=max_sigma,
            input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
            min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
            R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
            is_guided_sigma=True, fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
        )
    model_spectra, results, results_coeffs, output_el_models = r
    # write FITS RSS output
    output_rss__tsw = dump_rss_output(out_file_fit=auto_ssp_output_fits_filename,
        wavelength=org_wave__w,
        model_spectra=model_spectra
    )
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd_rss(): DONE!')

    #
    # EL: missing plot scripts plot_output_auto_ssp_elines_several_Av_log_rss_all.pl
    #
    # creating GAS cube
    time_init_gas_cube = print_block_init('Creating GAS cube and RSS...')
    # input_auto_ssp_rss_output_filename = f'output.{auto_ssp_rss_output_filename}.fits.gz'
    # output_rss__tsw, h_output_rss = get_data_from_fits(input_auto_ssp_rss_output_filename, header=True)
    print('# -----=> FIT3D_output_rss_seg2cube()', flush=True)
    ssp_mod_tmp__wyx = rss_seg2cube(copy(output_rss__tsw[1]), seg_map__yx)
    ssp_mod_cube__wyx = ssp_mod_tmp__wyx*scale_seg__yx
    tmp_cube__wyx = org_cube__wyx - ssp_mod_cube__wyx

    # smooth
    print('# -----=> smooth_spec_clip_cube()', flush=True)
    smooth_cube__wyx = smooth_spec_clip_cube(copy(tmp_cube__wyx), wavebox_width=75, sigma=1.5, wavepix_min=10, wavepix_max=1860)

    # generate GAS rss input
    print('# -----=> spec_extract_cube_mean()', flush=True)
    gas_cube__wyx = tmp_cube__wyx - smooth_cube__wyx
    gas_rss__sw, _, _x_mean, _y_mean, npt_mean = spec_extract_cube_mean(copy(gas_cube__wyx), seg_map__yx)
    # spec_extract_cube_mean(gas_cube_filename, cont_seg_filename, gas_seg_rss_filename)

    ssp_mod_filename = config_seg.get('ssp_mod_file', 'SSP_mod.NAME.cube.fits').replace('NAME', name)
    array_to_fits(ssp_mod_filename, ssp_mod_cube__wyx, overwrite=True)
    gas_cube_filename = config_seg.get('gas_cube_file', 'GAS.NAME.cube.fits').replace('NAME', name)
    array_to_fits(gas_cube_filename, gas_cube__wyx, header=h_set_cube, overwrite=True)
    print(f'# {gas_cube_filename} created')
    gas_seg_rss_filename = config_seg.get('gas_seg_file', 'GAS.CS.NAME.RSS.fits').replace('NAME', name)
    array_to_fits(gas_seg_rss_filename, gas_rss__sw, header=h_set_rss, overwrite=True)
    size = np.sqrt(nx**2+ny**2)/(2*ns)
    output_rss_txt = gas_seg_rss_filename.replace('fits', 'pt.txt')
    with open(output_rss_txt, 'w') as f:
        output_header = f'C {size} {size} 0'
        print(output_header, file=f)
        # output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
        np.savetxt(f, list(zip(list(range(ns)), _x_mean/npt_mean, _y_mean/npt_mean, [1]*ns)),
                   fmt=['%d'] + 2*['%.18g'] + ['%d'], delimiter=' ')
    print(f'# {gas_seg_rss_filename} and {output_rss_txt} created')

    ssp_mod_tmp_filename = f'SSP_mod_tmp.{name}.cube.fits'
    array_to_fits(ssp_mod_tmp_filename, ssp_mod_tmp__wyx, header=h_set_cube, overwrite=True)

    if save_aux_files:
        # EL: write TMP cube is not needed anymore, but is present as a sanity check
        tmp_cube_filename = f'TMP.{name}.cube.fits'
        array_to_fits(tmp_cube_filename, tmp_cube__wyx, overwrite=True)
        smooth_cube_filename = f'smooth.{name}.cube.fits'
        array_to_fits(smooth_cube_filename, smooth_cube__wyx, header=h_set_cube, overwrite=True)
    print_done(time_ini=time_init_gas_cube)

    # analysis of SSP spectra (guided RSS)
    time_ini_auto_ssp = print_block_init('auto_ssp_elines_rnd_rss(): Analyzing RSS with guided non-linear fit...')
    tmp_cf = input_config['auto_ssp_rss_guided']
    auto_ssp_rss_guided_output_filename = tmp_cf.get('output_filename', 'auto_ssp.CS.NAME.rss.out').replace('NAME', name)
    remove_isfile(auto_ssp_rss_guided_output_filename)
    auto_ssp_rss_guided_output_elines_filename = 'elines_' + auto_ssp_rss_guided_output_filename
    remove_isfile(auto_ssp_rss_guided_output_elines_filename)
    auto_ssp_rss_guided_output_coeffs_filename = 'coeffs_' + auto_ssp_rss_guided_output_filename
    remove_isfile(auto_ssp_rss_guided_output_coeffs_filename)
    auto_ssp_output_fits_filename = 'output.' + auto_ssp_rss_guided_output_filename + '.fits.gz'
    remove_isfile(auto_ssp_output_fits_filename)
    guided_nl = True
    AV = results[5]
    e_AV = results[6]
    redshift = results[7]
    e_redshift = results[8]
    sigma = results[9]
    e_sigma = results[10]
    # AV, e_AV, redshift, e_redshift, sigma, e_sigma = np.genfromtxt(
    #     fname=auto_ssp_rss_output_filename,
    #     comments="#", delimiter=",", usecols=(5,6,7,8,9,10), unpack=True
    # )
    input_guided = (redshift, sigma, AV)
    input_guided_errors = (e_redshift, e_sigma, e_AV)
    # SSP spectra
    ssp_rss__tsw = output_rss__tsw[0] - (output_rss__tsw[2] - output_rss__tsw[1])
    with open(auto_ssp_rss_guided_output_elines_filename,"w") as elines_out, open(auto_ssp_rss_guided_output_coeffs_filename,"w") as coeffs_out, open(auto_ssp_rss_guided_output_filename,"w") as summary_out:
        r = auto_ssp_elines_rnd_rss_main(
            wavelength=copy(org_wave__w), rss_flux=copy(ssp_rss__tsw), rss_eflux=copy(org_e_rss__sw),
            output_files=(elines_out,coeffs_out,summary_out),
            input_guided=input_guided, input_guided_errors=input_guided_errors,
            ssp_file=tmp_cf.get('models_file'),
            ssp_nl_fit_file=tmp_cf.get('nonlinear_models_file'),
            sigma_inst=tmp_cf.getfloat('instrumental_dispersion'),
            out_file=auto_ssp_rss_guided_output_filename,
            config_file=tmp_cf.get('config_file'),
            mask_list=tmp_cf.get('mask_file', None),
            elines_mask_file=tmp_cf.get('emission_lines_mask_file', None),
            min=-2, max=5, w_min=w_min, w_max=w_max, nl_w_min=nl_w_min, nl_w_max=nl_w_max,
            input_redshift=red, delta_redshift=d_red, min_redshift=min_red, max_redshift=max_red,
            input_sigma=guess_sigma, delta_sigma=tmp_cf.getfloat('delta_sigma'),
            min_sigma=tmp_cf.getfloat('min_sigma'), max_sigma=max_sigma,
            input_AV=tmp_cf.getfloat('input_AV'), delta_AV=tmp_cf.getfloat('delta_AV'),
            min_AV=tmp_cf.getfloat('min_AV'), max_AV=tmp_cf.getfloat('max_AV'),
            R_V=tmp_cf.getfloat('RV'), extlaw=tmp_cf.get('extlaw'), plot=plot,
            fit_sigma_rnd=tmp_cf.getboolean('fit_sigma_rnd', True),
        )
    model_spectra, results, results_coeffs, _ = r

    # write FITS RSS output
    output_guided_rss__tsw = dump_rss_output(out_file_fit=auto_ssp_output_fits_filename,
        wavelength=org_wave__w,
        model_spectra=model_spectra
    )
    print_done(time_ini=time_ini_auto_ssp, message='auto_ssp_elines_rnd_rss(): DONE!')
    print_done(time_ini=time_ini_loc, message='RSS analysis DONE!')
    # copy elines from auto_ssp disp_min run to final name.
    shutil.copy(
        src=f'elines_{auto_ssp_rss_output_filename}',
        dst=f'elines_{auto_ssp_rss_guided_output_filename}'
    )
    #
    # EL: missing plot scripts plot_output_auto_ssp_elines_several_Av_log_rss_all.pl
    #
    ##########################################################################

    ##########################################################################
    # Indices analysis
    #
    time_ini_loc = print_block_init('Indices analysis...')
    print('# -----=> get_index_output_auto_ssp_elines_rnd_rss_outFIT3D()', flush=True)
    tmp_cf = input_config['indices']
    indices_output_filename = tmp_cf.get('output_file', 'indices.CS.NAME.rss.out').replace('NAME', name)
    redshift__s = results[7]
    indices, indices__Iyx = get_index(
        wave__w=org_wave__w,
        flux_ssp__sw=output_guided_rss__tsw[0] - output_guided_rss__tsw[3],
        res__sw=output_guided_rss__tsw[4],
        redshift__s=redshift__s,
        n_sim=tmp_cf.getint('n_MonteCarlo', 5),
        plot=plot,
        seg__yx=seg_map__yx,
    )
    indices_names = list(__indices__.keys())
    f = open(indices_output_filename, 'w')
    for i_s in range(redshift__s.size):
        for i in range(len(indices_names)):
            ind_name = indices_names[i]
            print(f'{ind_name}', end=' ', file=f)
            EW_now = indices[ind_name]['EW'][i_s]
            s_EW_now = indices[ind_name]['sigma_EW'][i_s]
            print(f' {EW_now} {s_EW_now}', end=' ', file=f)
        med_flux = indices['SN'][i_s]
        std_flux = indices['e_SN'][i_s]
        print(f'SN  {med_flux} {std_flux}', file=f)
    f.close()
    # get_index_output_auto_ssp_elines_rnd_rss_outFIT3D(
    #     # ssp_flux__sw = output_guided_rss__tsw[0] - output_guided_rss__tsw[3]
    #     # gas_flux__sw
    #     # output_guided_rss__tsw,
    #     f'output.{auto_ssp_rss_guided_output_filename}.fits.gz',
    #     input_auto_ssp_rss_output=f'{auto_ssp_rss_guided_output_filename}',
    #     # redshift__s
    #     output_file=indices_output_filename,
    #     n_sim=tmp_cf.getint('n_MonteCarlo', 5),
    # )

    indices_output_fits_filename = tmp_cf.get('output_cube_file', 'indices.CS.NAME.cube.fits').replace('NAME', name)
    h_indices = {
        'COMMENT': 'FIT-header',
        'FILENAME': indices_output_fits_filename,
    }
    ind_k = [x for x in indices.keys() if 'SN' not in x]
    n_ind = len(ind_k)
    for i, k in enumerate(ind_k):
        h_indices[f'INDEX{i}'] = k
        h_indices[f'INDEX{i + n_ind + 1}'] = f'e_{k}'
    i += 1
    k = 'SN'
    h_indices[f'INDEX{i}'] = k
    h_indices[f'INDEX{i + n_ind + 1}'] = f'e_{k}'
    array_to_fits(indices_output_fits_filename, indices__Iyx, header=h_indices, overwrite=True)
    # index_seg_cube(indices_output_filename, cont_seg_filename, indices_output_fits_filename)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Generating maps
    #
    time_ini_loc = print_block_init('Generating maps...')
    print('# -----=> map_auto_ssp_rnd_seg()', flush=True)
    input_elines_filename = f'elines_{auto_ssp_rss_guided_output_filename}'
    map_auto_ssp_rnd_seg(
        input_elines=input_elines_filename,
        segmentation_fits=cont_seg_filename,
        output_prefix=config_seg.get('map_output_prefix', 'map.CS.NAME').replace('NAME', name),
        inst_disp=config_seg.getfloat('instrumental_dispersion', 0.9),
        wave_norm=config_seg.getfloat('wave_norm', None),
        # auto_ssp_config=config_file,
    )
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Emission Lines analysis
    #
    time_ini_loc = print_block_init('Emission Lines analysis...')
    wave_ref = config_elines.getfloat('vel_eline_reference_wavelength', __Ha_central_wl__)
    vel_hr = config_elines.getfloat('vel_eline_half_range', 200)
    nsearch = config_elines.getint('vel_eline_nsearch', 1)
    imin = config_elines.getfloat('vel_eline_imin', 0.95)
    w_min = wave_ref*(1 + min_red - vel_hr/__c__)
    w_max = wave_ref*(1 + max_red + vel_hr/__c__)
    print('# -----=> vel_eline_cube()', flush=True)
    vel_eline_map_filename = config_elines.get('vel_eline_map_file', 've.NAME.vel_map.fits').replace('NAME', name)
    vel_eline_mask_filename = config_elines.get('vel_eline_mask_map_file', 've.NAME.mask_map.fits').replace('NAME', name)
    vel_map__yx = np.zeros((ny, nx))
    vel_mask_map__yx = np.zeros((ny, nx))
    sel_wl = trim_waves(org_wave__w, [w_min, w_max])
    wave = org_wave__w[sel_wl]
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        flux = gas_cube__wyx[sel_wl, iy, ix]
        ve, mask, npeaks = vel_eline(flux, wave, nsearch=nsearch, imin=imin,
                                      wave_ref=wave_ref, set_first_peak=False)
        vel_map__yx[iy, ix] = ve
        vel_mask_map__yx[iy, ix] = mask
    # array_to_fits(vel_eline_map_filename, vel_map__yx, header=h_set_vel, overwrite=True)
    # h_set_vel['FILENAME'] = vel_eline_mask_filename
    # array_to_fits(vel_eline_mask_filename, vel_mask_map__yx, header=h_set_vel, overwrite=True)
    # vel_eline_cube(gas_cube_filename, nsearch=1, imin=0.95,
    #                outfile=vel_eline_prefix,
    #                wave_ref=wave_ref, wmin=w_min, wmax=w_max,
    #                dev='/null')
    vel_hr = config_elines.getfloat('clean_Ha_map_vel_half_range', 500)
    min_vel = red*__c__ - vel_hr
    max_vel = red*__c__ + vel_hr
    print('# -----=> clean_Ha_map()', flush=True)
    vel_map_clean__yx, vel_mask_map_clean__yx = clean_Ha_map(copy(vel_map__yx), copy(vel_mask_map__yx),
                                                             min_vel=min_vel, max_vel=max_vel)
    h_set_vel = {
        'COMMENT': 'vel_eline_cube result',
        'WMIN': w_min,
        'WMAX': w_max,
        'WREF': wave_ref,
        'FILENAME': vel_eline_map_filename,
    }
    array_to_fits(vel_eline_map_filename, vel_map_clean__yx, overwrite=True, header=h_set_vel)
    h_set_vel['FILENAME'] = vel_eline_mask_filename
    array_to_fits(vel_eline_mask_filename, vel_mask_map_clean__yx, overwrite=True, header=h_set_vel)

    _tmpcf = ConfigAutoSSP(config_file)
    k = f'{_tmpcf.systems[0]["start_w"]}_{_tmpcf.systems[0]["end_w"]}'
    index_model_Ha = 0
    disp_max_elines = output_el_models[k]['sigma'][index_model_Ha][0]*1.5
    input_config_file = config_elines.get('auto_ssp_config_file')

    # Preparing config to kin_cube_elines
    cf = ConfigAutoSSP(input_config_file)
    vel_hr = config_elines.getfloat('vel_half_range', 300)
    vel_min = vel - vel_hr
    vel_max = vel + vel_hr

    vel_map = copy(vel_map_clean__yx)
    vel_mask_map = copy(vel_mask_map_clean__yx)
    sigma_map = None
    sigma_fixed = None

    for i_s in range(cf.n_systems):
        syst = cf.systems[i_s]
        z_fact = 1 + red
        w_min = syst['start_w']
        w_max = syst['end_w']
        w_min_corr = int(w_min*z_fact)
        w_max_corr = int(w_max*z_fact)
        elcf = cf.systems_config[i_s]
        # v0
        elcf.guess[0][_MODELS_ELINE_PAR['v0']] = vel
        elcf.to_fit[0][_MODELS_ELINE_PAR['v0']] = 1
        elcf.pars_0[0][_MODELS_ELINE_PAR['v0']] = vel_min
        elcf.pars_1[0][_MODELS_ELINE_PAR['v0']] = vel_max
        elcf.links[0][_MODELS_ELINE_PAR['v0']] = -1
        # sigma
        elcf.guess[0][_MODELS_ELINE_PAR['sigma']] = config_elines.getfloat('dispersion_guess', 1.2)
        elcf.to_fit[0][_MODELS_ELINE_PAR['sigma']] = 1
        elcf.pars_0[0][_MODELS_ELINE_PAR['sigma']] = config_elines.getfloat('dispersion_min', 0.5)
        elcf.pars_1[0][_MODELS_ELINE_PAR['sigma']] = disp_max_elines
        elcf.links[0][_MODELS_ELINE_PAR['sigma']] = -1

        if save_aux_files:
            # print config to file
            fname = f'tmp.{name}.{i_s}.config'
            elcf.print(filename=fname)
        w_min = int(w_min)
        w_max = int(w_max)
        w_minmax_prefix = f'{w_min}_{w_max}'
        _m_str = 'model'
        if elcf.n_models > 1:
            _m_str += 's'
        print(f'# analyzing {elcf.n_models} {_m_str} in {w_minmax_prefix.replace("_", "-")} wavelength range')
        output_filename = config_elines.get('output_file', f'KIN.GAS.prefix.NAME.out').replace('NAME', name)
        output_filename = output_filename.replace('prefix', w_minmax_prefix)
        f_log = None
        output_log_filename = config_elines.get('log_file', None)
        if output_log_filename is not None:
            output_log_filename = output_log_filename.replace('NAME', name)
            output_log_filename = output_log_filename.replace('prefix', w_minmax_prefix)
            f_log = open(output_log_filename, 'w')
        map_output_prefix = config_elines.get('map_output_prefix', f'map.prefix.NAME').replace('NAME', name).replace('prefix', w_minmax_prefix)
        map_output_prefix = map_output_prefix.replace('prefix', w_minmax_prefix)
        fix_disp = 0
        if w_min == 3700:
            sigma_fixed = 1
        print('# -----=> kin_cube_elines_rnd()', flush=True)
        time_ini_kin = print_time(print_seed=False)
        sel_wl_range = trim_waves(org_wave__w, [w_min_corr, w_max_corr])
        if sel_wl_range.astype('int').sum() == 0:
            print('[kin_cube_elines]: n_wavelength = 0: No avaible spectra to perform the configured analysis.')
            output_el_models = create_emission_lines_parameters(elcf, shape=(ny, nx))
        else:
            wave_msk__w = org_wave__w[sel_wl_range]
            flux_msk__wyx = gas_cube__wyx[sel_wl_range]
            eflux_msk__wyx = None
            if org_error__wyx is not None:
                eflux_msk__wyx = copy(org_error__wyx[sel_wl_range])
            n_MC = config_elines.getint('n_MonteCarlo', 30)
            n_loops = config_elines.getint('n_loops', 3)
            scale_ini = config_elines.getfloat('scale_ini', 0.15)
            with redirect_stdout(f_log):
                r = kin_cube_elines_main(
                    wavelength=copy(wave_msk__w),
                    cube_flux=copy(flux_msk__wyx),
                    cube_eflux=eflux_msk__wyx,
                    config=elcf, out_file=output_filename,
                    n_MC=n_MC, n_loops=n_loops, scale_ini=scale_ini,
                    vel_map=vel_map, sigma_map=sigma_map,
                    vel_fixed=0, sigma_fixed=sigma_fixed,
                    redefine_max=1, vel_mask_map=vel_mask_map, memo=0,
                    plot=plot, run_mode=config_elines.get('run_mode', 'RND'),
                )
            if f_log is not None:
                f_log.close()
            output_el_spectra, output_el_models = r
            output_emission_lines_spectra(wave_msk__w, output_el_spectra, h_set_cube, map_output_prefix.replace('map', 'KIN.cube'))
        output_emission_lines_parameters(map_output_prefix, elcf, output_el_models)
        print_done(time_ini=time_ini_kin, message='DONE kin_cube_elines_rnd()!')
        if not i_s:
            NIIHa_output_el_models = output_el_models
            print('# -----=> med2df() v_Ha map', flush=True)
            vel_map_Ha__yx = NIIHa_output_el_models['v0'][index_model_Ha]
            vel_map_Ha__yx[~np.isfinite(vel_map_Ha__yx)] = 0
            vel_map = copy(vel_map_Ha__yx)
            vel_map_Ha__yx = median_filter(copy(vel_map_Ha__yx), size=(3, 3), mode='reflect')
            # med2df(f'{map_output_prefix}_vel_00.fits', f'vel.{name}.fits', 3, 3)
            sigma_map_Ha__yx = NIIHa_output_el_models['sigma'][index_model_Ha]
            print('# -----=> med2df() disp_Ha map', flush=True)
            sigma_map_Ha__yx[~np.isfinite(sigma_map_Ha__yx)] = 0
            sigma_map = copy(sigma_map_Ha__yx)
            sigma_map_flux_elines__yx = copy(sigma_map_Ha__yx)
            disp_map_Ha_filtered__yx = median_filter(sigma_map_Ha__yx*__sigma_to_FWHM__, size=(3, 3), mode='reflect')
            # med2df(f'{map_output_prefix}_disp_00.fits', f'disp.{name}.fits', 3, 3)
            print('# -----=> imarith()', flush=True)
            # imarith(f'disp.{name}.fits', '*', str(__FWHM_to_sigma__), f'disp.{name}.fits')
            if save_aux_files:
                vel_filename = f'vel.{name}.fits'
                remove_isfile(vel_filename)
                array_to_fits(vel_filename, vel_map_Ha__yx, overwrite=True)
                disp_filename = f'disp.{name}.fits'
                remove_isfile(disp_filename)
                sigma_map_Ha_filtered__yx = __FWHM_to_sigma__*disp_map_Ha_filtered__yx
                array_to_fits(disp_filename, sigma_map_Ha_filtered__yx, overwrite=True)
        print(f'# emission lines in wavelength range {w_minmax_prefix.replace("_", "-")} analyzed')
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # gzip fits
    #
    time_ini_loc = print_block_init('Compressing FITS files...')
    compresslevel = config.getint('gzip_compresslevel', 6)
    for file in glob.glob(f'*{name}*.fits'):
        with open(file, 'rb') as f_in:
            # EL: compresslevel 6 is biased towars high compression
            # at expense of speed, also 6 is also the value of gzip
            # in shell mode.
            with gzip.open(f'{file}.gz', mode='wb', compresslevel=compresslevel) as f_comp:
                shutil.copyfileobj(f_in, f_comp)
        # remove uncompressed file
        remove(file)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Momentum analysis of emission lines
    #
    time_ini_loc = print_block_init('Momentum analysis of emission lines (flux_elines)...')
    tmp_cf = input_config['flux_elines']
    elines_list = tmp_cf.get('elines_list')
    flux_elines_output_filename = tmp_cf.get('output_file', 'flux_elines.NAME.cube.fits.gz').replace('NAME', name)
    print('# -----=> flux_elines_cube_EW()', flush=True)

    fe_output, fe_header = flux_elines_cube_EW(
        flux__wyx = gas_cube__wyx,
        input_header = h_set_cube,
        n_MC=tmp_cf.getint('n_MonteCarlo', 10),
        elines_list=elines_list,
        vel__yx=vel_map_clean__yx,
        sigma__yx=sigma_map_flux_elines__yx,
        eflux__wyx=org_error__wyx,
        flux_ssp__wyx=ssp_mod_cube__wyx,
        # flux_ssp__wyx=ssp_mod_tmp__wyx,
    )
    array_to_fits(flux_elines_output_filename, fe_output, header=fe_header, overwrite=True)
    # flux_elines_cube_EW(
    #     n_mc=tmp_cf.getint('n_MonteCarlo', 10),
    #     input_cube=gas_cube_filename + '.gz',
    #     input_e_cube=cube_filename,
    #     input_cont_cube=ssp_mod_tmp_filename + '.gz',
    #     elines_list=elines_list,
    #     output=flux_elines_output_filename,
    #     guided_map=vel_eline_map_filename + '.gz',
    #     guided_sigma=f'map.6530_6630.{name}_disp_00.fits.gz',
    # )
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # generate mass age met maps
    #
    time_ini_loc = print_block_init('Creating mass, age and metallicities map...')
    sum_mass_age_filename = config_pack.get('sum_mass_age_out_file_1').replace('NAME', name)
    print('# -----=> sum_mass_age()', flush=True)
    sum_mass_age(name, output_csv_filename=sum_mass_age_filename)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Final pack, and store files
    #
    # add a / at the end of directories names
    time_ini_final_pack = print_block_init('Begin final pack of files...')
    if not dir_out.endswith('/'):
        dir_out += '/'
    if not dir_datacubes_out.endswith('/'):
        dir_datacubes_out += '/'
    ##########################################################################

    ##########################################################################
    # Mask maps
    #
    time_ini_loc = print_block_init('Masking maps...')
    for fname in glob.glob(f'map.CS*{name}*.fits.gz'):
        print(f' ---=> imarith() {fname}', flush=True)
        imarith(fname, '*', f'{SN_mask_map_filename}.gz', fname)
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Pack files
    #
    time_ini_loc = print_block_init('Packing files...')
    print('# -----=> pack_NAME()', flush=True)
    pack_NAME(name,
              ssp_pack_filename=config_pack.get('SSP_file'),
              elines_pack_filename=config_pack.get('ELINES_file'),
              sfh_pack_filename=config_pack.get('SFH_file'),
              mass_out_filename=config_pack.get('sum_mass_age_out_file_2').replace('NAME', name))
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # Create final directory
    #
    time_ini_loc = print_block_init('Store generated files...')
    if 'manga' in name:
        try:
            _, plate, ifu = name.split('-')
            dir_out += f'{plate}/{ifu}/'
        except:
            dir_out += f'{name}/'
    else:
        dir_out += f'{name}/'
    try:
        makedirs(dir_out)
    except FileExistsError:
        print(f'{basename(sys.argv[0])}: {dir_out}: directory already exists')
    try:
        makedirs(dir_datacubes_out)
    except FileExistsError:
        print(f'{basename(sys.argv[0])}: {dir_datacubes_out}: directory already exists')
    # copy and move files
    # the filename should be in dst in order to rewrite file
    print(f'Moving files to {dir_out}', flush=True)
    for file in glob.glob(f'*{name}*'):
        shutil.move(src=file, dst=f'{dir_out}{file}')
    print_done(time_ini=time_ini_loc, message='DONE move files!')
    print(f'Copying datacubes to {dir_datacubes_out}', flush=True)
    output_fits_auto_ssp_cen = 'output.' + input_config['cen_auto_ssp_inst_disp'].get('output_filename', 'auto_ssp.NAME.cen.out').replace('NAME', name) + '.fits.gz'
    output_auto_ssp_int = input_config['int_auto_ssp_inst_disp'].get('output_filename', 'auto_ssp.NAME.int.out').replace('NAME', name)
    files_to_copy = [
        output_auto_ssp_int,
        int_spec_filename,
        flux_elines_output_filename,
        indices_output_fits_filename + '.gz',
        f'{name}.SSP.cube.fits.gz',
        f'{name}.SFH.cube.fits.gz',
        f'{name}.ELINES.cube.fits.gz',
        output_fits_auto_ssp_cen,
    ]
    for file in files_to_copy:
        shutil.copy(src=f'{dir_out}{file}', dst=f'{dir_datacubes_out}')
    print_done(time_ini=time_ini_loc, message='DONE: store files!')
    ##########################################################################
    print_done(time_ini=time_ini_final_pack, message='DONE: final pack!')

    ##########################################################################
    # Plot needed
    # TODO ana_single_MaNGA_plot.pl
    ##########################################################################
    return dir_out

def main(args):
    name = args.name
    force_z = args.redshift
    x0 = args.x0
    y0 = args.y0
    config = configparser.ConfigParser(
        # allow a variables be set without value
        allow_no_value=True,
        # allows duplicated keys in different sections
        strict=False,
        # deals with variables inside configuratio file
        interpolation=configparser.ExtendedInterpolation())
    config.read(args.config_file)
    dir_log = 'log'
    log_file = config['general'].get('log_file', None)
    f = None
    if (log_file is not None):
        if 'NAME' in log_file:
            log_file = log_file.replace('NAME', name)
            omode = 'w'
        else:
            omode='a'
        if log_file[0:5] != '/dev/':
            try:
                makedirs(dir_log)
                log_file = f'{dir_log}/{log_file}'
            except FileExistsError:
                print(f'{basename(sys.argv[0])}: {dir_log}: directory already exists')
                log_file = f'{dir_log}/{log_file}'
            except:
                print(f'{basename(sys.argv[0])}: {dir_log}: cannot create directory')
        else:
            omode = 'w'
        f = open(log_file, omode)
    with redirect_stdout(f):
        with redirect_stderr(f):
            init_message = f'Initiating run for galaxy {name} - May the force be with you!'
            init_message += f'\n# Configuration file = {args.config_file}'
            init_message += f'\n# Output log file = {log_file}'
            cube_filename = config['general']['cube_filename'].replace('NAME', name)
            init_message += f'\n# Cube file = {cube_filename}'
            time_ini_run = print_block_init(init_message, print_seed=True)
            seed = config['general'].getint('seed', None)
            if seed is not None:
                print(f'# Forcing seed: {seed}')
            else:
                seed = time_ini_run
            np.random.seed(seed)
            dir_out = ana_single(name, config, force_z=force_z, x0=x0, y0=y0)
            print_done(time_ini=time_ini_run, message=f'DONE: galaxy {name} analyzed.')
    # After some problems with the write in the log_file
    # we move the log_file after everithing is done.
    # If the program was not able to create the dir_log directory
    # in some machines the final writting of the log file
    # could be incomplete.
    if (log_file is not None) and os.path.isfile(log_file):
        f.close()
        if name in log_file:
            _tmp = config['general'].get('log_file', 'ana_single.NAME.log').replace('NAME', name)
            shutil.move(src=log_file, dst=f'{dir_out}{_tmp}')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
