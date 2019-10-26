from astropy.io.fits import getdata

print("CATANIA###############################################################################################")
d, h = getdata("/observations/solarnet-campaign/level0/catania/oact_halph_fi_20190708_083333.fts", header=True)
print(repr(h))

print("ROME###############################################################################################")
d, h = getdata("/observations/solarnet-campaign/level0/rome/pspt_oar_CaIIK_20190708_072728.ffc", header=True)
print(repr(h))

print("KSO################################################################################################")
d, h = getdata("/observations/solarnet-campaign/level0/kso/kanz_bband_fi_20190710_120729.fts.gz", header=True)
print(repr(h))