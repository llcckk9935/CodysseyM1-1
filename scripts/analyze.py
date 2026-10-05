"""Reproducible descriptive analysis; never modify raw or processed inputs."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'analysis'
FIG = ROOT / 'outputs' / 'figures'
METRICS = ['dubai_oil', 'usd_krw', 'bond_3y', 'gasoline', 'gold_usd', 'kospi']
LABELS = ['Dubai oil (USD/bbl)', 'USD/KRW (KRW/USD)', '3Y bond yield (%)',
          'Gasoline (KRW/L)', 'Gold (USD/oz)', 'KOSPI (index)']

def save(fig, name):
    fig.savefig(FIG / name, dpi=160, bbox_inches='tight')
    plt.close(fig)

def export(frame, name):
    frame.to_csv(OUT / name, index=False, encoding='utf-8-sig')

def correlations(levels, changes, sample):
    rows = []
    for x, y in [('dubai_oil', 'gasoline'), ('usd_krw', 'gold_usd'),
                 ('usd_krw', 'kospi'), ('bond_3y', 'kospi')]:
        for kind, frame in [('level', levels), ('change', changes)]:
            pair = frame[[x, y]].dropna()
            rows.append(dict(sample=sample, kind=kind, x=x, y=y, n=len(pair),
                             pearson=pair[x].corr(pair[y]), spearman=pair[x].corr(pair[y], method='spearman')))
    return rows

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    w = pd.read_csv(ROOT / 'data/processed/market_indicators_weekly.csv', parse_dates=['week']).set_index('week')
    if w.index.has_duplicates or not w.index.is_monotonic_increasing:
        raise ValueError('Weekly dates must be unique and sorted')
    if not w.index.equals(pd.date_range('2021-10-03', '2026-10-04', freq='W-SUN', name='week')):
        raise ValueError('Unexpected weekly coverage')
    if w[METRICS].isna().any().any() or not np.isfinite(w[METRICS]).all().all():
        raise ValueError('Missing or nonfinite levels')
    levels = w[METRICS]
    changes = levels.pct_change(fill_method=None) * 100
    changes['bond_3y'] = levels.bond_3y.diff()
    features = w.copy()
    for k in METRICS:
        features[k + ('_change_pp' if k == 'bond_3y' else '_change_pct')] = changes[k]
        features[k + '_ma4'] = levels[k].rolling(4, min_periods=4).mean()
        features[k + '_vol13'] = changes[k].rolling(13, min_periods=13).std(ddof=1)
    export(features.reset_index(), 'analysis_features.csv')
    summary = levels.describe().T
    summary['min_week'] = levels.idxmin()
    summary['max_week'] = levels.idxmax()
    summary['change_std'] = changes.std(ddof=1)
    export(summary.rename_axis('metric').reset_index(), 'summary_statistics.csv')

    # JSON/CSV consistency does not prove external source authenticity.
    raw = json.loads((ROOT / 'data/raw/gold_usd_daily_raw.json').read_text(encoding='utf-8-sig'))
    gold = pd.DataFrame(raw['data'])
    gold['date'] = pd.to_datetime(gold.date)
    gold['price'] = pd.to_numeric(gold.price)
    gold = gold.set_index('date').sort_index()
    daily = pd.read_csv(ROOT / 'data/processed/market_indicators_daily_standardized.csv', parse_dates=['date']).set_index('date')
    inside = gold.loc['2021-10-01':'2026-09-30', 'price']
    if inside.index.has_duplicates or not inside.index.equals(daily.index):
        raise ValueError('Gold JSON coverage mismatch')
    np.testing.assert_allclose(inside, daily.gold_usd, rtol=1e-12)
    export(pd.DataFrame([dict(json_rows=len(gold), period_rows=len(inside),
        weekend_rows=int((inside.index.dayofweek >= 5).sum()), csv_matches_json=True,
        source_authenticity_verified=False)]), 'gold_validation.csv')

    fig, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True, layout='constrained')
    for ax, k, label in zip(axes.flat, METRICS, LABELS):
        ax.plot(levels.index, levels[k], lw=1, label='Weekly mean')
        ax.plot(levels.index, features[k + '_ma4'], lw=1.4, label='4-week trailing mean')
        ax.set_title(label); ax.grid(alpha=.2)
    axes.flat[0].legend(fontsize=8)
    fig.suptitle('Weekly levels and trailing means (boundary weeks are partial)')
    save(fig, '01_levels_ma.png')
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True, layout='constrained')
    for ax, k, label in zip(axes.flat, METRICS, LABELS):
        ax.plot(changes.index, changes[k], lw=.8)
        ax.axhline(0, color='gray', lw=.7)
        ax.set_title(label); ax.set_ylabel('pp' if k == 'bond_3y' else '%'); ax.grid(alpha=.2)
    fig.suptitle('Change in weekly means (not end-of-week trading returns)')
    save(fig, '02_weekly_changes.png')
    fig, ax = plt.subplots(figsize=(11, 5), layout='constrained')
    for k in METRICS:
        ax.plot(levels.index, levels[k] / levels[k].iloc[0] * 100, label=k)
    ax.set_title('Relative levels: first partial week = 100'); ax.set_ylabel('Index')
    ax.legend(ncol=3); ax.grid(alpha=.2)
    save(fig, '03_normalized_levels.png')

    candidates = []
    for k in METRICS:
        s = changes[k].dropna(); q1, q3 = s.quantile([.25, .75]); iqr = q3-q1
        for week, value in s[(s < q1-1.5*iqr) | (s > q3+1.5*iqr)].items():
            candidates.append(dict(week=week, metric=k, change=value,
                unit='pp' if k == 'bond_3y' else '%', lower=q1-1.5*iqr,
                upper=q3+1.5*iqr, action='retained_pending_source_review'))
    export(pd.DataFrame(candidates), 'outlier_candidates.csv')
    rows = correlations(levels, changes, 'all')
    # Recompute changes after dropping boundaries; removes transitions involving them.
    inner = levels.iloc[1:-1]
    inner_changes = inner.pct_change(fill_method=None)*100
    inner_changes['bond_3y'] = inner.bond_3y.diff()
    rows += correlations(inner, inner_changes, 'exclude_boundary_weeks')
    export(pd.DataFrame(rows), 'correlations.csv')
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), layout='constrained')
    for row, y in enumerate(['gold_usd', 'kospi']):
        for col, (kind, frame) in enumerate([('level', levels), ('change', changes)]):
            pair = frame[['usd_krw', y]].dropna()
            axes[row, col].scatter(pair.usd_krw, pair[y], s=12, alpha=.6)
            axes[row, col].set(title=f'{y}: {kind}, r={pair.usd_krw.corr(pair[y]):.3f}',
                xlabel='USD/KRW (KRW/USD)' if kind == 'level' else 'USD/KRW change (%)',
                ylabel=y if kind == 'level' else f'{y} change (%)')
            axes[row, col].grid(alpha=.2)
    save(fig, '06_q2_scatter.png')
    lags = []
    for sample, lv, ch in [('all', levels, changes), ('exclude_boundary_weeks', inner, inner_changes)]:
        for kind, frame in [('level', lv), ('change', ch)]:
            for lag in range(13):
                pair = pd.concat([frame.dubai_oil.shift(lag).rename('oil'), frame.gasoline.rename('gasoline')], axis=1).dropna()
                lags.append(dict(sample=sample, kind=kind, lag_weeks=lag, n=len(pair), pearson=pair.oil.corr(pair.gasoline)))
    lag_table = pd.DataFrame(lags)
    export(lag_table, 'q1_lag_correlations.csv')
    fig, ax = plt.subplots(figsize=(9, 5), layout='constrained')
    for (sample, kind), group in lag_table.groupby(['sample', 'kind']):
        ax.plot(group.lag_weeks, group.pearson, marker='o', label=f'{sample}: {kind}')
    ax.set(xlabel='Oil leads gasoline by k weeks', ylabel='Pearson r', title='Q1: exploratory lag correlations (0–12 weeks)')
    ax.legend(); ax.grid(alpha=.2)
    save(fig, '04_q1_lags.png')
    rolling = pd.DataFrame({f'rolling_{n}w': changes.bond_3y.rolling(n, min_periods=n).corr(changes.kospi) for n in [26, 52]})
    export(rolling.reset_index(), 'q3_rolling_correlations.csv')
    fig, ax = plt.subplots(figsize=(11, 5), layout='constrained')
    rolling.plot(ax=ax); ax.axhline(0, color='gray', lw=.8)
    ax.set(title='Q3: bond yield changes vs KOSPI changes', ylabel='Rolling Pearson r'); ax.grid(alpha=.2)
    save(fig, '05_q3_rolling.png')
    annual = []
    for year, frame in changes.groupby(changes.index.year):
        pair = frame[['bond_3y', 'kospi']].dropna()
        annual.append(dict(year=year, n=len(pair), pearson=pair.bond_3y.corr(pair.kospi)))
    export(pd.DataFrame(annual), 'q3_yearly_correlations.csv')
    # Use contiguous full-week years. Shift within each year so both endpoints
    # belong to that year; recompute changes so prior-year levels cannot leak in.
    yearly = []
    yearly_lags = []
    for year, lv in inner.groupby(inner.index.year):
        ch = lv.pct_change(fill_method=None) * 100
        ch['bond_3y'] = lv.bond_3y.diff()
        yearly += correlations(lv, ch, str(year))
        for lag in range(13):
            pair = pd.concat([ch.dubai_oil.shift(lag).rename('oil'), ch.gasoline], axis=1).dropna()
            # At least 20 paired observations for this exploratory comparison.
            yearly_lags.append(dict(year=year, lag_weeks=lag, n=len(pair),
                pearson=pair.oil.corr(pair.gasoline) if len(pair) >= 20 else np.nan))
    export(pd.DataFrame(yearly), 'yearly_relationships.csv')
    yl = pd.DataFrame(yearly_lags)
    export(yl, 'q1_yearly_lags.csv')
    eligible = yl.dropna(subset=['pearson'])
    best = eligible.loc[eligible.groupby('year').pearson.idxmax()].copy()
    export(best, 'q1_yearly_best_lags.csv')
    fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
    for year, group in eligible.groupby('year'):
        ax.plot(group.lag_weeks, group.pearson, marker='o', label=str(year))
    ax.set(title='Q1: within-year change correlations (minimum n=20)',
           xlabel='Oil leads gasoline by k weeks', ylabel='Pearson r')
    ax.legend(ncol=3); ax.grid(alpha=.2)
    save(fig, '07_q1_yearly_lags.png')
    # Mask after deriving shifts/differences on the complete time grid.
    # Both weeks used in each change must meet each metric's threshold.
    sensitivity = []
    for threshold in [3, 4]:
        for x, y in [('dubai_oil', 'gasoline'), ('usd_krw', 'gold_usd'),
                     ('usd_krw', 'kospi'), ('bond_3y', 'kospi')]:
            for lag in (range(13) if x == 'dubai_oil' else [0]):
                xgood = w[x+'_obs_days'].ge(threshold) & w[x+'_obs_days'].shift(1).ge(threshold)
                ygood = w[y+'_obs_days'].ge(threshold) & w[y+'_obs_days'].shift(1).ge(threshold)
                valid = xgood.shift(lag, fill_value=False) & ygood
                # Exclude changes involving either partial boundary week.
                valid.iloc[:lag+2] = False
                valid.iloc[-1] = False
                pair = pd.concat([changes[x].shift(lag).rename('x'), changes[y].rename('y')], axis=1).loc[valid].dropna()
                sensitivity.append(dict(min_obs_days=threshold, x=x, y=y, lag_weeks=lag,
                    n=len(pair), pearson=pair.x.corr(pair.y)))
    export(pd.DataFrame(sensitivity), 'observation_count_sensitivity.csv')
    # Influence diagnostics: keep weekly grid intact, then mask both endpoints.
    influence = []
    for scenario in ['full', 'exclude_2026', 'exclude_2026_mar_apr']:
        keep = pd.Series(True, index=inner.index)
        if scenario == 'exclude_2026':
            keep = pd.Series(inner.index.year != 2026, index=inner.index)
        elif scenario == 'exclude_2026_mar_apr':
            keep = pd.Series(~((inner.index.year == 2026) & inner.index.month.isin([3, 4])), index=inner.index)
        # Each change also requires its preceding level to be in kept sample.
        good = keep & keep.shift(1, fill_value=False)
        for lag in range(13):
            pair = pd.concat([inner_changes.dubai_oil.shift(lag).rename('oil'), inner_changes.gasoline], axis=1)
            pair = pair.loc[good & good.shift(lag, fill_value=False)].dropna()
            influence.append(dict(scenario=scenario, lag_weeks=lag, n=len(pair),
                pearson=pair.oil.corr(pair.gasoline), spearman=pair.oil.corr(pair.gasoline, method='spearman')))
    influence = pd.DataFrame(influence)
    export(influence, 'q1_influence.csv')
    fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
    for scenario, group in influence.groupby('scenario'):
        ax.plot(group.lag_weeks, group.pearson, marker='o', label=scenario)
    ax.set(title='Q1: influence diagnostics (changes, partial weeks excluded)',
           xlabel='Oil leads gasoline by k weeks', ylabel='Pearson r')
    ax.legend(); ax.grid(alpha=.2)
    save(fig, '08_q1_influence.png')
    # Rank candidate movements separately by metric; % and pp are not comparable.
    audit = []
    for k in METRICS:
        for week in changes[k].abs().nlargest(3).index:
            start = week-pd.Timedelta(days=6)
            values = daily.loc[start:week, k].dropna()
            audit.append(dict(metric=k, week=week, change=changes.loc[week, k],
                unit='pp' if k == 'bond_3y' else '%', daily_n=len(values),
                daily_min=values.min(), daily_max=values.max(),
                weekly_mean_from_daily=values.mean(), weekly_saved=levels.loc[week, k],
                source_confirmation='external_exact_value_unverified'))
    export(pd.DataFrame(audit), 'extreme_week_audit.csv')
    annual_vol = inner_changes.groupby(inner_changes.index.year).std(ddof=1)
    export(annual_vol.rename_axis('year').reset_index(), 'yearly_change_volatility.csv')
    print('Influence maximum correlations:')
    print(influence.loc[influence.groupby('scenario').pearson.idxmax()].round(4).to_string(index=False))
    print('Within-year best exploratory lags:')
    print(best.round(4).to_string(index=False))
    # Group by week-label month; descriptive, not a seasonality test.
    monthly = changes.groupby(changes.index.month).agg(['mean', 'count'])
    monthly.columns = [f'{a}_{b}' for a, b in monthly.columns]
    export(monthly.rename_axis('week_label_month').reset_index(), 'monthly_changes_exploratory.csv')
    print(summary[['min','max','change_std']].round(4).to_string())
    print(pd.DataFrame(rows).round(4).to_string(index=False))
    print(lag_table.loc[lag_table.groupby(['sample','kind']).pearson.idxmax()].round(4).to_string(index=False))
    print('Outputs:', OUT, FIG)

if __name__ == '__main__':
    main()
