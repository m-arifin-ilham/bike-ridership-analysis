import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# create ridership by day dataframe
def create_day_dataframe(df):
  daily_df = df.copy()

  # membuat kolom hari
  daily_df["day"] = daily_df["dteday"].dt.day_name()
  daily_df = daily_df.groupby(by="day").agg({
      "casual": "sum",
      "registered": "sum",
      "cnt": "sum"
  })
  daily_df = daily_df.reset_index()
  return daily_df

# create monthly dataframe
def create_monthly_dataframe(df):
  month_df = df.resample(rule="ME", on="dteday").agg({
      "casual": "sum",
      "registered": "sum",
      "cnt": "sum"
  })

  # mengubah format index menjadi nama bulan
  month_df.index = month_df.index.strftime('%B %Y')

  month_df = month_df.reset_index()
  month_df.rename(columns={
      "dteday": "month"
  }, inplace=True)
  return month_df

# create quarterly dataframe
def create_quarterly_dataframe(df):
  quarter_df = df.copy()

  # membuat kolom kuartal
  quarter_df["quarter"] = quarter_df["dteday"].dt.strftime('%Y-Q') + quarter_df['dteday'].dt.quarter.astype('string')
  quarter_df = quarter_df.groupby(by="quarter").agg({
      "casual": "sum",
      "registered": "sum",
      "cnt": "sum"
  })
  quarter_df = quarter_df.reset_index()
  return quarter_df

# load all_df
all_df = pd.read_csv("dashboard\main_data.csv")
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# create filter component
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
  # adding start_date and end_date
  start_date, end_date = st.date_input(
      label="Rentang Waktu",
      min_value=min_date,
      max_value=max_date,
      value=[min_date, max_date]
  )

# filtering all_df
main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                (all_df["dteday"] <= str(end_date))]

# create supporting df
daily_df = create_day_dataframe(main_df)
month_df = create_monthly_dataframe(main_df)
quarter_df = create_quarterly_dataframe(main_df)

# adding header
st.header("Bike Ridership Dashboard :sparkles:")

# daily ridership metric
st.subheader("Daily Bike Ridership")
col1, col2, col3 = st.columns(3)

with col1:
  total_cnt = main_df.cnt.sum()
  st.metric("Total Riders", value=total_cnt)

with col2:
  total_reg = main_df.registered.sum()
  st.metric("Total Registered Riders", value=total_reg)

with col3:
  total_cas = main_df.casual.sum()
  st.metric("Total Casual Riders", value=total_cas)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
    label="total"
)
ax.plot(
    main_df["dteday"],
    main_df["registered"],
    marker="o",
    linewidth=2,
    color="#BCD472",
    label="registered"
)
ax.plot(
    main_df["dteday"],
    main_df["casual"],
    marker="o",
    linewidth=2,
    color="#F990CA",
    label="casual"
)
ax.legend()
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
st.pyplot(fig)

# monthly ridership metric
st.subheader("Monthly Bike Ridership")
col1, col2, col3 = st.columns(3)

with col1:
  total_cnt = month_df.cnt.sum()
  st.metric("Total Riders", value=total_cnt)

with col2:
  total_reg = month_df.registered.sum()
  st.metric("Total Registered Riders", value=total_reg)

with col3:
  total_cas = month_df.casual.sum()
  st.metric("Total Casual Riders", value=total_cas)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_df["month"],
    month_df["cnt"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
    label="total"
)
ax.plot(
    month_df["month"],
    month_df["registered"],
    marker="o",
    linewidth=2,
    color="#BCD472",
    label="registered"
)
ax.plot(
    month_df["month"],
    month_df["casual"],
    marker="o",
    linewidth=2,
    color="#F990CA",
    label="casual"
)
ax.legend()
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15, rotation=45)
xticks = ax.get_xticks()
xlabels = ax.get_xticklabels()
ax.set_xticks(xticks[::len(xticks) // 8], xlabels[::len(xlabels) // 8], ha="right")
st.pyplot(fig)

# quarterly ridership metric
st.subheader("Quarterly Bike Ridership")
col1, col2, col3 = st.columns(3)

with col1:
  total_cnt = quarter_df.cnt.sum()
  st.metric("Total Riders", value=total_cnt)

with col2:
  total_reg = quarter_df.registered.sum()
  st.metric("Total Registered Riders", value=total_reg)

with col3:
  total_cas = quarter_df.casual.sum()
  st.metric("Total Casual Riders", value=total_cas)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    quarter_df["quarter"],
    quarter_df["cnt"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
    label="total"
)
ax.plot(
    quarter_df["quarter"],
    quarter_df["registered"],
    marker="o",
    linewidth=2,
    color="#BCD472",
    label="registered"
)
ax.plot(
    quarter_df["quarter"],
    quarter_df["casual"],
    marker="o",
    linewidth=2,
    color="#F990CA",
    label="casual"
)
ax.legend()
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
st.pyplot(fig)

# ridership by day metric
st.subheader("Day with Highest Ridership")
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(30, 20))
sns.barplot(y="day", hue="day", x="cnt", data=daily_df.sort_values(by=["cnt"], ascending=False), palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Total Bike Riders", fontsize=30)
ax.set_title("Total Bike Ridership By Day", loc="center", fontsize=50)
ax.tick_params(axis ='y', labelsize=35)
ax.tick_params(axis ='x', labelsize=30)
ax.locator_params(axis="x", nbins=4)
st.pyplot(fig) 

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(60, 20))
sns.barplot(y="day", hue="day",x="registered", data=daily_df.sort_values(by=["registered"], ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Registered Bike Riders", fontsize=30)
ax[0].set_title("Registered Bike Ridership By Day", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)
ax[0].locator_params(axis="x", nbins=4)

sns.barplot(y="day", hue="day", x="casual", data=daily_df.sort_values(by=["casual"], ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Casual Bike Riders", fontsize=30)
ax[1].set_title("Casual Bike Ridership By Day", loc="center", fontsize=50)
ax[1].tick_params(axis ='y', labelsize=35)
ax[1].tick_params(axis ='x', labelsize=30)
ax[1].locator_params(axis="x", nbins=4)

st.pyplot(fig)
st.caption("Dashboard")
