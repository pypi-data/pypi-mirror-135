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

from pyFIT3D.common.tools import flux_elines_cube_EW
from pyFIT3D.common.auto_ssp_tools import ConfigAutoSSP
from pyFIT3D.common.tools import array_to_fits, get_wave_from_header, pack_results_name
from pyFIT3D.common.tools import trim_waves, get_data_from_fits, vel_eline, clean_Ha_map, imarith
from pyFIT3D.common.gas_tools import output_emission_lines_spectra, create_emission_lines_parameters
from pyFIT3D.common.io import ReadArguments, print_time, remove_isfile, print_done, print_block_init
from pyFIT3D.common.constants import _MODELS_ELINE_PAR, __c__, __FWHM_to_sigma__, __sigma_to_FWHM__, __Ha_central_wl__
from pyFIT3D.common.gas_tools import kin_cube_elines_main, output_emission_lines_parameters, create_emission_lines_parameters

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])

    __mandatory__ = ['name', 'config_file']
    __optional__ = ['dir_out', 'dir_datacubes_out']
    __arg_names__ = __mandatory__ + __optional__
    __N_tot_args__ = len(__arg_names__)

    __conv_func_mandatory__ = {'name': str, 'config_file': str}
    __conv_func_optional__ = {'dir_out': str, 'dir_datacubes_out': str}
    __conv_func__ = __conv_func_mandatory__.copy()
    __conv_func__.update(__conv_func_optional__)

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' NAME CONFIG_FILE [DIR_OUT] [DIR_DATACUBES_OUT]'
    usage_msg_tmp3 = '\nCONFIG_FILE is mandatory but defaults to ana_single_kin.ini'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2 + usage_msg_tmp3

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self._parse()

    def _parse(self):
        if self.config_file is None:
            self.config_file = 'ana_single.ini'
        if not isfile(self.config_file):
            print(f'{self.__script_name__}: {self.config_file}: not found')
            sys.exit()

def ana_single_kin(name, input_config, input_dir_out=None, input_dir_datacubes_out=None):
    config = input_config['general']
    config_elines = input_config['emission_lines']
    config_pack = input_config['pack']
    config_seg = input_config['cube_segmentation']
    cube_filename = config['cube_filename'].replace('NAME', name)
    plot = config.getint('plot', 0)
    save_aux_files = config.getboolean('save_aux_files', True)
    dir_conf = config.get('dir_conf', '../legacy')
    dir_out = config.get('dir_out', '../out')
    # Try to set a new dir_datacubes_out
    dir_datacubes_out = input_dir_datacubes_out
    if dir_datacubes_out is None:
        dir_datacubes_out = config.get('dir_datacubes_out', '../out')
    inst_disp = config.getfloat('instrumental_dispersion')

    if not dir_out.endswith('/'):
        dir_out += '/'
    if not dir_datacubes_out.endswith('/'):
        dir_datacubes_out += '/'
    if 'manga' in name:
        _, plate, ifu = name.split('-')
        dir_out += f'{plate}/{ifu}/'
    else:
        dir_out += f'{name}/'

    ##########################################################################
    # Load datacube
    #
    time_ini_loc = print_block_init('Loading datacube and redshift information...')
    org_cube__wyx, org_h, n_ext = get_data_from_fits(cube_filename, header=True, return_n_extensions=True)
    ny, nx = org_cube__wyx.shape[1:]
    h_set_cube = {'CRVAL3': org_h['CRVAL3'], 'CDELT3': org_h['CDELT3'], 'CRPIX3': org_h['CRPIX3']}
    org_error__wyx = None
    if org_h['EXTEND']:
        org_error__wyx = get_data_from_fits(cube_filename, extension=1)
    else:
        print('# Unable to find an EXTEND key on cube: ', flush=True)
        print('# - missing error spectra', flush=True)

    # original wavelength
    wave_org__w = get_wave_from_header(org_h, wave_axis=3)
    auto_ssp_config_file = f'{dir_out}auto.{name}.config'
    gas_cube_filename = config_seg.get('gas_cube_file', 'GAS.NAME.cube.fits').replace('NAME', name)
    gas_cube_filename = f'{dir_out}{gas_cube_filename}.gz'
    print(f'# Gas cube = {gas_cube_filename}')
    gas_cube__wyx = get_data_from_fits(gas_cube_filename)

    # reading redshift from auto_ssp_Z
    tmp_cf = input_config['cen_auto_ssp_no_lines']
    auto_ssp_output_filename = tmp_cf.get('output_filename', 'auto_ssp_Z.NAME.cen.out').replace('NAME', name)
    auto_ssp_output_filename = f'{dir_out}{auto_ssp_output_filename}'
    red = np.loadtxt(fname=auto_ssp_output_filename, unpack=True, comments='#', delimiter=',', usecols=12)
    red_f = 300/__c__
    min_red = red - red_f
    max_red = red + red_f
    d_red = 0.1*red_f
    vel = red*__c__
    print(f'# Redshift = {red:.8f} - Vel = {vel:.8f}')
    print_done(time_ini=time_ini_loc)

    # Read SSP MOD
    ssp_mod_filename = config_seg.get('ssp_mod_file', 'SSP_mod.NAME.cube.fits').replace('NAME', name)
    ssp_mod_filename = f'{dir_out}{ssp_mod_filename}.gz'
    ssp_mod_cube__wyx = get_data_from_fits(ssp_mod_filename)

    # elines file
    tmp_cf = input_config['auto_ssp_rss_guided']
    elines_file = tmp_cf.get('output_filename', 'auto_ssp.CS.NAME.rss.out').replace('NAME', name)
    elines_file = f'{dir_out}elines_{elines_file}'
    print(f'# elines file = {elines_file}')

    # SN_mask_map
    SN_mask_map_filename = f'{dir_out}mask.{name}.V.fits'
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
    sel_wl = trim_waves(wave_org__w, [w_min, w_max])
    wave = wave_org__w[sel_wl]
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        flux = gas_cube__wyx[sel_wl, iy, ix]
        ve, mask, npeaks = vel_eline(flux, wave, nsearch=nsearch, imin=imin,
                                      wave_ref=wave_ref, set_first_peak=False)
        vel_map__yx[iy, ix] = ve
        vel_mask_map__yx[iy, ix] = mask
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

    # auto_ssp_elines_rnd_rss_main output() by file.
    with open(elines_file, 'r') as f:
        line = f.readline()
        while not line.startswith('eline'):
            line = f.readline()
        disp_max_elines = eval(line.split(' ')[5])*1.5
    print(f'disp_max_elines = {disp_max_elines}')
    dispersion_guess = config_elines.getfloat('dispersion_guess', 1.2)
    dispersion_min = config_elines.getfloat('dispersion_min', 0.5)
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
        elcf.guess[0][_MODELS_ELINE_PAR['sigma']] = dispersion_guess
        elcf.to_fit[0][_MODELS_ELINE_PAR['sigma']] = 1
        elcf.pars_0[0][_MODELS_ELINE_PAR['sigma']] = dispersion_min
        elcf.pars_1[0][_MODELS_ELINE_PAR['sigma']] = disp_max_elines
        elcf.links[0][_MODELS_ELINE_PAR['sigma']] = -1
        if save_aux_files:
            # print config to file
            fname = f'tmp.{name}.{i_s}.config'
            elcf.print(filename=fname)
        w_min = int(w_min)
        w_max = int(w_max)
        w_minmax_prefix = f'{w_min}_{w_max}'
        print(f'w_minmax_prefix = {w_minmax_prefix}')
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
        sel_wl_range = trim_waves(wave_org__w, [w_min_corr, w_max_corr])
        if sel_wl_range.astype('int').sum() == 0:
            print('[kin_cube_elines]: n_wavelength = 0: No avaible spectra to perform the configured analysis.')
            output_el_models = create_emission_lines_parameters(elcf, shape=(ny, nx))
        else:
            wave_msk__w = copy(wave_org__w[sel_wl_range])
            flux_msk__wyx = copy(gas_cube__wyx[sel_wl_range])
            eflux_msk__wyx = None
            if org_error__wyx is not None:
                eflux_msk__wyx = copy(org_error__wyx[sel_wl_range])
            n_MC = config_elines.getint('n_MonteCarlo', 30)
            n_loops = config_elines.getint('n_loops', 3)
            scale_ini = config_elines.getfloat('scale_ini', 0.15)
            with redirect_stdout(f_log):
                r = kin_cube_elines_main(
                    wave_msk__w, flux_msk__wyx, elcf, output_filename,
                    cube_eflux=eflux_msk__wyx, n_MC=n_MC, n_loops=n_loops, scale_ini=scale_ini,
                    vel_map=vel_map, sigma_map=sigma_map,
                    vel_fixed=0, sigma_fixed=sigma_fixed,
                    redefine_max=True, vel_mask_map=vel_mask_map, memo=0,
                    plot=plot,
                    run_mode=config_elines.get('run_mode', 'RND'),
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
            index_model_Ha = 0
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
    )
    array_to_fits(flux_elines_output_filename, fe_output, header=fe_header, overwrite=True)
    print_done(time_ini=time_ini_loc)
    ##########################################################################


    ##########################################################################
    # Final pack, and store files
    #
    time_ini_final_pack = print_block_init('Begin final pack of files...')

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
    print('# -----=> pack_results_name()', flush=True)
    pack_results_name(name,
                      pack_filename=config_pack.get('ELINES_file'),
                      prefix='ELINES')
    print_done(time_ini=time_ini_loc)
    ##########################################################################

    ##########################################################################
    # copy and move files
    # the filename should be in dst in order to rewrite file

    if input_dir_out is not None:
        dir_out = input_dir_out
        if not dir_out.endswith('/'):
            dir_out += '/'
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
    if not dir_datacubes_out.endswith('/'):
        dir_datacubes_out += '/'
    try:
        makedirs(dir_datacubes_out)
    except FileExistsError:
        print(f'{basename(sys.argv[0])}: {dir_datacubes_out}: directory already exists')
    print(f'Moving files to {dir_out}', flush=True)
    for file in glob.glob(f'*{name}*'):
        shutil.move(src=file, dst=f'{dir_out}{file}')
    print_done(time_ini=time_ini_loc, message='DONE move files!')
    print(f'Copying datacube to {dir_datacubes_out}', flush=True)
    files_to_copy = [
        f'{name}.ELINES.cube.fits.gz',
        flux_elines_output_filename,
    ]
    for file in files_to_copy:
        shutil.copy(src=f'{dir_out}{file}', dst=f'{dir_datacubes_out}')
    print_done(time_ini=time_ini_loc, message='DONE: store files!')
    ##########################################################################

    print_done(time_ini=time_ini_final_pack, message='DONE: final pack!')
    ##########################################################################

    return dir_out

def main(args):
    name = args.name
    config = configparser.ConfigParser(
        # allow a variables be set without value
        allow_no_value=True,
        # allows duplicated keys in different sections
        strict=False,
        # deals with variables inside configuratio file
        interpolation=configparser.ExtendedInterpolation())
    config.read(args.config_file)
    dir_log = 'log'
    log_file = config['general'].get('kin_log_file', None)
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
            dir_out = ana_single_kin(name, config,
                                     input_dir_out=args.dir_out,
                                     input_dir_datacubes_out=args.dir_datacubes_out)
            print_done(time_ini=time_ini_run, message=f'DONE: galaxy {name} analyzed.')
    # After some problems with the write in the log_file
    # we move the log_file after everithing is done.
    # If the program was not able to create the dir_log directory
    # in some machines the final writting of the log file
    # could be incomplete.
    if (log_file is not None) and os.path.isfile(log_file):
        f.close()
        if name in log_file:
            _tmp = config['general'].get('kin_log_file', 'ana_single_kin.NAME.log').replace('NAME', name)
            shutil.move(src=log_file, dst=f'{dir_out}{_tmp}')

if __name__ == '__main__':
    main(ReadArgumentsLocal())
