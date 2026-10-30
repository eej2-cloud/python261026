"""인터넷에서 타이타닉 데이터를 내려받아 정제하고 생존율을 분석합니다."""

import pandas as pd
import matplotlib.pyplot as plt


DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"


def load_and_clean_data() -> pd.DataFrame:
    """데이터를 내려받고 결측치를 처리해 분석용 데이터프레임을 반환합니다."""
    df = pd.read_csv(DATA_URL)

    required_columns = {
        "survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"
    }
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"데이터에 필요한 컬럼이 없습니다: {sorted(missing_columns)}")

    print("원본 데이터 크기:", df.shape)
    print("\n원본 결측치 개수:")
    print(df.isnull().sum())
    print(f"\n완전히 같은 행의 개수: {df.duplicated().sum()}")
    print("승객 식별자 없이 같은 특징을 가진 승객을 중복으로 단정할 수 없어 행은 유지합니다.")

    # 객실 등급별·성별 나이 중앙값으로 채우고, 남은 값은 전체 중앙값으로 채웁니다.
    age_medians = df.groupby(["sex", "pclass"])["age"].transform("median")
    df["age"] = df["age"].fillna(age_medians).fillna(df["age"].median())

    df["embarked"] = df["embarked"].fillna(df["embarked"].mode().iloc[0])
    df["fare"] = df["fare"].fillna(df["fare"].median())

    # 결측치가 많은 컬럼과 분석에 중복되는 파생 컬럼을 제외합니다.
    df = df.drop(
        columns=["deck", "class", "who", "adult_male", "embark_town", "alive", "alone"],
        errors="ignore",
    )
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["alone"] = df["family_size"] == 1
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 13, 20, 36, 61, float("inf")],
        labels=["12세 이하", "13~19세", "20~35세", "36~60세", "61세 이상"],
        right=False,
    )

    print("\n정제 후 결측치 개수:")
    print(df.isnull().sum())
    print("\n정제 후 데이터 크기:", df.shape)
    return df


def print_analysis(df: pd.DataFrame) -> None:
    """생존 여부를 여러 기준으로 요약해 출력합니다."""
    print(f"\n전체 승객 수: {len(df)}명")
    print(f"전체 생존율: {df['survived'].mean():.1%}")

    for column, title in [
        ("sex", "성별 생존 현황"),
        ("pclass", "객실 등급별 생존 현황"),
        ("age_group", "연령대별 생존 현황"),
        ("embarked", "승선 항구별 생존 현황"),
        ("alone", "혼자 탑승 여부별 생존 현황"),
    ]:
        summary = (
            df.groupby(column, observed=True)["survived"]
            .agg(승객수="size", 생존자수="sum", 생존율="mean")
        )
        summary["생존율"] = summary["생존율"].map("{:.1%}".format)
        print(f"\n{title}:")
        print(summary)

    print("\n생존 여부별 요금 통계:")
    fare_summary = df.groupby("survived")["fare"].agg(["count", "mean", "median"])
    fare_summary.index = ["사망", "생존"]
    fare_summary.columns = ["승객수", "평균 요금", "중앙값 요금"]
    print(fare_summary.round(2))


def plot_survival_rates(df: pd.DataFrame) -> None:
    """성별 등 여러 기준의 생존율을 막대그래프로 표시합니다."""
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    charts = [
        (
            "sex",
            ["female", "male"],
            ["여성", "남성"],
            "성별 생존율",
            ["#e76f51", "#457b9d"],
        ),
        (
            "pclass",
            [1, 2, 3],
            ["1등석", "2등석", "3등석"],
            "객실 등급별 생존율",
            ["#457b9d", "#8ab17d", "#e9c46a"],
        ),
        (
            "age_group",
            ["12세 이하", "13~19세", "20~35세", "36~60세", "61세 이상"],
            ["12세 이하", "13~19세", "20~35세", "36~60세", "61세 이상"],
            "연령대별 생존율",
            ["#8ab17d"] * 5,
        ),
        (
            "alone",
            [False, True],
            ["가족 동반", "혼자"],
            "혼자 탑승 여부별 생존율",
            ["#8ab17d", "#e9c46a"],
        ),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for ax, (column, order, labels, title, colors) in zip(axes.flat, charts):
        rates = df.groupby(column, observed=True)["survived"].mean().reindex(order)
        bars = ax.bar(labels, rates.values, color=colors)
        ax.set_title(title)
        ax.set_ylabel("생존율")
        ax.set_ylim(0, 1.05)
        ax.grid(axis="y", alpha=0.25)
        ax.bar_label(bars, labels=[f"{rate:.1%}" for rate in rates], padding=3)

    fig.suptitle("타이타닉 승객 생존율 분석", fontsize=16)
    fig.tight_layout()
    plt.show()


def main() -> None:
    data = load_and_clean_data()
    print_analysis(data)
    plot_survival_rates(data)


if __name__ == "__main__":
    main()
