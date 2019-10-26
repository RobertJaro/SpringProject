import glob
import os
from datetime import datetime

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io.fits import getdata, getheader
from dateutil.parser import parse
from scipy.misc import imsave
from sunpy.coordinates import frames, sun
from sunpy.coordinates.sun import angular_radius
from sunpy.map import header_helper, Map

for file in glob.glob("/observations/solarnet-campaign/level0/catania/*.fts")[-5:]:
    d, h = getdata(file, header=True)
    print(repr(h))

    imsave("demo.jpg", d)
    myCmd = os.popen('/home/rja/PythonProjects/SpringProject/spring/limbcenter/sunlimb demo.jpg').read()
    center_x, center_y, radius, d_radius = map(float, myCmd.splitlines())

    obs_time = parse(h["DATE-OBS"])
    obs_type = "HALPHA"
    rsun = angular_radius(obs_time)
    b0_angle = sun.B0(obs_time)
    l0 = sun.L0(obs_time)
    p_angle = sun.P(obs_time)

    scale = rsun / (radius * u.pix)
    coord = SkyCoord(0 * u.arcsec, 0 * u.arcsec, obstime=obs_time, observer='earth', frame=frames.Helioprojective)

    header = header_helper.make_fitswcs_header(
        d, coord,
        rotation_angle=p_angle,
        reference_pixel=u.Quantity([center_x, center_y] * u.pixel),
        scale=u.Quantity([scale, scale]),
        instrument=h["INSTRUME"],
        telescope=h["TELESCOP"],
        observatory=h["OBSVTRY"],
        exposure=h["EXP_TIME"] * u.ms,
        wavelength=h["WAVELNTH"] * u.angstrom)

    filename = "oact_%s_fi_%s.fits" % (obs_type.lower(), obs_time.strftime("%Y%m%d_%H%M%S"))

    header["KEYCOMMENTS"] = {"EXPTIME": "[s] exposure time in seconds",
                             "DATE": "file creation date (YYYY-MM-DDThh:mm:ss UT)",
                             "DATE-OBS": "date of observation",
                             "DETECTOR": "camera type",
                             "WAVELNTH": "[Angstrom] wavelength",
                             "BANDPASS": "[Angstrom] filter FWHM",
                             "WAVEMIN": "[Angstrom] minimum wavelength",
                             "WAVEMAX": "[Angstrom] maximum wavelength",
                             "BZERO": "offset data range to that of unsigned short",
                             "CDELT1": "[arcsec/pix]",
                             "CDELT2": "[arcsec/pix]",
                             "SOLAR_R": "[pix]",
                             "RSUN_REF": "[m]",
                             "RSUN_ARC": "[%s]" % rsun.unit,
                             "SOLAR_P": "[%s]" % p_angle.unit,
                             "SOLAR_L0": "[%s]" % l0.unit,
                             "SOLAR_B0": "[%s]" % b0_angle.unit,
                             "QUALITY": "[1-3] image quality",
                             "EXP_MODE": "exp. mode (0=auto,1=dbl,2=fix,3=both)",
                             }

    header["FILENAME"] = filename
    header["DATE"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    header["DETECTOR"] = h["DETECTOR"]
    header["FILTER"] = h["FILTER"]
    header["BZERO"] = h["BZERO"]  # only KSO check
    header["BUNIT"] = h["BUNIT"]
    # TODO CHECK ANGLE
    # TODO check CRVAL1
    header["SOLAR_R"] = radius
    header["RSUN_ARC"] = rsun.value
    header["SOLAR_P"] = p_angle.value
    header["SOLAR_L0"] = l0.value
    header["SOLAR_B0"] = b0_angle.value
    # TODO CAR_ROT
    header["QUALITY"] = h["QUALITY"]
    header["OBS_TYPE"] = obs_type  # TODO CHECK KSO
    header["OBS_PROG"] = h["OBS_PROG"]  # TODO CHECK KSO
    header["ORIGIN"] = h["ORIGIN"]
    # TODO check TYPE-DP, PRE_INT, A_O_INT,

    header["DATAMIN"] = np.min(d)
    header["DATAMEAN"] = np.mean(d)
    header["DATAMAX"] = np.max(d)

    if "COMMENT" in h:
        header["COMMENT"] = h["COMMENT"]
    if "HISTORY" in h:
        header["HISTORY"] = h["HISTORY"]

    s_map = Map(d.astype(np.float32), header)
    s_map.save(filename, overwrite=True)
    print("###############################################################")
    print(repr(getheader(filename)))

    # s_map = s_map.rotate(recenter=True, scale=1, missing=s_map.min())
    # s_map.plot()
    # s_map.draw_limb()
    # s_map.draw_grid()
    # pyplot.savefig("res.jpg")
    break
