import zipfile
import glob

for f in glob.glob("/observations/solarnet-campaign/homogenization/rome/**/*.zip", recursive=True):
    with zipfile.ZipFile(f, 'r') as zip_ref:
        zip_ref.extractall("/observations/solarnet-campaign/homogenization/rome")