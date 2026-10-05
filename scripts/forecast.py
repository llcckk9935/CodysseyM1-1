"""One-week rolling-origin hindcast; model selection uses validation only.

Full-history EDA was already viewed: this is an educational retrospective
comparison, not a pristine prospective test. No future rows enter any fit.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/forecast'

def predict_ridge(x, y, row, alpha=10):
    mean, scale = x.mean(axis=0), x.std(axis=0)
    scale = np.where(scale > 0, scale, 1)
    z = np.column_stack([np.ones(len(x)), (x-mean)/scale])
    penalty = np.eye(z.shape[1])*alpha
    penalty[0, 0] = 0
    beta = np.linalg.solve(z.T@z + penalty, z.T@y)
    return float(np.r_[1, (row-mean)/scale]@beta)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    w = pd.read_csv(ROOT/'data/processed/market_indicators_weekly.csv', parse_dates=['week']).set_index('week').iloc[1:-1]
    # Feature row t contains only t or earlier; target is average price at t+1.
    f = pd.DataFrame(index=w.index)
    f['gas_change'] = w.gasoline.diff()
    f['gas_change_lag1'] = f.gas_change.shift(1)
    f['oil_change'] = w.dubai_oil.pct_change(fill_method=None)*100
    f['oil_change_lag1'] = f.oil_change.shift(1)
    f['oil_change_lag2'] = f.oil_change.shift(2)
    f['fx_change'] = w.usd_krw.pct_change(fill_method=None)*100
    f['target_change'] = w.gasoline.shift(-1)-w.gasoline
    f['target_week'] = pd.Series(w.index, index=w.index).shift(-1)
    f['actual'] = w.gasoline.shift(-1)
    f['persistence'] = w.gasoline
    f['ma4'] = w.gasoline.rolling(4).mean()
    f = f.dropna()
    groups = {'ridge_gas': ['gas_change','gas_change_lag1'],
              'ridge_market': ['gas_change','gas_change_lag1','oil_change','oil_change_lag1','oil_change_lag2','fx_change']}
    candidates = ['persistence','ma4',*groups]
    # 52 validation target weeks ending 2025; test is available full weeks of 2026.
    test_start = pd.Timestamp('2026-01-04')
    test_index = f.index[f.target_week.ge(test_start)]
    test_pos = f.index.get_loc(test_index[0])
    validation_pos = test_pos-52
    rows = []
    for pos in range(validation_pos, len(f)):
        current = f.iloc[pos]
        # At origin t, previous target t is observed, so previous row may train.
        history = f.iloc[:pos]
        result = dict(origin_week=f.index[pos], target_week=current.target_week,
            fit_last_target_week=history.target_week.iloc[-1], actual=current.actual,
            split='validation' if pos < test_pos else 'test', persistence=current.persistence, ma4=current.ma4)
        assert pd.Timestamp(result['fit_last_target_week']) <= pd.Timestamp(result['origin_week'])
        for name, cols in groups.items():
            delta = predict_ridge(history[cols].to_numpy(), history.target_change.to_numpy(), current[cols].to_numpy(dtype=float))
            result[name] = current.persistence+delta
        rows.append(result)
    predictions = pd.DataFrame(rows)
    metrics = []
    for split, frame in predictions.groupby('split'):
        for model in candidates:
            err = frame[model]-frame.actual
            metrics.append(dict(split=split, model=model, n=len(frame), mae=float(err.abs().mean()), rmse=float(np.sqrt((err**2).mean()))))
    metrics = pd.DataFrame(metrics)
    winner = metrics.loc[metrics.split.eq('validation')].sort_values(['mae','model']).iloc[0]['model']
    predictions['selected'] = predictions[winner]
    predictions.to_csv(OUT/'predictions.csv', index=False, encoding='utf-8-sig')
    metrics.to_csv(OUT/'metrics.csv', index=False, encoding='utf-8-sig')
    metadata = dict(horizon_weeks=1, selected_model=winner, selection='validation MAE',
        ridge_alpha=10, validation_weeks=52, test_weeks=int(predictions.split.eq('test').sum()),
        validation_start=str(predictions.loc[predictions.split.eq('validation'),'target_week'].min().date()),
        validation_end=str(predictions.loc[predictions.split.eq('validation'),'target_week'].max().date()),
        test_start=str(predictions.loc[predictions.split.eq('test'),'target_week'].min().date()),
        test_end=str(predictions.target_week.max().date()), prospective_holdout=False)
    (OUT/'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    test = predictions.loc[predictions.split.eq('test')]
    fig, ax = plt.subplots(figsize=(11,5), layout='constrained')
    ax.plot(test.target_week,test.actual,label='Actual',lw=2)
    ax.plot(test.target_week,test.selected,label=f'Validation-selected: {winner}',ls='--')
    if winner != 'persistence':
        ax.plot(test.target_week,test.persistence,label='Persistence baseline',alpha=.65)
    ax.set(title='One-week rolling hindcast: full weeks of 2026', ylabel='Gasoline (KRW/L)',xlabel='Target week')
    ax.legend(); ax.grid(alpha=.2)
    fig.savefig(ROOT/'outputs/figures/09_forecast.png',dpi=160,bbox_inches='tight')
    plt.close(fig)
    print(json.dumps(metadata,ensure_ascii=False))
    print(metrics.round(3).to_string(index=False))

if __name__ == '__main__':
    main()
