"""Create standardized daily and weekly datasets from the six raw market indicators.

Raw files are read from data/raw and are never modified. Outputs are written to
data/processed. The weekly key is Sunday (W-SUN), so 2021-10-01 belongs to the
partial week ending 2021-10-03.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "data" / "processed"
START = pd.Timestamp("2021-10-01")
END = pd.Timestamp("2026-09-30")

METRICS = ["dubai_oil", "usd_krw", "bond_3y", "gasoline", "gold_usd", "kospi"]


def read_csv_with_encoding(path: Path) -> pd.DataFrame:
    """Read Korean public-data CSV files without changing their raw encoding."""
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error
    raise last_error or RuntimeError(f"Could not read {path}")


def parse_date(value: object) -> pd.Timestamp:
    """Parse ISO, ECOS (YYYY/MM/DD), and Korean YY년MM월DD일 date strings."""
    text = str(value).strip()
    direct = pd.to_datetime(text, errors="coerce")
    if pd.notna(direct):
        return pd.Timestamp(direct).normalize()

    numbers = re.findall(r"\d+", text)
    if len(numbers) >= 3:
        year, month, day = map(int, numbers[:3])
        if year < 100:
            year += 2000
        return pd.Timestamp(year=year, month=month, day=day)
    raise ValueError(f"Unrecognized date value: {value!r}")


def parse_number(values: pd.Series) -> pd.Series:
    return pd.to_numeric(
        values.astype(str).str.replace(",", "", regex=False).str.strip().replace({"": pd.NA, "nan": pd.NA}),
        errors="coerce",
    )


def read_simple_series(filename: str, metric: str) -> pd.DataFrame:
    raw = read_csv_with_encoding(RAW_DIR / filename)
    if raw.shape[1] < 2:
        raise ValueError(f"{filename} must have at least date and value columns")
    frame = raw.iloc[:, :2].copy()
    frame.columns = ["date", metric]
    frame["date"] = frame["date"].map(parse_date)
    frame[metric] = parse_number(frame[metric])
    return frame


def read_ecos_wide_series(filename: str, metric: str) -> pd.DataFrame:
    """Convert the one-row ECOS export with date headers into date/value rows."""
    raw = read_csv_with_encoding(RAW_DIR / filename)
    if len(raw) != 1:
        raise ValueError(f"{filename} should contain exactly one ECOS series row")

    row = raw.iloc[0]
    records: list[dict[str, object]] = []
    for column, value in row.items():
        if re.fullmatch(r"20\d{2}/\d{2}/\d{2}", str(column)):
            records.append({"date": pd.Timestamp(column), metric: value})
    frame = pd.DataFrame(records)
    frame[metric] = parse_number(frame[metric])
    return frame


def validate_and_filter(frame: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, dict[str, object]]:
    frame = frame.copy()
    source_rows = len(frame)
    frame = frame[(frame["date"] >= START) & (frame["date"] <= END)].sort_values("date")
    duplicate_dates = int(frame["date"].duplicated().sum())
    if duplicate_dates:
        raise ValueError(f"{metric}: duplicate dates found ({duplicate_dates})")

    missing_values = int(frame[metric].isna().sum())
    non_positive_values = int((frame[metric].dropna() <= 0).sum())
    clean = frame.dropna(subset=[metric]).reset_index(drop=True)
    diagnostics = {
        "metric": metric,
        "source_rows": source_rows,
        "rows_in_period": len(frame),
        "valid_rows": len(clean),
        "missing_values": missing_values,
        "duplicate_dates": duplicate_dates,
        "non_positive_values": non_positive_values,
        "first_valid_date": clean["date"].min().date().isoformat(),
        "last_valid_date": clean["date"].max().date().isoformat(),
    }
    return clean, diagnostics


def weekly_aggregate(frame: pd.DataFrame, metric: str) -> pd.DataFrame:
    weekly = (
        frame.set_index("date")[metric]
        .resample("W-SUN")
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"date": "week", "mean": metric, "count": f"{metric}_obs_days"})
    )
    # The daily input is already limited to START~END. Keep its boundary bins,
    # including the final partial week ending after END.
    return weekly.copy()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sources = {
        "dubai_oil": read_simple_series("dubai_oil_daily_20211001_20260930.csv.csv", "dubai_oil"),
        "usd_krw": read_ecos_wide_series("usdkrw_daily_20211001_20260930.csv.csv", "usd_krw"),
        "bond_3y": read_ecos_wide_series("korea_treasury_3y_daily_20211001_20260930.csv.csv", "bond_3y"),
        "gasoline": read_simple_series("gasoline_korea_daily_20211001_20260930.csv.csv", "gasoline"),
        "gold_usd": read_simple_series("gold_usd_daily_or_weekly_20211001_20260930.csv.csv", "gold_usd"),
        "kospi": read_ecos_wide_series("kospi_daily_20211001_20260930.csv.csv", "kospi"),
    }

    cleaned: dict[str, pd.DataFrame] = {}
    diagnostics: list[dict[str, object]] = []
    for metric, source in sources.items():
        cleaned[metric], report = validate_and_filter(source, metric)
        diagnostics.append(report)

    daily = pd.DataFrame({"date": pd.date_range(START, END, freq="D")})
    for metric in METRICS:
        daily = daily.merge(cleaned[metric], on="date", how="left", validate="one_to_one")
    daily.to_csv(OUTPUT_DIR / "market_indicators_daily_standardized.csv", index=False, encoding="utf-8-sig")

    weekly = pd.DataFrame({"week": pd.date_range("2021-10-03", "2026-10-04", freq="W-SUN")})
    for metric in METRICS:
        weekly = weekly.merge(weekly_aggregate(cleaned[metric], metric), on="week", how="left", validate="one_to_one")
    weekly.to_csv(OUTPUT_DIR / "market_indicators_weekly.csv", index=False, encoding="utf-8-sig")

    diagnostics_frame = pd.DataFrame(diagnostics)
    diagnostics_frame.to_csv(OUTPUT_DIR / "preprocessing_diagnostics.csv", index=False, encoding="utf-8-sig")

    weekly_missing = weekly[METRICS].isna().sum().to_dict()
    weekly_min_obs = weekly[[f"{metric}_obs_days" for metric in METRICS]].min().to_dict()
    report = [
        "# 전처리 품질 보고서",
        "",
        f"- 분석기간: {START.date()} ~ {END.date()}",
        "- 주간 기준: 일요일 종료 주차(`W-SUN`)",
        "- 경계 주차: 2021-10-03과 2026-10-04은 부분 주간으로 유지",
        "- 결측값 보간: 수행하지 않음",
        "",
        "## 일별 원자료 점검",
        "",
        diagnostics_frame.to_markdown(index=False),
        "",
        "## 주간 통합 데이터셋 점검",
        "",
        f"- 주간 행 수: {len(weekly)}",
        f"- 지표값 결측 주 수: {weekly_missing}",
        f"- 지표별 최소 유효 관측일 수: {weekly_min_obs}",
        "- `*_obs_days` 열은 각 주간 평균에 실제 사용된 일별 관측치 수다.",
    ]
    (OUTPUT_DIR / "preprocessing_quality_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Created {OUTPUT_DIR / 'market_indicators_daily_standardized.csv'}")
    print(f"Created {OUTPUT_DIR / 'market_indicators_weekly.csv'}")
    print(f"Weekly rows: {len(weekly)}")


if __name__ == "__main__":
    main()
