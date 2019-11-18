import glob
import os
from datetime import datetime

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io.fits import getheader
from dateutil.parser import parse
from matplotlib import pyplot as plt
from scipy.misc import imsave
from sunpy.coordinates import frames, sun
from sunpy.coordinates.sun import angular_radius
from sunpy.map import header_helper, Map
from tqdm import tqdm


def padScale(s_map):
    data = s_map.data
    new_meta = s_map.meta
    missing = s_map.min()


    diff = np.asarray(np.ceil((2048 - np.array(data.shape)) / 2), dtype=int).ravel()
    # Pad the image array
    pad_x = int(np.max((diff[1], 0)))
    pad_y = int(np.max((diff[0], 0)))

    new_data = np.pad(data,
                      ((pad_y, pad_y), (pad_x, pad_x)),
                      mode='constant',
                      constant_values=(missing, missing))
    new_meta['crpix1'] += pad_x
    new_meta['crpix2'] += pad_y

    return Map(new_data, new_meta)


def prepData(files, base_dir, prefix, custom_keywords={}):
    diffs = {'center_x': [], 'center_y': [], 'radius': [], 'scale': []}
    os.makedirs(os.path.join(base_dir, 'level1'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'level1_5'), exist_ok=True)
    for file in tqdm(files):
        # load existing file
        hdul = fits.open(file)
        hdu = hdul[0]
        hdu.verify('fix')
        d, h = hdu.data, hdu.header
        print('ORIGINAL ##################################')
        print(repr(h))
        print('###########################################')

        # set custom keywords
        h.update(custom_keywords)

        # evaluate center and radius
        imsave("demo.jpg", d)
        myCmd = os.popen('/home/rja/PythonProjects/SpringProject/spring/limbcenter/sunlimb demo.jpg').read()
        center_x, center_y, radius, d_radius = map(float, myCmd.splitlines())

        if "EXPTIME" in h:
            h['EXP_TIME'] = h['EXPTIME']
            del h['EXPTIME']
        if 'TIME-OBS' in h:
            obs_date = datetime.strptime(h['DATE-OBS'] + 'T' + h['TIME-OBS'], "%m/%d/1%yT%H:%M:%S")
            h['DATE-OBS'] = obs_date.isoformat()
            del h["TIME-OBS"]
        if 'TIME' in h:
            obs_date = datetime.strptime(h['DATE-OBS'] + 'T' + h['TIME'], "%d/%m/%YT%H:%M:%S")
            h['DATE-OBS'] = obs_date.isoformat()
            del h["TIME"]

        obs_time = parse(h["DATE-OBS"])
        rsun = angular_radius(obs_time)
        b0_angle = sun.B0(obs_time)
        l0 = sun.L0(obs_time)
        p_angle = sun.P(obs_time)
        filename = "%s_%s_fi_%s.fits" % (prefix, h["OBS_TYPE"].lower(), obs_time.strftime("%Y%m%d_%H%M%S"))

        # prepare existing header information
        if "ANGLE" not in h:
            h["ANGLE"] = p_angle.value


        scale = rsun / (radius * u.pix)
        coord = SkyCoord(0 * u.arcsec, 0 * u.arcsec, obstime=obs_time, observer='earth', frame=frames.Helioprojective)

        # create WCS header info
        header = header_helper.make_fitswcs_header(
            d, coord,
            rotation_angle=h["ANGLE"] * u.deg,
            reference_pixel=u.Quantity([center_x, center_y] * u.pixel),
            scale=u.Quantity([scale, scale]),
            instrument=h["INSTRUME"],
            telescope=h["TELESCOP"],
            observatory=h["OBSVTRY"],
            exposure=h["EXP_TIME"] * u.ms,
            wavelength=h["WAVELNTH"] * u.angstrom)

        header["KEYCOMMENTS"] = {"EXPTIME": "[s] exposure time in seconds",
                                 "DATE": "file creation date (YYYY-MM-DDThh:mm:ss UT)",
                                 "DATE-OBS": "date of observation",
                                 "WAVELNTH": "[Angstrom] wavelength",
                                 "BANDPASS": "[Angstrom] filter FWHM",
                                 "WAVEMIN": "[Angstrom] minimum wavelength",
                                 "WAVEMAX": "[Angstrom] maximum wavelength",
                                 "BZERO": "offset data range to that of unsigned short",
                                 "CDELT1": "[arcsec/pix]",
                                 "CDELT2": "[arcsec/pix]",
                                 "SOLAR_R": "[pix]",
                                 "DSUN_OBS": "[m]",
                                 "RSUN_REF": "[m]",
                                 "RSUN_ARC": "[%s]" % rsun.unit,
                                 "ANGLE": "[deg]",
                                 "SOLAR_P": "[%s]" % p_angle.unit,
                                 "SOLAR_L0": "[%s]" % l0.unit,
                                 "SOLAR_B0": "[%s]" % b0_angle.unit,
                                 'SIMPLE': 'file does conform to FITS standard',
                                 'BITPIX': 'number of bits per data pixel',
                                 'CUNIT1': '[arcsec]',
                                 'CUNIT2': '[arcsec]',
                                 'CRVAL1': 'coordinate system value at reference pixel',
                                 'CRVAL2': 'coordinate system value at reference pixel',
                                 'CTYPE1': 'name of the coordinate axis',
                                 'CTYPE2': 'name of the coordinate axis',
                                 'INSTRUME': 'name of instrument',
                                 'TELESCOP': 'name of telescope',
                                 'OBSRVTRY': 'name of observatory',
                                 }

        # set constants and default values
        header["FILENAME"] = filename
        header["DATE"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        header["SOLAR_R"] = radius
        header["RSUN_ARC"] = rsun.value
        header["SOLAR_P"] = p_angle.value
        header["SOLAR_L0"] = l0.value
        header["SOLAR_B0"] = b0_angle.value

        header["DATAMIN"] = np.min(d)
        header["DATAMEAN"] = np.mean(d)
        header["DATAMAX"] = np.max(d)

        # copy existing keys
        for key, value in h.items():
            if key not in header:
                header[key] = value

        # copy comments
        for key, value in zip(list(h.keys()), list(h.comments)):
            if key not in header["KEYCOMMENTS"]:
                print(key)
                header["KEYCOMMENTS"][key] = value

        # LEVEL 1
        s_map = Map(d.astype(np.float32), header)
        level1_path = os.path.join(base_dir, 'level1', filename)

        h.add_history("unified FITS header")
        s_map.meta["HISTORY"] = h["HISTORY"]
        s_map.meta["LVL_NUM"] = "1.0"
        s_map = Map(s_map.data.astype(np.float32), s_map.meta)
        s_map.save(level1_path, overwrite=True)

        # LEVEL 1.5
        scale = s_map.scale[0].value
        s_map = padScale(s_map)

        s_map = s_map.rotate(recenter=True, scale=scale, missing=s_map.min(), )
        center = np.floor(s_map.meta['crpix1'])
        range_side = (center + np.array([-1, 1]) * 2048 / 2) * u.pix
        s_map = s_map.submap(u.Quantity([range_side[0], range_side[0]]),
                             u.Quantity([range_side[1], range_side[1]]))
        level1_5_path = os.path.join(base_dir, 'level1_5', filename)

        h.add_history("recentered and derotated")
        s_map.meta["HISTORY"] = h["HISTORY"]
        s_map.meta["LVL_NUM"] = "1.5"
        s_map = Map(s_map.data.astype(np.float32), s_map.meta)
        s_map.save(level1_5_path, overwrite=True)

        s_map.plot()
        s_map.draw_grid()
        plt.savefig(level1_5_path.replace(".fits", ".jpg"))
        plt.close()

        print(repr(getheader(level1_5_path)))

        # evaluate difference
        if 'center_x' in h and not isinstance(h["center_x"], str):
            diffs['center_x'].append(np.abs(h['center_x'] - header['crpix1']))
        if 'center_y' in h and not isinstance(h["center_y"], str):
            diffs['center_y'].append(np.abs(h['center_y'] - header['crpix2']))
        if 'SOLAR_R' in h and not isinstance(h["SOLAR_R"], str):
            diffs['radius'].append(np.abs(h['SOLAR_R'] - header['SOLAR_R']))
        if 'cdelt1' in h and not isinstance(h["cdelt1"], str):
            diffs['scale'].append(np.abs(h['cdelt1'] - header['cdelt1']))
    return diffs


if __name__ == '__main__':
    # KSO
    files = glob.glob("/observations/solarnet-campaign/level0/kso/*.fts.gz")[:1]
    base_dir = "/localdata/USER/rja/solarnet"
    os.makedirs(os.path.join(base_dir, 'kso'), exist_ok=True)

    diffs = prepData(files, base_dir, prefix='kanz')
    np.save(os.path.join(base_dir, 'kso', 'diffs'), diffs)

    print('Center-X', np.mean(diffs["center_x"]))
    print('Center-Y', np.mean(diffs["center_y"]))
    print('Radius', np.mean(diffs["radius"]))
    print('Scale', np.mean(diffs["scale"]))

    # OACT

    # files = glob.glob("/observations/solarnet-campaign/level0/catania/*.fts")[:1]
    # base_dir = "/localdata/USER/rja/solarnet"
    # os.makedirs(os.path.join(base_dir, 'oact'), exist_ok=True)
    #
    # diffs = prepData(files, base_dir, prefix='oact', custom_keywords={'OBS_TYPE': "halph", })
    # np.save(os.path.join(base_dir, 'oact', 'diffs'), diffs)
    #
    # print('Center-X', np.mean(diffs["center_x"]))
    # print('Center-Y', np.mean(diffs["center_y"]))
    # print('Radius', np.mean(diffs["radius"]))
    # print('Scale', np.mean(diffs["scale"]))
    #
    #
    # # PSPT
    # files = glob.glob("/observations/solarnet-campaign/level0/rome/*.ffc")[:1]
    # base_dir = "/localdata/USER/rja/solarnet"
    # os.makedirs(os.path.join(base_dir, 'pspt'), exist_ok=True)
    #
    # diffs = prepData(files, base_dir, prefix='pspt', custom_keywords={'OBS_TYPE': "caiik",
    #                                                                   'INSTRUME': '',
    #                                                                   'TELESCOP': '',
    #                                                                   'OBSVTRY': '',
    #                                                                   'WAVELNTH':0})
    # np.save(os.path.join(base_dir, 'pspt', 'diffs'), diffs)
    #
    # print('Center-X', np.mean(diffs["center_x"]))
    # print('Center-Y', np.mean(diffs["center_y"]))
    # print('Radius', np.mean(diffs["radius"]))
    # print('Scale', np.mean(diffs["scale"]))
    #
    # # ROB - caiik
    # files = glob.glob("/observations/solarnet-campaign/level0/rob/UCC*.FTS")[:1]
    # base_dir = "/localdata/USER/rja/solarnet"
    # os.makedirs(os.path.join(base_dir, 'rob'), exist_ok=True)
    #
    # diffs = prepData(files, base_dir, prefix='rob', custom_keywords={'OBS_TYPE':'caiik',
    #                                                                  'OBSVTRY': 'ROB',
    #                                                                  'WAVELNTH': 0})
    # np.save(os.path.join(base_dir, 'rob', 'diffs_caiik'), diffs)
    #
    # print('Center-X', np.mean(diffs["center_x"]))
    # print('Center-Y', np.mean(diffs["center_y"]))
    # print('Radius', np.mean(diffs["radius"]))
    # print('Scale', np.mean(diffs["scale"]))
    #
    # # ROB - h-alpha
    # files = glob.glob("/observations/solarnet-campaign/level0/rob/UCH*.FTS")[:1]
    # base_dir = "/localdata/USER/rja/solarnet"
    # os.makedirs(os.path.join(base_dir, 'rob'), exist_ok=True)
    #
    # diffs = prepData(files, base_dir, prefix='rob', custom_keywords={'OBS_TYPE': 'halph',
    #                                                                  'OBSVTRY': 'ROB',
    #                                                                  'WAVELNTH': 0})
    # np.save(os.path.join(base_dir, 'rob', 'diffs_halph'), diffs)
    #
    # print('Center-X', np.mean(diffs["center_x"]))
    # print('Center-Y', np.mean(diffs["center_y"]))
    # print('Radius', np.mean(diffs["radius"]))
    # print('Scale', np.mean(diffs["scale"]))
    #
    # # ROB - white light
    # files = glob.glob("/observations/solarnet-campaign/level0/rob/UPH*.FTS")[:1]
    # base_dir = "/localdata/USER/rja/solarnet"
    # os.makedirs(os.path.join(base_dir, 'rob'), exist_ok=True)
    #
    # diffs = prepData(files, base_dir, prefix='rob', custom_keywords={'OBS_TYPE': 'bband',
    #                                                                  'OBSVTRY': 'ROB',
    #                                                                  'WAVELNTH': 0})
    # np.save(os.path.join(base_dir, 'rob', 'diffs_bband'), diffs)
    #
    # print('Center-X', np.mean(diffs["center_x"]))
    # print('Center-Y', np.mean(diffs["center_y"]))
    # print('Radius', np.mean(diffs["radius"]))
    # print('Scale', np.mean(diffs["scale"]))