"""Verify model chronology, independent metrics, source aggregation and links."""
from pathlib import Path
import json
import re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = pd.read_csv(ROOT/'outputs/forecast/predictions.csv', parse_dates=['origin_week','target_week','fit_last_target_week'])
    meta = json.loads((ROOT/'outputs/forecast/metadata.json').read_text(encoding='utf-8'))
    assert (p.target_week-p.origin_week).eq(pd.Timedelta(days=7)).all()
    assert p.fit_last_target_week.le(p.origin_week).all()
    assert p.target_week.is_unique
    w = pd.read_csv(ROOT/'data/processed/market_indicators_weekly.csv',parse_dates=['week']).set_index('week')
    np.testing.assert_allclose(p.persistence,w.loc[p.origin_week,'gasoline'])
    np.testing.assert_allclose(p.actual,w.loc[p.target_week,'gasoline'])
    metrics = pd.read_csv(ROOT/'outputs/forecast/metrics.csv')
    for row in metrics.itertuples():
        frame = p.loc[p.split.eq(row.split)]
        errors = frame[row.model].to_numpy()-frame.actual.to_numpy()
        np.testing.assert_allclose([abs(errors).mean(),np.sqrt(np.mean(errors**2))],[row.mae,row.rmse])
        assert len(frame)==row.n
    validation = metrics.loc[metrics.split.eq('validation')].sort_values(['mae','model'])
    assert meta['selected_model']==validation.iloc[0].model
    assert p.loc[p.split.eq('validation'),'target_week'].max()<p.loc[p.split.eq('test'),'target_week'].min()
    # Independent weekly means/counts from standardized daily inputs.
    d = pd.read_csv(ROOT/'data/processed/market_indicators_daily_standardized.csv',parse_dates=['date']).set_index('date')
    for k in ['dubai_oil','usd_krw','bond_3y','gasoline','gold_usd','kospi']:
        np.testing.assert_allclose(d[k].resample('W-SUN').mean(),w[k])
        np.testing.assert_array_equal(d[k].resample('W-SUN').count(),w[k+'_obs_days'])
    for name in ['README.md','REPORT.md','DASHBOARD_DEMO.md']:
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',(ROOT/name).read_text(encoding='utf-8')):
            if not target.startswith(('http','app:','#')):
                assert (ROOT/target.split('#')[0]).exists(), (name,target)
    payload = json.loads((ROOT/'dashboard/data.json').read_text(encoding='utf-8'))
    assert len(payload['weekly'])==262 and len(payload['forecast'])==len(p)
    assert len(list((ROOT/'outputs/figures').glob('*.png')))>=10-1
    print('PASS: forecast chronology, baseline/actual alignment, independent MAE/RMSE,')
    print('validation-only selection, weekly means/counts, local links and dashboard data.')

if __name__ == '__main__':
    main()
