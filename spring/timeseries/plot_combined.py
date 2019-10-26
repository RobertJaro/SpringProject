import datetime
import os

import pandas as pd
from matplotlib import pyplot as plt, dates
from pytz import UTC

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\kso\\"
kso_df = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)
kso_df["observatory"] = "kso"

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\catania\\"
catania_df = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)
catania_df["observatory"] = "catania"

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rome\\"
rome_df = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)
rome_df["observatory"] = "rome"

fp = "C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\rob\\"
rob_df = pd.read_csv(os.path.join(fp, "converted_ds.csv"), parse_dates=['date'], index_col=0)
rob_df["observatory"] = "rob"

full_df = pd.concat([kso_df, catania_df, rome_df, rob_df])
full_df = full_df.sort_values("date")
full_df.to_csv("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\data_set.csv", index=False)

df = full_df[full_df.type == "halpha"]
df = df.groupby(df.date.dt.day)


def plotSun(sunrise, sunset, observatory):
    plt.vlines(sunrise, ymin=0, ymax=3, linewidth=7, colors="yellow")
    plt.text(sunrise, 1.5, "Sunrise %s" % observatory, rotation=90, verticalalignment="center", fontsize=4)
    plt.vlines(sunset, ymin=0, ymax=3, linewidth=7, colors="yellow")
    plt.text(sunset, 1.5, "Sunset %s" % observatory, rotation=90, verticalalignment="center", fontsize=4)

plt.figure(figsize=(11, 19))
plt.suptitle('Overview - H-alpha')
for i, (group, day) in enumerate(df):
    plt.subplot(len(df) + 1, 1, i + 2)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.observatory == "kso"].date, 0, 1, color="red", label="KSO")
    plt.vlines(day[day.observatory == "catania"].date, 1, 2, color="black", label="Catania")
    plt.vlines(day[day.observatory == "rob"].date, 2, 3, color="blue", label="ROB")
    plt.ylim((0, 3))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    sunrise = datetime.datetime(2019, 7, group, 3, 19, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 59, tzinfo=UTC)
    plotSun(sunrise, sunset, "KSO")

    sunrise = datetime.datetime(2019, 7, group, 3, 46, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 24, tzinfo=UTC)
    plotSun(sunrise, sunset, "Catania")

    sunrise = datetime.datetime(2019, 7, group, 3, 39, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 19, 56, tzinfo=UTC)
    plotSun(sunrise, sunset, "ROB")

    if i == 0:
        plt.legend(bbox_to_anchor=(1, 1), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.8, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\halpha_overview.png", dpi=300)

df = full_df[full_df.type == "caIIk"]
df = df.groupby(df.date.dt.day)

plt.figure(figsize=(11, 19))
plt.suptitle('Overview - Ca-II-K')
for i, (group, day) in enumerate(df):
    plt.subplot(len(df) + 1, 1, i + 2)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.observatory == "kso"].date, 0, 1, color="red", label="KSO")
    plt.vlines(day[day.observatory == "rome"].date, 1, 2, color="green", label="Rome")
    plt.vlines(day[day.observatory == "rob"].date, 2, 3, color="blue", label="ROB")
    plt.ylim((0, 3))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    sunrise = datetime.datetime(2019, 7, group, 3, 19, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 59, tzinfo=UTC)
    plotSun(sunrise, sunset, "KSO")

    sunrise = datetime.datetime(2019, 7, group, 3, 42, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 47, tzinfo=UTC)
    plotSun(sunrise, sunset, "Rome")

    sunrise = datetime.datetime(2019, 7, group, 3, 39, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 19, 56, tzinfo=UTC)
    plotSun(sunrise, sunset, "ROB")

    if i == 0:
        plt.legend(bbox_to_anchor=(1, 1), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\caIIk_overview.png", dpi=300)


df = full_df[full_df.type == "wl"]
df = df.groupby(df.date.dt.day)

plt.figure(figsize=(11, 19))
plt.suptitle('Overview - White Light')
for i, (group, day) in enumerate(df):
    plt.subplot(len(df) + 1, 1, i + 2)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.observatory == "kso"].date, 1.5, 3, color="red", label="KSO")
    plt.vlines(day[day.observatory == "rob"].date, 0, 1.5, color="blue", label="ROB")
    plt.ylim((0, 3))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    sunrise = datetime.datetime(2019, 7, group, 3, 19, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 18, 59, tzinfo=UTC)
    plotSun(sunrise, sunset, "KSO")

    sunrise = datetime.datetime(2019, 7, group, 3, 39, tzinfo=UTC)
    sunset = datetime.datetime(2019, 7, group, 19, 56, tzinfo=UTC)
    plotSun(sunrise, sunset, "ROB")

    if i == 0:
        plt.legend(bbox_to_anchor=(1, 1), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\wl_overview.png", dpi=300)