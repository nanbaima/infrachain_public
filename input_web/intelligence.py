# data:
# solar fcst
import pandas as pd
import numpy as np
import requests


dir = "data"
agg_gen_files = [
    "2022_01_DayAheadAggregatedGeneration_14.1.C.csv",
    "2022_04_DayAheadAggregatedGeneration_14.1.C.csv",
    # "2022_07_DayAheadAggregatedGeneration_14.1.C.csv",
]
re_gen_files = [
    "2022_01_DayAheadGenerationForecastForWindAndSolar_14.1.D.csv",
    "2022_04_DayAheadGenerationForecastForWindAndSolar_14.1.D.csv",
    # "2022_07_DayAheadGenerationForecastForWindAndSolar_14.1.D.csv"
]


def get_ac_hour_num(t, insulation_factor=.5, max_ac_num=20):
    # handle temperature information
    target_t = 20
    assert 0 <= t and t <= 40
    abs_t_delta = abs(t - target_t)
    t_factor=(abs_t_delta / 20)

    # combine temperature and insulation factor
    total_factor=((t_factor+(1-insulation_factor))/2)** 1.5#.5#1.5

    # compute number of hours based on total factor
    #ac_hour_num = int((abs_t_delta / 20) ** 1.5 * max_ac_num)
    ac_hour_num=int(total_factor*max_ac_num)

    return max(1,ac_hour_num)


def analyse_re(re_df, agg_gen_s, day=None):
    # pv
    pv_idxs = re_df["ProductionType"] == "Solar"
    pv_df = re_df[pv_idxs]
    # if day is not None:
    #     pv_day_idxs=pv_df.index.day==day
    #     pv_df=re_df[pv_day_idxs]
    pv_gen_s = (
        pv_df["AggregatedGenerationForecast"]
        .groupby(pv_df.reset_index().index // 4)
        .sum()
        / 4
    )
    pv_share_s = pv_gen_s / agg_gen_s

    # wind
    wind_idxs = (re_df["ProductionType"] == "Wind Onshore") | (
        re_df["ProductionType"] == "Wind Offshore"
    )
    wind_df = re_df[wind_idxs]
    # if day is not None:
    #     wind_day_idxs=wind_df.index.day==day
    #     wind_df=wind_df[wind_day_idxs]
    wind_gen_s = (
        wind_df["AggregatedGenerationForecast"]
        .groupby(wind_df.reset_index().index // 8)
        .sum()
        / 4
    )
    wind_share_s = wind_gen_s / agg_gen_s

    # all re
    re_share = pv_share_s + wind_share_s

    return pv_share_s, wind_share_s, re_share


def optimize_hours(re_share_s, ac_hour_num):
    sorted_idxs = [
        idx for _, idx in sorted(sorted(zip(re_share_s, range(len(re_share_s)))))
    ]
    ac_on = [False] * len(re_share_s)
    for idx in sorted_idxs[-ac_hour_num:]:
        ac_on[idx] = True
    return ac_on


def get_bc_data(ac_on, re_share, re_share_increase):
    ac_on_str = ""
    re_share_str = ""

    for val in ac_on:
        ac_on_str += ["off", "on"][val]
        ac_on_str += ","

    for val in re_share:
        re_share_str += str(int(val * 100))
        re_share_str += ","

    re_share_increase_str = str(int(re_share_increase * 100))

    return ac_on_str[:-1], re_share_str[:-1], re_share_increase_str


def get_re_share_increase(re_share, ac_on):
    re_share_increase = np.average(re_share, weights=ac_on) / np.average(re_share) - 1
    #print(re_share_increase)
    return re_share_increase


def push_to_sc(ac_on_str, re_share_str, re_share_increase_str):
    # push all values to smart contract
    r = requests.get(
        "http://localhost:8888/push_schedule?key=e25b1a9e-0999-406a-a910-3e9a3f0cca2d&values="
        + ac_on_str
    )
    r = requests.get(
        "http://localhost:8888/push_renewable_share?key=rs_281ec91d-d143-4c04-ae78-645f2129f23d&data="
        + re_share_str
    )
    r = requests.get(
        "http://localhost:8888/push_total_energy_saved?key=t_c04e2ea6-f487-407a-b04b-a52fd25cb3db&value="
        + re_share_increase_str
    )
    #print(r.text)

    # print("uncomment push requests!!!")


def magic_time(t, scenario, insulation_factor=1):
    agg_dfs = list()
    re_dfs = list()
    for f_agg, f_re in zip(agg_gen_files, re_gen_files):
        # read aggregated generation
        agg_df = (
            pd.read_csv(
                dir + "/" + f_agg,
                parse_dates=["DateTime"],
                sep="\t",
            )
            .set_index("DateTime")
            .sort_values(["DateTime"])
        )
        idxs_agg = agg_df["MapCode"] == "DE"
        agg_df = agg_df[idxs_agg]
        agg_dfs.append(agg_df)

        # read planned renewable generation
        re_df = (
            pd.read_csv(
                dir + "/" + f_re,
                parse_dates=["DateTime"],
                sep="\t",
            )
            .set_index("DateTime")
            .sort_values(["DateTime"])
        )
        idxs_re = re_df["MapCode"] == "DE"
        re_df = re_df[idxs_re]
        re_dfs.append(re_df)

    month_idx = [0, 0, 1][scenario]
    day = [1, 30, 30][scenario]
    # get scenarios
    # for i, day in zip([0,0,1], [1,30,30]):
    re_df = re_dfs[month_idx]
    agg_df = agg_dfs[month_idx]

    # filter by day
    re_idxs = re_df.index.day == day
    agg_idxs = agg_df.index.day == day

    # analyse re production
    pv_share_s, wind_share_s, re_share = analyse_re(
        re_df[re_idxs], agg_df[agg_idxs]["ScheduledGeneration"].values, day
    )

    # print info
    # print("month:", i)
    # print("day:", day)
    # print(list(pv_share_s))
    # print(list(wind_share_s))
    # print(list(re_share))
    # print([str(i) for i in agg_df[agg_idxs].index.to_list()])
    # print("_______________________")
    ac_hour_num = get_ac_hour_num(t, insulation_factor)
    # print(ac_hour_num)

    ac_on = optimize_hours(re_share, ac_hour_num)

    re_share_increase = get_re_share_increase(re_share, ac_on)

    ac_on_str, re_share_str, re_share_increase_str = get_bc_data(
        ac_on, re_share, re_share_increase
    )
    # print(re_share_increase_str)
    push_to_sc(ac_on_str, re_share_str, re_share_increase_str)

    print(ac_on_str, re_share_str, re_share_increase_str)


#t = 40
#print(magic_time(t, 0))
#print(magic_time(t, 1))
#print(magic_time(t, 2))
# for i in range(20,41):
#     print(get_ac_hour_num(i,1))
