"""Build local dashboard data; no raw files are modified."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main():
    weekly = pd.read_csv(ROOT/'data/processed/market_indicators_weekly.csv')
    forecast = pd.read_csv(ROOT/'outputs/forecast/predictions.csv')
    metadata = json.loads((ROOT/'outputs/forecast/metadata.json').read_text(encoding='utf-8'))
    payload = dict(weekly=weekly.to_dict('records'), forecast=forecast.to_dict('records'), metadata=metadata)
    (ROOT/'dashboard/data.json').write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    print('Built dashboard/data.json (local use; excluded from Git)')

if __name__ == '__main__':
    main()
