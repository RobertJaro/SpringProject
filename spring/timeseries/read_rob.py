import glob
import os

import pandas as pd
import pytz
from dateutil import parser, tz

from matplotlib import pyplot as plt


fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rob\\"
halpha_file = os.path.join(fp, "halpha.csv")
halpha_data = pd.read_csv(halpha_file, delimiter=",")
halpha_data["type"] = "halpha"

wl_file = os.path.join(fp, "wl.csv")
wl_data = pd.read_csv(wl_file, delimiter=",")
wl_data["type"] = "wl"

ca_file = os.path.join(fp, "ca.csv")
ca_data = pd.read_csv(ca_file, delimiter=",")
ca_data["type"] = "caIIk"

data = pd.concat([halpha_data, wl_data, ca_data], ignore_index=True, sort =False)
print(data)

converted_data = []
for fits_file, month, date, time, type in zip(data["Column9"], data["Column6"], data["Column7"], data["Column8"], data["type"]):
    if ".FTS" not in fits_file:
        print(fits_file)
        continue
    time = parser.parse(fits_file[-18:-4]) # "%s %s %s" % (date, month, time)
    time = pytz.utc.localize(time)
    converted_data.append([fits_file, time, type, 1])

converted_data = pd.DataFrame(converted_data, columns=["file", "date", "type", "quality"])
converted_data.to_csv(os.path.join(fp, "converted_ds.csv"))



