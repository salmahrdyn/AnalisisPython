import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

# Load data
bike_per_day = pd.read_csv('day.csv')
bike_per_hour = pd.read_csv('hour.csv')


def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://bcassetcdn.com/social/lgxwqseyph/preview.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

date = sidebar(bike_per_day)
if len(date) == 2:
    main_df = bike_per_day[(bike_per_day["dteday"] >= str(date[0])) & (bike_per_day["dteday"] <= str(date[1]))]
else:
    main_df = bike_per_day[
        (bike_per_day["dteday"] >= str(st.session_state.date[0])) & (bike_per_day["dteday"] <= str(st.session_state.date[1]))]

# Tren Peminjaman Sepeda Setiap Tahun
bike_per_day['dteday'] = pd.to_datetime(bike_per_day['dteday'])
bike_per_day['year'] = bike_per_day['dteday'].dt.year
yearly_counts = bike_per_day.groupby('year')['cnt'].sum()
st.title('Dashboard Peminjaman Sepeda')
st.subheader('Tren Peminjaman Sepeda Setiap Tahun')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linestyle='-', color='b')
ax.set_title('Total Peminjaman Sepeda Setiap Tahun')
ax.set_xlabel('Tahun')
ax.set_ylabel('Total Peminjaman')
ax.grid(True)
st.pyplot(fig)

# Tren Jumlah Peminjaman Sepeda per Bulan
bike_per_hour['dteday'] = pd.to_datetime(bike_per_hour['dteday'])
bike_per_hour.set_index('dteday', inplace=True)
monthly_counts = bike_per_hour.resample('M').sum()
st.subheader('Tren Jumlah Peminjaman Sepeda per Bulan')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_counts['cnt'], marker='o')
ax.set_title('Tren Jumlah Peminjaman Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.grid(True)
st.pyplot(fig)

# Jumlah Peminjaman Sepeda Rata-rata per Musim
byseason_bike = bike_per_day.groupby(by="season")['cnt'].mean().reset_index()
byseason_bike.rename(columns={"cnt": "average_count"}, inplace=True)
season_palette = {'1': 'lightcoral', '2': 'gold', '3': 'mediumseagreen', '4': 'cornflowerblue'}
st.subheader('Jumlah Peminjaman Sepeda Rata-rata per Musim')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='average_count', data=byseason_bike, ci=None, palette=season_palette)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
ax.set_title('Jumlah Peminjaman Sepeda Rata-rata per Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman Rata-rata')
ax.grid(True)
st.pyplot(fig)

# Clustering
hourly_counts = bike_per_hour.groupby('hr')['cnt'].mean().reset_index()
hourly_counts['Cluster'] = pd.cut(hourly_counts['cnt'], bins=3, labels=['Low', 'Medium', 'High'])
st.subheader('Clustering Jam Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
for cluster, data in hourly_counts.groupby('Cluster'):
    ax.plot(data['hr'], data['cnt'], label=cluster)

ax.set_title('Clustering Jam Peminjaman Sepeda')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Peminjaman')
ax.legend(title='Cluster')
ax.grid(True)
st.pyplot(fig)

if __name__ == "__main__":
    copyright = "Copyright © " + "2024" + "Made by: @salmahrdyn"
    st.caption(copyright)
