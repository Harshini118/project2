from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gender.csv"
PROCESSED = ROOT / "data" / "processed"
VISUALS = ROOT / "visuals"

PRIMARY_F = "average_value_Adjusted net enrollment rate, primary, female (% of primary school age children)"
PRIMARY_M = "average_value_Adjusted net enrollment rate, primary, male (% of primary school age children)"
TERTIARY_F = "average_value_School enrollment, tertiary, female (% gross)"
TERTIARY_M = "average_value_School enrollment, tertiary, male (% gross)"

REGIONS = [
    "World",
    "High income",
    "Upper middle income",
    "Lower middle income",
    "Low income",
    "East Asia & Pacific",
    "Latin America & Caribbean",
    "South Asia",
    "Middle East & North Africa",
    "Sub-Saharan Africa",
]

INCOME_GROUPS = ["High income", "Upper middle income", "Lower middle income", "Low income"]


def latest_rows(df, countries, required_cols):
    rows = []
    for country in countries:
        sub = df[df["Country Name"].eq(country)].dropna(subset=required_cols)
        if not sub.empty:
            rows.append(sub.sort_values("Year").iloc[-1])
    return pd.DataFrame(rows)


def clean_label(label):
    return label.replace("Middle East & North Africa", "Middle East\n& North Africa").replace(
        "Latin America & Caribbean", "Latin America\n& Caribbean"
    )


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    VISUALS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW)

    primary = latest_rows(df, REGIONS, [PRIMARY_F, PRIMARY_M]).copy()
    primary["female_male_ratio"] = primary[PRIMARY_F] / primary[PRIMARY_M]
    primary["female_advantage_points"] = primary[PRIMARY_F] - primary[PRIMARY_M]
    primary = primary.sort_values("female_male_ratio", ascending=True)
    primary_export = primary[
        [
            "Country Name",
            "Country Code",
            "Year",
            PRIMARY_F,
            PRIMARY_M,
            "female_male_ratio",
            "female_advantage_points",
        ]
    ].copy()

    tertiary = latest_rows(df, INCOME_GROUPS, [TERTIARY_F, TERTIARY_M]).copy()
    tertiary["female_male_ratio"] = tertiary[TERTIARY_F] / tertiary[TERTIARY_M]
    tertiary["female_advantage_points"] = tertiary[TERTIARY_F] - tertiary[TERTIARY_M]
    tertiary["total_gap_from_high_income_female"] = (
        tertiary.loc[tertiary["Country Name"].eq("High income"), TERTIARY_F].iloc[0]
        - tertiary[TERTIARY_F]
    )
    tertiary = tertiary.set_index("Country Name").loc[INCOME_GROUPS].reset_index()
    tertiary_export = tertiary[
        [
            "Country Name",
            "Country Code",
            "Year",
            TERTIARY_F,
            TERTIARY_M,
            "female_male_ratio",
            "female_advantage_points",
            "total_gap_from_high_income_female",
        ]
    ].copy()

    primary_export.to_csv(PROCESSED / "latest_primary_gender_parity.csv", index=False)
    tertiary_export.to_csv(PROCESSED / "latest_tertiary_gender_access_by_income.csv", index=False)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
            "figure.dpi": 180,
        }
    )

    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    y = range(len(primary))
    colors = [
        "#3f8f72" if 0.97 <= value <= 1.03 else "#a95f4a"
        for value in primary["female_male_ratio"]
    ]
    ax.axvspan(0.97, 1.03, color="#d9efe5", zorder=0)
    ax.scatter(primary["female_male_ratio"], y, s=150, color=colors, edgecolor="white", linewidth=1.2)
    ax.axvline(1, color="#24584d", linewidth=1.4)
    for i, row in enumerate(primary.itertuples()):
        ax.text(
            row.female_male_ratio + 0.002,
            i,
            f"{row.female_male_ratio:.3f}",
            va="center",
            fontsize=9,
            color="#263631",
        )
    ax.set_yticks(list(y))
    ax.set_yticklabels([clean_label(x) for x in primary["Country Name"]], fontsize=10)
    ax.set_xlim(0.93, 1.015)
    ax.set_xlabel("Girls' primary net enrollment divided by boys' primary net enrollment")
    ax.set_title("By the latest data, girls are essentially at parity in primary school")
    ax.text(
        0.971,
        len(primary) - 0.1,
        "shaded band = within 3% of parity",
        fontsize=10,
        color="#40665c",
        ha="left",
    )
    ax.text(
        0.93,
        -1.25,
        "Source: World Bank Human Development Indicators, gender category. Latest available year by region, mostly 2018.",
        fontsize=8.5,
        color="#5f6663",
    )
    ax.grid(axis="x", color="#d8dfdc", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(VISUALS / "pro_gender_parity_primary.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    x = range(len(tertiary))
    width = 0.35
    ax.bar(
        [i - width / 2 for i in x],
        tertiary[TERTIARY_F],
        width=width,
        color="#8c3f5d",
        label="Women",
    )
    ax.bar(
        [i + width / 2 for i in x],
        tertiary[TERTIARY_M],
        width=width,
        color="#5a7896",
        label="Men",
    )
    low = tertiary[tertiary["Country Name"].eq("Low income")].iloc[0]
    ax.annotate(
        "Low-income countries:\nwomen's tertiary enrollment\nis still below men's",
        xy=(3 - width / 2, low[TERTIARY_F]),
        xytext=(2.05, 33),
        arrowprops={"arrowstyle": "->", "color": "#51323f", "lw": 1.2},
        fontsize=10,
        color="#51323f",
        ha="left",
    )
    ax.annotate(
        "The global success story is\nheavily shaped by richer regions",
        xy=(0 - width / 2, tertiary.iloc[0][TERTIARY_F]),
        xytext=(0.65, 77),
        arrowprops={"arrowstyle": "->", "color": "#51323f", "lw": 1.2},
        fontsize=10,
        color="#51323f",
        ha="left",
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(tertiary["Country Name"], fontsize=10)
    ax.set_ylabel("Gross tertiary enrollment (%)")
    ax.set_ylim(0, 92)
    ax.set_title("But higher education exposes the gap that primary-school parity hides")
    ax.legend(frameon=False, ncol=2, loc="upper right")
    ax.grid(axis="y", color="#d8dfdc", linewidth=0.8)
    ax.text(
        -0.45,
        -15,
        "Source: World Bank Human Development Indicators, gender category. Latest available year by income group, 2018-2019.",
        fontsize=8.5,
        color="#5f6663",
    )
    fig.tight_layout()
    fig.savefig(VISUALS / "con_gender_parity_tertiary.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
