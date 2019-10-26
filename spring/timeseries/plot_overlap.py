import datetime
import os

import pandas as pd
import pytz
from matplotlib import pyplot as plt, dates
from pytz import UTC

full_df = pd.read_csv("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\data_set.csv",parse_dates=['date'])

df = full_df[full_df.type == "halpha"]
df = df[(df.date > pytz.utc.localize(datetime.datetime(2019, 7, 17))) & (df.date < pytz.utc.localize(datetime.datetime(2019, 7, 20)))]
df = df.groupby(df.date.dt.day)

plt.figure(figsize=(10, 5))
plt.suptitle('Overlap - H-alpha')
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

    if i == 0:
        lgd = plt.legend(bbox_to_anchor=(1.15, 1.15), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.8, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\halpha_overlap.png", dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

df = full_df[full_df.type == "caIIk"]
df = df[(df.date > pytz.utc.localize(datetime.datetime(2019, 7, 17))) & (df.date < pytz.utc.localize(datetime.datetime(2019, 7, 20)))]
df = df.groupby(df.date.dt.day)

plt.figure(figsize=(10, 5))
plt.suptitle('Overlap - Ca-II-K')
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

    if i == 0:
        lgd = plt.legend(bbox_to_anchor=(1.15, 1.15), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.8, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\ca_overlap.png", dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

df = full_df[full_df.type == "wl"]
df = df[(df.date > pytz.utc.localize(datetime.datetime(2019, 7, 17))) & (df.date < pytz.utc.localize(datetime.datetime(2019, 7, 20)))]
df = df.groupby(df.date.dt.day)

plt.figure(figsize=(10, 5))
plt.suptitle('Overlap - White Light')
for i, (group, day) in enumerate(df):
    plt.subplot(len(df) + 1, 1, i + 2)
    plt.title(datetime.date(2019, 7, group))
    type_group = day.groupby(day.type)

    plt.vlines(day[day.observatory == "kso"].date, 0, 1.5, color="red", label="KSO")
    plt.vlines(day[day.observatory == "rob"].date, 1.5, 3, color="blue", label="ROB")
    plt.ylim((0, 3))
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    if i == 0:
        lgd = plt.legend(bbox_to_anchor=(1.15, 1.15), loc="upper right")

    plt.yticks([])
plt.tight_layout(pad=0.4, w_pad=0.8, h_pad=.8)
plt.savefig("C:\\Users\\Robert\\Documents\\Uni\\SOLARNET\\HomogenizationCampaign\\wl_overlap.png", dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')