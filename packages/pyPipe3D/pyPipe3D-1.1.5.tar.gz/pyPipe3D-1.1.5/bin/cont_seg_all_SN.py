#!/usr/bin/env python3
################################################################################
#
# cont_seg_all_SN.py
# ----------------------
# Perl script: cont_seg_all_SN.pl
#
################################################################################

# System imports
import sys
from os.path import basename

# Local imports
from pyFIT3D.common.io import ReadArguments
from pyFIT3D.common.io import get_data_from_fits, array_to_fits
from pyFIT3D.common.tools import cont_seg_all_SN

class ReadArgumentsLocal(ReadArguments):
    """
    Argument parser for this script
    """
    __script_name__ = basename(sys.argv[0])
    __mandatory__ = ['signoise_fits', 'flux_limit_peak', 'targetmin_SN', 'frac_peak', 'min_flux',
                     'segmentation_fits', 'diffuse_mask_fits']
    __arg_names__ = __mandatory__
    __N_tot_args__ = len(__arg_names__)
    __conv_func_mandatory__ = {'signoise_fits': str, 'segmentation_fits': str, 'diffuse_mask_fits': str}
    __conv_func__ = __conv_func_mandatory__.copy()

    usage_msg_tmp1 = 'USE: {}'.format(__script_name__)
    usage_msg_tmp2 = ' signal.fits,noise.fits FLUX_LIMIT_PEAK TARGET_SN,MIN_SN FRAC_PEAK MIN_FLUX SEGFILE.fits DIFFUSE_MASK.fits'
    __usage_msg__ = usage_msg_tmp1 + usage_msg_tmp2

    def __init__(self, args_list=None, verbose=False):
        ReadArguments.__init__(self, args_list, verbose=verbose)
        self.target_SN = self.targetmin_SN[0]
        self.min_SN = self.targetmin_SN[1]
        self.signal_fits = self.signoise_fits.split(',')[0]
        self.noise_fits = self.signoise_fits.split(',')[1]

def main(args):
    Ha_map__yx = get_data_from_fits(args.signal_fits)
    e_Ha_map__yx = get_data_from_fits(args.noise_fits)
    seg_map__yx, mask_map__yx = cont_seg_all_SN(Ha_map__yx, e_Ha_map__yx,
                                                args.flux_limit_peak,
                                                args.target_SN,
                                                args.min_SN,
                                                args.frac_peak,
                                                args.min_flux)
    array_to_fits(filename=args.segmentation_fits, arr=seg_map__yx, overwrite=True)
    array_to_fits(filename=args.diffuse_mask_fits, arr=mask_map__yx, overwrite=True)

if __name__ == '__main__':
    main(ReadArgumentsLocal())
    # sys.exit()
    # cont_seg_all_SN(parsed_args.signal_fits, parsed_args.noise_fits,
    #                 parsed_args.flux_limit_peak, parsed_args.target_SN,
    #                 parsed_args.min_SN, parsed_args.frac_peak, parsed_args.min_flux,
    #                 parsed_args.segmentation_fits, parsed_args.diffuse_mask_fits)
