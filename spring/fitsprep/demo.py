from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io.fits import getdata
from matplotlib import pyplot as plt
from matplotlib.colors import SymLogNorm
from scipy.misc import imsave
from sunpy.coordinates import frames
from sunpy.map import Map
from sunpy.map import header_helper

d, h = getdata("/observations/solarnet-campaign/level0/catania/oact_halph_fi_20190708_083333.fts", header=True)
print(repr(h))
plt.imshow(d, cmap="gray")
plt.colorbar()
plt.show()

imsave("/home/rja/PythonProjects/SpringProject/spring/limbcenter/demo.jpg", d)

coord = SkyCoord(0 * u.arcsec, 0 * u.arcsec, obstime=h["DATE-OBS"], observer='earth', frame=frames.Helioprojective)

header = header_helper.make_fitswcs_header(d,
                                           coordinate=coord,
                                           reference_pixel=(h["CENTER_X"], h["CENTER_Y"]) * u.pix,
                                           scale=(h["CDELT1"] , h["CDELT2"] ) * u.arcsec / u.pix,
                                           rotation_angle=h["SOLAR_B0"] * u.deg,
                                           instrument='Barra Equatoriale',
                                           telescope='Equatorial Spar',
                                           observatory='Catania Astrophysical Observatory',
                                           wavelength=6562.80 * u.AA,
                                           exposure=h["EXP_TIME"] * u.ms)

d_map = Map(d, header)
d_map.peek(draw_grid=True)
