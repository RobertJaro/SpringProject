import glob
import os
import shutil

target_path = "/observations/solarnet-campaign/homogenization/catania"
os.makedirs(target_path, exist_ok=True)

for f in glob.glob("/observations/solarnet-campaign/ftp.oact.inaf.it/Romano/SOLARNET_SPRING/**/*.fts", recursive=True):
    shutil.move(f, os.path.join(target_path, os.path.basename(f)))
