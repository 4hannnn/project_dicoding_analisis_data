from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


@st.cache_data
def load_day_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow",
    }

    weekday_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }

    df["season_label"] = df["season"].map(season_map)
    df["weather_label"] = df["weathersit"].map(weather_map)
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month
    df["month_name"] = df["dteday"].dt.strftime("%b")
    df["workingday_label"] = df["workingday"].map({1: "Working Day", 0: "Holiday/Weekend"})
    df["weekday_label"] = df["weekday"].map(weekday_map)

    return df


@st.cache_data
def load_hour_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "hour.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow",
    }

    weekday_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }

    df["season_label"] = df["season"].map(season_map)
    df["weather_label"] = df["weathersit"].map(weather_map)
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month
    df["month_name"] = df["dteday"].dt.strftime("%b")
    df["workingday_label"] = df["workingday"].map({1: "Working Day", 0: "Holiday/Weekend"})
    df["weekday_label"] = df["weekday"].map(weekday_map)

    return df


def main() -> None:
    st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
    st.title("Bike Sharing Dashboard")
    st.caption("Daily bike rental analysis from 2011 to 2012")

    df_day = load_day_data()
    df_hour = load_hour_data()

    with st.sidebar:
        st.header("Filters")
        year_options = sorted(df_day["year"].unique())
        year_choice = st.multiselect("Year", year_options, default=year_options)

        season_options = ["Spring", "Summer", "Fall", "Winter"]
        season_choice = st.multiselect("Season", season_options, default=season_options)

        weather_options = ["Clear", "Mist/Cloudy", "Light Snow/Rain", "Heavy Rain/Snow"]
        weather_choice = st.multiselect("Weather", weather_options, default=weather_options)

        workingday_options = ["Working Day", "Holiday/Weekend"]
        workingday_choice = st.multiselect("Day Type", workingday_options, default=workingday_options)

        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_choice = st.multiselect("Month", month_order, default=month_order)

        hour_range = st.slider("Hour Range", min_value=0, max_value=23, value=(0, 23))

    filtered = df_day[
        df_day["year"].isin(year_choice)
        & df_day["season_label"].isin(season_choice)
        & df_day["weather_label"].isin(weather_choice)
        & df_day["workingday_label"].isin(workingday_choice)
        & df_day["month_name"].isin(month_choice)
    ]

    hour_filtered = df_hour[
        df_hour["year"].isin(year_choice)
        & df_hour["season_label"].isin(season_choice)
        & df_hour["weather_label"].isin(weather_choice)
        & df_hour["workingday_label"].isin(workingday_choice)
        & df_hour["month_name"].isin(month_choice)
        & df_hour["hr"].between(hour_range[0], hour_range[1])
    ]

    if filtered.empty or hour_filtered.empty:
        st.warning("No data for the selected filters.")
        return

    total_rentals = int(filtered["cnt"].sum())
    avg_rentals = float(filtered["cnt"].mean())
    avg_hourly = float(hour_filtered["cnt"].mean())
    peak_day = filtered.loc[filtered["cnt"].idxmax()]
    peak_hour = hour_filtered.loc[hour_filtered["cnt"].idxmax()]

    weekday_avg = (
        filtered.groupby("weekday_label", as_index=False)["cnt"]
        .mean()
        .sort_values("cnt", ascending=False)
    )
    busiest_weekday = weekday_avg.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Rentals", f"{total_rentals:,}")
    col2.metric("Average Daily", f"{avg_rentals:,.0f}")
    col3.metric("Average Hourly", f"{avg_hourly:,.0f}")
    col4.metric("Peak Day", f"{peak_day['dteday'].date()} ({int(peak_day['cnt']):,})")
    col5.metric("Peak Hour", f"{int(peak_hour['hr'])}:00 ({int(peak_hour['cnt']):,})")
    monthly = (
        filtered.groupby(["year", "month", "month_name"], as_index=False)["cnt"]
        .mean()
        .sort_values(["year", "month"])
    )

    fig_trend = px.line(
        monthly,
        x="month_name",
        y="cnt",
        color="year",
        category_orders={"month_name": month_order},
        markers=True,
        title="Average Daily Rentals by Month",
    )
    fig_trend.update_layout(yaxis_title="Average Rentals", xaxis_title="Month")

    weather_avg = (
        filtered.groupby("weather_label", as_index=False)["cnt"]
        .mean()
        .sort_values("cnt", ascending=False)
    )
    fig_weather = px.bar(
        weather_avg,
        x="weather_label",
        y="cnt",
        title="Average Rentals by Weather",
    )
    fig_weather.update_layout(yaxis_title="Average Rentals", xaxis_title="Weather")

    workingday_avg = (
        filtered.groupby("workingday_label", as_index=False)["cnt"]
        .mean()
        .sort_values("cnt", ascending=False)
    )
    fig_working = px.bar(
        workingday_avg,
        x="workingday_label",
        y="cnt",
        title="Average Rentals: Working Day vs Holiday/Weekend",
    )
    fig_working.update_layout(yaxis_title="Average Rentals", xaxis_title="Day Type")

    best_weather = weather_avg.iloc[0]
    worst_weather = weather_avg.iloc[-1]
    workingday_top = workingday_avg.iloc[0]
    workingday_bottom = workingday_avg.iloc[-1]
    month_peak = monthly.loc[monthly["cnt"].idxmax()]

    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Story Highlights")
    st.markdown(
        "\n".join(
            [
                "**A quick story from the selected filters:**",
                f"- Demand reaches its seasonal high in **{month_peak['month_name']} {int(month_peak['year'])}**, averaging **{month_peak['cnt']:.0f} rentals/day**.",
                f"- Clear skies matter: **{best_weather['weather_label']}** leads with **{best_weather['cnt']:.0f} rentals/day**, while **{worst_weather['weather_label']}** drops to **{worst_weather['cnt']:.0f}**.",
                f"- Routine drives volume: **{workingday_top['workingday_label']}** exceeds **{workingday_bottom['workingday_label']}** by **{(workingday_top['cnt'] - workingday_bottom['cnt']):.0f} rentals/day**.",
                f"- The busiest weekday is **{busiest_weekday['weekday_label']}** at **{busiest_weekday['cnt']:.0f} rentals/day**, and the daily rush peaks around **{int(peak_hour['hr'])}:00** with **{peak_hour['cnt']:.0f} rentals/hour**.",
                "Use these signals to align fleet availability with the strongest demand windows.",
            ]
        )
    )

    col6, col7 = st.columns(2)
    col6.plotly_chart(fig_weather, use_container_width=True)
    col7.plotly_chart(fig_working, use_container_width=True)

    st.subheader("Hourly Demand Pattern")
    hourly = (
        hour_filtered.groupby(["hr", "workingday_label"], as_index=False)["cnt"]
        .mean()
        .sort_values(["workingday_label", "hr"])
    )

    fig_hourly = px.line(
        hourly,
        x="hr",
        y="cnt",
        color="workingday_label",
        markers=True,
        title="Average Rentals by Hour: Working Day vs Holiday/Weekend",
    )
    fig_hourly.update_layout(yaxis_title="Average Rentals", xaxis_title="Hour")
    st.plotly_chart(fig_hourly, use_container_width=True)

    st.subheader("Hourly Pattern by Season")
    hourly_season = (
        hour_filtered.groupby(["hr", "season_label"], as_index=False)["cnt"]
        .mean()
        .sort_values(["season_label", "hr"])
    )
    fig_hourly_season = px.line(
        hourly_season,
        x="hr",
        y="cnt",
        color="season_label",
        markers=True,
        title="Average Rentals by Hour and Season",
    )
    fig_hourly_season.update_layout(yaxis_title="Average Rentals", xaxis_title="Hour")
    st.plotly_chart(fig_hourly_season, use_container_width=True)

    st.subheader("Heatmap: Hour vs Weekday")
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = hour_filtered.pivot_table(
        index="weekday_label",
        columns="hr",
        values="cnt",
        aggfunc="mean",
    ).reindex(weekday_order)

    fig_heatmap = px.imshow(
        heatmap_data,
        labels={"x": "Hour", "y": "Weekday", "color": "Avg Rentals"},
        aspect="auto",
        title="Average Rentals Heatmap",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


if __name__ == "__main__":
    main()
