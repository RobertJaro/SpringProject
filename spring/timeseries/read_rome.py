import glob
import os

import pandas as pd
import pytz
from dateutil import parser, tz

from matplotlib import pyplot as plt


fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rome\\"
file = os.path.join(fp, "data.csv")
data = pd.read_csv(file, delimiter=" ")
print(data)

converted_data = []
for fits_file, ut in zip(data.file, data.UT):
    time = parser.parse(fits_file[-15:-7] +"T" + ut)
    time = pytz.utc.localize(time)
    type = fits_file[9:14]
    if type != "CaIIK":
        print(fits_file)
    converted_data.append([fits_file, time, type, 1])

converted_data = pd.DataFrame(converted_data, columns=["file", "date", "type", "quality"])
converted_data.to_csv(os.path.join(fp, "converted_ds.csv"))



