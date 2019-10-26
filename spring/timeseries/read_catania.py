import glob
import os

import pandas as pd
import pytz
from dateutil import parser, tz

from matplotlib import pyplot as plt


fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\catania\\"
df = [pd.read_csv(file, delimiter=" ", names=["file", "date", "time", "tz"])
      for file in glob.glob(os.path.join(fp , "*.txt"))]
data = pd.concat(df, ignore_index=True, sort =False)

converted_data = []
for fits_file in data.file:
    time = parser.parse(fits_file[-19:-4].replace("_", "T"))
    time = pytz.utc.localize(time)
    type = fits_file[28:32]
    if type != "halp":
        print(fits_file)
    converted_data.append([fits_file, time, "halpha", 1])

converted_data = pd.DataFrame(converted_data, columns=["file", "date", "type", "quality"])
converted_data.to_csv(os.path.join(fp, "converted_ds.csv"))



