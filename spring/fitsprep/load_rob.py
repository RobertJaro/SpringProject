import glob
import os
import shutil

# for f in glob.glob("/observations/solarnet-campaign/ftp-as.oma.be/pub/astro/Bechet.S/*.tar.gz", recursive=True):
#     with tarfile.open(f, 'r:gz') as zip_ref:
#         zip_ref.extractall("/observations/solarnet-campaign/level0/rob")

for f in glob.glob(
        "/observations/solarnet-campaign/level0/rob/07/**/*.FTS",
        recursive=True):
    print(f)
    shutil.move(f, "/observations/solarnet-campaign/level0/rob/%s" % os.path.basename(f))
