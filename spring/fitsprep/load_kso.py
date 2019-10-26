import glob
import os
import shutil
from datetime import datetime, timedelta

days = [datetime(2019, 7, 8) + timedelta(days=i) for i in range(16)]
target_path = "/observations/solarnet-campaign/kso"
os.makedirs(target_path, exist_ok=True)

for type in ["caii", "halpha3", "phokad"]:
    for date in days:
        for file in glob.glob(
                "/observations/%s/archive/2019/2019%02d%02d/processed/*.fts.gz" % (type, date.month, date.day)):
            shutil.copy(file, os.path.join(target_path, os.path.basename(file)))
