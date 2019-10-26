import datetime
import os

import pandas as pd
from matplotlib import pyplot as plt, dates
from pytz import UTC

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rob\\"
converted_data = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)
df = converted_data.groupby(converted_data.date.dt.day)

plt.figure(figsize=(12, 15))
for i, (group, day) in enumerate(df):
    plt.subplot(len(df), 1, i + 1)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.type == "halpha"].date, 2, 3, color="red", label="Halpha")
    plt.vlines(day[day.type == "wl"].date, 1, 2, color="green", label="White Light")
    plt.vlines(day[day.type == "caIIk"].date, 0, 1, color="blue", label="Ca II K")
    plt.ylim((0, 3))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    sunrise = datetime.datetime(2019, 7, group, 3, 19, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 59, tzinfo=UTC)

    plt.vlines(sunrise, ymin=0, ymax=3, linewidth=5, colors="yellow")
    plt.text(sunrise, 1.5, "Sunrise ROB", rotation=90, verticalalignment="center", fontsize=6)

    plt.vlines(sunset, ymin=0, ymax=3, linewidth=5, colors="yellow")
    plt.text(sunset, 1.5, "Sunset ROB", rotation=90, verticalalignment="center", fontsize=6)

    if i == 0:
        plt.legend(bbox_to_anchor=(1.0, 1.1), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rob_overview.png")