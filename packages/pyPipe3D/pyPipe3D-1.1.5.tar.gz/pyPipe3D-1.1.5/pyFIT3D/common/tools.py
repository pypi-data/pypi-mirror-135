#!/usr/bin/env python3

# System imports
import io
import sys
import warnings
import itertools
import numpy as np
from copy import deepcopy as copy
from os.path import basename, isfile
from scipy.interpolate import interp1d
from scipy.ndimage import median_filter
from astropy.io.fits.verify import VerifyWarning

from .stats import median_filter as st_median_filter
from .stats import hyperbolic_fit_par, std_m, pdl_stats, _STATS_POS
from .io import trim_waves, get_data_from_fits, get_wave_from_header
from .constants import __c__, __sigma_to_FWHM__, __indices__, _INDICES_POS
from .io import output_spectra, array_to_fits, write_img_header, print_verbose
from .constants import __Hubble_constant__, __Omega_matter__, __Omega_Lambda__
from .constants import __solar_luminosity__, __solar_metallicity__, _figsize_default

warnings.simplefilter('ignore', category=VerifyWarning)

def gen_rebin(a, e, bin_e, mean=True):
    '''
    Rebinning function. Given the value array `a`, with generic
    positions `e` such that `e.shape == a.shape`, return the sum
    or the mean values of `a` inside the bins defined by `bin_e`.

    Parameters
    ----------
    a : array like
        The array values to be rebinned.

    e : array like
        Generic positions of the values in `a`.

    bin_e : array like
        Bins of `e` to be used in the rebinning.

    mean : boolean
        Divide the sum by the number of points inside the bin.
        Defaults to `True`.

    Returns
    -------
    a_e : array
        An array of length `len(bin_e)-1`, containing the sum or
        mean values of `a` inside each bin.
    '''
    a_e = np.histogram(e.ravel(), bin_e, weights=a.ravel())[0]
    if mean:
        N = np.histogram(e.ravel(), bin_e)[0]
        mask = N > 0
        a_e[mask] /= N[mask]
    return a_e

def gen_frac_radius(X, r, r_max=None, frac=0.5):
    '''
    Evaluate radius where the cumulative value of `X` reaches FRAC of its value.

    Parameters
    ----------
    X : array like
        The property whose FRAC radius will be evaluated.

    r : array like
        Radius associated to each value of `X`. Must be the
        same shape as `X`.

    r_max : int
        Integrate up to `r_max`. Defaults to `np.max(r)`.

    frac : float
        Fraction of X where the radius will be evaluated

    Returns
    -------
    FXR : float
        The "frac X radius". If frac is 0.5 (default), will return HXR (half X
        radius).

    Examples
    --------

    Find the radius containing half of the volume of a gaussian.

    >>> import numpy as np
    >>> xx, yy = np.indices((100, 100))
    >>> x0, y0, A, a = 50.0, 50.0, 1.0, 20.0
    >>> z = A * np.exp(-((xx-x0)**2 + (yy-y0)**2)/a**2)
    >>> r = np.sqrt((xx - 50)**2 + (yy-50)**2)
    >>> gen_frac_radius(z, r, f=0.5)
    16.786338066912215

    '''
    if r_max is None:
        r_max = np.max(r)
    bin_r = np.arange(0, r_max, 1)
    cumsum_X = gen_rebin(X, r, bin_r, mean=False).cumsum()

    from scipy.interpolate import interp1d
    invX_func = interp1d(cumsum_X, bin_r[1:])
    halfRadiusPix = invX_func(frac * cumsum_X.max())
    return float(halfRadiusPix)

def get_distance(x, y, x0, y0, pa=0.0, ba=1.0):
    '''
    Return an image (:class:`numpy.ndarray`)
    of the distance from the center ``(x0, y0)`` in pixels,
    assuming a projected disk.

    Parameters
    ----------
    x : array
        X coordinates to get the pixel distances.

    y : array
        y coordinates to get the pixel distances.

    x0 : float
        X coordinate of the origin.

    y0 : float
        Y coordinate of the origin.

    pa : float, optional
        Position angle in radians, counter-clockwise relative
        to the positive X axis.

    ba : float, optional
        Ellipticity, defined as the ratio between the semiminor
        axis and the semimajor axis (:math:`b/a`).

    Returns
    -------
    pixel_distance : array
        Pixel distances.
    '''
    y = np.asarray(y) - y0
    x = np.asarray(x) - x0
    x2 = x**2
    y2 = y**2
    xy = x * y

    a_b = 1.0/ba
    cos_th = np.cos(pa)
    sin_th = np.sin(pa)

    A1 = cos_th ** 2 + a_b ** 2 * sin_th ** 2
    A2 = -2.0 * cos_th * sin_th * (a_b ** 2 - 1.0)
    A3 = sin_th ** 2 + a_b ** 2 * cos_th ** 2

    return np.sqrt(A1 * x2 + A2 * xy + A3 * y2)

def get_image_distance(shape, x0, y0, pa=0.0, ba=1.0):
    '''
    Return an image (:class:`numpy.ndarray`)
    of the distance from the center ``(x0, y0)`` in pixels,
    assuming a projected disk.

    Parameters
    ----------
    shape : (float, float)
        Shape of the image to get the pixel distances.

    x0 : float
        X coordinate of the origin.

    y0 : float
        Y coordinate of the origin.

    pa : float, optional
        Position angle in radians, counter-clockwise relative
        to the positive X axis. Defaults to ``0.0``.

    ba : float, optional
        Ellipticity, defined as the ratio between the semiminor
        axis and the semimajor axis (:math:`b/a`). Defaults to ``1.0``.

    Returns
    -------
    pixel_distance : 2-D array
        Image containing the distances.

    See also
    --------
    :func:`get_distance`

    '''
    y, x = np.indices(shape)
    return get_distance(x, y, x0, y0, pa, ba)

def radial_profile(prop, bin_r, x0, y0, pa=0.0, ba=1.0, rad_scale=1.0,
                   mask=None, mode='mean', return_npts=False):
    '''
    Calculate the radial profile of an N-D image.

    Parameters
    ----------
    prop : array
        Image of property to calculate the radial profile.

    bin_r : array
        Semimajor axis bin boundaries in units of ``rad_scale``.

    x0 : float
        X coordinate of the origin.

    y0 : float
        Y coordinate of the origin.

    pa : float, optional
        Position angle in radians, counter-clockwise relative
        to the positive X axis.

    ba : float, optional
        Ellipticity, defined as the ratio between the semiminor
        axis and the semimajor axis (:math:`b/a`).

    rad_scale : float, optional
        Scale of the bins, in pixels. Defaults to 1.0.

    mask : array, optional
        Mask containing the pixels to use in the radial profile.
        Must be bidimensional and have the same shape as the last
        two dimensions of ``prop``. Default: no mask.

    mode : string, optional
        One of:
            * ``'mean'``: Compute the mean inside the radial bins (default).
            * ``'median'``: Compute the median inside the radial bins.
            * ``'sum'``: Compute the sum inside the radial bins.
            * ``'var'``: Compute the variance inside the radial bins.
            * ``'std'``: Compute the standard deviation inside the radial bins.

    return_npts : bool, optional
        If set to ``True``, also return the number of points inside
        each bin. Defaults to ``False``.


    Returns
    -------
    radProf : [masked] array
        Array containing the radial profile as the last dimension.
        Note that ``radProf.shape[-1] == (len(bin_r) - 1)``
        If ``prop`` is a masked aray, this and ``npts`` will be
        a masked array as well.

    npts : [masked] array, optional
        The number of points inside each bin, only if ``return_npts``
        is set to ``True``.


    See also
    --------
    :func:`get_image_distance`
    '''
    def red(func, x, fill_value):
        if x.size == 0: return fill_value, fill_value
        if x.ndim == 1: return func(x), len(x)
        return func(x, axis=-1), x.shape[-1]

    imshape = prop.shape[-2:]
    nbins = len(bin_r) - 1
    new_shape = prop.shape[:-2] + (nbins,)
    r__yx = get_image_distance(imshape, x0, y0, pa, ba) / rad_scale
    if mask is None:
        mask = np.ones(imshape, dtype=bool)
    if mode == 'mean':
        reduce_func = np.mean
    elif mode == 'median':
        reduce_func = np.median
    elif mode == 'sum':
        reduce_func = np.sum
    elif mode == 'var':
        reduce_func = np.var
    elif mode == 'std':
        reduce_func = np.std
    else:
        raise ValueError('Invalid mode: %s' % mode)

    if isinstance(prop, np.ma.MaskedArray):
        n_bad = prop.mask.astype('int')
        max_bad = 1.0
        while n_bad.ndim > 2:
            max_bad *= n_bad.shape[0]
            n_bad = n_bad.sum(axis=0)
        mask = mask & (n_bad / max_bad < 0.5)
        prop_profile = np.ma.masked_all(new_shape)
        npts = np.ma.masked_all((nbins,))
        prop_profile.fill_value = prop.fill_value
        reduce_fill_value = np.ma.masked
    else:
        prop_profile = np.empty(new_shape)
        npts = np.empty((nbins,))
        reduce_fill_value = np.nan
    if mask.any():
        dist_flat = r__yx[mask]
        dist_idx = np.digitize(dist_flat, bin_r)
        prop_flat = prop[...,mask]
        for i in range(0, nbins):
            prop_profile[..., i], npts[i] = red(reduce_func, prop_flat[..., dist_idx == i+1], reduce_fill_value)

    if return_npts:
        return prop_profile, npts
    return prop_profile

def get_ellipse_pars(image, x0, y0, mask=None):
    '''
    Estimate ellipticity and orientation of the galaxy using the
    "Stokes parameters", as described in Sec. 4.4.6.5 at:
    http://adsabs.harvard.edu/abs/2002AJ....123..485S

    The image used is ``signal``.

    Parameters
    ----------
    image : array
        Image to use when calculating the ellipse parameters.

    x0 : float
        X coordinate of the origin.

    y0 : float
        Y coordinate of the origin.

    mask : array, optional
        Mask containing the pixels to take into account.

    Returns
    -------
    pa : float
        Position angle in radians, counter-clockwise relative
        to the positive X axis.

    ba : float
        Ellipticity, defined as the ratio between the semiminor
        axis and the semimajor axis (:math:`b/a`).
    '''
    if mask is None:
        mask = np.ones_like(image, dtype=bool)

    yy, xx = np.indices(image.shape)
    y = yy - y0
    x = xx - x0
    x2 = x**2
    y2 = y**2
    xy = x * y
    r2 = x2 + y2

    mask &= (r2 > 0.0)
    norm = image[mask].sum()
    Mxx = ((x2[mask] / r2[mask]) * image[mask]).sum() / norm
    Myy = ((y2[mask] / r2[mask]) * image[mask]).sum() / norm
    Mxy = ((xy[mask] / r2[mask]) * image[mask]).sum() / norm

    Q = Mxx - Myy
    U = Mxy

    pa = np.arctan2(U, Q) / 2.0

    # b/a ratio
    ba = (np.sin(2 * pa) - U) / (np.sin(2 * pa) + U)
    # Should be the same as ba
    #ba_ = (np.cos(2*pa) - Q) / (np.cos(2*pa) + Q)

    return pa, ba

def get_SN_cube(org_cube__wyx, wave__w, wmin=None, wmax=None):
    '''
    Generates the SN, the mean and the standard deviation maps of
    ``org_cube__wyx`` within ``wmin`` and ``wmax``.

    Parameters
    ----------
    org_cube__wyx : array
        The cube spectra. Dimensions are :math:`(NW, NY, NX)`, where
        :math:`NW` is the number of wavelengths, and :math:`(NY, NX)`
        the 2D-image dimension.

    wave__w : array
        The wavelengths with dimension NW

    wmin : int, optional
        Blue-side border (leftmost) of the wavelength range to generate the
        outputted maps. Defaults to None.

    wmax : int, optional
        Red-side border (rightmost) of the wavelength range to generate the
        outputted maps. Defaults to None.

    Returns
    -------
    SN__yx : array
        The signal-to-noise map (:math:`NX, NY`) within [``wmin``, ``wmax``]
        wavelength range.

    mean_flux__yx : array
        The mean flux map (:math:`NX, NY`) within [``wmin``, ``wmax``]
        wavelength range.

    sigma_flux__yx : array
        The standard deviation of the flux map (:math:`NX, NY`) within [``wmin``, ``wmax``]
        wavelength range.
    '''
    if ((wmin is None) and (wmax is None)) or (wmin == wmax):
        wmin = 5589
        wmax = 5680
    wmin = wave__w[0] if wmin is None else wmin
    wmax = wave__w[-1] if wmin is None else wmax

    sel_wave__w = trim_waves(wave__w, [wmin, wmax])
    cube__wyx = org_cube__wyx[sel_wave__w, :, :]
    _, ny, nx = cube__wyx.shape

    # kernel size is 1/10 of the wavelenght window
    kernel_size = int(sel_wave__w.astype(int).sum()/10)

    # create residual cube
    res_cube__wyx = np.zeros_like(cube__wyx)
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        _data = cube__wyx[:, iy, ix]
        smoothed = median_filter(_data, size=kernel_size, mode='reflect')
        res_cube__wyx[:, iy, ix] = _data - smoothed

    # calculate signal
    mean_flux__yx = np.ma.masked_array(cube__wyx, mask=~np.isfinite(cube__wyx)).mean(axis=0)
    mean_flux__yx = mean_flux__yx.filled(0)

    # calculate noise
    sigma_flux__yx = np.ma.masked_array(res_cube__wyx, mask=~np.isfinite(res_cube__wyx)).std(axis=0)
    sigma_flux__yx[sigma_flux__yx == 0] = np.ma.masked
    sigma_flux__yx = sigma_flux__yx.filled(1)

    # calculate Signal to noise
    SN__yx = mean_flux__yx/sigma_flux__yx

    return SN__yx, mean_flux__yx, sigma_flux__yx

def get_SN_rss(org_rss__sw, wave__w, wmin=None, wmax=None):
    '''
    Generates the SN, the mean and the standard deviation maps of
    ``org_rss__sw`` within ``wmin`` and ``wmax``.

    Parameters
    ----------
    org_rss__sw : array
        The row-stacked spectra (RSS). Dimensions are :math:`(NS, NW)`, where
        NS the RSS dimension and :math:`NW` is the number of wavelengths

    wave__w : array
        The wavelengths with dimension NW.

    wmin : int, optional
        Blue-side border (leftmost) of the wavelength range to generate the
        outputted maps. Defaults to None.

    wmax : int, optional
        Red-side border (rightmost) of the wavelength range to generate the
        outputted maps. Defaults to None.

    Returns
    -------
    SN__s : array
        The signal-to-noise for the RSS within [``wmin``, ``wmax``]wavelength
        range.

    mean_flux__s : array
        The mean flux of the RSS within [``wmin``, ``wmax``] wavelength range.

    sigma_flux__s : array
        The standard deviation of the flux of the RSS within [``wmin``, ``wmax``]
        wavelength range.
    '''
    if (wmin is None) and (wmax is None) or (wmin == wmax):
        wmin = 5589
        wmax = 5680
    wmin = wave__w[0] if wmin is None else wmin
    wmax = wave__w[-1] if wmin is None else wmax

    sel_wave__w = trim_waves(wave__w, [wmin, wmax])
    rss__sw = org_rss__sw[:, sel_wave__w]
    ns, _ = rss__sw.shape

    # kernel size is 1/10 of the wavelenght window
    kernel_size = int(sel_wave__w.astype(int).sum()/10)

    # create residual cube
    res_rss__sw = np.zeros_like(rss__sw)
    for ispec in range(ns):
        _data = rss__sw[ispec, :]
        smoothed = median_filter(_data, size=kernel_size, mode='reflect')
        res_rss__sw[ispec, :] = _data - smoothed

    # calculate signal
    mean_flux__s = np.ma.masked_array(rss__sw, mask=~np.isfinite(rss__sw)).mean(axis=1)
    mean_flux__s = mean_flux__s.filled(0)

    # calculate noise
    sigma_flux__s = np.ma.masked_array(res_rss__sw, mask=~np.isfinite(res_rss__sw)).std(axis=1, ddof=1)
    sigma_flux__s[sigma_flux__s == 0] = np.ma.masked
    sigma_flux__s = sigma_flux__s.filled(1)

    # calculate Signal to noise
    SN__s = mean_flux__s/sigma_flux__s

    return SN__s, mean_flux__s, sigma_flux__s

def rss_seg2cube(rss__sw, seg__yx):
    ns, nw = rss__sw.shape
    ny, nx = seg__yx.shape

    # attribute spec to cube
    cube__wyx = np.zeros((nw, ny, nx), dtype=rss__sw.dtype)
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i > 0:
            spec_i = spec_i - 1
            cube__wyx[:, iy, ix] = rss__sw[spec_i, :]
    return cube__wyx

def img2spec_e(input_fits, index_image, output):
    # read data
    image__sw, h = get_data_from_fits(input_fits, header=True)
    image__w = image__sw[index_image]
    e_image__w = get_data_from_fits(f'e_{input_fits}')[index_image]
    wave__w = get_wave_from_header(h, wave_axis=1)

    # calculate and clean data
    image__w = np.ma.masked_array(image__w, mask=~np.isfinite(image__w))
    image__w = image__w.filled(0)
    sqrt_image__w = np.sqrt(np.abs(image__w))
    e_image__w = np.ma.masked_array(e_image__w, mask=~np.isfinite(e_image__w))
    e_image__w = e_image__w.filled(1e12)
    e_image__w = np.where(e_image__w > sqrt_image__w, sqrt_image__w, e_image__w)

    # output data
    output_spectra(wave__w, [image__w, e_image__w], output)

def clean_Ha_map(v__yx, mask__yx, max_vel, min_vel):
    ny, nx = v__yx.shape
    v_med = np.median(v__yx[mask__yx == 1])
    mask_1 = v__yx > max_vel
    #mask_2 = v__yx - v_med > 300
    mask = mask_1 #| mask_2
    lo = 6562 * (1 + v__yx[mask] / __c__)
    v__yx[mask] = ( (lo / 6583) - 1) * __c__
    mask__yx[mask] = 1
    mask = v__yx < min_vel
    mask__yx[mask] = 0
    for iyx in itertools.product(range(1, ny - 1),range(1, nx - 1)):
        iy, ix = iyx
        if mask__yx[iy, ix] == 0:
            iy0 = iy - 1
            iy1 = iy + 2
            ix0 = ix - 1
            ix1 = ix + 2
            sum_mask = mask__yx[iy0:iy1, ix0:ix1].sum()
            if sum_mask > 5:
                val = copy(v__yx[iy0:iy1, ix0:ix1])
                val[~np.isfinite(val)] = 0
                st_val = pdl_stats(val[val > 0])
                v__yx[iy, ix] = st_val[_STATS_POS['median']]
                mask__yx[iy, ix] = 1
    for iyx in itertools.product(range(1, ny - 1),range(1, nx - 1)):
        iy, ix = iyx
        if v__yx[iy, ix] == 0:
            iy0 = iy - 1
            iy1 = iy + 2
            ix0 = ix - 1
            ix1 = ix + 2
            sum_mask = mask__yx[iy0:iy1, ix0:ix1].sum()
            if sum_mask > 5:
                val = copy(v__yx[iy0:iy1, ix0:ix1])
                val[~np.isfinite(val)] = 0
                st_val = pdl_stats(val[val > 0])
                v__yx[iy, ix] = st_val[_STATS_POS['median']]
                mask__yx[iy, ix] = 1
    return v__yx, mask__yx

def clean_nan(in_file, badval):
    a_in1, h = get_data_from_fits(in_file, header=True)
    a_in1[np.isnan(a_in1)] = badval
    array_to_fits(in_file, a_in1, overwrite=True, header=h)

def create_mask_map(input_file, cut, output_file):
    a_in1, h = get_data_from_fits(input_file, header=True)
    output = (a_in1 > cut).astype(int)
    array_to_fits(output_file, output, overwrite=True, header=h)

def SN_map_seg(SN__s, seg_map__yx):
    map__yx = np.zeros_like(seg_map__yx)
    area_map__yx = np.zeros_like(seg_map__yx)
    mask = seg_map__yx != 0
    id_, sum_ = np.unique(seg_map__yx[mask], return_counts=True)
    for i, region in enumerate(id_):
        mask = seg_map__yx == region
        val_now = SN__s[i]
        sum_now = sum_[i]
        map__yx[mask] = val_now
        area_map__yx[mask] = sum_now
    norm_map__yx = map__yx / area_map__yx
    return map__yx, norm_map__yx, area_map__yx

def csv_to_map_seg(csvfile, column, seg_file_fits, map_fits):
    norm_file="norm_" + map_fits
    area_file="area_" + map_fits
    seg, h = get_data_from_fits(seg_file_fits, header=True)
    map_ = np.zeros_like(seg)
    sum_map = np.zeros_like(seg)
    print("Reading input files")
    val = np.genfromtxt(csvfile, comments="#", delimiter=",")
    val = val[:, column]
    map__yx, norm_map__yx, area_map__yx = SN_map_seg(val, seg)
    array_to_fits(map_fits, map__yx, overwrite=True, header=h)
    array_to_fits(norm_file, norm_map__yx, overwrite=True, header=h)
    array_to_fits(area_file, area_map__yx, overwrite=True, header=h)

def imarith(in1_file, operator, in2_file, out_file):
    a_in1, h = get_data_from_fits(in1_file, header=True)
    if isinstance(in2_file, str):
        a_in2 = get_data_from_fits(in2_file)
    else:
        a_in2 = in2_file
    if isinstance(a_in2, str):
        a_in2 = eval(a_in2)
    if operator == "+":
        a_in1 += a_in2
    if operator == "-":
        a_in1 -= a_in2
    if operator == "/":
        a_in1 /= a_in2
    if operator == "*":
        a_in1 *= a_in2
    array_to_fits(out_file, a_in1, overwrite=True, header=h)

# def smooth_spec_clip_cube(input, output, wavebox_width, sigma, wavepix_min, wavepix_max):
def smooth_spec_clip_cube(cube__wyx, wavebox_width, sigma, wavepix_min, wavepix_max):
    # read data
    nw, ny, nx = cube__wyx.shape

    # wavelenght pixels borders
    if wavepix_min < 1:
        wavepix_min = 1
    if wavepix_max > (nw - 2):
        wavepix_max = nw - 2

    # smooth spec
    output_data__wyx = copy(cube__wyx)
    for ix in range(nx):
        data__yw = cube__wyx[:, :, ix]
        data_slice__ys = data__yw[:, wavepix_min:wavepix_max]
        finite_data_slice = data_slice__ys[np.isfinite(data_slice__ys)]
        if finite_data_slice.any():
            data_slice_stats = pdl_stats(finite_data_slice)
            med_slice = data_slice_stats[_STATS_POS['median']]
            pRMS_slice = data_slice_stats[_STATS_POS['pRMS']]
            min_slice = data_slice_stats[_STATS_POS['min']]
            # max_slice = med_slice + sigma*pRMS_slice
            max_slice = data_slice_stats[_STATS_POS['max']]
            data_clipped__yw = np.clip(data__yw, min_slice, max_slice)
            data_smoothed__yw = median_filter(data_clipped__yw, size=(wavebox_width, 1), mode='wrap')
            output_data__wyx[:, :, ix] = data_smoothed__yw

    return output_data__wyx

def get_slice(data__wyx, wave__w, prefix, config_file):
    # read config
    names, start_w, end_w = np.loadtxt(fname=config_file, unpack=True,
                                       dtype=np.dtype([('names', 'U8'),
                                                       ('start_w', np.int),
                                                       ('end_w', np.int)]))
    ns = names.size
    print(f'{ns} slices to cut')
    print(f'Reading cube')

    # correct one slice case
    if ns == 1:
        names = [names.tolist()]
        start_w = [start_w.tolist()]
        end_w = [end_w.tolist()]

    output = {}

    # generate mean image under a defined wavelength window (a slice)
    for n, s_w, e_w in zip(names, start_w, end_w):
        k = f'{prefix}_{n}_{s_w}_{e_w}'
        output[k] = None
        if (s_w > wave__w[0]) and (e_w < wave__w[-1]):
            sel_wave__w = trim_waves(wave__w, [s_w, e_w])
            data_slice__wyx = data__wyx[sel_wave__w, :, :]
            mean__yx = data_slice__wyx.mean(axis=0)
            output[k] = mean__yx

    return output

def check_max(ix, iy, ixp, iyp, Ha_map__yx, seg_map__yx, frac_peak):
    is_max = -3
    ny, nx = Ha_map__yx.shape
    ix1 = ix - 1
    ix2 = ix + 2
    iy1 = iy - 1
    iy2 = iy + 2
    if ix1 < 0:
        ix1 = 0
        ix2 = ix1 + 3
    if ix2 > (nx - 1):
        ix2 = nx - 1
        ix1 = ix2 - 3
    if iy1 < 0:
        iy1 = 0
        iy2 = iy1 + 3
    if iy2 > (ny - 1):
        iy2 = ny - 1
        iy1 = iy2 - 3
    flux = []
    for iixy in itertools.product(range(ix1, ix2),range(iy1, iy2)):
        iix, iiy = iixy
        if (iix!=ix) and (iiy!=iy) and (iix > 0) and (iix < nx) and (iiy > 0) and (iiy < ny):
            nr = seg_map__yx[iiy, iix]
            if nr == 0:
                flux.append(Ha_map__yx[iiy, iix])
    flux = np.array(flux)
    if flux.size == 0:
        median_flux = 0
        sigma_flux = 0
    else:
        median_flux = np.median(flux)
        sigma_flux = flux.std()
    if (ix > 0) and (ix < nx) and (iy > 0) and (iy < ny):
        Ha = Ha_map__yx[iy, ix]
        Ha_peak = Ha_map__yx[iyp, ixp]
        if Ha > (frac_peak * Ha_peak):
            ncut = 2
            if (Ha - median_flux) < 0:
                is_max = -1
            if np.abs(median_flux - Ha) <= (ncut * sigma_flux):
                is_max = 0
            if Ha > median_flux:
                is_max = 1
    return is_max

def check_near(ix, iy, seg_map__yx):
    ny, nx = seg_map__yx.shape
    ix1 = ix - 1
    ix2 = ix + 2
    iy1 = iy - 1
    iy2 = iy + 2
    if ix1 < 0:
        ix1 = 0
        ix2 = ix1 + 3
    if ix2 > (nx - 1):
        ix2 = nx - 1
        ix1 = ix2 - 3
    if iy1 < 0:
        iy1 = 0
        iy2 = iy1 + 3
    if iy2 > (ny - 1):
        iy2 = ny - 1
        iy1 = iy2 - 3
    a = 0
    for iixy in itertools.product(range(ix1, ix2),range(iy1, iy2)):
        iix, iiy = iixy
        if (iix != ix) and (iiy != iy) and (iix > 0) and (iix < nx) and (iiy > 0) and (iiy < ny):
            if seg_map__yx[iiy, iix] > 0:
                a += 1
    return a

def check_point_SN(ix, iy, ixp, iyp, area,
                   Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                   Ha_peaks, NR, max_dist, min_SN, min_flux, frac_peak):
    ny, nx = Ha_map__yx.shape
    dist = np.sqrt((ix - ixp)**2 + (iy - iyp)**2)
    is_max = check_max(ix, iy, ixp, iyp, Ha_map__yx, seg_map__yx, frac_peak)
    Ha_peak_now = Ha_map__yx[iyp, ixp]
    frac_dist = 1
    if NR != 1:
        frac_dist = 0.5/((Ha_peak_now/Ha_peaks[1])**0.5)
        if frac_dist > 1:
            frac_dist = 1
    dist_max_now = max_dist/frac_dist
    if dist_max_now < 1.5:
        dist_max_now = 1.5
    is_point = 0
    if (ix > 0) and (ix < nx) and (iy > 0) and (iy < ny):
        Ha = Ha_map__yx[iy, ix]
        Ha_peak = Ha_map__yx[iyp, ixp]
        SN = SN__yx[iy, ix]
        if SN < min_SN:
            mask_map__yx[iy, ix] = 0
            seg_map__yx[iy, ix] = 0
        else:
            if (dist < max_dist) and (Ha > min_flux) and (SN > min_SN) and (Ha > (frac_peak * Ha_peak)):
                nr = seg_map__yx[iy, ix]
                if nr == 0:
                    seg_map__yx[iy, ix] = NR
                    area += 1
                    is_point = 1
                    mask_map__yx[iy, ix] = 0
    return is_point, area

def proceed_loop_SN(ixp, iyp, area, is_point,
                    tmp_Ha_map__yx, Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                    Ha_peaks, NR, flux_limit_peak, max_dist, min_SN, min_flux,
                    frac_peak):
    ny, nx = Ha_map__yx.shape
    nmax = (nx - 1)*(ny - 1)
    n_now = 0
    delta = 2
    k = 0
    sig = 0
    ix = ixp
    iy = iyp
    _ixp = ixp
    _iyp = iyp
    seg_map__yx[iy, ix] = NR
    mask_map__yx[iy, ix] = 0
    n_now = n_now + is_point
    stop = 0
    while stop == 0:
        if sig == 0:
            for iy in range(_iyp + 1, _iyp + delta):
                is_point, area = check_point_SN(ix, iy, ixp, iyp, area,
                                                Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                                                Ha_peaks, NR, max_dist, min_SN, min_flux, frac_peak)
                n_now += 1
            for ix in range(_ixp + 1, _ixp + delta):
                is_point, area = check_point_SN(ix, iy, ixp, iyp, area,
                                                Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                                                Ha_peaks, NR, max_dist, min_SN, min_flux, frac_peak)
                n_now += 1
            sig = 1
        else:
            for iy in range(_iyp - delta + 1, _iyp)[::-1]:
                is_point, area = check_point_SN(ix, iy, ixp, iyp, area,
                                                Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                                                Ha_peaks, NR, max_dist, min_SN, min_flux, frac_peak)
                n_now += 1
            for ix in range(_ixp - delta + 1, _ixp)[::-1]:
                is_point, area = check_point_SN(ix, iy, ixp, iyp, area,
                                                Ha_map__yx, seg_map__yx, mask_map__yx, SN__yx,
                                                Ha_peaks, NR, max_dist, min_SN, min_flux, frac_peak)
                n_now += 1
            sig = 0
        delta += 1
        _ixp = ix
        _iyp = iy
        dist = np.sqrt((ix - ixp)**2 + (iy - iyp)**2)
        if (ix > 0) and (ix < nx) and (iy > 0) and (iy < ny):
            Ha_now = tmp_Ha_map__yx[iy, ix]
        else:
            Ha_now = 0
        if ((dist > (1.5*max_dist)) or (Ha_now > 10*flux_limit_peak)):
            stop = 1
    return area, is_point

def nearest(ix, iy, ix_peaks, iy_peaks, NR, seg_map__yx):
    min_dist = 1e12
    for ii in range(NR):
        dist = np.sqrt((ix_peaks[ii] - ix)**2 + (iy_peaks[ii] - iy)**2)
        if dist < min_dist:
            min_dist = dist
            seg_map__yx[iy, ix] = ii

def cont_seg_all_SN(map__yx, e_map__yx, flux_limit_peak, target_SN, min_SN, frac_peak, min_flux):
    # segmentation_fits, diffuse_mask_fits):
    # signal_fits, noise_fits, flux_limit_peak, target_SN, min_SN, frac_peak,
    #                 min_flux, segmentation_fits, diffuse_mask_fits):

    # equivalent to setnantobad -> setbadtoval(val)
    map__yx[~np.isfinite(map__yx)] = -1e12
    e_map__yx[~np.isfinite(e_map__yx)] = 1e20

    # derive the radius
    SN__yx = map__yx/e_map__yx
    max_dist__yx = target_SN/SN__yx
    max_dist__yx[~np.isfinite(max_dist__yx)] = 0

    ny, nx = map__yx.shape
    seg_map__yx = np.zeros_like(map__yx)
    mask_map__yx = np.ones_like(map__yx)
    R_max_abs = 0.15 * np.sqrt(nx**2 + ny**2)

    _sel = (map__yx > 0) & (map__yx < 1e30)
    flux = np.ma.masked_array(map__yx, mask=~_sel).compressed()
    nup = flux.size
    _stats = pdl_stats(flux)
    print(f'{nup} {_stats}')

    _sel = (map__yx > 0) & (map__yx < 1e30) & (map__yx < _stats[_STATS_POS['median']])
    flux = np.ma.masked_array(map__yx, mask=~_sel).compressed()
    nul = flux.size
    _stats = pdl_stats(flux)
    print(f'{nul} {_stats}')

    stop = 0
    is_point = 0
    NR = 1
    max_dist = None
    Ha_max_dist = None
    _tmp_map__yx = map__yx
    ix_peaks = np.zeros(nx*ny)
    iy_peaks = np.zeros(nx*ny)
    Ha_peaks = np.zeros(nx*ny)
    while stop == 0:
        k = 0
        lower_lim = flux_limit_peak
        upper_lim = 1e30
        ixp = -1
        iyp = -1
        for ixy in itertools.product(range(nx),range(ny)):
            ix, iy = ixy
            Ha = _tmp_map__yx[iy, ix]
            if Ha > lower_lim:
                is_max = check_max(ix, iy, ixp, iyp, map__yx, seg_map__yx, frac_peak)
                if NR == 1:
                    is_near = 1
                else:
                    is_near = check_near(ix, iy, seg_map__yx)
                if (Ha < upper_lim) and (Ha > lower_lim) and (is_max == 1):
                    lower_lim = Ha
                    ixp = ix
                    iyp = iy

        ix_peaks[NR] = ixp
        iy_peaks[NR] = iyp
        Ha_peaks[NR] = map__yx[iyp, ixp]
        print(f'{NR},{ixp},{iyp},{NR},{Ha_max_dist},{max_dist},', end='')
        area = 1
        if (ixp == -1) and (iyp == -1):
            print('0')
            stop = 1
        else:
            Ha_max_dist = max_dist__yx[iyp, ixp]
            M = 15
            pi_R_sqr = np.pi*Ha_max_dist**2
            a = M*pi_R_sqr
            b = M + pi_R_sqr - 1
            area_factor = np.sqrt(a/b)
            max_dist = np.ceil(Ha_max_dist*area_factor/np.sqrt(np.pi))
            if max_dist < 1:
                max_dist = 1
            if max_dist > R_max_abs:
                max_dist = np.int(R_max_abs)
            area, is_point = proceed_loop_SN(ixp, iyp, area, is_point,
                                             _tmp_map__yx, map__yx, seg_map__yx, mask_map__yx, SN__yx,
                                             Ha_peaks, NR, flux_limit_peak, max_dist, min_SN, min_flux,
                                             frac_peak)
            print(f'{area}')
            _tmp_map__yx = _tmp_map__yx*mask_map__yx
            NR += 1
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        Ha = map__yx[iy, ix]
        if (Ha >= min_flux):
            mask_map__yx[iy, ix] = 0
        nr = seg_map__yx[iy, ix]
        if (nr == 0) and (Ha != -1e12):
            nearest(ix, iy, ix_peaks, iy_peaks, NR, seg_map__yx)
        if Ha == 0 or Ha < 0:
            seg_map__yx[iy, ix] = 0
    # array_to_fits(filename=segmentation_fits, arr=seg_map__yx, overwrite=True)
    # array_to_fits(filename=diffuse_mask_fits, arr=mask_map__yx, overwrite=True)
    return seg_map__yx, mask_map__yx

def check_point(ix, iy, ixp, iyp,
                Ha_map__yx, seg_map__yx, mask_map__yx,
                Ha_peaks, NR, max_dist_peak, min_flux, frac_peak):
    ny, nx = Ha_map__yx.shape
    dist = np.sqrt((ix - ixp)**2 + (iy - iyp)**2)
    is_max = check_max(ix, iy, ixp, iyp, Ha_map__yx, seg_map__yx, frac_peak)
    Ha_peak_now = Ha_map__yx[iyp, ixp]
    frac_dist = 1
    if NR != 1:
        frac_dist = 0.5/((Ha_peak_now/Ha_peaks[1])**0.5)
        if frac_dist > 1:
            frac_dist = 1
    dist_max_now = max_dist_peak/frac_dist
    if dist_max_now < 1.5:
        dist_max_now = 1.5
    is_point = 0
    if (ix > 0) and (ix < nx) and (iy > 0) and (iy < ny):
        Ha = Ha_map__yx[iy, ix]
        Ha_peak = Ha_map__yx[iyp, ixp]
        if (dist < max_dist_peak) and (Ha > min_flux) and (Ha > (frac_peak * Ha_peak)):
            nr = seg_map__yx[iy, ix]
            if nr == 0:
                seg_map__yx[iy, ix] = NR
                is_point = 1
                mask_map__yx[iy, ix] = 0
    return is_point

def proceed_loop(ixp, iyp, is_point,
                 tmp_Ha_map__yx, Ha_map__yx, seg_map__yx, mask_map__yx,
                 Ha_peaks, NR, flux_limit_peak, max_dist_peak, min_flux, frac_peak):
    ny, nx = Ha_map__yx.shape
    nmax = (nx - 1)*(ny - 1)
    n_now = 0
    delta = 2
    k = 0
    sig = 0
    ix = ixp
    iy = iyp
    _ixp = ixp
    _iyp = iyp
    seg_map__yx[iy, ix] = NR
    mask_map__yx[iy, ix] = 0
    n_now = n_now + is_point
    stop = 0
    while stop == 0:
        if sig == 0:
            for iy in range(_iyp + 1, _iyp + delta):
                is_point = check_point(ix, iy, ixp, iyp,
                                       Ha_map__yx, seg_map__yx, mask_map__yx,
                                       Ha_peaks, NR, max_dist_peak, min_flux, frac_peak)
                n_now += 1
            for ix in range(_ixp + 1, _ixp + delta):
                is_point = check_point(ix, iy, ixp, iyp,
                                       Ha_map__yx, seg_map__yx, mask_map__yx,
                                       Ha_peaks, NR, max_dist_peak, min_flux, frac_peak)
                n_now += 1
            sig = 1
        else:
            for iy in range(_iyp - delta + 1, _iyp)[::-1]:
                is_point = check_point(ix, iy, ixp, iyp,
                                       Ha_map__yx, seg_map__yx, mask_map__yx,
                                       Ha_peaks, NR, max_dist_peak, min_flux, frac_peak)
                n_now += 1
            for ix in range(_ixp - delta + 1, _ixp)[::-1]:
                is_point = check_point(ix, iy, ixp, iyp,
                                       Ha_map__yx, seg_map__yx, mask_map__yx,
                                       Ha_peaks, NR, max_dist_peak, min_flux, frac_peak)
                n_now += 1
            sig = 0
        delta += 1
        _ixp = ix
        _iyp = iy
        dist = np.sqrt((ix - ixp)**2 + (iy - iyp)**2)
        if (ix > 0) and (ix < nx) and (iy > 0) and (iy < ny):
            Ha_now = tmp_Ha_map__yx[iy, ix]
        else:
            Ha_now = 0
        if ((dist > (1.5*max_dist_peak)) or (Ha_now > 10*flux_limit_peak)):
            stop = 1
    return is_point

def cont_seg_all(signal_fits, flux_limit_peak, max_dist_peak, frac_peak,
                    min_flux, segmentation_fits, diffuse_mask_fits):
    Ha_map__yx, h_Ha = get_data_from_fits(signal_fits, header=True)

    # equivalent to setnantobad -> setbadtoval(val)
    Ha_map__yx[~np.isfinite(Ha_map__yx)] = -1e12

    ny, nx = Ha_map__yx.shape
    seg_map__yx = np.zeros_like(Ha_map__yx)
    mask_map__yx = np.ones_like(Ha_map__yx)

    _sel = (Ha_map__yx > 0) & (Ha_map__yx < 1e30)
    flux = np.ma.masked_array(Ha_map__yx, mask=~_sel).compressed()
    nup = flux.size
    _stats = pdl_stats(flux)
    print(f'{nup} {_stats}')

    _sel = (Ha_map__yx > 0) & (Ha_map__yx < 1e30) & (Ha_map__yx < _stats[_STATS_POS['median']])
    flux = np.ma.masked_array(Ha_map__yx, mask=~_sel).compressed()
    nul = flux.size
    _stats = pdl_stats(flux)
    print(f'{nul} {_stats}')

    ix_peaks = np.zeros(nx*ny)
    iy_peaks = np.zeros(nx*ny)
    Ha_peaks = np.zeros(nx*ny)

    _tmp_map__yx = Ha_map__yx
    is_point = 0
    stop = 0
    NR = 1
    while stop == 0:
        k = 0
        lower_lim = flux_limit_peak
        upper_lim = 1e30
        ixp = -1
        iyp = -1
        for ixy in itertools.product(range(nx),range(ny)):
            ix, iy = ixy
            Ha = _tmp_map__yx[iy, ix]
            if Ha > lower_lim:
                is_max = check_max(ix, iy, ixp, iyp, Ha_map__yx, seg_map__yx, frac_peak)
                if NR == 1:
                    is_near = 1
                else:
                    is_near = check_near(ix, iy, seg_map__yx)
                if (Ha < upper_lim) and (Ha > lower_lim) and (is_max == 1):
                    lower_lim = Ha
                    ixp = ix
                    iyp = iy

        ix_peaks[NR] = ixp
        iy_peaks[NR] = iyp
        Ha_peaks[NR] = Ha_map__yx[iyp, ixp]
        print(f'ip,jp {ixp},{iyp} {NR}')
        area = 1
        if (ixp == -1) and (iyp == -1):
            stop = 1
        else:
            is_point = proceed_loop(ixp, iyp, is_point,
                                    _tmp_map__yx, Ha_map__yx, seg_map__yx, mask_map__yx, Ha_peaks,
                                    NR, flux_limit_peak, max_dist_peak, min_flux, frac_peak)
            _tmp_map__yx = _tmp_map__yx*mask_map__yx
            NR += 1
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        Ha = Ha_map__yx[iy, ix]
        if (Ha >= min_flux):
            mask_map__yx[iy, ix] = 0
        nr = seg_map__yx[iy, ix]
        if (nr == 0) and (Ha != -1e12):
            nearest(ix, iy, ix_peaks, iy_peaks, NR, seg_map__yx)
        # if Ha == 0 or Ha < 0:
        #     seg_map__yx[iy, ix] = 0
    array_to_fits(filename=segmentation_fits, arr=seg_map__yx, overwrite=True)
    array_to_fits(filename=diffuse_mask_fits, arr=mask_map__yx, overwrite=True)

def flux_elines_cube_EW(flux__wyx, input_header, n_MC, elines_list, vel__yx, sigma__yx,
                        eflux__wyx=None, flux_ssp__wyx=None):
    nw, ny, nx = flux__wyx.shape
    crpix = input_header['CRPIX3']
    crval = input_header['CRVAL3']
    cdelt = input_header['CDELT3']
    flux__wyx[np.isnan(flux__wyx)] = 0
    if eflux__wyx is not None:
        median_data = np.nanmedian(eflux__wyx)
        np.clip(eflux__wyx, -5*median_data, 5*median_data, out=eflux__wyx)
        eflux__wyx[np.isnan(eflux__wyx)] = 5*median_data
    else:
        eflux__wyx = np.zeros_like(flux__wyx)
    if flux_ssp__wyx is not None:
        mean_data = np.nanmean(flux_ssp__wyx)
        flux_ssp__wyx[np.isnan(flux_ssp__wyx)] = mean_data
    ny1, nx1 = vel__yx.shape
    if not isinstance(sigma__yx, np.ndarray):
        sigma__yx = sigma__yx*np.ones([ny1, nx1])
    if nx1 < nx:
        nx = nx1
    if ny1 < ny:
        ny = ny1
    wavelengths = np.array([])
    name_elines = np.array([])
    ne = 0
    with open(elines_list) as fp:
        line = fp.readline()
        while line:
            if not line.startswith('#'):
                tmp_line = line.strip().split()
                if len(tmp_line) > 1:
                    wavelengths = np.append(wavelengths, float(tmp_line[0]))
                    name_elines = np.append(name_elines, tmp_line[1])
                else:
                    wavelengths = np.append(wavelengths, 0)
                    name_elines = np.append(name_elines, ' ')
                ne += 1
            line = fp.readline()
    NZ_out = ne * 4 * 2
    out = np.zeros([NZ_out, ny, nx])
    print('{} emission lines'.format(ne))
    labels = ['flux', 'vel', 'disp', 'EW','e_flux', 'e_vel', 'e_disp', 'e_EW']
    for i, name in enumerate(name_elines):
        _tmp = [i, i + ne, i + 2*ne, i + 3*ne, i + 4*ne, i + 5*ne, i + 6*ne, i + 7*ne]
        for j, I in enumerate(_tmp):
            header_label = 'NAME{}'.format(I)
            wavelen_label = 'WAVE{}'.format(I)
            units_label = 'UNIT{}'.format(I)
            if ('vel'==labels[j]) | ('e_vel'==labels[j]):
                units = 'km/s'
            if ('disp'==labels[j]) | ('e_disp'==labels[j]):
                units = 'km/s'
            if ('flux'==labels[j]) | ('e_flux'==labels[j]):
                units = '10^-16 erg/s/cm^2'
            if ('EW'==labels[j]) | ('e_EW'==labels[j]):
                units = 'Angstrom'
            input_header[header_label] = '{} {}'.format(labels[j], name)
            input_header[wavelen_label] = '{}'.format(wavelengths[i])
            input_header[units_label] = "{}".format(units)
    for k in np.arange(0, ne):
        f_m = 1 + vel__yx / __c__
        start_w_m = wavelengths[k]*f_m - 1.5*__sigma_to_FWHM__*sigma__yx
        end_w_m = wavelengths[k]*f_m + 1.5*__sigma_to_FWHM__*sigma__yx
        start_i_m = ((start_w_m - crval)/cdelt).astype(int)
        end_i_m = ((end_w_m - crval)/cdelt).astype(int)
        d_w_m = (end_w_m - start_w_m)/4
        start_i_lim_m = ((start_w_m - crval - 60)/cdelt).astype(int)
        end_i_lim_m = ((end_w_m - crval + 60)/cdelt).astype(int)
        mask1 = (start_i_m < 0) | (end_i_m < 0)
        mask2 = (start_i_m >= nw - 1) | (end_i_m >= nw - 1)
        mask3 = (start_i_lim_m >= nw - 1) | (end_i_lim_m >= nw - 1)
        sigma_mask = sigma__yx > 0
        mask = (~(mask1 | mask2 | mask3)) & sigma_mask
        j_m, i_m = np.where(mask)
        for i, j in zip(i_m, j_m):
            I0, vel_I1, I2, EW, s_I0, s_vel_I1, s_I2, e_EW = momana_spec_wave(
                gas_flux__w=flux__wyx[:, j, i],
                egas_flux__w=eflux__wyx[:, j, i],
                wave=wavelengths[k],
                vel=vel__yx[j, i],
                sigma=sigma__yx[j, i],
                crval=crval, cdelt=cdelt,
                n_MC=n_MC, flux_ssp__w=flux_ssp__wyx[:, j, i],
            )
            out[k, j, i] = I0
            out[ne + k, j, i] = vel_I1
            out[2*ne + k, j, i] = I2
            out[3*ne + k, j, i] = EW
            out[4*ne + k, j, i] = s_I0
            out[5*ne + k, j, i] = s_vel_I1
            out[6*ne + k, j, i] = s_I2
            out[7*ne + k, j, i] = e_EW
        print('{}/{}, {},{} DONE'.format(k + 1, ne, wavelengths[k], name_elines[k]))
    return out, input_header

def momana_spec_wave(gas_flux__w, wave, vel, sigma, crval, cdelt,
                     n_MC=10, egas_flux__w=None, flux_ssp__w=None):
    """
    It will proceed the moment analysis of emission line centered at `wave`.
    The parameters `crval` and `cdelt` are required in order to generate
    wavelength interval to proceed the analysis.

    ::

        NW = len(gas_flux__w)
        wavelengths = crval + cdelt*[0, 1, ..., NW],


    *TODO*: create wavelength intervals withoud crval and cdelt, i.e., set intervals using `wave` and a defined interval in Angstroms.

    Parameters
    ----------
    gas_flux__w : array like
        Gas spectrum.

    wave : float
        Emission line central wavelength to be analyzed.

    vel : float
        Ha velocity

    sigma : float
        Ha sigma.

    crval : float
        The wavelength attributed to the flux at position 0.

    cdelt : float
        The step which the wavelengths varies.

    n_MC : int, optional
        Number of Monte-Carlo iterations. Defaults to 10.

    egas_flux__w : array like or None
        Error in `gas_flux__w` used to randomize the gas flux value at each MC
        iteration. If None the gas flux value is not randomized. Defaults to None.

    flux_ssp__w : array like or None
        Stellar population spectrum used to the EW computation. If None, the EW
        will be 0. Defaults to None.

    Returns
    -------
    array like :
        The result of the moment analysis of emission line centered in `wave`.
        ::

            [
                integrated flux [10^-16 erg/s/cm^2],
                velocity [km/s],
                dispersion [km/s],
                equivalent width [Angstroms],
                sigma(integrated flux),
                sigma(velocity),
                sigma(dispersion),
                sigma(equivalent width),
            ]
    """
    flux_ssp__w = np.zeros_like(gas_flux__w) if flux_ssp__w is None else flux_ssp__w
    egas_flux__w = np.zeros_like(gas_flux__w) if egas_flux__w is None else egas_flux__w

    nw = gas_flux__w.size
    a_I0 = np.zeros(n_MC)
    a_I1 = np.zeros(n_MC)
    a_I2 = np.zeros(n_MC)
    a_I2_new = np.zeros(n_MC)
    a_vel_I1 = np.zeros(n_MC)
    s_I0 = 0
    s_I1 = 0
    s_I2 = 0
    s_vel_I1 = 0
    for i_mc in np.arange(0, n_MC):
        I0 = 0
        I1 = 0
        I2 = 0
        I2_new = 0
        vel_I1 = 0
        f = 1 + vel/__c__
        start_w = wave*f - 1.5*__sigma_to_FWHM__*sigma
        end_w = wave*f + 1.5*__sigma_to_FWHM__*sigma
        start_i = int((start_w - crval) / cdelt)
        end_i = int((end_w - crval) / cdelt)
        d_w = (end_w - start_w) / 4
        if start_i < 0:
            start_i = 0
        if start_i >= nw:
            start_i = nw - 1
        if end_i < 0:
            end_i = 0
        if end_i >= nw:
            end_i = nw - 1
        if i_mc == 0:
            rnd_a = np.zeros(end_i - start_i + 1)
        else:
            rnd_a = 0.5 - np.random.uniform(size=(end_i - start_i + 1))
        n_I0 = 0
        s_WE = 0
        sum_val = 0
        sum_val_abs = 0
        for iz in np.arange(start_i, end_i):
            val = gas_flux__w[iz]
            e_val = egas_flux__w[iz]
            val = val + rnd_a[n_I0]*e_val
            val = val*np.abs(sigma)*np.sqrt(2*np.pi)
            w = crval + iz*cdelt
            WE = np.exp(-0.5*((w - wave*f)/sigma)**2)
            I0 = I0 + WE*val*np.exp(0.5*((w - wave*f)/sigma)**2)
            I1 = I1 + np.abs(val)*w
            s_WE = s_WE + WE
            sum_val_abs = sum_val_abs + np.abs(val)
            sum_val = sum_val + val
            n_I0 += 1
        if n_I0 != 0:
            s_WE /= n_I0
            I0 = I0/n_I0/s_WE
            if sum_val_abs != 0:
                I1 = I1/sum_val_abs
                if (I1 != 0) & (I0 != 0):
                    vel_I1 = (I1/wave - 1)*__c__
                s_WE = 0
                for iz in np.arange(start_i, end_i):
                    val = gas_flux__w[iz]
                    val = val*np.abs(sigma)*np.sqrt(2*np.pi)
                    f1 = (1 + vel_I1/__c__)
                    if (I0 > 0) & (val > 0) & (I0 > val):
                        S_now = (w - wave*f1)/(np.sqrt(2*(np.log(I0) - np.log(val))))
                        if S_now > 0:
                            WE = val/I0
                            I2 = I2 + S_now*WE
                            s_WE = s_WE + WE
                            n_I0 += 1
                if s_WE > 0:
                    I2 = I2/s_WE/__sigma_to_FWHM__
                else:
                    I2 = sigma
                n_I0 = 0
                I2_new = 0
                sum_val_abs = 0
                for iz in np.arange(start_i, end_i):
                    w = crval + iz*cdelt
                    val = gas_flux__w[iz]
                    val = val + rnd_a[n_I0]*e_val*0.5
                    WE1 = np.exp(-0.5*((w - wave*f1)/sigma)**2)
                    if (I0 > 0) & (val > 0):
                        I2_new += np.abs(val)*(w - (wave * f1))**2*WE1
                        sum_val_abs += np.abs(val)*WE1
                    n_I0 += 1
                if sum_val_abs > 0:
                    I2_new = I2_new/sum_val_abs
                else:
                    I2_new = sigma
        a_I0[i_mc] = I0
        a_I1[i_mc] = I1
        a_I2[i_mc] = I2
        a_I2_new[i_mc] = I2_new
        a_vel_I1[i_mc] = vel_I1
    if n_MC > 1:
        I0 = np.mean(a_I0)
        I1 = np.mean(a_I1)
        I2 = np.sqrt(2)*__sigma_to_FWHM__*np.sqrt(np.abs(np.median(a_I2_new)))
        vel_I1 = np.mean(a_vel_I1)
        s_I0 = __sigma_to_FWHM__*np.std(a_I0, ddof=1)
        s_I1 = __sigma_to_FWHM__*np.std(a_I1, ddof=1)
        s_I2 = np.sqrt(std_m(a_I2_new))
        s_vel_I1 = np.std(a_vel_I1, ddof=1)
    else:
        I0 = a_I0[0]
        I1 = a_I1[0]
        I2 = a_I2[0]
        vel_I1 = a_vel_I1[0]
        s_I0 = 0
        s_I1 = 0
        s_I2 = 0
        s_vel_I1 = 0;
    s_I0 = np.abs(s_I0)
    s_I1 = np.abs(s_I1)
    s_I2 = np.abs(s_I2)
    s_vel_I1 = np.abs(s_vel_I1)
    #
    # Continuum error
    #
    start_i_0 = int((start_w -60 - crval) / cdelt)
    end_i_0 = int((start_w -30 - crval) / cdelt)
    start_i_1 = int((end_w + 30 - crval)/ cdelt)
    end_i_1 = int((end_w + 60 - crval) / cdelt)

    if start_i_0 < 0:
        start_i_0 = 0
    if start_i_1 < 0:
        start_i_1 = 0
    if end_i_0 >= nw:
        end_i_0 = nw - 4
    if end_i_1 >= nw:
        end_i_1 = nw - 1
    cont_0 = gas_flux__w[start_i_0:end_i_0]
    cont_1 = gas_flux__w[start_i_1:end_i_1]
    mean_0 = np.mean(cont_0)
    mean_1 = np.mean(cont_1)
    std_0 = np.std(cont_0, ddof=1)
    std_1 = np.std(cont_1, ddof=1)
    val_cont = 0.5*(mean_0 + mean_1)
    e_val_cont = np.sqrt((std_0**2 + std_1**2)/2)
    s_I0 = np.sqrt(s_I0**2 + (e_val_cont*I2)**2)
    s_I2 = np.sqrt(s_I2**2 + (e_val_cont/I2) **2 + (0.1*I2)**2)
    s_vel_I1 = np.sqrt(s_vel_I1**2 + (e_val_cont*(s_I2/5500)*__c__)**2 + ((0.02*I2/wave)*__c__)**2)
    #
    # EW
    #
    start_i_0 = int((start_w - 60 - crval)/cdelt)
    end_i_0 = int((start_w - 30 - crval)/cdelt)
    start_i_1 = int((end_w + 30 - crval)/cdelt)
    end_i_1 = int((end_w + 60 - crval)/cdelt)
    if start_i_0 < 0:
        start_i_0 = 0
    if start_i_1 < 0:
        start_i_1 = 0
    if end_i_0 > nw - 1:
        end_i_0 = nw - 1
    if end_i_1 > nw - 1:
        end_i_1 = nw - 1
    cont_0 = flux_ssp__w[start_i_0:end_i_0]
    cont_1 = flux_ssp__w[start_i_1:end_i_1]
    mean_0 = np.mean(cont_0)
    mean_1 = np.mean(cont_1)
    std_0 = np.std(cont_0, ddof=1)
    std_1 = np.std(cont_1, ddof=1)
    val_cont = 0.5*(mean_0 + mean_1)
    e_val_cont = np.sqrt((std_0**2 + std_1**2)/2)
    if val_cont != 0:
        EW = -1*I0/np.abs(val_cont)
        e_EW = np.abs(s_I0)/np.abs(val_cont) + (I0*np.abs(e_val_cont))/(val_cont**2)
        if np.abs(EW) < e_EW:
            EW = 0
        if EW > 0:
            EW = 0
    else:
        EW = np.nan
        e_EW = np.nan
    return I0, vel_I1, I2, EW, s_I0, s_vel_I1, s_I2, e_EW

def med2df(input_fits, output_fits, x_width, y_width):
    # read data
    image__yx = get_data_from_fits(input_fits)
    # 2D median filter
    # XXX: The median_filter produces a different result from perl med2df()
    #      when x_width or y_width are pairs
    filt_image__yx = median_filter(image__yx, size=(y_width, x_width), mode='reflect')
    array_to_fits(output_fits, arr=filt_image__yx, overwrite=True)

def read_img_header(input_fits, header_cards, filename=None):
    clf = False
    if filename is not None:
        if isinstance(filename, io.TextIOWrapper):
            f = filename
        else:
            clf = True
            f = open(filename, 'w')
    else:
        f = sys.stdout
    # read data
    _, h = get_data_from_fits(input_fits, header=True)
    print(f'{input_fits}', end=' ', file=f)
    for card in header_cards:
        _tmp = h.get(card)
        if _tmp is not None:
            print(f'{_tmp}', end=' ', file=f)
    print(f'', end='\n', file=f)
    if clf:
        f.close()

def get_Ha(input_fits, redshift, output_fits):
    output_cont_fits = f'cont.{output_fits}'
    output_EW_fits = f'EW.{output_fits}'

    # Ha window
    Ha_wl = 6562
    range_boxes = np.array([0, -100, 100])
    _tmp = np.array([Ha_wl]*3) + range_boxes
    start_w = (_tmp - 30)*(1 + redshift)
    end_w = (_tmp + 30)*(1 + redshift)
    ns = len(range_boxes)
    print(f'{ns} slices to cut')
    print(f'Reading cube')

    # read cube
    data__wyx, h = get_data_from_fits(input_fits, header=True)
    wave__w = get_wave_from_header(h, wave_axis=3)
    nw, ny, nx = data__wyx.shape
    crval = h['CRVAL3']
    cdelt = h['CDELT3']

    map = np.ndarray((ns, ny, nx), dtype='float64')
    map_med = np.ndarray((ns, ny, nx), dtype='float64')
    for i, msk in enumerate(zip(start_w, end_w)):
        i_st = int((msk[0]-crval)/cdelt)
        i_en = int((msk[1]-crval)/cdelt)+1
        if (i_st > 0) and (i_en < nw):
            mean_Ha__yx = data__wyx[i_st:i_en].mean(axis=0)
            median_Ha__yx = np.median(data__wyx[i_st:i_en], axis=0)
            map[i] = mean_Ha__yx*(msk[1] - msk[0])
            map_med[i] = median_Ha__yx*(msk[1] - msk[0])
        else:
            print(f'get_Ha: [{msk[0]}:{msk[1]}]: start index={i_st} end_index={i_en} n_wave={nw}: slice out of range')
    map_cont__yx = 0.5*(map_med[1] + map_med[2])
    map_Ha__yx = map[0] - map_cont__yx
    map_EW_Ha__yx = map_Ha__yx/(map_cont__yx/(start_w[0] - end_w[0]))
    map_Ha__yx[~np.isfinite(map_Ha__yx)] = 0
    map_cont__yx[~np.isfinite(map_cont__yx)] = 0
    map_EW_Ha__yx[~np.isfinite(map_EW_Ha__yx)] = 0

    h['NAXIS'] = 2
    h.pop('NAXIS3')
    array_to_fits(filename=output_fits, arr=map_Ha__yx, header=h, overwrite=True)
    array_to_fits(filename=output_cont_fits, arr=map_cont__yx, header=h, overwrite=True)
    array_to_fits(filename=output_EW_fits, arr=map_EW_Ha__yx, header=h, overwrite=True)

def spec_extract_cube(input_fits, segmentation_fits, output_rss_fits, diffuse_output=None):
    if diffuse_output is None:
        diffuse_output = 'diffuse.fits'
    # read cube
    data__wyx, h = get_data_from_fits(input_fits, header=True)
    wave__w = get_wave_from_header(h, wave_axis=3)
    crval = h['CRVAL3']
    cdelt = h['CDELT3']
    crpix = h['CRPIX3']
    nw, ny, nx = data__wyx.shape

    # read segmentation
    seg__yx = get_data_from_fits(segmentation_fits)
    nys, nxs = seg__yx.shape

    if (nx > nxs) or (ny > nys):
        print(f'spec_extract_cube: Dimensions does not match ({nx},{ny}) != ({nxs},{nys})')
        # XXX: deal function returns in all tools
        sys.exit()

    inv_seg__yx = np.zeros_like(seg__yx)
    ns = seg__yx.max().astype('int')

    if ns > 0:
        out_data__sw = np.zeros((ns, nw))
        x = np.zeros(ns, dtype='int')
        y = np.zeros(ns, dtype='int')
        npt = np.zeros(ns, dtype='int')
        for ixy in itertools.product(range(nx),range(ny)):
            ix, iy = ixy
            spec_i = int(seg__yx[iy, ix])
            if spec_i == 0:
                inv_seg__yx[iy, ix] = 1
            spec_i_out = spec_i - 1
            data__w = data__wyx[:, iy, ix]
            data__w[~np.isfinite(data__w)] = 0
            out_data__sw[spec_i_out] += data__w
            if spec_i_out >= 0:
                x[spec_i_out] += ix
                y[spec_i_out] += iy
                npt[spec_i_out] += 1
                # print(f'{ix},{iy},{x[spec_i_out]},{y[spec_i_out]},{spec_i_out}')

        print(f'ONE = {x[1]},{y[1]}')

        # write output rss fits
        array_to_fits(output_rss_fits, out_data__sw, overwrite=True)
        write_img_header(output_rss_fits, f'CRVAL1', crval)
        write_img_header(output_rss_fits, f'CDELT1', cdelt)
        write_img_header(output_rss_fits, f'CRPIX1', crpix)
        array_to_fits(diffuse_output, inv_seg__yx, overwrite=True)

    size = np.sqrt(nx**2+ny**2)/(2*ns)
    output_rss_txt = output_rss_fits.replace('fits', 'pt.txt')
    with open(output_rss_txt, 'w') as f:
        output_header = f'C {size} {size} 0'
        print(output_header, file=f)
        # output_header = f'(1) id\n(2) S/N\n(3) Signal\n(4) Noise'
        np.savetxt(f, list(zip(list(range(ns)), x/npt, y/npt, [1]*ns)),
                   fmt=['%d'] + 2*['%.18g'] + ['%d'], delimiter=' ')
    print(f'{output_rss_fits} and {output_rss_txt} created')

# def spec_extract_cube_error(input_fits, segmentation_fits, output_rss_fits, diffuse_output=None):
def spec_extract_cube_error(error__wyx, seg__yx, badpix__wyx=None, fov_selection__yx=None):
    nw, ny, nx = error__wyx.shape
    inv_seg__yx = np.zeros_like(seg__yx)
    ns = seg__yx.max().astype('int')

    # XXX EADL: 2021-04-26 badpix mask add
    if badpix__wyx is None:
        badpix__wyx = np.zeros_like(error__wyx, dtype='bool')
    if fov_selection__yx is None:
        # Select all FoV
        fov_selection__yx = np.ones((ny, nx), dtype='bool')
    # masking pixels from not selected spaxels
    badpix__wyx[:, ~fov_selection__yx] = True

    # median_error = np.median(error__wyx)
    median_error = np.median(error__wyx[badpix__wyx == False])

    h_lim = 10*median_error
    l_lim = 0.001*median_error
    error__wyx = np.clip(error__wyx, l_lim, h_lim)
    # from error to variance
    var__wyx = error__wyx**2

    # XXX EADL: 2021-04-26 badpix mask add
    var__wyx[badpix__wyx] = 0

    # if ns > 0:
    out_data__sw = np.zeros((ns, nw))
    x = np.zeros(ns, dtype='int')
    y = np.zeros(ns, dtype='int')
    npt = np.zeros(ns, dtype='int')
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i == 0:
            inv_seg__yx[iy, ix] = 1
        spec_i_out = spec_i - 1
        var__w = var__wyx[:, iy, ix]
        var__w[~np.isfinite(var__w)] = 0
        out_data__sw[spec_i_out] += var__w
        if spec_i_out >= 0:
            x[spec_i_out] += ix
            y[spec_i_out] += iy
            npt[spec_i_out] += 1
            # print(f'{ix},{iy},{x[spec_i_out]},{y[spec_i_out]},{spec_i_out}')
    for i in range(ns):
        print(f'{i} {npt[i]}')
        out_data__sw[i] = out_data__sw[i]/npt[i]

    out_data__sw = np.sqrt(np.abs(out_data__sw)/10)

    return out_data__sw, inv_seg__yx, x, y, npt

# def spec_extract_cube_mean(input_fits, segmentation_fits, output_rss_fits, diffuse_output=None):
def spec_extract_cube_mean(data__wyx, seg__yx, badpix__wyx=None):
    nw, ny, nx = data__wyx.shape
    inv_seg__yx = np.zeros_like(seg__yx)
    ns = seg__yx.max().astype('int')

    # XXX EADL: 2021-04-26 badpix mask add
    if badpix__wyx is None:
        badpix__wyx = np.zeros_like(data__wyx, dtype='bool')
    data__wyx[badpix__wyx] = 0

    # if ns > 0:
    out_data__sw = np.zeros((ns, nw))
    x = np.zeros(ns, dtype='int')
    y = np.zeros(ns, dtype='int')
    npt = np.zeros(ns, dtype='int')
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i == 0:
            inv_seg__yx[iy, ix] = 1
        spec_i_out = spec_i - 1
        data__w = data__wyx[:, iy, ix]
        data__w[~np.isfinite(data__w)] = 0
        out_data__sw[spec_i_out] += data__w
        if spec_i_out >= 0:
            x[spec_i_out] += ix
            y[spec_i_out] += iy
            npt[spec_i_out] += 1
            # print(f'{ix},{iy},{x[spec_i_out]},{y[spec_i_out]},{spec_i_out}')

    for i in range(ns):
        print(f'{i} {npt[i]}')
        out_data__sw[i] = out_data__sw[i]/npt[i]

    return out_data__sw, inv_seg__yx, x, y, npt

def spec_extract_diffuse(input_fits, Ha_map_fits, segmentation_diffuse_fits,
                         output_rss_fits, lower_limit=None):
    if lower_limit is None:
        lower_limit = 0

    output_rss_spec = output_rss_fits.replace('fits', 'spec').replace('.gz', '')

    # read cube
    data__wyx, h = get_data_from_fits(input_fits, header=True)
    wave__w = get_wave_from_header(h, wave_axis=3)
    crval = h['CRVAL3']
    cdelt = h['CDELT3']
    crpix = h['CRPIX3']
    nw, ny, nx = data__wyx.shape

    # read Ha
    Ha__yx = get_data_from_fits(Ha_map_fits)
    nyHa, nxHa = Ha__yx.shape

    # read segmentation
    seg__yx = get_data_from_fits(segmentation_diffuse_fits)
    seg_out__yx = np.zeros_like(seg__yx)
    nys, nxs = seg__yx.shape

    if (nxs != nxHa) or (nys != nyHa):
        print(f'spec_extract_diffuse: Dimensions does not match ({nxHa},{nyHa}) != ({nxs},{nys})')
        # XXX: deal function returns in all tools
        _tmp_Ha__yx = seg__yx - seg__yx
        if (nxHa < nxs) or (nyHa < nys):
            Ha__yx = _tmp_Ha__yx[0:nyHa, 0:nxHa]

    _tmp_Ha__yx = Ha__yx * seg__yx

    if (nx > nxs) or (ny > nys):
        print(f'spec_extract_diffuse: Dimensions does not match ({nx},{ny}) != ({nxs},{nys})')
        # XXX: deal function returns in all tools
        # sys.exit()

    ns = 3
    out_data__sw = np.zeros((ns, nw))
    array_to_fits('test.int.fits', _tmp_Ha__yx, overwrite=True)

    F = _tmp_Ha__yx[_tmp_Ha__yx > lower_limit]
    med = F.mean()
    sig = F.std()
    if med < sig:
        sig = 0.95*med

    K = np.zeros(ns, dtype='int')
    x = np.zeros(ns, dtype='int')
    y = np.zeros(ns, dtype='int')
    npt = np.zeros(ns, dtype='int')
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        Ha = _tmp_Ha__yx[iy, ix]
        spec_i_out = -1
        if (Ha > lower_limit) and (Ha < (med - 0.5*sig)):
            spec_i_out = 0
            seg_out__yx[iy, ix] = 1
            K[0] += 1
        if (abs(Ha - med)<=(0.5*sig)):
            spec_i_out = 1
            seg_out__yx[iy, ix] = 2
            K[1] += 1
        if (Ha > (med + 0.5*sig)):
            spec_i_out = 2
            seg_out__yx[iy, ix] = 3
            K[2] += 1
        if spec_i_out >= 0:
            data__w = data__wyx[:, iy, ix]
            data__w[~np.isfinite(data__w)] = 0
            out_data__sw[spec_i_out] += data__w
            x[spec_i_out] += ix
            y[spec_i_out] += iy
            npt[spec_i_out] += 1
            # print(f'{ix},{iy},{x[spec_i_out]},{y[spec_i_out]},{spec_i_out}')

    # write output rss fits
    array_to_fits(output_rss_fits, out_data__sw, overwrite=True)
    write_img_header(output_rss_fits, f'CRVAL1', crval)
    write_img_header(output_rss_fits, f'CDELT1', cdelt)
    write_img_header(output_rss_fits, f'CRPIX1', crpix)
    print(f'{output_rss_fits} created')

    print(f'{F.size} diffuse points')
    print(f'med = {med}')
    print(f'sig = {sig}')
    print(f'{K[0]} F<med-sig')
    print(f'{K[1]} abs(F-med)<=sig')
    print(f'{K[2]} F>med-sig')
    out_data_sum__w = out_data__sw.sum(axis=0)
    with open(output_rss_spec, 'w') as f:
        np.savetxt(f, list(zip(list(range(1,nw+1)), wave__w, out_data_sum__w)),
                   fmt=['%d']*2 + ['%.18g'], delimiter=' ')

    out_diffuse_fits = f'seg.{segmentation_diffuse_fits}'
    array_to_fits(out_diffuse_fits, seg_out__yx, overwrite=True)

def correct_vel_map_cube_rot(input_fits, velocity_map_fits, output_fits, final_velocity=None):
    if final_velocity is None:
        final_velocity = 0

    # read cube
    data__wyx, h = get_data_from_fits(input_fits, header=True)
    wave__w = get_wave_from_header(h, wave_axis=3)
    crval = h['CRVAL3']
    cdelt = h['CDELT3']
    crpix = h['CRPIX3']
    nw, ny, nx = data__wyx.shape
    out_data__wyx = np.zeros_like(data__wyx)

    # read velocity map
    v_map__yx = get_data_from_fits(velocity_map_fits)
    nyv, nxv = v_map__yx.shape

    if (nx > nxv) or (ny > nyv):
        _msg = f'Cube Dimensions ({nx},{ny},{nw}) does not match'
        _msg += f' with vel-map dimensions ({nxv},{nyv})'
        print(f'correct_vel_map_cube_rot: {_msg}')
        # XXX: deal function returns in all tools
        sys.exit()

    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec__w = data__wyx[:, iy, ix]
        v = v_map__yx[iy, ix]
        v -= final_velocity
        new_wave__w = wave__w*(1 + v/__c__)
        spec__w[~np.isfinite(spec__w)] = 0
        f = interp1d(wave__w, spec__w, bounds_error=False, fill_value='extrapolate')
        out_data__wyx[:, iy, ix] = f(new_wave__w)
        # out_data__wyx[:, iy, ix] = np.interp(new_wave__w, wave__w, spec__w)
        print('.', end = '')
    print('', end = '\n')

    array_to_fits(output_fits, out_data__wyx, overwrite=True, header=h)

def read_coeffs_CS(filename):
    """ Reads the output coefficients file of the AutoSSP RSS run and
    returns a dictionary with each output as a key. The dimensions of
    each array stored in the dictionay has shape (NC, NS), where NC is
    the number max of coefficients and NS is the number of spectra.

    Parameters
    ----------
    filename: str
        The coefficients output filename from AutoSSP RSS run.

    Returns
    -------
    dict:
        keys:
            shape          : a tuple with NC, NS
            age__cs        : ages
            met__cs        : metallicities
            coeffs__cs     : coefficients
            norm__cs       : normalized coefficients
            e_norm__cs     : error in normalized coefficients
            ml__cs         : mass-to-light
            Av__cs         : dust extinction parameters A_V
            coeff_mass__cs : coeffs*10**(ml__cs)
    """
    _m = np.loadtxt(fname=filename, usecols=[0,1,2,3,4,5,6,8], unpack=True)
    ns = (_m[0] == 0).astype('int').sum()
    nc_max = _m[0].astype('int').max() + 1
    age__cs = _m[1].reshape(ns, nc_max).T
    met__cs = _m[2].reshape(ns, nc_max).T
    coeff__cs = _m[3].reshape(ns, nc_max).T
    norm__cs = _m[4].reshape(ns, nc_max).T
    e_norm__cs = _m[7].reshape(ns, nc_max).T
    ml__cs = _m[5].reshape(ns, nc_max).T
    Av__cs = _m[6].reshape(ns, nc_max).T
    coeff_mass__cs = coeff__cs*10**(ml__cs)
    data = {
        'shape': (nc_max, ns),
        'age__cs': age__cs,
        'met__cs': met__cs,
        'coeff__cs': coeff__cs,
        'norm__cs': norm__cs,
        'e_norm__cs': e_norm__cs,
        'ml__cs': ml__cs,
        'Av__cs': Av__cs,
        'coeff_mass__cs': coeff_mass__cs,
    }
    return data

# def read_output_CS(input):
#     _m = np.loadtxt(fname=input, unpack=True, comments='#', delimiter=',')
#     # ,
#     #                 usecols=[0,1,2,3,4,5,6,7,8,9,10,13,14])
#     chi__s = _m[0]
#     age_LW__s = _m[1]
#     e_age_LW__s = _m[2]
#     met_LW__s = _m[3]
#     e_met_LW__s = _m[4]
#     Av__s = _m[5]
#     e_Av__s = _m[6]
#     vel__s = _m[7]*__c__
#     e_vel__s = _m[8]*__c__
#     disp__s = _m[9]/(1 + _m[7])
#     e_disp__s = np.abs(_m[10])
#     orig_flux_sum__s = _m[11]
#     redshift_ssp__s = _m[12]
#     med_flux_norm_window__s = _m[13]   # flux__s
#     res_std__s = _m[14]                # e_flux__s
#     # flux__s = _m[11]
#     # e_flux__s = _m[12]
#     age_MW__s = _m[15]
#     e_age_MW__s = _m[16]
#     met_MW__s = _m[17]
#     e_met_MW__s = _m[18]
#     sys_vel__s = _m[19]
#     log_ml__s = _m[20]
#     log_mass__s = _m[21]

def map_auto_ssp_AGE_MET_rnd_seg(auto_ssp_output_filename, segmentation_fits, output_prefix, central_wavelength, inst_disp):
    # read segmentation
    seg__yx = get_data_from_fits(segmentation_fits)
    ny, nx = seg__yx.shape

    chi__yx = np.zeros((ny, nx))
    age__yx = np.zeros((ny, nx))
    age_mass__yx = np.zeros((ny, nx))
    e_age__yx = np.zeros((ny, nx))
    age_lum__yx = np.zeros((ny, nx))
    e_age_lum__yx = np.zeros((ny, nx))
    age_lum_M__yx = np.zeros((ny, nx))
    e_age_lum_M__yx = np.zeros((ny, nx))
    met_lum__yx = np.zeros((ny, nx))
    met_mass__yx = np.zeros((ny, nx))
    met_lumI__yx = np.zeros((ny, nx))
    met_lumII__yx = np.zeros((ny, nx))
    met_lumII_mass__yx = np.zeros((ny, nx))
    e_met_lumII__yx = np.zeros((ny, nx))
    met_e_lumII_mass__yx = np.zeros((ny, nx))
    met__yx = np.zeros((ny, nx))
    e_met__yx = np.zeros((ny, nx))
    Av__yx = np.zeros((ny, nx))
    e_Av__yx = np.zeros((ny, nx))
    disp__yx = np.zeros((ny, nx))
    vel__yx = np.zeros((ny, nx))
    e_disp__yx = np.zeros((ny, nx))
    e_vel__yx = np.zeros((ny, nx))
    flux__yx = np.zeros((ny, nx))
    e_flux__yx = np.zeros((ny, nx))
    ml__yx = np.zeros((ny, nx))
    mass__yx = np.zeros((ny, nx))
    disp_km__yx = np.zeros((ny, nx))
    e_disp_km__yx = np.zeros((ny, nx))

    print('Reading input files')
    coeffs_input = f'coeffs_{auto_ssp_output_filename}'

    data = read_coeffs_CS(coeffs_input)
    (nc_max, ns) = data['shape']
    age__cs = data['age__cs']
    met__cs = data['met__cs']
    coeff__cs = data['coeff__cs']
    norm__cs = data['norm__cs']
    e_norm__cs = data['e_norm__cs']
    ml__cs = data['ml__cs']
    Av__cs = data['Av__cs']
    coeff_mass__cs = data['coeff_mass__cs']

    sum_coeff__s = coeff__cs.sum(axis=0)
    sum_mass__s = coeff_mass__cs.sum(axis=0)
    coeff__cyx = np.zeros((nc_max, ny, nx))
    norm__cyx = np.zeros((nc_max, ny, nx))
    e_norm__cyx = np.zeros((nc_max, ny, nx))
    Av__cyx = np.zeros((nc_max, ny, nx))

    _m = np.loadtxt(fname=auto_ssp_output_filename, unpack=True, comments='#', delimiter=',',
                    usecols=[0,1,2,3,4,5,6,7,8,9,10,13,14])
    chi__s = _m[0]
    age__s = _m[1]
    e_age__s = _m[2]
    met__s = _m[3]
    e_met__s = _m[4]
    Av__s = _m[5]
    e_Av__s = _m[6]
    vel__s = _m[7]*__c__
    e_vel__s = _m[8]*__c__
    disp__s = _m[9]/(1 + _m[7])
    e_disp__s = np.abs(_m[10])
    flux__s = _m[11]
    e_flux__s = _m[12]

    print('Feeding the arrays')
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i > 0:
            spec_i -= 1
            chi__yx[iy, ix] = chi__s[spec_i]
            age__yx[iy, ix] = age__s[spec_i]
            met__yx[iy, ix] = met__s[spec_i]
            Av__yx[iy, ix] = Av__s[spec_i]
            vel__yx[iy, ix] = vel__s[spec_i]
            disp__yx[iy, ix] = disp__s[spec_i]
            if disp__s[spec_i] > inst_disp:
                disp_km__yx[iy, ix] = (np.sqrt(np.abs(disp__s[spec_i]**2 - inst_disp**2))/central_wavelength)*__c__
            else:
                disp_km__yx[iy, ix] = 0
            flux__yx[iy, ix] = flux__s[spec_i]
            e_age__yx[iy, ix] = e_age__s[spec_i]
            e_met__yx[iy, ix] = e_met__s[spec_i]
            e_Av__yx[iy, ix] = e_Av__s[spec_i]
            e_vel__yx[iy, ix] = e_vel__s[spec_i]
            e_disp__yx[iy, ix] = e_disp__s[spec_i]
            e_disp_km__yx[iy, ix] = (e_disp__s[spec_i]/central_wavelength)*__c__
            e_flux__yx[iy, ix] = e_flux__s[spec_i]
            for i_c in range(nc_max):
                # print(f'{ix},{iy}, [{nx},{ny}] {i_c} [{nc_max}] {spec_i}')
                norm__cyx[i_c, iy, ix] = coeff__cs[i_c, spec_i]
                e_norm__cyx[i_c, iy, ix] = e_norm__cs[i_c, spec_i]
                age_now = age__cs[i_c][0]
                met_now = met__cs[i_c][0]
                age_val = age_lum__yx[iy, ix]
                age_val += coeff__cs[i_c, spec_i]*(np.log10(age_now))
                age_lum__yx[iy, ix] = age_val
                if sum_mass__s[spec_i] > 0:
                    age_val = age_mass__yx[iy, ix]
                    age_val += coeff_mass__cs[i_c, spec_i]*(np.log10(age_now)/sum_mass__s[spec_i])
                    age_mass__yx[iy, ix] = age_val
                    ml_now = ml__yx[iy, ix]
                    ml_now += coeff__cs[i_c, spec_i]*ml__cs[i_c, spec_i]
                    ml__yx[iy, ix] = ml_now
                    mass_now = mass__yx[iy, ix]
                    mass_now += coeff__cs[i_c, spec_i]*10**(ml__cs[i_c, spec_i])*flux__s[spec_i]*1e-16
                    mass__yx[iy, ix] = mass_now
                met_val = met_lum__yx[iy, ix]
                met_val += coeff__cs[i_c, spec_i]*met_now
                met_lum__yx[iy, ix] = met_val
                met_val = met_lumI__yx[iy, ix]
                met_val += norm__cs[i_c, spec_i]*np.log10(met_now/__solar_metallicity__)
                met_lumI__yx[iy, ix] = met_val
                met_val = met_lumII__yx[iy, ix]
                met_val += coeff__cs[i_c, spec_i]*np.log10(met_now/__solar_metallicity__)
                met_lumII__yx[iy, ix] = met_val
                if sum_mass__s[spec_i] > 0:
                    met_val = met_mass__yx[iy, ix]
                    met_val += coeff_mass__cs[i_c, spec_i]*np.log10(met_now/__solar_metallicity__)/sum_mass__s[spec_i]
                    met_mass__yx[iy, ix] = met_val
            met_now = met__yx[iy, ix]
            e_met_now = e_met__yx[iy, ix]
            if met_now > 0:
                e_met_lumII__yx[iy, ix] = e_met_now/met_now
            age_now = age_lum__yx[iy, ix]
            e_age_now = e_age__yx[iy, ix]
            if age_now > 0:
                # XXX: found a probable error in perl script (line:273)
                # original line:
                #   set($pdl_e_age_lum,$ix,$iy,$age_val);
                # probable correct line:
                #   set($pdl_e_age_lum,$ix,$iy,$e_age_now);
                e_age_lum__yx[iy, ix] = e_age_now/age_now
            age_lum__yx[iy, ix] = 9 + age_lum__yx[iy, ix]
            age_lum_M__yx[iy, ix] = 9 + age_mass__yx[iy, ix]
            met_val = met_lum__yx[iy, ix]
            met_val = np.log10(met_val/__solar_metallicity__)
            met_lum__yx[iy, ix] = met_val
    print('DONE')
    print('Writting the output files')
    chi_name = f'{output_prefix}_chi_ssp.fits'
    array_to_fits(chi_name, chi__yx, overwrite=True)
    age_name = f'{output_prefix}_age_ssp.fits'
    array_to_fits(age_name, age__yx, overwrite=True)
    age_name = f'{output_prefix}_age_mass_ssp.fits'
    array_to_fits(age_name, age_mass__yx, overwrite=True)
    e_age_name = f'{output_prefix}_e_age_ssp.fits'
    array_to_fits(e_age_name, e_age__yx, overwrite=True)
    age_name = f'{output_prefix}_log_age_yr_ssp.fits'
    array_to_fits(age_name, age_lum__yx, overwrite=True)
    age_name = f'{output_prefix}_e_log_age_yr_ssp.fits'
    array_to_fits(age_name, e_age_lum__yx, overwrite=True)
    age_name = f'{output_prefix}_log_age_yr_mass_ssp.fits'
    array_to_fits(age_name, age_lum_M__yx, overwrite=True)
    met_name = f'{output_prefix}_met_ssp.fits'
    array_to_fits(met_name, met__yx, overwrite=True)
    met_name = f'{output_prefix}_met_ZH_mass_ssp.fits'
    array_to_fits(met_name, met_mass__yx, overwrite=True)
    met_name = f'{output_prefix}_met_ZH_ssp.fits'
    array_to_fits(met_name, met_lumII__yx, overwrite=True)
    met_name = f'{output_prefix}_e_met_ZH_ssp.fits'
    array_to_fits(met_name, e_met_lumII__yx, overwrite=True)
    Av_name = f'{output_prefix}_Av_ssp.fits'
    array_to_fits(Av_name, Av__yx, overwrite=True)
    disp_name = f'{output_prefix}_disp_ssp.fits'
    array_to_fits(disp_name, disp__yx, overwrite=True)
    disp_km_name = f'{output_prefix}_disp_km_h_ssp.fits'
    array_to_fits(disp_km_name, disp_km__yx, overwrite=True)
    vel_name = f'{output_prefix}_vel_ssp.fits'
    array_to_fits(vel_name, vel__yx, overwrite=True)
    flux_name = f'{output_prefix}_flux_ssp.fits'
    array_to_fits(flux_name, flux__yx, overwrite=True)
    e_met_name = f'{output_prefix}_e_met_ssp.fits'
    array_to_fits(e_met_name, e_met__yx, overwrite=True)
    e_Av_name = f'{output_prefix}_e_Av_ssp.fits'
    array_to_fits(e_Av_name, e_Av__yx, overwrite=True)
    e_disp_name = f'{output_prefix}_e_disp_ssp.fits'
    array_to_fits(e_disp_name, e_disp__yx, overwrite=True)
    e_disp_km_name = f'{output_prefix}_e_disp_km_h_ssp.fits'
    array_to_fits(e_disp_km_name, e_disp_km__yx, overwrite=True)
    e_vel_name = f'{output_prefix}_e_vel_ssp.fits'
    array_to_fits(e_vel_name, e_vel__yx, overwrite=True)
    e_flux_name = f'{output_prefix}_e_flux_ssp.fits'
    array_to_fits(e_flux_name, e_flux__yx, overwrite=True)
    mass_name = f'{output_prefix}_mass_ssp.fits'
    array_to_fits(mass_name, mass__yx, overwrite=True)
    ml_name = f'{output_prefix}_ml_ssp.fits'
    array_to_fits(ml_name, ml__yx, overwrite=True)
    for i_c in range(nc_max):
        filename = f'{output_prefix}_NORM_{i_c}_ssp.fits'
        sec__yx = norm__cyx[i_c]
        array_to_fits(filename, sec__yx, overwrite=True)
        write_img_header(filename, 'AGE', age__cs[i_c, 0])
        write_img_header(filename, 'MET', met__cs[i_c, 0])
        filename = f'{output_prefix}_eNORM_{i_c}_ssp.fits'
        sec__yx = e_norm__cyx[i_c]
        array_to_fits(filename, sec__yx, overwrite=True)
        write_img_header(filename, 'AGE', age__cs[i_c, 0])
        write_img_header(filename, 'MET', met__cs[i_c, 0])

def map_auto_ssp_rnd_seg(input_elines, segmentation_fits, output_prefix, inst_disp=None,
                         wave_norm=None):  #, auto_ssp_config=None):
    if inst_disp is None:
        inst_disp = 2.45
    if wave_norm is None:
        wave_norm = 4275

    # read segmentation
    seg__yx = get_data_from_fits(segmentation_fits)
    ny, nx = seg__yx.shape

    input_ssp = input_elines.replace('elines_', '')
    map_auto_ssp_AGE_MET_rnd_seg(input_ssp, segmentation_fits, output_prefix, wave_norm, inst_disp)

    print('Reading fit output file')
    models = []
    chi_sq = []
    j = 0
    with open(input_elines, 'r') as f:
        for line in f:
            while line.startswith('#'):
                line = f.readline()
            if line:
                n_models, _chi_sq = line.split()
                n_models = eval(n_models)
                chi_sq.append(_chi_sq)
                models.append({})
                for i in range(n_models):
                    line = f.readline()
                    _s = line.split()
                    model = _s[0]
                    if not (model in models[j].keys()):
                        models[j][model] = []
                    if model == 'eline':
                        models[j][model].append({
                            'central_wavelength': eval(_s[1]),
                            'e_central_wavelength': eval(_s[2]),
                            'flux': eval(_s[3]),
                            'e_flux': eval(_s[4]),
                            'sigma': eval(_s[5]),
                            'e_sigma': eval(_s[6]),
                            'v0': eval(_s[7]),
                            'e_v0': eval(_s[8]),
                            'disp':  __sigma_to_FWHM__*eval(_s[5]),
                            'e_disp':  __sigma_to_FWHM__*eval(_s[6]),
                        })
                    elif model == 'poly1d':
                        models[j][model].append({
                            'flux': eval(_s[1]),
                            'e_flux': eval(_s[2])
                        })
                j += 1
    n_models = len(models)
    ns = seg__yx.max().astype('int')
    n_models_spec = int(n_models/ns)
    n_el_mod = np.sum([len(models[i]['eline']) for i in range(n_models_spec)])
    wave__m = np.zeros((n_el_mod))
    wave_name__m = np.empty((n_el_mod), dtype=object);
    flux__ms = np.zeros((n_el_mod, ns))
    eflux__ms = np.zeros((n_el_mod, ns))
    sig__ms = np.zeros((n_el_mod, ns))
    esig__ms = np.zeros((n_el_mod, ns))
    vel__ms = np.zeros((n_el_mod, ns))
    evel__ms = np.zeros((n_el_mod, ns))

    i_s = 0
    i_el_mod = 0
    for i_mod in range(n_models):
        i_s_ant = i_s
        i_s = i_mod // n_models_spec
        if i_s != i_s_ant:
            i_el_mod = 0
        n = len(models[i_mod]['eline'])
        for i in range(n):
            wave__m[i_el_mod] = models[i_mod]['eline'][i]['central_wavelength']
            if wave__m[i_el_mod] != 0:
                wave_name__m[i_el_mod] = str(int(models[i_mod]['eline'][i]['central_wavelength']))
            flux__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['flux']
            eflux__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['e_flux']
            sig__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['sigma']
            esig__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['e_sigma']
            vel__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['v0']
            evel__ms[i_el_mod, i_s] = models[i_mod]['eline'][i]['e_v0']
            i_el_mod += 1

    # first = None
    # i_m = 0
    # i_s = 0
    # nmod = 0
    # if auto_ssp_config is not None:
    #     from .auto_ssp_tools import ConfigAutoSSP
    #     cf = ConfigAutoSSP(auto_ssp_config)
    #     for elcf in cf.systems_config:
    #         sel_eline_models = np.array(elcf.model_types) == 'eline'
    #         nmod += sel_eline_models.astype('int').sum()
    #         tmp_nmod = nmod
    # else:
    #     tmp_nmod = 20
    # ns = seg__yx.max().astype('int')
    # wave__m = np.zeros((tmp_nmod))
    # wave_name__m = np.empty((tmp_nmod), dtype=object);
    # flux__ms = np.zeros((tmp_nmod, ns))
    # eflux__ms = np.zeros((tmp_nmod, ns))
    # sig__ms = np.zeros((tmp_nmod, ns))
    # esig__ms = np.zeros((tmp_nmod, ns))
    # vel__ms = np.zeros((tmp_nmod, ns))
    # evel__ms = np.zeros((tmp_nmod, ns))
    #
    # with open(input_elines) as f:
    #     for line in f:
    #         if line.startswith('eline'):
    #             _tmp = line.split(' ')
    #             print('begin>> i_s: ', i_s, _tmp)
    #             if (nmod, i_s, eval(_tmp[1])) == (0, 0, 0):
    #                 raise ValueError((
    #                     f'map_auto_ssp_rnd_seg(): Missing emission lines results in first voxel.'
    #                     ' Re-run map_auto_ssp_rnd_seg() with auto_ssp_config in order to setup'
    #                     ' the right number of emission lines eline models.'
    #                 ))
    #             ###################################################
    #             # XXX EL 2020-07-16 @ CDMX
    #             # This piece of code FIX voxel id when there is a
    #             # problem with the emission lines fit in auto_ssp
    #             # and the voxel output is all zeros for all models.
    #             # The problem stills when the problem is in the
    #             # voxel id = 0 because nmod is not evaluated yet.
    #             # the best fix would include a new input variable,
    #             # the summed number of eline models in all emission
    #             # lines systems inside the auto_ssp analysis. This
    #             # could be calculated before this loop if the config
    #             # config file of auto_ssp is provided.
    #             ###################################################
    #             i = 0
    #             s_jump = 0
    #             s_jump_now = 0
    #             print(ns, i_s, i_m, _tmp)
    #             while eval(_tmp[1]) == 0:
    #                 s_jump = s_jump_now + 1
    #                 if (i_s + s_jump) >= (ns - 1):
    #                     break
    #                 print('>>>>', ns, i_s, i_m, s_jump, _tmp)
    #                 if (i == nmod):
    #                     i = 0
    #                     s_jump_now += 1
    #                 i += 1
    #                 line = f.readline()
    #                 while not line.startswith('eline'):
    #                     line = f.readline()
    #                 _tmp = line.split(' ')
    #             if first is None:
    #                 first = eval(_tmp[1])
    #                 i_s = -1 if auto_ssp_config is None else 0
    #             if not s_jump:
    #                 if auto_ssp_config is None:
    #                     if (first == eval(_tmp[1])):
    #                         i_s += 1
    #                         i_m = 0
    #                 else:
    #                     if i_m == nmod:
    #                         i_s += 1
    #                         i_m = 0
    #             else:
    #                 print('>>', s_jump, i_s, i_m)
    #                 if (i_s != 0) and ((i_s + s_jump) <= (ns - 1)):
    #                     s_jump += 1
    #                 print('<<', s_jump)
    #                 i_s += s_jump
    #                 i_m = 0
    #             print(i_s)
    #             wave__m[i_m] = eval(_tmp[1])
    #             wave_name__m[i_m] = str(_tmp[1].split('.')[0])
    #             flux__ms[i_m, i_s] = eval(_tmp[3])
    #             eflux__ms[i_m, i_s] = eval(_tmp[4])
    #             sig__ms[i_m, i_s] = eval(_tmp[5])
    #             esig__ms[i_m, i_s] = eval(_tmp[6])
    #             vel__ms[i_m, i_s] = eval(_tmp[7])
    #             evel__ms[i_m, i_s] = eval(_tmp[8])
    #             ###################################################
    #             # EL: This is the problem, nmod is filled in the
    #             # first voxel.
    #             ###################################################
    #             if (auto_ssp_config is None) and (i_m > 0):
    #                 nmod = i_m + 1
    #             ###################################################
    #             i_m += 1

    nmod = n_el_mod
    print(f'{nmod}, {i_s + 1} data')
    print('DONE')
    print('Feeding arrays')
    flux__myx = np.zeros((nmod, ny, nx))
    eflux__myx = np.zeros((nmod, ny, nx))
    vel__myx = np.zeros((nmod, ny, nx))
    disp__myx = np.zeros((nmod, ny, nx))
    disp_km_s__myx = np.zeros((nmod, ny, nx))

    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i > 0:
            spec_i -= 1
            for i_m in range(nmod):
                flux__myx[i_m, iy, ix] = flux__ms[i_m, spec_i]
                eflux__myx[i_m, iy, ix] = eflux__ms[i_m, spec_i]
                disp__myx[i_m, iy, ix] = sig__ms[i_m, spec_i]
                if (sig__ms[i_m, spec_i] > inst_disp):
                    sig_km_s = np.sqrt(sig__ms[i_m, spec_i]**2 - inst_disp**2)/eval(wave_name__m[i_m])*__c__
                else:
                    sig_km_s = 0
                disp_km_s__myx[i_m, iy, ix] = sig_km_s
                vel__myx[i_m, iy, ix] = vel__ms[i_m, spec_i]

    print('Done')
    print('Writting output')
    for i_m in range(nmod):
        ii = f'{i_m:02d}'
        flux_name = f'{output_prefix}_flux_{wave_name__m[i_m]}.fits'
        array_to_fits(flux_name, flux__myx[i_m], overwrite=True)
        write_img_header(flux_name, 'CRVAL1', wave__m[i_m])

        eflux_name = f'{output_prefix}_eflux_{wave_name__m[i_m]}.fits'
        array_to_fits(eflux_name, eflux__myx[i_m], overwrite=True)
        write_img_header(eflux_name, 'CRVAL1', wave__m[i_m])

        disp_name = f'{output_prefix}_disp_{wave_name__m[i_m]}.fits'
        array_to_fits(disp_name, disp__myx[i_m], overwrite=True)
        write_img_header(disp_name, 'CRVAL1', wave__m[i_m])

        # XXX filename should be *disp_km_s*
        disp_km_s_name = f'{output_prefix}_disp_km_h_{wave_name__m[i_m]}.fits'
        array_to_fits(disp_km_s_name, disp_km_s__myx[i_m], overwrite=True)
        write_img_header(disp_km_s_name, 'CRVAL1', wave__m[i_m])

        vel_name = f'{output_prefix}_vel_{wave_name__m[i_m]}.fits'
        array_to_fits(vel_name, vel__myx[i_m], overwrite=True)
        write_img_header(vel_name, 'CRVAL1', wave__m[i_m])
        print(f'{wave_name__m[i_m]} DONE')
    print('DONE')

def redshift_config(input_config, redshift, output_config=None):
    if output_config is None:
        fo = sys.stdout
    else:
        fo = open(output_config, 'w')
    with open(input_config) as f:
        for i in range(3):
            print(f.readline(), file=fo, end='')
        line = f.readline()
        n_systems = int(line)
        print(line, file=fo, end='')
        print(f'NC={n_systems}')
        for i in range(n_systems):
            line = f.readline()
            sline = line.split(' ')
            sline[0] = str(int(int(sline[0])*(1 + redshift)))
            sline[1] = str(int(int(sline[1])*(1 + redshift)))
            print(' '.join(sline), file=fo, end='')
        print(' '.join(f.readlines()).replace('\n ', '\n'), file=fo, end='')
        if output_config is not None:
            fo.close()

def get_CS_slice(input_name):
    segmentation_fits = f'cont_seg.{input_name}.fits.gz'
    Ha_map_fits = f'{input_name}.V.fits.gz'
    output_file = f'CS.{input_name}.slice'

    # read segmentation

    seg__yx = get_data_from_fits(segmentation_fits)
    ny, nx = seg__yx.shape
    ns = seg__yx.max().astype('int') + 1

    # read Ha map
    Ha_map__yx = get_data_from_fits(Ha_map_fits)

    # filling
    n = 0
    x__s = np.zeros(ns)
    y__s = np.zeros(ns)
    flux__s = np.zeros(ns)
    area__s = np.zeros(ns)
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        if spec_i > 0:
            if n < spec_i:
                n = spec_i
            Ha = Ha_map__yx[iy, ix]
            if Ha == 0:
                Ha = 1
            flux__s[spec_i] += Ha
            x__s[spec_i] += (ix * Ha)
            y__s[spec_i] += (iy * Ha)
            area__s[spec_i] += 1

    # print output slice
    header = ' (1) ID\n (2) X\n (3) Y\n (4) Flux\n (5) Area'
    x = np.where(flux__s > 0, x__s/flux__s, x__s)
    y = np.where(flux__s > 0, y__s/flux__s, y__s)
    # XXX: x and y are integers in perl when area == 1.
    #      The behaviour could be reproduced with replacing np.savetxt to a loop
    #      printint the values.
    np.savetxt(output_file, list(zip(list(range(1, ns)), x, y, flux__s, area__s)),
               fmt = ['%d'] + 3*['%.18g'] + ['%d'], delimiter=' ', header=header)

# def radial_sum_cube_e(input_cube_fits, delta_R, x0, y0, output_rss_fits, plot=False):
def radial_sum_cube_e(cube__wyx, delta_R, x0, y0, input_mask=None, input_error=None, plot=False):
    nw, ny, nx = cube__wyx.shape
    y0 = ny - y0
    # XXX: plot needed to be implemented, perl version run always as plot = 0
    # plot_shape = 'R'
    # plot_size = 1
    mask__wyx = np.ones_like(cube__wyx)
    e_cube__wyx = np.zeros_like(cube__wyx)
    # weight__wyx = np.zeros_like(cube__wyx)
    if input_mask is not None:
        mask__wyx -= input_mask
    if input_error is not None:
        e_cube__wyx = input_error
    cube__wyx *= mask__wyx
    nw_med = int(nw/2)
    start_iw = nw_med - 50
    end_iw = nw_med + 50
    weight__yx = cube__wyx[start_iw:end_iw+1].mean(axis=0)/mask__wyx[start_iw:end_iw+1].mean(axis=0)
    ns = nx * ny
    cube__sw = np.zeros((ns, nw))
    e_cube__sw = np.zeros((ns, nw))
    mask__sw = np.zeros((ns, nw))
    weight__s = np.zeros((ns))
    x__s = np.zeros((ns))
    y__s = np.zeros((ns))
    r__s = np.zeros((ns))
    # c__s = np.zeros((ns))
    # s__s = np.zeros((ns))
    # S__s = np.zeros((ns))
    rmax = 0
    n = 0
    xmin = 10e10
    xmax = -10e10
    ymin = 10e10
    ymax = -10e10
    for iyx in itertools.product(range(ny),range(nx)):
        iy, ix = iyx
        i_s = ix + (ny - 1 - iy)*nx
        cube__sw[i_s] = cube__wyx[:, iy, ix]
        e_cube__sw[i_s] = e_cube__wyx[:, iy, ix]
        mask__sw[i_s] = mask__wyx[:, iy, ix]
        weight__s[i_s] = weight__yx[iy, ix]
        x__s[n] = ix
        y__s[n] = iy
        r__s[n] = np.sqrt((x__s[n] - x0)**2 + (y__s[n] - y0)**2)
        # print(f'(({ix} - {x0})**2 + ({iy} - {y0})**2)**0.5 = {r__s[n]}')
        rmax = r__s[n] if r__s[n] > rmax else rmax
        xmin = x__s[n] if x__s[n] < xmin else xmin
        xmax = x__s[n] if x__s[n] > xmax else xmax
        ymin = y__s[n] if y__s[n] < ymin else ymin
        ymax = y__s[n] if y__s[n] > ymax else ymax
        # nk = r__s[n]/delta_R
        # _i = int(nk/2.)
        # c__s[n] = 2 + _i
        # s__s[n] = 3 + _i
        # S__s[n] = 2.5 - nk/15
        n += 1
    nr = int(rmax/delta_R) + 1
    output__rw = np.zeros((nr, nw))
    e_output__rw = np.zeros((nr, nw))
    mask_output__rw = np.zeros((nr, nw))
    NN__r = np.zeros((nr))
    nw1 = int(0.25*nw)
    nw2 = int(0.6*nw)
    _tmp = cube__sw[:, nw1:nw2+1]
    flux__s = np.nansum(_tmp, axis=1)
    flux__s[np.isnan(flux__s)] = 0
    flux_min = flux__s.min()
    flux_max = flux__s.max()
    if np.isinf(flux_min):
        flux_min = 0
    spaxels = []
    for ir in range(nr):
        rmin = delta_R*ir
        rmax = delta_R*(ir + 1)
        nsum = 0
        spaxels.append([])
        nspaxels = 0
        K = 0
        for i_s in range(ns):
            if r__s[i_s] < rmax:
                spaxels[ir].append(i_s)
                if flux__s[i_s] > 0:
                    K += 1
                    output__rw[ir] += cube__sw[i_s]
                    e_output__rw[ir] += e_cube__sw[i_s]
                    mask_output__rw[ir] += mask__sw[i_s]*weight__s[i_s]
                    nsum += weight__s[i_s]
        NN__r[ir] = nsum
        if NN__r[ir] > 0:
            output__rw[ir] = NN__r[ir]*(output__rw[ir]/mask_output__rw[ir])
            e_output__rw[ir] = np.sqrt(np.abs(NN__r[ir]))*(e_output__rw[ir]/mask_output__rw[ir])
            mask_output__rw[ir] /= NN__r[ir]
    return output__rw, e_output__rw, mask_output__rw

def get_cosmo(z, h, om, ol):
    zdot = lambda z, om, ol: (1 + z)**2*np.sqrt(1 + om*z + ol*(-1 + (1 + z)**(-2)))
    invzdot = lambda z, om, ol: 1/zdot(z, om, ol)

    def chi(z, om, ol):
        if (om + ol) == 1:
            k = 1
        else:
            k = np.sqrt(np.abs(1-om-ol))
        return k/((1 + z)*np.sqrt(om*z + 1 + ol*((1 + z)**(-2) - 1)))

    def chiint(zmax, om, ol):
        dz = 0.001
        sum = 0
        zi = 0
        while zi <= (zmax - dz):
            inc = (chi(zi, om, ol) + chi(zi+dz,om,ol))/2
            sum += dz*inc
            zi += dz
        return sum

    def tint(zmax, om, ol):
        sum = 0
        zi = 0
        dz = 0.001
        while (zi <= (zmax - dz)):
            inc = (invzdot(zi, om, ol) + invzdot(zi + dz, om, ol))/2
            sum += dz*inc
            zi += dz
        return sum

    th = 978.0/h
    ch = chiint(z, om, ol)
    zfact = 1 + z
    if (om + ol) == 1:
        sigma = ch
        r0 = __c__/h
    if (om + ol) > 1:
        r0 = __c__/(h*np.sqrt(om + ol - 1))
        sigma = np.sin(ch)
    if (om + ol) < 1:
        r0 = __c__/(h * np.sqrt(1 - om - ol))
        sigma = (np.exp(ch) - np.exp(-ch))/2
    r = sigma*r0/zfact
    if r < 1:
        r = 1
    cosmo = {
         'ludis': r*zfact**2,                     # Luminosity Distance (Mpc)
         'angsize': r,                            # Angular Distance (Mpc)
         'propmo': r*zfact,                       # Proper Motion Distance (Mpc)
         'lbtime': th*tint(z, om, ol),            # Look-back time (Gyr)
         'dm': 5*0.4343*np.log(r*(zfact**2))+25,  # Distance Modulus
         'scale': r/206.264806                    # Angular Scale (Kpc/");
    }
    return cosmo

def sum_mass_age(name, output_csv_filename=None):
    def filter_coeffs(f, comments=None):
        if comments is None:
            comments = '#'
        l = []
        for i, line in enumerate(f):
            if line.startswith(comments): continue
            line = line.replace('\t', ' ').strip()
            _l = line.split(' ')
            _l = [i.strip(' ') for i in _l if (i != '') or (i == '\n')]
            _l = _l[0]
            if _l not in l:
                l.append(_l)
                yield line

    clf = False
    if output_csv_filename is not None:
        if isinstance(output_csv_filename, io.TextIOWrapper):
            f_out = output_csv_filename
        else:
            clf = True
            f_out = open(output_csv_filename, 'w')
    else:
        f_out = sys.stdout
    # seg__yx = get_data_from_fits(f'cont_seg.{name}.fits.gz')
    flux__yx = get_data_from_fits(f'map.CS.{name}_flux_ssp.fits.gz')
    ny, nx = flux__yx.shape
    _mf = f'mask.{name}.V.fits.gz'
    mask__yx = np.ones_like(flux__yx)
    if isfile(_mf):
        mask__yx = get_data_from_fits(_mf)
    _redshift = np.loadtxt(f'auto_ssp.CS.{name}.rss.out', delimiter=',', usecols=7, unpack=True)
    ns = _redshift.size
    redshift = np.median(_redshift)
    cosmo = get_cosmo(redshift, __Hubble_constant__, __Omega_matter__, __Omega_Lambda__)
    ratio = 3.08567758e24
    _luminosity_distance = 10**((cosmo['dm']-25)/5)*ratio
    _luminosity_factor = ((4*np.pi*(_luminosity_distance**2))*1e-16)/__solar_luminosity__
    dtype = [
        # ('ID', 'int'),
        ('AGE', 'float'), ('MET', 'float'),
        # ('COEFF', 'float'), ('NORM', 'float'),
        ('logML', 'float'),
        # ('AV', 'float')
    ]
    i_pack_out = 1
    f = open(f'sum_mass_age.{name}.pack.csv', 'w')
    print("# (1) ID\n# (2) File\n# (3) Description\n# (4) Type\n# (5) units", file=f)
    # read_coeffs = np.loadtxt(f'coeffs_auto_ssp.CS.{name}.rss.out', usecols=(1,2,5), dtype=dtype, max_rows=156)
    with open(f'coeffs_auto_ssp.CS.{name}.rss.out', 'r') as fcoeffs:
        read_coeffs = np.genfromtxt(filter_coeffs(fcoeffs), usecols=(1,2,5), dtype=dtype)
    age_unique = np.unique(read_coeffs['AGE'])
    met_unique = np.unique(read_coeffs['MET'])
    n_models = len(read_coeffs)
    n_age = age_unique.size
    n_met = met_unique.size
    print(f'# N={n_models} models', file=f_out)
    print(f'# N.AGE={n_age}', file=f_out)
    print(f'# N.MET={n_met}', file=f_out)
    ML__yx = np.zeros_like(flux__yx)
    mass__yx = np.zeros_like(flux__yx)
    e_mass__yx = np.zeros_like(flux__yx)
    for im in range(n_models):
        age = read_coeffs['AGE'][im]
        met = read_coeffs['MET'][im]
        ML = read_coeffs['logML'][im]
        map__yx = get_data_from_fits(f'map.CS.{name}_NORM_{im}_ssp.fits.gz')
        map__yx[~np.isfinite(map__yx)] = 0
        e_map__yx = get_data_from_fits(f'map.CS.{name}_eNORM_{im}_ssp.fits.gz')
        e_map__yx[~np.isfinite(e_map__yx)] = 0
        _fact = 10**ML
        _fact__yx = _fact*flux__yx
        ML__yx += map__yx*_fact
        mass__yx += map__yx*_fact__yx
        e_mass__yx += e_map__yx*_fact__yx
        if not im:
            cube__myx = np.zeros((n_models, ny, nx), dtype='float')
            e_cube__myx = np.zeros_like(cube__myx)
        cube__myx[im] = map__yx
        e_cube__myx[im] = e_map__yx
        print(f'{i_pack_out},map.CS.NAME_NORM_{im}_ssp.fits.gz,Luminosity Fraction for age-met {age:.4f}-{met:.4f} SSP, flux, fraction', file=f)
        i_pack_out += 1
    cube__myx *= mask__yx
    e_cube__myx *= mask__yx
    Av__yx = get_data_from_fits(f'map.CS.{name}_Av_ssp.fits.gz')
    lum__yx = flux__yx*_luminosity_factor*3500
    mass__yx *= _luminosity_factor
    mass_to_light__yx = np.divide(mass__yx, lum__yx, where=lum__yx!=0, out=np.zeros((ny, nx)))
    e_mass__yx *= _luminosity_factor
    log10e = np.log10(np.exp(1))
    loge10 = np.log(10)
    logMass__yx = np.log(mass__yx)/loge10
    logMass__yx *= mask__yx
    array_to_fits(f'map.CS.{name}_Mass_ssp.fits.gz', logMass__yx, overwrite=True)
    e_logMass__yx = np.divide(log10e*e_mass__yx, mass__yx, where=mass__yx!=0, out=np.zeros((ny, nx)))
    e_logMass__yx *= mask__yx
    array_to_fits(f'map.CS.{name}_eMass_ssp.fits.gz', e_logMass__yx, overwrite=True)
    logMass_dust_corr__yx = logMass__yx + log10e*Av__yx
    array_to_fits(f'map.CS.{name}_Mass_dust_cor_ssp.fits.gz', logMass_dust_corr__yx, overwrite=True)
    logML__yx = np.log(mass_to_light__yx)/loge10
    array_to_fits(f'map.CS.{name}_ML_ssp.fits.gz', logML__yx, overwrite=True)
    mass_sum = mass__yx.sum()
    e_mass_sum = e_mass__yx.sum()
    logMass_sum = np.log10(mass_sum)
    logeMass_sum = log10e*e_mass_sum/mass_sum
    logMass__yx[~np.isfinite(logMass__yx)] = 0
    logMass_dust_corr__yx[~np.isfinite(logMass_dust_corr__yx)] = 0
    mass_sum_dust_corr = np.where(np.abs(logMass_dust_corr__yx) > 0,
                                  10**np.abs(logMass_dust_corr__yx),
                                  np.where(np.abs(logMass__yx) > 0, 10**np.abs(logMass__yx), 0))
    logMass_dust_corr = np.log10(mass_sum_dust_corr.sum())
    print(f'# name, log10(Mass)', file=f_out)
    print(f'Mass,{name},{logMass_sum},{logMass_dust_corr},{logeMass_sum}', file=f_out)
    for ia in range(n_age):
        age = age_unique[ia]
        age_t = f'{age:0>7.4f}'
        age__yx = np.zeros((ny, nx), dtype='float')
        e_age__yx = np.zeros((ny, nx), dtype='float')
        for im in range(n_models):
            if age == read_coeffs['AGE'][im]:
                age__yx += cube__myx[im]
                e_age__yx += e_cube__myx[im]**2
        array_to_fits(f'map.CS.{name}_{age_t}_NORM_age.fits.gz', age__yx, overwrite=True)
        array_to_fits(f'map.CS.{name}_{age_t}_eNORM_age.fits.gz', np.sqrt(e_age__yx), overwrite=True)
        print(f'{i_pack_out},map.CS.NAME_{age_t}_NORM_age.fits.gz,Luminosity Fraction for age {age:.4f} SSP, flux, fraction', file=f)
        i_pack_out += 1
    for iZ in range(n_met):
        met = met_unique[iZ]
        met_t = f'{met:0>6.4f}'
        met__yx = np.zeros((ny, nx), dtype='float')
        e_met__yx = np.zeros((ny, nx), dtype='float')
        for im in range(n_models):
            if met == read_coeffs['MET'][im]:
                met__yx += cube__myx[im]
                e_met__yx += e_cube__myx[im]**2
        array_to_fits(f'map.CS.{name}_{met_t}_NORM_met.fits.gz', met__yx, overwrite=True)
        array_to_fits(f'map.CS.{name}_{met_t}_eNORM_met.fits.gz', np.sqrt(e_met__yx), overwrite=True)
        print(f'{i_pack_out},map.CS.NAME_{met_t}_NORM_met.fits.gz,Luminosity Fraction for met {met:.4f} SSP, flux, fraction', file=f)
        i_pack_out += 1
    f.close()
    if f_out.name != '<stdout>':
        f_out.close()

def pack_results_name(name, pack_filename, prefix):
    output_filename = f'{name}.{prefix}.cube.fits.gz'
    dtype_pack = [('ID', 'int'), ('FILE', 'object'), ('DESC', 'object'), ('TYPE', 'object'),
                  ('UNITS' , 'object')]
    pack = np.loadtxt(pack_filename, dtype=dtype_pack, delimiter=',')
    n_p = pack.size
    output_header = {'COMMENT': 'FITs header', 'OBJECT': name}
    for ip in range(n_p):
        pack['FILE'][ip] = pack['FILE'][ip].replace('NAME', name)
        filename = pack['FILE'][ip]
        data, h = get_data_from_fits(f'{filename}', header=True)
        if not ip:
            nx = h['NAXIS1']
            ny = h['NAXIS2']
            output_cube__pyx = np.zeros((n_p, ny, nx), dtype=data.dtype)
        output_cube__pyx[ip] = data
        keys = list(zip(*dtype_pack))[0]
        output_header.update({f'{key}_{ip}': pack[key][ip] for ik, key in enumerate(keys)})
    array_to_fits(output_filename, output_cube__pyx, overwrite=True)
    write_img_header(output_filename, list(output_header.keys()), list(output_header.values()))

def pack_NAME(name, ssp_pack_filename=None, elines_pack_filename=None, sfh_pack_filename=None, mass_out_filename=None):
    if ssp_pack_filename is None:
        ssp_pack_filename = '../legacy/pack_CS_inst_disp.csv'
    pack_results_name(name, ssp_pack_filename, 'SSP')
    if elines_pack_filename is None:
        elines_pack_filename = '../legacy/pack_elines_v1.5.csv'
    pack_results_name(name, elines_pack_filename, 'ELINES')
    if mass_out_filename is None:
        mass_out_filename = f'Mass.{name}.csv'
    sum_mass_age(name, mass_out_filename)
    if sfh_pack_filename is None:
        sfh_pack_filename = '../legacy/pack_SFH.csv'
    pack_results_name(name, sfh_pack_filename, 'SFH')

def indices_spec(wave__w, flux_ssp__w, res__w, redshift, n_sim, plot=0, wl_half_range=200, verbose=False):
    if plot:
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt

        #plt.style.use('dark_background')
        f, ax = plt.subplots()
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Flux')

    nw = wave__w.size
    cdelt = wave__w[1] - wave__w[0]
    names__i = list(__indices__.keys())
    _ind = np.array(list(__indices__.values()))
    wmin = _ind.T[_INDICES_POS['OLb1']].min() - wl_half_range
    wmax = _ind.T[_INDICES_POS['OLr2']].max() + wl_half_range
    n_ind = _ind.shape[0]

    FWHM = __sigma_to_FWHM__*3*cdelt

    stflux = pdl_stats(flux_ssp__w)
    if (stflux[_STATS_POS['mean']] == 0) and (stflux[_STATS_POS['min']] == stflux[_STATS_POS['max']]):
        flux_ssp__w = np.ones_like(flux_ssp__w)
        res__w = 100*np.ones_like(flux_ssp__w)

    med_res__w = median_filter(res__w, size=np.int(3*FWHM/cdelt), mode='reflect')

    _ind_corr = _ind*(1 + redshift)
    _ind_corr.T[_INDICES_POS['OLb']] = (_ind_corr.T[_INDICES_POS['OLb1']] + _ind_corr.T[_INDICES_POS['OLb2']])/2
    _ind_corr.T[_INDICES_POS['OLr']] = (_ind_corr.T[_INDICES_POS['OLr1']] + _ind_corr.T[_INDICES_POS['OLr2']])/2
    wmin = _ind_corr.T[_INDICES_POS['OLb1']].min() - wl_half_range
    wmax = _ind_corr.T[_INDICES_POS['OLr2']].max() + wl_half_range

    med_flux = np.median(flux_ssp__w[np.isfinite(flux_ssp__w)])
    std_flux = np.std(flux_ssp__w[np.isfinite(flux_ssp__w)])
    EW__ki = np.zeros((n_sim, n_ind))
    for k in range(n_sim):
        noise = np.random.normal(size=nw)
        noise *= res__w
        _flux__w = flux_ssp__w + noise
        _med_flux = np.median(_flux__w)
        _min_flux = -0.1*np.abs(_med_flux)
        _max_flux = 3.5*_med_flux
        for ii in range(n_ind):
            if plot:
                plt.cla()
                ax = plt.gca()
                ax.set_xlim(wmin, wmax)
                ax.set_ylim(_min_flux - 0.2*np.abs(_min_flux), _max_flux + 0.2*np.abs(_max_flux))
                ax.plot(wave__w, _flux__w, 'k-')
            name = names__i[ii]
            Lb1 = _ind_corr[ii][_INDICES_POS['OLb1']]
            Lb2 = _ind_corr[ii][_INDICES_POS['OLb2']]
            Lr1 = _ind_corr[ii][_INDICES_POS['OLr1']]
            Lr2 = _ind_corr[ii][_INDICES_POS['OLr2']]
            L1 = _ind_corr[ii][_INDICES_POS['OL1']]
            L2 = _ind_corr[ii][_INDICES_POS['OL2']]
            Lb = _ind_corr[ii][_INDICES_POS['OLb']]
            Lr = _ind_corr[ii][_INDICES_POS['OLr']]

            str_verbose = f'L1:{L1}, L2:{L2}\nblue: Lb:{Lb}, Lb1:{Lb1}, Lb2:{Lb2}\nred: Lr:{Lr}, Lr1:{Lr1}, Lr2:{Lr2}'
            print_verbose(str_verbose, verbose=verbose, level=1)

            if name != 'D4000':
                iw1_b = (Lb1 - wave__w[0] - 0.5*cdelt)/cdelt
                iw2_b = (Lb2 - wave__w[0] - 0.5*cdelt)/cdelt
                Sb = 0
                nb = 0
                for iw in range(np.int(iw1_b + 1), np.int(iw2_b)):
                    Sb += _flux__w[iw]*cdelt
                    nb += 1
                iw = np.int(iw1_b)
                ff = iw + 1 - iw1_b
                Sb += (_flux__w[iw]*ff*cdelt)
                iw = np.int(iw2_b)
                ff = iw2_b - iw
                Sb += (_flux__w[iw]*ff*cdelt)
                Sb = Sb/(Lb2 - Lb1)

                iw1_r = (Lr1 - wave__w[0] - 0.5*cdelt)/cdelt
                iw2_r = (Lr2 - wave__w[0] - 0.5*cdelt)/cdelt
                Sr = 0
                nr = 0
                for iw in range(np.int(iw1_r + 1), np.int(iw2_r)):
                    Sr += _flux__w[iw]*cdelt
                    nr += 1
                iw = np.int(iw1_r)
                ff = iw + 1 - iw1_r
                Sr += (_flux__w[iw]*ff*cdelt)
                iw = np.int(iw2_r)
                ff = iw2_r - iw
                Sr += (_flux__w[iw]*ff*cdelt)
                Sr = Sr/(Lr2 - Lr1)
                EW = 0
                CK = []
                waveK = []
                iw1 = (L1 - wave__w[0] - 0.5*cdelt)/cdelt
                iw2 = (L2 - wave__w[0] - 0.5*cdelt)/cdelt
                for iw in range(np.int(iw1 + 1), np.int(iw2)):
                    C = Sb*((Lr - wave__w[iw])/(Lr - Lb)) + Sr*((wave__w[iw] - Lb)/(Lr - Lb))
                    EW = EW + (1 - _flux__w[iw]/C)*(wave__w[iw] - wave__w[iw - 1])
                    CK.append(C)
                    waveK.append(wave__w[iw])
                iw = np.int(iw1)
                ff = iw + 1 - iw1
                C = Sb*((Lr - wave__w[iw])/(Lr - Lb)) + Sr*((wave__w[iw] - Lb)/(Lr - Lb))
                EW = EW + (1 - _flux__w[iw]/C)*(wave__w[iw] - wave__w[iw - 1])*ff
                iw = np.int(iw2)
                ff = iw2 - iw
                C = Sb*((Lr - wave__w[iw])/(Lr - Lb)) + Sr*((wave__w[iw] - Lb)/(Lr - Lb))
                EW = EW + (1 - _flux__w[iw]/C)*(wave__w[iw] - wave__w[iw - 1])*ff
                EW = EW/(1 + redshift)
                if plot:
                    _xy, dx, dy = (Lb1, _max_flux*0.5), Lb2-Lb1, _max_flux*0.3
                    rectLb1Lb2 = patches.Rectangle(_xy, dx, dy, edgecolor='b', facecolor='none')
                    ax.add_patch(rectLb1Lb2)
                    _xy, dx, dy = (Lr1, _max_flux*0.5), Lr2-Lr1, _max_flux*0.3
                    rectLr1Lr2 = patches.Rectangle(_xy, dx, dy, edgecolor='r', facecolor='none')
                    ax.add_patch(rectLr1Lr2)
                    _xy, dx, dy = (L1, _max_flux*0.5), L2-L1, _max_flux*0.3
                    rectL1L2 = patches.Rectangle(_xy, dx, dy, edgecolor='g', facecolor='none')
                    ax.add_patch(rectL1L2)
                    ax.plot(waveK, CK, ls='--', c='gray')
                    ax.scatter(Lb, Sb, marker='x', color='b', s=50)
                    ax.scatter(Lr, Sr, marker='x', color='r', s=50)
                    ax.set_xlim(Lb1 - 0.02*Lb1, Lr2 + 0.02*Lr2)
                    ax.text(0.98, 0.98, name, transform=ax.transAxes, va='top', ha='right')
                    plt.pause(0.001)
            else:
                Sb = 0
                nb = 0
                iw1_b = (Lb1 - wave__w[0] - 0.5*cdelt)/cdelt
                iw2_b = (Lb2 - wave__w[0] - 0.5*cdelt)/cdelt
                for iw in range(np.int(iw1_b + 1), np.int(iw2_b)):
                    Sb += _flux__w[iw]*cdelt
                    nb += 1
                iw = np.int(iw1_b)
                ff = iw + 1 - iw1_b
                Sb += _flux__w[iw]*ff*cdelt
                iw = np.int(iw2_b)
                ff = iw2_b - iw
                Sb += _flux__w[iw]*ff*cdelt
                Sb = Sb/(Lb2 - Lb1)

                S = 0
                K = 0
                iw1 = (L1 - wave__w[0] - 0.5*cdelt)/cdelt
                iw2 = (L2 - wave__w[0] - 0.5*cdelt)/cdelt
                for iw in range(np.int(iw1 + 1), np.int(iw2)):
                    S += _flux__w[iw]*cdelt
                    K += 1
                iw = np.int(iw1)
                ff = iw + 1 - iw1
                S += _flux__w[iw]*ff*cdelt
                iw = np.int(iw2)
                ff = iw2 - iw
                S += _flux__w[iw]*ff*cdelt
                S = S/(L2 - L1)
                if Sb != 0:
                    EW = S/Sb
                else:
                    EW = 1e16
                if plot:
                    _xy, dx, dy = (Lb1, _max_flux*0.5), Lb2-Lb1, _max_flux*0.3
                    rectLb1Lb2 = patches.Rectangle(_xy, dx, dy, edgecolor='b', facecolor='none')
                    ax.add_patch(rectLb1Lb2)
                    # _xy, dx, dy = (Lr1, _max_flux*0.5), Lr2-Lr1, _max_flux*0.3
                    # rectLr1Lr2 = patches.Rectangle(_xy, dx, dy, edgecolor='r', facecolor='none')
                    # ax.add_patch(rectLr1Lr2)
                    _xy, dx, dy = (L1, _max_flux*0.5), L2-L1, _max_flux*0.3
                    rectL1L2 = patches.Rectangle(_xy, dx, dy, edgecolor='r', facecolor='none')
                    ax.add_patch(rectL1L2)
                    # ax.plot(waveK, CK, '--k')
                    ax.scatter(Lb, Sb, marker='x', color='b', s=50)
                    ax.scatter((L1 + L2)/2, S, marker='x', color='r', s=50)
                    ax.set_xlim(Lb1 - 0.02*Lb1, L2 + 0.02*L2)
                    ax.text(0.98, 0.98, name, transform=ax.transAxes, va='top', ha='right')
                    plt.pause(0.001)
            EW__ki[k, ii] = EW
    if plot:
        plt.close(f)
    return EW__ki, med_flux, std_flux

def get_index(wave__w, flux_ssp__sw, res__sw, redshift__s, n_sim, plot=0, wl_half_range=200, seg__yx=None):
    n_spectra, nw = flux_ssp__sw.shape
    names__i = list(__indices__.keys())
    # build up output variable
    indices = {}
    for name in names__i:
        indices[name] = {
            'EW': np.zeros(n_spectra, dtype='float'),
            'sigma_EW': np.zeros(n_spectra, dtype='float')
        }
    indices['SN'] = np.zeros(n_spectra, dtype='float')
    indices['e_SN'] = np.zeros(n_spectra, dtype='float')
    for i_s in range(n_spectra):
        redshift = redshift__s[i_s]
        res__w = res__sw[i_s]
        flux_ssp__w = flux_ssp__sw[i_s] + res__w
        EW__ki, med_flux, std_flux = indices_spec(wave__w, flux_ssp__w, res__w, redshift, n_sim, plot=plot, wl_half_range=200)
        for ii, name in enumerate(names__i):  # in range(n_ind):
            # name = names__i[ii]
            indices[name]['EW'][i_s] = EW__ki[:, ii].mean()
            indices[name]['sigma_EW'][i_s] = EW__ki[:, ii].std()
        indices['SN'][i_s] = med_flux
        indices['e_SN'][i_s] = std_flux
    if seg__yx is not None:
        # read segmentation
        ny, nx = seg__yx.shape
        ns = seg__yx.max().astype('int') + 1
        k_list = [x for x in indices.keys() if 'SN' not in x]
        nI = len(k_list)
        output_cube__Iyx = np.zeros((nI*2 + 2, ny, nx))
        for ixy in itertools.product(range(nx),range(ny)):
            ix, iy = ixy
            spec_i = int(seg__yx[iy, ix])
            spec_i_out = spec_i - 1
            if spec_i_out >= 0:
                _a = [indices[k]['EW'][spec_i_out] for k in k_list]
                _b = [indices[k]['sigma_EW'][spec_i_out] for k in k_list]
                _a.append(indices['SN'][spec_i_out])
                _b.append(indices['e_SN'][spec_i_out])
                output_cube__Iyx[:, iy, ix] = np.append(_a, _b)
        return indices, output_cube__Iyx
    return indices

def read_indices_file(indices_file):
    nindex = 0
    names = None
    indices = []
    e_indices = []
    with open(indices_file, 'r') as f:
        for line in f:
            line = line.replace('e4000', 'D4000')
            data = [x for x in line.split(' ') if x != '']
            if names is None:
                names = data[::3]
                nindex = len(names)
                names += [f'e_{i}' for i in names]
            if len(data) == 3*nindex:
                indices.append(np.array(data[1::3], dtype='float'))
                e_indices.append(np.array(data[2::3], dtype='float'))
            else:
                indices.append(np.zeros(nindex, dtype='float'))
                e_indices.append(np.zeros(nindex, dtype='float'))
    indices__si = np.asarray(indices)
    e_indices__si = np.asarray(e_indices)

    return names, indices__si, e_indices__si

def index_seg_cube(indices_file, segmentation_fits, indices_cube_fits):
    header = {
        'COMMENT': 'FIT-header',
        'FILENAME': indices_cube_fits,
    }
    names, indices__si, e_indices__si = read_indices_file(indices_file)
    nindex = indices__si.shape[-1]
    for i in range(nindex):
        j = i + nindex
        header[f'INDEX{i}'] = names[i]
        header[f'INDEX{j}'] = names[j]
    # read segmentation
    seg__yx = get_data_from_fits(segmentation_fits)
    ny, nx = seg__yx.shape
    ns = seg__yx.max().astype('int') + 1
    nIndex = 2*nindex
    output_cube__Iyx = np.empty((nIndex, ny, nx))
    for ixy in itertools.product(range(nx),range(ny)):
        ix, iy = ixy
        spec_i = int(seg__yx[iy, ix])
        spec_i_out = spec_i - 1
        if spec_i_out >= 0:
            _a = indices__si[spec_i_out]
            _b = e_indices__si[spec_i_out]
            output_cube__Iyx[:, iy, ix] = np.append(_a, _b)
    array_to_fits(indices_cube_fits, output_cube__Iyx, header=header, overwrite=True)

def vel_eline(flux, wave, nsearch, imin, wave_ref, set_first_peak=True):
    y_min = 1e12
    y_max = -1e12
    mask_fin = np.isfinite(flux)
    mask_y_max = flux[mask_fin] > y_max
    if mask_y_max.sum() > 0:
        y_max = np.nanmax(flux[mask_fin][mask_y_max])
    mask_y_min = flux[mask_fin] < y_min
    if mask_y_min.sum() > 0:
        y_min = np.nanmin(flux[mask_fin][mask_y_min])
    # print("y_max=", y_max, "\t y_min=", y_min)
    crval = wave[0]
    cdelt = wave[1] - wave[0]
    peak_y_max = np.array([])
    peak_y_pixel = np.array([])
    i = 0
    vel = 0
    dmin = 0
    npeaks = 0
    mask_out = 0
    med = np.mean(flux)
    sig = np.std(flux, ddof=1)
    for j in np.arange(nsearch, len(flux)-nsearch):
        peak = True
        if set_first_peak:
            if flux[j - i] > (med + 2 * sig):
                peak = True
            else:
                peak = False
        for i in np.arange(nsearch):
            if flux[j-i] < flux[j-i-1]:
                peak = False
            if flux[j+i] < flux[j+i+1]:
                peak = False
        if peak:
            if flux[j] < imin * y_max:
                peak = False
        if peak:
            if npeaks > 0:
                delta = j - peak_y_pixel[int(npeaks - 1)]
                if delta < dmin:
                    peak = False
        if peak:
            peak_y_pixel = np.append(peak_y_pixel, j)
            a, b, c = j - 1, j, j + 1
            x = [a, b, c]
            y = [-flux[a], -flux[b], -flux[c]]
            peak_y, _ = hyperbolic_fit_par(x, y)
            peak_y_max = np.append(peak_y_max, peak_y)
            npeaks += 1
        if (y_max > y_min) and (y_min != 0):
            wave_peak = np.array([crval + cdelt * peak for peak in peak_y_max])
            if npeaks == 1:
                vel = (wave_peak[0]/wave_ref - 1) * __c__
                mask_out = 1
            if npeaks == 2:
                vel = (wave_peak[0] / wave_ref - 1) * __c__
                mask_out = 2
            if npeaks == 3:
                vel = (wave_peak[1] / wave_ref - 1) * __c__
                mask_out = 2
    return vel, mask_out, npeaks

def clean_map(map__yx, vel_map__yx, max_vel, min_vel):
    # Fill non finite values with zeroes.
    ny, nx = map__yx.shape
    map__yx[~np.isfinite(map__yx)] = 0
    # Looking for non positive or non finite values in vel_map__yx
    mask_vel_map__yx = np.ones((ny, nx), dtype=bool)
    mask__yx = (vel_map__yx <= 0) | ~np.isfinite(vel_map__yx)
    mask_vel_map__yx[mask__yx] = False
    for iyx in itertools.product(range(1, ny - 1),range(1, nx - 1)):
        iy, ix = iyx
        if not mask_vel_map__yx[iy, ix]:
            iy0 = iy - 1
            iy1 = iy + 2
            ix0 = ix - 1
            ix1 = ix + 2
            mask_slice = mask_vel_map__yx[iy0:iy1, ix0:ix1]
            if mask_slice.astype('int').sum() > 5:
                val = map__yx[iy0:iy1, ix0:ix1]
                st_val = pdl_stats(val[mask_slice > 0])
                new_val = st_val[_STATS_POS['median']]
                print(f'correcting spaxel ix:{ix} iy:{iy} - val: {map__yx[iy, ix]} -> {new_val}')
                map__yx[iy, ix] = new_val
    # Looking for values outside the range defined by [min_vel, max_vel]
    mask_vel_map__yx = np.ones((ny, nx), dtype=bool)
    mask__yx = (vel_map__yx > max_vel) | (vel_map__yx < min_vel)
    mask_vel_map__yx[mask__yx] = False
    for iyx in itertools.product(range(1, ny - 1),range(1, nx - 1)):
        iy, ix = iyx
        if not mask_vel_map__yx[iy, ix]:
            iy0 = iy - 1
            iy1 = iy + 2
            ix0 = ix - 1
            ix1 = ix + 2
            mask_slice = mask_vel_map__yx[iy0:iy1, ix0:ix1]
            if mask_slice.astype('int').sum() > 5:
                val = map__yx[iy0:iy1, ix0:ix1]
                st_val = pdl_stats(val[mask_slice > 0])
                new_val = st_val[_STATS_POS['median']]
                print(f'correcting spaxel ix:{ix} iy:{iy} - val: {map__yx[iy, ix]} -> {new_val}')
                map__yx[iy, ix] = new_val
    return map__yx

def list_eml_compare(wave_list, filename_list_ref, redshift, abs_max_dist_AA=4, plot=0, verbose=0):
    """
    Compare a list of emission lines central wavelengths of detected automatically
    with a theoretical list of emission lines central wavelengths.


    Parameters
    ----------
    wave_list: array like

    filename_list_ref: str

    redshift: float

    abs_max_dist_AA: float, optional
        Defaults to 4 AA.

    plot: int, optional
        Defaults to 0.

    verbose: int, optional
        Defaults to 0.

    Returns
    -------
        array like
            Final list of detected emission lines.

        array like
            Indexes from ``wave_list`` for the peaks associated to each final list
            of detected emission lines.

        array like
            Final list of ``wave_list`` peaks associated to the detected emission
            lines.

        if ``filename_list_ref`` presents a second column with the names of the
        emission lines:
            array like
                The names of the emission lines if
    """
    wave_arr = np.asarray(wave_list)
    wave_arr_corr = wave_arr/(1 + redshift)
    iS = np.argsort(wave_list)
    wave_arr_sorted = wave_arr[iS]
    wave_arr_corr_sorted = wave_arr_corr[iS]

    wave_ref_arr = np.array([])
    name_eml = np.array([])
    ne = 0
    with open(filename_list_ref) as fp:
        line = fp.readline()
        while line:
            if not line.startswith('#'):
                tmp_line = line.strip().split()
                nfields = len(tmp_line)
                if nfields:
                    wave_ref_arr = np.append(wave_ref_arr, float(tmp_line[0]))
                    if nfields > 1:
                        name_eml = np.append(name_eml, tmp_line[1])
                    ne += 1
            line = fp.readline()

    iwrS = np.argsort(wave_ref_arr)
    wave_ref_arr = wave_ref_arr[iwrS]
    if name_eml.size == wave_ref_arr.size:
        name_eml = name_eml[iwrS]
    org_wave_ref_arr = copy(wave_ref_arr)

    final_wave_list = []
    ifinal_wave_list = []
    final_assoc_peaks = []
    ifinal_assoc_peaks = []
    dist_AA = wave_ref_arr[:, np.newaxis] - wave_arr_corr_sorted
    abs_dist_AA = np.abs(dist_AA)

    idist_sorted_wl = np.argsort(abs_dist_AA, axis=1)
    dist_sorted_wl = np.sort(abs_dist_AA, axis=1)

    idist_sorted_wl_wref = np.argsort(dist_sorted_wl, axis=0)
    dist_sorted_wl_wref = np.sort(dist_sorted_wl, axis=0)

    _ind = np.where(dist_sorted_wl_wref < abs_max_dist_AA)

    if _ind[0].size > 0:
        ii, jj = _ind
        for i, j in zip(ii, jj):
            i_wref = idist_sorted_wl_wref[i, j]
            wref = wave_ref_arr[i_wref]
            i_assoc_peak = idist_sorted_wl[i_wref, j]
            assoc_peak = wave_arr_sorted[i_assoc_peak]
            if not ((wref in final_wave_list) or (assoc_peak in final_assoc_peaks)):
                ifinal_wave_list.append(i_wref)
                final_wave_list.append(wref)
                ifinal_assoc_peaks.append(i_assoc_peak)
                final_assoc_peaks.append(assoc_peak)
                print_verbose(f'list_eml_compare: EML {wref} AA associated to peak {assoc_peak} AA', verbose=verbose)

    ifinal_assoc_peaks = np.asarray([iS[i] for i in ifinal_assoc_peaks], dtype=int)

    final_wave_arr = np.asarray(final_wave_list)
    ifinal_wave_arr = np.asarray(ifinal_wave_list, dtype=int)
    ifwS = np.argsort(final_wave_arr)
    final_wave_arr = final_wave_arr[ifwS]
    ifinal_wave_arr = ifinal_wave_arr[ifwS]

    final_assoc_peaks = np.asarray(final_assoc_peaks)
    ifinal_assoc_peaks = np.asarray(ifinal_assoc_peaks, dtype=int)
    final_assoc_peaks = final_assoc_peaks[ifwS]
    ifinal_assoc_peaks = ifinal_assoc_peaks[ifwS]

    txt = f'list_eml_compare: '
    if len(final_assoc_peaks):
        txt += f'peaks found: {len(final_assoc_peaks)}'
    else:
        txt += 'no peaks found'

    print_verbose(txt, verbose=verbose)

    if name_eml.size == wave_ref_arr.size:
        return final_wave_arr, ifinal_assoc_peaks, final_assoc_peaks, name_eml[ifinal_wave_arr]
    else:
        return final_wave_arr, ifinal_assoc_peaks, final_assoc_peaks

def peak_finder(wave, flux, nsearch, peak_threshold=2, dmin=2, plot=False, verbose=0):
    """
    Search for peaks in a spectrum (a.k.a. emission lines finder).
    ::

        flux_filtered = median_filter(flux)
        probable peaks = flux_filtered > median(flux_filtered) + peak_threshold*std(flux_filtered)

    Ther final peak list do not include peaks closer than ``dmin`` pixels.

    Parameters
    ----------
    wave : array like
        Wavelengths array.

    flux : array like
        Fluxes array.

    nsearch : int
        A peak will have the highest flux around the interval (in pixels):
            (peak - nsearch, peak + nsearch)

    peak_threshold : float, optional
        Defines the standard deviation multiplicative factor for the probable
        peak threshold calculation. Defaults to 2.

    dmin : int, optional
        Defines the minimal distance between peaks (in pixels). Defaults to 2.

    plot : bool, str, optional
        If True plots the result. If is a string, it configures plot as True and
        uses the string as the plot filename. Defaults to False.

    verbose : int, optional
        Print detect information at ``verbose`` level. Defaults to 0.

    Returns
    -------
    array like
        The indices of the peaks in wave/flux arrays.

    array like
        The probable peaks (in wavelengths).

    array like
        The hyperbolic fit of the wavelength associated to each peak.

    array like
        The flux associated to each peak.
    """
    nsearch = int(nsearch)
    dmin = int(dmin)

    wl_chunk = f'{int(np.floor(wave[0]))}_{int(np.ceil(wave[-1]))}'
    plot_filename = f'autodetect.peaks_{wl_chunk}.png'
    if isinstance(plot, str):
        plot_filename = plot
        plot = True
    flux_filt = flux - st_median_filter(box=int(20*__sigma_to_FWHM__), x=copy(flux))
    # fast and not-precise method to remove continuum (apply median filter).

    # probable peaks
    sigma_flux = np.std(flux_filt)
    median_flux = np.median(flux_filt)
    flux_ref_top = median_flux + peak_threshold*sigma_flux
    print_verbose(f'median_flux:{median_flux:.4f} sigma_flux:{sigma_flux:.4f}', verbose=verbose)
    probable_peaks = np.where(flux_filt > flux_ref_top)[0]

    if plot:
        if 'matplotlib.pyplot' not in sys.modules:
            from matplotlib import pyplot as plt
        else:
            plt = sys.modules['matplotlib.pyplot']

        plt.gcf().set_size_inches(15, 5)
        plt.cla()
        ax = plt.gca()
        ax.set_ylabel(r'Flux', fontsize=18)
        ax.set_xlabel(r'wavelength [$\AA$]', fontsize=18)
        ax.plot(wave, flux_filt, '-', alpha=0.2, color='k')

    i_peaks = []
    wave_peaks = []
    wave_hyperb_peaks = []
    flux_peaks = []

    for j in probable_peaks:
        # Flux to be analyzed
        peak = True
        ana_flux = flux_filt[j]

        # look nearby pixels: ana_flux is a real peak?
        if (j + nsearch + 1) < len(flux_filt):
            for i in range(nsearch):
                if (flux_filt[j-i] < flux_filt[j-i-1]) or (flux_filt[j+i] < flux_filt[j+i+1]):
                    peak = False
        else: # unable to perform nsearch peak test
            peak = False

        # Remove ana_flux close peaks
        if peak:
            if len(i_peaks) > 0:
                dlt = j - i_peaks[-1]
                if dlt <= dmin: peak = False

        # Append pixel coordinate of the peak
        if peak:
            i_peaks.append(j)
            wave_peaks.append(wave[j])
            flux_peaks.append(ana_flux)
            a, b, c = j - 1, j, j + 1
            x = [wave[a], wave[b], wave[c]]
            y = [flux_filt[a], flux_filt[b], flux_filt[c]]
            wave_peak, _ = hyperbolic_fit_par(x, y)
            wave_hyperb_peaks.append(wave_peak)
            if plot:
                ax.plot(x, y, '.r-', alpha=0.5)
                ax.plot(wave_peak, ana_flux, 'xb')

    n_peaks = len(wave_peaks)
    if n_peaks:
        _txt = f'found {n_peaks} peak'
        if n_peaks > 1:
            _txt += 's'
        print_verbose(f'{_txt}!', verbose=verbose)
    if plot:
        if plot > 1:
            plt.savefig(plot_filename)
            plt.close()
        else:
            plt.show()

    return np.array(i_peaks), np.array(wave_peaks), np.array(wave_hyperb_peaks), np.array(flux_peaks)

# def read_flux_elines(filename, filename_lines=None):
#     _flux_elines, h = get_data_from_fits(filename, header=True)
#     flux_elines = {}
#     units = {}
#     desc = {}
#     ids = {}
#     n = h['NAXIS3']
#     nx, ny = h['NAXIS1'], h['NAXIS2']
#     wavelengths = np.array([])
#     if filename_lines is not None:
#         # TODO create lines
#         ne = 0
#         with open(filename_lines) as fp:
#             line = fp.readline()
#             while line:
#                 if not line.startswith('#'):
#                     tmp_line = line.strip().split()
#                     if len(tmp_line) > 1:
#                         wavelengths = np.append(wavelengths, tmp_line[0])
#                     else:
#                         wavelengths = np.append(wavelengths, 0)
#                     ne += 1
#                 line = fp.readline()
#     else:
#         if 'WAVE0' not in h.keys():
#             print('missing wavelength information.')
#             return None
#         else:
#             for i in range(n):
#                 wavelengths = np.append(wavelengths, h[f'WAVE{i}'])
#     props = np.unique([h[f'NAME{i}'].split(' ')[0] for i in range(n)])
#     n_props = len(props)
#     _wavelengths = copy(wavelengths)
#     wavelengths = np.unique(_wavelengths)
#     nw = len(wavelengths)
#     for l in wavelengths:
#         flux_elines[l] = {}
#         units[l] = {}
#         desc[l] = {}
#         ids[l] = {}
#         for p in props:
#             flux_elines[l][p] = np.zeros((ny, nx))
#     for i in range(n):
#         wl = _wavelengths[i]
#         prop_lname = h[f'NAME{i}'].split(' ')
#         if len(prop_lname) < 2: continue
#         flux_elines[wl][prop_lname[0]] = copy(_flux_elines[i])
#         ids[l][p] = i
#         if h.get(f'UNIT{i}', None) is not None:
#             units[l][p] = h[f'UNIT{i}']
#         else:
#             units[l][p] = None
#         if h.get(f'NAME{i}', None) is not None:
#             desc[l][p] = h[f'NAME{i}']
#         else:
#             desc[l][p] = None
#     del _flux_elines
#     return flux_elines, h, ids, desc, units
#
# def read_SSP(filename):
#     _SSP, h = get_data_from_fits(filename, header=True)
#     units = {}
#     desc = {}
#     SSP = {
#         'V': copy(_SSP[0]),
#         'cont_seg': copy(_SSP[1]),
#         'scale_seg': copy(_SSP[2]),
#     }
#     ids = {
#         'V': 0,
#         'cont_seg': 1,
#         'scale_seg': 2,
#     }
#     units['V'] = h['UNITS_0'].strip()
#     units['cont_seg'] = h['UNITS_1'].strip()
#     units['scale_seg'] = h['UNITS_2'].strip()
#     desc['V'] = h['DESC_0'].strip()
#     desc['cont_seg'] = h['DESC_1'].strip()
#     desc['scale_seg'] = h['DESC_2'].strip()
#     for i in range(3, h['NAXIS3']):
#         _s = h[f'FILE_{i}'].strip().split('.')[2].split('_')
#         _tmp = '_'.join(_s[1:-1])
#         SSP[_tmp] = copy(_SSP[i])
#         ids[_tmp] = i
#         units[_tmp] = h[f'UNITS_{i}'].strip()
#         desc[_tmp] = h[f'DESC_{i}'].strip()
#     del _SSP
#     return SSP, h, ids, desc, units
#
# def read_ELINES(filename):
#     _ELINES, h = get_data_from_fits(filename, header=True)
#     n_ELINES = h['NAXIS3']
#     units = {}
#     desc = {}
#     ids = {
#         'v_Halpha': 0,
#         'disp_Halpha': 1,
#     }
#     ELINES = {
#         'v_Halpha': copy(_ELINES[0]),
#         'disp_Halpha': copy(_ELINES[1])
#     }
#     units['v_Halpha'] = h['UNITS_0'].strip()
#     units['disp_Halpha'] = h['UNITS_1'].strip()
#     desc['v_Halpha'] = h['DESC_0'].strip()
#     desc['disp_Halpha'] = h['DESC_1'].strip()
#     for i in range(2, n_ELINES):
#         _tmp = h[f'DESC_{i}'].strip().split(' ')[0]
#         ELINES[_tmp] = copy(_ELINES[i])
#         units[_tmp] = h[f'UNITS_{i}'].strip()
#         desc[_tmp] = h[f'DESC_{i}'].strip()
#         ids[_tmp] = i
#     del _ELINES
#     return ELINES, h, ids, desc, units
#
# def read_SFH(filename):
#     _SFH, h = get_data_from_fits(filename, header=True)
#     name = h['OBJECT'].strip()
#     n_models = len([i for i in range(h['NAXIS3']) if f'{name}_NORM' in h[f'FILE_{i}']])
#     mets_str = [
#         h[f'FILE_{i}'].split('_')[1]
#         for i in range(h['NAXIS3']) if 'NORM_met' in h[f'FILE_{i}']
#     ]
#     ages_str = [
#         h[f'FILE_{i}'].split('_')[1]
#         for i in range(h['NAXIS3']) if 'NORM_age' in h[f'FILE_{i}']
#     ]
#     age_models = np.asarray([eval(x) for x in ages_str])
#     met_models = np.asarray([eval(x) for x in mets_str])
#     n_age = len(age_models)
#     n_met = len(met_models)
#     n_models = n_models
#     age_met_models = [
#          h[f'DESC_{i}'].strip('Luminosity Fraction for age-met ').strip(' SSP').split('-')
#          for i in range(h['NAXIS3']) if f'{name}_NORM' in h[f'FILE_{i}']
#     ]
#     age_met_models = copy(age_met_models)
#     age_met_models_index = []
#     for age, met in age_met_models:
#         i_age = np.arange(n_age)[eval(age) == age_models]
#         i_met = np.arange(n_met)[eval(met) == met_models]
#         age_met_models_index.append((i_age, i_met))
#     nx, ny = h['NAXIS1'], h['NAXIS2']
#     SFH = {
#         'models': np.zeros((n_models, ny, nx)),
#         'age': np.zeros((n_age, ny, nx)),
#         'met': np.zeros((n_met, ny, nx))
#     }
#     units = {
#         'models': [],
#         'age': [],
#         'met': []
#     }
#     desc = {
#         'models': [],
#         'age': [],
#         'met': []
#     }
#     ids = {
#         'models': [],
#         'age': [],
#         'met': []
#     }
#     j, k, l = 0, 0, 0
#     for i in range(h['NAXIS3']):
#         _id = h[f'ID_{i}'] - 1
#         val = _SFH[_id]
#         try:
#             _desc = h[f'DESC_{i}']
#         except KeyError:
#             _desc = None
#         try:
#             _units = h['UNITS_{i}']
#         except KeyError:
#             _units = 'fraction'
#         if f'{name}_NORM_{_id}' in h[f'FILE_{i}']:
#             SFH['models'][j] = copy(val)
#             units['models'].append(_units)
#             desc['models'].append(_desc)
#             ids['models'].append(i)
#             j += 1
#         elif 'NORM_age' in h[f'FILE_{i}']:
#             SFH['age'][k] = copy(val)
#             units['age'].append(_units)
#             desc['age'].append(_desc)
#             ids['age'].append(i)
#             k += 1
#         elif 'NORM_met' in h[f'FILE_{i}']:
#             SFH['met'][l] = copy(val)
#             units['met'].append(_units)
#             desc['met'].append(_desc)
#             ids['met'].append(i)
#             l += 1
#     del _SFH
#     models_metainfo = [age_met_models, age_met_models_index, age_models, met_models]
#     return SFH, h, ids, desc, units, models_metainfo
#
# def read_indices(filename):
#     _indices, h = get_data_from_fits(filename, header=True)
#     indices = {}
#     units = None
#     desc = None
#     ids = {}
#     n = h['NAXIS3']
#     nx, ny = h['NAXIS1'], h['NAXIS2']
#     for i in range(n):
#         desc = h[f'INDEX{i}']
#         indices[desc] = copy(_indices[i])
#         ids[desc] = i
#     del _indices
#     return indices, h, ids, desc, units

def read_flux_elines(filename, filename_lines=None, cube=True):
    _flux_elines, h = get_data_from_fits(filename, header=True)
    flux_elines = {}
    units = {}
    desc = {}
    ids = {}
    if cube:
        n = h['NAXIS3']
        nx, ny = h['NAXIS1'], h['NAXIS2']
        _dim = (ny, nx)
    else:
        n = h['NAXIS1']
        ns = h['NAXIS2']
        _dim = (ns)
        _flux_elines =  _flux_elines.T
    wavelengths = np.array([])
    if filename_lines is not None:
        # TODO create lines
        ne = 0
        with open(filename_lines) as fp:
            line = fp.readline()
            while line:
                if not line.startswith('#'):
                    tmp_line = line.strip().split()
                    if len(tmp_line) > 1:
                        wavelengths = np.append(wavelengths, tmp_line[0])
                    else:
                        wavelengths = np.append(wavelengths, 0)
                    ne += 1
                line = fp.readline()
    else:
        if 'WAVE0' not in h.keys():
            print('missing wavelength information.')
            return None
        else:
            for i in range(n):
                wavelengths = np.append(wavelengths, h[f'WAVE{i}'])
    props = np.unique([h[f'NAME{i}'].split(' ')[0] for i in range(n)])
    n_props = len(props)
    _wavelengths = copy(wavelengths)
    wavelengths = np.unique(_wavelengths)
    nw = len(wavelengths)
    for l in wavelengths:
        flux_elines[l] = {}
        units[l] = {}
        desc[l] = {}
        ids[l] = {}
        for p in props:
            flux_elines[l][p] = np.zeros(_dim)
    for i in range(n):
        wl = _wavelengths[i]
        prop_lname = h[f'NAME{i}'].split(' ')
        if len(prop_lname) < 2: continue
        p = prop_lname[0]
        flux_elines[wl][p] = copy(_flux_elines[i])
        ids[wl][p] = i
        if h.get(f'UNIT{i}', None) is not None:
            units[wl][p] = h[f'UNIT{i}']
        else:
            units[wl][p] = None
        if h.get(f'NAME{i}', None) is not None:
            desc[wl][p] = h[f'NAME{i}']
        else:
            desc[wl][p] = None
    del _flux_elines
    return flux_elines, h, ids, desc, units

def read_SSP(filename):
    _SSP, h = get_data_from_fits(filename, header=True)
    units = {}
    desc = {}
    SSP = {
        'V': copy(_SSP[0]),
        'cont_seg': copy(_SSP[1]),
        'scale_seg': copy(_SSP[2]),
    }
    ids = {
        'V': 0,
        'cont_seg': 1,
        'scale_seg': 2,
    }
    units['V'] = h['UNITS_0'].strip()
    units['cont_seg'] = h['UNITS_1'].strip()
    units['scale_seg'] = h['UNITS_2'].strip()
    desc['V'] = h['DESC_0'].strip()
    desc['cont_seg'] = h['DESC_1'].strip()
    desc['scale_seg'] = h['DESC_2'].strip()
    for i in range(3, h['NAXIS3']):
        _s = h[f'FILE_{i}'].strip().split('.')[2].split('_')
        _tmp = '_'.join(_s[1:-1])
        SSP[_tmp] = copy(_SSP[i])
        ids[_tmp] = i
        units[_tmp] = h[f'UNITS_{i}'].strip()
        desc[_tmp] = h[f'DESC_{i}'].strip()
    del _SSP
    return SSP, h, ids, desc, units

def read_ELINES(filename):
    _ELINES, h = get_data_from_fits(filename, header=True)
    n_ELINES = h['NAXIS3']
    units = {}
    desc = {}
    ids = {
        'v_Halpha': 0,
        'disp_Halpha': 1,
    }
    ELINES = {
        'v_Halpha': copy(_ELINES[0]),
        'disp_Halpha': copy(_ELINES[1])
    }
    units['v_Halpha'] = h['UNITS_0'].strip()
    units['disp_Halpha'] = h['UNITS_1'].strip()
    desc['v_Halpha'] = h['DESC_0'].strip()
    desc['disp_Halpha'] = h['DESC_1'].strip()
    for i in range(2, n_ELINES):
        _tmp = h[f'DESC_{i}'].strip().split(' ')[0]
        ELINES[_tmp] = copy(_ELINES[i])
        units[_tmp] = h[f'UNITS_{i}'].strip()
        desc[_tmp] = h[f'DESC_{i}'].strip()
        ids[_tmp] = i
    del _ELINES
    return ELINES, h, ids, desc, units

def read_SFH(filename):
    _SFH, h = get_data_from_fits(filename, header=True)
    name = h['OBJECT'].strip()
    n_models = len([i for i in range(h['NAXIS3']) if f'{name}_NORM' in h[f'FILE_{i}']])
    mets_str = [
        h[f'FILE_{i}'].split('_')[1]
        for i in range(h['NAXIS3']) if 'NORM_met' in h[f'FILE_{i}']
    ]
    ages_str = [
        h[f'FILE_{i}'].split('_')[1]
        for i in range(h['NAXIS3']) if 'NORM_age' in h[f'FILE_{i}']
    ]
    age_models = np.asarray([eval(x) for x in ages_str])
    met_models = np.asarray([eval(x) for x in mets_str])
    n_age = len(age_models)
    n_met = len(met_models)
    n_models = n_models
    age_met_models = [
         h[f'DESC_{i}'].strip('Luminosity Fraction for age-met ').strip(' SSP').split('-')
         for i in range(h['NAXIS3']) if f'{name}_NORM' in h[f'FILE_{i}']
    ]
    age_met_models = copy(age_met_models)
    age_met_models_index = []
    for age, met in age_met_models:
        i_age = np.arange(n_age)[eval(age) == age_models]
        i_met = np.arange(n_met)[eval(met) == met_models]
        age_met_models_index.append((i_age, i_met))
    nx, ny = h['NAXIS1'], h['NAXIS2']
    SFH = {
        'models': np.zeros((n_models, ny, nx)),
        'age': np.zeros((n_age, ny, nx)),
        'met': np.zeros((n_met, ny, nx))
    }
    units = {
        'models': [],
        'age': [],
        'met': []
    }
    desc = {
        'models': [],
        'age': [],
        'met': []
    }
    ids = {
        'models': [],
        'age': [],
        'met': []
    }
    j, k, l = 0, 0, 0
    for i in range(h['NAXIS3']):
        _id = h[f'ID_{i}'] - 1
        val = _SFH[_id]
        try:
            _desc = h[f'DESC_{i}']
        except KeyError:
            _desc = None
        try:
            _units = h['UNITS_{i}']
        except KeyError:
            _units = 'fraction'
        if f'{name}_NORM_{_id}' in h[f'FILE_{i}']:
            SFH['models'][j] = copy(val)
            units['models'].append(_units)
            desc['models'].append(_desc)
            ids['models'].append(i)
            j += 1
        elif 'NORM_age' in h[f'FILE_{i}']:
            SFH['age'][k] = copy(val)
            units['age'].append(_units)
            desc['age'].append(_desc)
            ids['age'].append(i)
            k += 1
        elif 'NORM_met' in h[f'FILE_{i}']:
            SFH['met'][l] = copy(val)
            units['met'].append(_units)
            desc['met'].append(_desc)
            ids['met'].append(i)
            l += 1
    del _SFH
    models_metainfo = [age_met_models, age_met_models_index, age_models, met_models]
    return SFH, h, ids, desc, units, models_metainfo

def read_indices(filename):
    _indices, h = get_data_from_fits(filename, header=True)
    indices = {}
    units = None
    desc = None
    ids = {}
    n = h['NAXIS3']
    nx, ny = h['NAXIS1'], h['NAXIS2']
    for i in range(n):
        desc = h[f'INDEX{i}']
        indices[desc] = copy(_indices[i])
        ids[desc] = i
    del _indices
    return indices, h, ids, desc, units

class ReadDatacubes(object):
    """
    This class groups the results from the entire analysis of **pyFIT3D**.

    For now is reading output datacubes::

        NAME.SSP.cube.fits.gz
        NAME.ELINES.cube.fits.gz
        NAME.SFH.cube.fits.gz
        flux_elines.NAME.cube.fits.gz
        indices.CS.NAME.cube.fits.gz

    If available, it will read also the file::

        flux_elines_long.NAME.cube.fits.gz

    Attributes
    ----------
    name : str
        Object name.

    input_dir : str
        Location of the needed files.

    ELINES : dict
        The data from `NAME.ELINES.cube.fits.gz` FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.ELINES.keys()
            # dict_keys(['v_Halpha', 'disp_Halpha', '[OII]3727', '[OIII]5007',
            #            '[OIII]4959', 'Hbeta', 'Halpha', '[NII]6583', '[NII]6548',
            #            '[SII]6731', '[SII]6717'])

        Each element is an 2D numpy array with galaxy image dimension (ny, nx).

    SSP : dict
        The data from `NAME.SSP.cube.fits.gz` FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.SSP.keys()
            # dict_keys(['V', 'cont_seg', 'scale_seg', 'flux_ssp', 'e_flux_ssp',
                         'log_age_yr_ssp', 'log_age_yr_mass_ssp', 'e_log_age_yr_ssp',
                         'et_ZH_ssp', 'et_ZH_mass_ssp', 'e_met_ZH_ssp', 'Av_ssp',
                         'e_Av_ssp', 'vel_ssp', 'e_vel_ssp', 'disp_ssp', 'e_disp_ssp',
                         'ML_ssp', 'Mass_ssp', 'Mass_dust_cor_ssp', 'eMass_ssp'])

            Each element is an 2D numpy array with galaxy image dimension (ny, nx).

    SFH : dict
        The data from `NAME.SFH.cube.fits.gz` FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.SFH.keys()
            # dict_keys(['models', 'age', 'met'])

        ::

            models: Luminosity fraction (grouped by age-met)
                3D array (n_models, ny, nx)
            age: Luminosity fraction (grouped by age)
                3D array (n_age, ny, nx)
            met: Luminosity fraction (grouped by met)
                3D array (n_met, ny, nx)

    n_models : int
        The number of SSP models used in the SFH derivation.

    age_models : array like
        Ages of SSP models.

    met_models : array like
        Metallicities of SSP models.

    age_met_models : array like
        Age-Met of each SSP model.

    age_met_models_index : array like
        Each position saves a tuple with (i_age, i_met), the indexes of `age_models`
        and `met_models` of each model.

    n_age : int
        The number of different ages in SSP models used in the SFH derivation.

    n_met : int
        The number of different metallicities in SSP models used in the SFH derivation.

    flux_elines : dict
        The data from `flux_elines.NAME.cube.fits.gz` FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.flux_elines.keys()
            # dict_keys(['H10', 'H11', 'H12', 'H8', 'H9', 'Ha', 'Hb', 'Hd', 'He',
                         'HeI3819', 'HeI4026', 'HeI4471', 'HeI4713', 'HeI4922',
                         'HeI5876', 'HeI6678', 'HeII', 'Hg', 'OI', 'SiII', '[ArIII]',
                         '[ClIII]', '[FeIII]', '[FeII]', '[NII]', '[NII]6548',
                         '[NII]6584', '[NI]', '[NeIII]', '[OIII]4363', '[OIII]4959',
                         '[OIII]5007', '[OII]', '[OII]3727', '[OI]', '[SIII]',
                         '[SII]', '[SII]6717', '[SII]6731'])

        Each line has a dict with the derivated properties as keys:

        .. code-block:: python

            flux_elines['Ha'].keys()
            # dict_keys(['EW', 'disp', 'e_EW', 'e_disp', 'e_flux', 'e_vel',
                         'flux', 'vel'])

        Each element is an 2D numpy array with galaxy image dimension (ny, nx).

    flux_elines_long : dict
        The data from `flux_elines_long.NAME.cube.fits.gz` FITS file.

    indices : dict
        The data from `indices.CS.NAME.cube.fits.gz` FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.indices.keys()
            # dict_keys(['Hd', 'Hb', 'Mgb', 'Fe5270', 'Fe5335', 'D4000', 'Hdmod',
                         'Hg', 'SN', 'e_Hd', 'e_Hb', 'e_Mgb', 'e_Fe5270', 'e_Fe5335',
                         'e_D4000', 'e_Hdmod', 'e_Hg', 'e_SN'])

        Each element is an 2D numpy array with galaxy image dimension (ny, nx).

    header : dict of astropy.io.fits.header.Header
        The headers of each loaded FITS file.

        The keys are build automatically. Example:

        .. code-block:: python

            self.headers.keys()
            # dict_keys(['ELINES', 'SSP', 'SFH', 'flux_elines', 'flux_elines_long',
                         'indices'])

    units : dict
        The units of each available data of each loaded FITS file.
        The keys are the main datacubes keys.

    ids : dict
        The original id (INDEX) of each available data of each loaded FITS file.
        The keys are the main datacubes keys.

    signal : array like
        Image selecting valid spaxels. By default is True where `self.SSP['V']` != 0.

    pa : float
        Position Angle. By default, the ellipcity is derived based on second moments
        by the derivation of the Stokes parameters. The image used is `self.SSP['V']`.
        See `self.get_ellipse_pars()`.

    ba : float
        Ellipse axis ratio. By default, the ellipcity is derived based on second moments
        by the derivation of the Stokes parameters. The image used is `self.SSP['V']`.
        See `self.get_ellipse_pars()`.

    x0 : int
        The x coordinate of the central spaxel. By default `x0` and `y0` are defined
        by the pixel where `self.SSP['V']` is max.
        See `self.get_central_spaxel()`.

    y0 : int
        The y coordinate of the central spaxel. By default `x0` and `y0` are defined
        by the pixel where `self.SSP['V']` is max.
        See `self.get_central_spaxel()`.

    pixel_distance__yx : array like
        The distance of each pixel in pixels.

    HLR_pix : float
        The radial scale of the HLR in bins. I. e., the radius of 1 HLR in pixels.
        The HLR is derived from `self.SSP['V']`.

    pixel_distance_HLR__yx : array like
        The distance of each pixel in units of HLR.

    desc : dict
        The description of each property when disponible at the FITS header with
        the keyword UNITS_.

    Methods
    -------
    get_signal :
        Get the galaxy selection of good pixels.

    get_central_spaxel :
        Get central spaxel coordinates.

    get_ellipse_pars :
        Get the ellipcity of the galaxy based on the Stokes parameters derivation.

    set_central_spaxel :
        Set the central spaxel coordinates.
        Will recalculate ellipcity, distances and the HLR.

    set_ellipse_pars :
        Set the ellipcity parameters, i. e., position angle and the axis ratio.
        Will recalculate distances and the HLR.

    get_half_radius :
        Find the half radius of the desired property.

    radial_profile :
        Calculate the radial profile of an N-D image.

    plot_maps :
        Plot all maps stored in a datacube (or all datacubes).

    """
    def __init__(self, name, input_dir=None,
                 filename_SSP=None, filename_ELINES=None, filename_SFH=None,
                 filename_flux_elines=None, filename_flux_elines_long=None,
                 filename_indices=None):
        self.input_dir = '.' if input_dir is None else input_dir
        self.name = name
        self.ELINES = None
        self.SSP = None
        self.SFH = None
        self.flux_elines = None
        self.indices = None
        if filename_SSP is None:
            filename_SSP = f'{self.name}.SSP.cube.fits.gz'
        if filename_ELINES is None:
            filename_ELINES = f'{self.name}.ELINES.cube.fits.gz'
        if filename_SFH is None:
            filename_SFH = f'{self.name}.SFH.cube.fits.gz'
        if filename_flux_elines is None:
            filename_flux_elines = f'flux_elines.{self.name}.cube.fits.gz'
        if filename_flux_elines_long is None:
            filename_flux_elines_long = f'flux_elines_long.{self.name}.cube.fits.gz'
        if filename_indices is None:
            filename_indices = f'indices.CS.{self.name}.cube.fits.gz'
        self.filenames = {
            'SSP': f'{self.input_dir}/{filename_SSP}',
            'ELINES': f'{self.input_dir}/{filename_ELINES}',
            'SFH': f'{self.input_dir}/{filename_SFH}',
            'flux_elines': f'{self.input_dir}/{filename_flux_elines}',
            'flux_elines_long': f'{self.input_dir}/{filename_flux_elines_long}',
            'indices': f'{self.input_dir}/{filename_indices}',
        }
        self.filenames_check = {k:False for k in self.filenames.keys()}
        self.units = {}
        self.desc = {}
        self.headers = {}
        self.ids = {}
        self._check_files()
        self._read_SSP()
        self._read_ELINES()
        self._read_SFH()
        self._read_flux_elines()
        self._read_indices()
        self._init_params()
        self._init_distances()

    def _check_files(self):
        for k, v in self.filenames.items():
            if not isfile(v):
                print(f'[ReadDatacubes]: {k}: {v}: file not found')
                if k == 'SSP':
                    print('[ReadDatacubes]: missing needed file')
                    sys.exit()
            else:
                self.filenames_check[k] = True

    def _init_distances(self, image=None):
        image = self.SSP['V'] if image is None else image
        self.pixel_distance__yx = self.get_pixel_distance()
        self.HLR_pix = self.get_half_radius(image)
        self.pixel_distance_HLR__yx = self.get_pixel_distance(use_HLR_units=True)

    def _init_params(self):
        self.signal = self.get_signal()
        self.x0, self.y0 = self.get_central_spaxel()
        self.pa, self.ba = self.get_ellipse_pars()

    def set_ellipse_pars(self, pa, ba, image=None):
        """ Sets the ellipse parameters (position angle and axis ratio). Will
        change all the relative properties such as distances and `HLR_pix`.

        Parameters
        ----------
        pa : float
            Position angle.

        ba : float
            Minor-to-major axis ratio.
        """
        self.pa = pa
        self.ba = ba
        self._init_distances(image=image)

    def set_central_spaxel(self, x0, y0, image=None):
        """ Sets the central spaxel coordinates. Will change all the relative
        properties such as distances, ellipse parameters and `HLR_pix`.

        Parameters
        ----------
        x0 : int
            The x-coordinate of the central spaxel.

        y0 : int
            The y-coordinate of the central spaxel.

        See also
        --------
        :func:`get_ellipse_pars`
        """
        self.x0 = x0
        self.y0 = y0
        self.pa, self.ba = self.get_ellipse_pars(image=image)
        self._init_distances(image=image)

    def get_signal(self, image=None):
        image = self.SSP['V'] if image is None else image
        signal = np.ones_like(image, dtype='bool')
        signal[image == 0] = False
        return signal

    def get_central_spaxel(self, image=None):
        image = self.SSP['V'] if image is None else image
        y0, x0 = np.where(image == image.max())
        if len(y0) > 1:
            y0 = y0[0]
        if len(x0) > 1:
            x0 = x0[0]
        return x0, y0

    def get_ellipse_pars(self, image=None, x0=None, y0=None, mask=None):
        image = self.SSP['V'] if image is None else image
        if (x0 is None) or (y0 is None):
            x0, y0 = self.get_central_spaxel(image=image)
        return get_ellipse_pars(image, x0, y0, mask=mask)

    def radial_profile(self, prop, bin_r, rad_scale=1.0, mask=None, mode='mean', return_npts=False):
        return radial_profile(prop, bin_r, self.x0, self.y0, pa=self.pa, ba=self.ba,
                              rad_scale=rad_scale, mask=mask, mode=mode, return_npts=return_npts)

    def _read_SSP(self):
        k = 'SSP'
        r = read_SSP(self.filenames[k])
        self.SSP, self.headers[k], self.ids[k], self.desc[k], self.units[k] = r

    def _read_ELINES(self):
        k = 'ELINES'
        if self.filenames_check[k]:
            r = read_ELINES(self.filenames[k])
            self.ELINES, self.headers[k], self.ids[k], self.desc[k], self.units[k] = r

    def _read_SFH(self):
        k = 'SFH'
        if self.filenames_check[k]:
            r = read_SFH(self.filenames[k])
            self.SFH, self.headers[k], self.ids[k], self.desc[k], self.units[k], models_metainfo = r
            self.age_met_models, self.age_met_models_index, self.age_models, self.met_models = models_metainfo
            self.n_models = len(self.age_met_models)
            self.n_age = len(self.age_models)
            self.n_met = len(self.met_models)

    def _read_flux_elines(self):
        k = 'flux_elines'
        if self.filenames_check[k]:
            r = read_flux_elines(self.filenames[k])
            if r is not None:
                self.flux_elines, self.headers[k], self.ids[k], self.desc[k], self.units[k] = r
        k = 'flux_elines_long'
        if self.filenames_check[k]:
            r = read_flux_elines(self.filenames[k])
            if r is not None:
                self.flux_elines_long, self.headers[k], self.ids[k], self.desc[k], self.units[k] = r

    def _read_indices(self):
        k = 'indices'
        if self.filenames_check[k]:
            r = read_indices(self.filenames[k])
            self.indices, self.headers[k], self.ids[k], self.desc[k], self.units[k] = r

    def get_pixel_distance(self, use_HLR_units=False, pixel_scale=None, x=None, y=None, pa=None, ba=None):
        '''
        Return an image (:class:`numpy.ndarray` of same shape as :attr`qSignal`)
        of the distance from the center of the galaxy ``(x0, y0)`` in HLR units
        (default), assuming a projected disk.

        Parameters
        ----------
        use_HLR_units : boolean, optional
            Whether to use units of half light radius or pixels.

        pixel_scale : float, optional
            Pixel distance scale, used if ``use_HLR_units`` is ``False``.
            If not set, do not scale the distance.

        x : array, optional
            X coordinates to calculate the distance. If not set, the
            coordinates of the core images will be used.

        y : array, optional
            Y coordinates to calculate the distance. Must have the same
            length as ``x``. If not set, the coordinates of the core
            images will be used.

        pa : float, optional
            Position angle in radians, counter-clockwise relative
            to the positive X axis.

        ba : float, optional
            Ellipticity, defined as the ratio between the semiminor
            axis and the semimajor axis (:math:`b/a`).

        Returns
        -------
        pixel_distance : array
            Array (or image) containing the pixel distances.

        See also
        --------
        :func:`get_distance`, :func:`get_image_distance`

        '''
        if pa is None or ba is None:
            pa = self.pa
            ba = self.ba
        if x is not None or y is not None:
            pixel_distance = get_distance(x, y, self.x0, self.y0, pa, ba)
        else:
            pixel_distance = get_image_distance(self.signal.shape, self.x0, self.y0, pa, ba)
        if use_HLR_units:
            return pixel_distance / self.HLR_pix
        if pixel_scale is not None:
            return pixel_distance / pixel_scale
        return pixel_distance

    def get_half_radius(self, prop, mask=None):
        '''
        Find the half radius of the desired property. Using radial
        bins of 1 pixel, calculate the cumulative sum of ``prop``. The "half
        prop radius" is the radius where the cumulative sum reaches 50% of
        its peak value.

        Parameters
        ----------
        prop : array
            Image to get the half radius.

        mask : array(bool), optional
            Boolean array with the valid data. Defaults to ``qMask``.

        Returns
        -------
        HXR : float
            The half ``prop`` radius, in pixels.

        Notes
        -----
        This value should be close to $\dfrac{HLR_{circular}}{\sqrt{b/a}}$
        if the isophotes of the galaxy are all ellipses with parameters
        p.a. and b/a.
        '''
        if mask is None:
            mask = self.signal
        return gen_frac_radius(prop[mask], self.pixel_distance__yx[mask], frac=0.5)

    def _plot_all_maps(self):
        self._plot_SSP_maps()
        self._plot_SFH_maps()
        self._plot_ELINES_maps()
        self._plot_indices_maps()
        self._plot_flux_elines_maps()

    # def _plot_ELINES_maps(self):
    #     from matplotlib import pyplot as plt
    #     from mpl_toolkits.axes_grid1 import make_axes_locatable
    #
    #     for k, v in self.ELINES.items():
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'ELINES_{k}.pdf'
    #         unit = self.units['ELINES'][k]
    #         desc = self.desc['ELINES'][k]
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         cb.set_label(unit, fontsize=fs, labelpad=10)
    #         ax.set_title(desc, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)
    #
    # def _plot_indices_maps(self):
    #     from matplotlib import pyplot as plt
    #     from mpl_toolkits.axes_grid1 import make_axes_locatable
    #
    #     for k, v in self.indices.items():
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'indices_{k}.pdf'
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         ax.set_title(k, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)
    #
    # def _plot_SSP_maps(self):
    #     from matplotlib import pyplot as plt
    #     from mpl_toolkits.axes_grid1 import make_axes_locatable
    #
    #     for k, v in self.SSP.items():
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'SSP_{k}.pdf'
    #         unit = self.units['SSP'][k]
    #         desc = self.desc['SSP'][k]
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         cb.set_label(unit, fontsize=fs, labelpad=10)
    #         ax.set_title(desc, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)
    #
    # def _plot_flux_elines_maps(self):
    #     from matplotlib import pyplot as plt
    #     from mpl_toolkits.axes_grid1 import make_axes_locatable
    #
    #     for k, v in self.flux_elines.items():
    #         for k2, v2 in v.items():
    #             sel = (v2 != 0) & np.isfinite(v2)
    #             vmin, vmax = np.percentile(v2[sel], [2, 98])
    #             fs = 10
    #             filename = f'flux_elines_{k}_{k2}.pdf'
    #             unit = self.units['flux_elines'][k][k2]
    #             desc = self.desc['flux_elines'][k][k2]
    #             f, ax = plt.subplots()
    #             im = ax.imshow(v2, origin='lower', vmax=vmax, vmin=vmin)
    #             cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #             cb.set_label(unit, fontsize=fs, labelpad=10)
    #             ax.set_title(f'{desc} {k2}', fontsize=fs)
    #             for ax in f.axes:
    #                 ax.tick_params(axis='both', which='major', labelsize=fs)
    #             f.savefig(filename)
    #             plt.close(f)
    #
    # def _plot_SFH_maps(self):
    #     from matplotlib import pyplot as plt
    #     from mpl_toolkits.axes_grid1 import make_axes_locatable
    #     _models = self.SFH['models']
    #     n_mod = len(_models)
    #     _age = self.SFH['age']
    #     n_age = len(_age)
    #     _met = self.SFH['met']
    #     n_met = len(_met)
    #     for i in range(n_mod):
    #         v = _models[i]
    #         desc = self.desc['SFH']['models'][i]
    #         unit = self.units['SFH']['models'][i]
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'SFH_models_{i}.pdf'
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         cb.set_label(unit, fontsize=fs, labelpad=10)
    #         ax.set_title(desc, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)
    #     for i in range(n_age):
    #         v = _age[i]
    #         desc = self.desc['SFH']['models'][i]
    #         unit = self.units['SFH']['models'][i]
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'SFH_age_{i}.pdf'
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         cb.set_label(unit, fontsize=fs, labelpad=10)
    #         ax.set_title(desc, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)
    #     for i in range(n_met):
    #         v = _met[i]
    #         desc = self.desc['SFH']['models'][i]
    #         unit = self.units['SFH']['models'][i]
    #         sel = (v != 0) & np.isfinite(v)
    #         vmin, vmax = np.percentile(v[sel], [2, 98])
    #         fs = 10
    #         filename = f'SFH_met_{i}.pdf'
    #         f, ax = plt.subplots()
    #         im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
    #         cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
    #         cb.set_label(unit, fontsize=fs, labelpad=10)
    #         ax.set_title(desc, fontsize=fs)
    #         for ax in f.axes:
    #             ax.tick_params(axis='both', which='major', labelsize=fs)
    #         f.savefig(filename)
    #         plt.close(f)

    def _plot_ELINES_maps(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        for k, v in self.ELINES.items():
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_ELINES_{k}.pdf'
                unit = self.units['ELINES'][k]
                desc = self.desc['ELINES'][k]
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                cb.set_label(unit, fontsize=fs, labelpad=10)
                ax.set_title(desc, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)

    def _plot_indices_maps(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        for k, v in self.indices.items():
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_indices_{k}.pdf'
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                ax.set_title(k, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)

    def _plot_SSP_maps(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        for k, v in self.SSP.items():
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_SSP_{k}.pdf'
                unit = self.units['SSP'][k]
                desc = self.desc['SSP'][k]
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                cb.set_label(unit, fontsize=fs, labelpad=10)
                ax.set_title(desc, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)

    def _plot_flux_elines_maps(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        for k, v in self.flux_elines.items():
            for k2, v2 in v.items():
                sel = (v2 != 0) & np.isfinite(v2)
                if sel.any():
                    vmin, vmax = np.percentile(v2[sel], [2, 98])
                    fs = 10
                    filename = f'{self.name}_flux_elines_{k}_{k2}.pdf'
                    unit = self.units['flux_elines'][k][k2]
                    desc = self.desc['flux_elines'][k][k2]
                    f, ax = plt.subplots(figsize=_figsize_default)
                    im = ax.imshow(v2, origin='lower', vmax=vmax, vmin=vmin)
                    cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                    cb.set_label(unit, fontsize=fs, labelpad=10)
                    ax.set_title(f'{desc} {k2}', fontsize=fs)
                    for ax in f.axes:
                        ax.tick_params(axis='both', which='major', labelsize=fs)
                    f.savefig(filename)
                    plt.close(f)

    def _plot_SFH_maps(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        _models = self.SFH['models']
        n_mod = len(_models)
        _age = self.SFH['age']
        n_age = len(_age)
        _met = self.SFH['met']
        n_met = len(_met)
        for i in range(n_mod):
            v = _models[i]
            desc = self.desc['SFH']['models'][i]
            unit = self.units['SFH']['models'][i]
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_SFH_models_{i}.pdf'
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                cb.set_label(unit, fontsize=fs, labelpad=10)
                ax.set_title(desc, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)
        for i in range(n_age):
            v = _age[i]
            desc = self.desc['SFH']['age'][i]
            unit = self.units['SFH']['age'][i]
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_SFH_age_{i}.pdf'
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                cb.set_label(unit, fontsize=fs, labelpad=10)
                ax.set_title(desc, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)
        for i in range(n_met):
            v = _met[i]
            desc = self.desc['SFH']['met'][i]
            unit = self.units['SFH']['met'][i]
            sel = (v != 0) & np.isfinite(v)
            if sel.any():
                vmin, vmax = np.percentile(v[sel], [2, 98])
                fs = 10
                filename = f'{self.name}_SFH_met_{i}.pdf'
                f, ax = plt.subplots(figsize=_figsize_default)
                im = ax.imshow(v, origin='lower', vmax=vmax, vmin=vmin)
                cb = plt.colorbar(im, cax=make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05))
                cb.set_label(unit, fontsize=fs, labelpad=10)
                ax.set_title(desc, fontsize=fs)
                for ax in f.axes:
                    ax.tick_params(axis='both', which='major', labelsize=fs)
                f.savefig(filename)
                plt.close(f)

    def plot_maps(self, datacube=None):
        '''
        Plot all maps from desired datacube. If ``datacube`` is None, will plot
        the maps from all datacubes.

        Parameters
        ----------
        datacube : str, optional
            The name of the datacube, e.g. ELINES, SFH. Defaults to None, i.e.,
            print all maps.
        '''
        if datacube is not None:
            getattr(self, f'_plot_{datacube}_maps')()
        else:
            self._plot_all_maps()
