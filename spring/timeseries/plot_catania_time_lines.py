import datetime
import os

import pandas as pd
from matplotlib import pyplot as plt, dates
from pytz import UTC

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\catania\\"
converted_data = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)

df = converted_data.groupby(converted_data.date.dt.day)

plt.figure(figsize=(12, 15))
for i, (group, day) in enumerate(df):
    plt.subplot(len(df), 1, i + 1)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.type == "halp"].date, 0, 1, color="black")
    plt.ylim((0, 1))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    sunrise = datetime.datetime(2019, 7, group, 3, 46, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 24, tzinfo=UTC)

    plt.vlines(sunrise, ymin=0, ymax=1, linewidth=5, colors="yellow")
    plt.text(sunrise, .5, "Sunrise Catania", rotation=90, verticalalignment="center")

    plt.vlines(sunset, ymin=0, ymax=1, linewidth=5, colors="yellow")
    plt.text(sunset, .5, "Sunset Catania", rotation=90, verticalalignment="center")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\catania_overview.png")