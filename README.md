# 시장지표 시계열 분석

저장소: [llcckk9935/CodysseyM1-1](https://github.com/llcckk9935/CodysseyM1-1).
현재 공개 저장소에는 코드·문서만 제공합니다. 데이터·그래프가 제외되어 GitHub에서 리포트 이미지가
표시되지 않습니다. 로컬에서 원자료를 준비하고 파이프라인을 실행하면 생성됩니다.
이 상태는 시각화·대시보드 증빙까지 포함한 최종 제출본이 아닙니다.

국제유가·원/달러 환율·국고채 3년 금리와 국내 휘발유 가격·국제 금 가격·KOSPI의 주간 시계열 관계를 분석하는 M1-1 프로젝트입니다.

## 데이터 구성

- 원본 데이터: `data/raw/`
- 일별 표준화 데이터: `data/processed/market_indicators_daily_standardized.csv`
- 주간 통합 데이터: `data/processed/market_indicators_weekly.csv`
- 전처리 진단: `data/processed/preprocessing_diagnostics.csv`
- 품질 보고서: `data/processed/preprocessing_quality_report.md`

원본 데이터는 수정하지 않습니다. 분석용 데이터는 `scripts/preprocess.py`로 새로 생성합니다.

## 실행 방법

```bash
python -m pip install -r requirements.txt
python scripts/preprocess.py
python scripts/analyze.py
python scripts/forecast.py
python scripts/build_dashboard.py
python scripts/verify.py
```

한 번에 실행하고 실패 즉시 멈추려면 `python scripts/run_pipeline.py`를 사용할 수 있습니다.
원자료 7개를 준비한 로컬 폴더에서 사용하며 실행 전후 원자료 SHA256을 비교합니다.
새 가상환경에서 전체 재실행과 검증을 통과했습니다(Python 3.14.7, 같은 PC).
선택적 대시보드 계산 테스트는 `node scripts/check_dashboard.cjs`입니다.

## 주간 데이터 기준

- 주간 키: 일요일 종료 주차(`W-SUN`)
- 원자료의 실제 관측치만 평균에 사용
- 결측값 보간 없음
- 첫 주와 마지막 주는 부분 주간으로 유지
- `*_obs_days` 열은 각 주간 평균에 사용된 실제 관측일 수

마지막 행 `2026-10-04`는 분석 기간 종료일인 2026-09-30까지의 관측치만 사용한 부분 주간입니다.

## 국제 금 데이터

- 출처: Alpha Vantage — Gold & Silver Historical Prices API
- Function: `GOLD_SILVER_HISTORY`
- Symbol: `GOLD`
- Interval: `daily`
- 가격 정의: 일별 종가(Daily Close Price)
- 단위: USD / troy ounce (USD/oz)
- API Key는 저장소에 포함하지 않습니다.

상세 검증 기준은 [DATA_VALIDATION.md](DATA_VALIDATION.md)를 참고하세요.

## 분석 결과

[분석 리포트 초안](REPORT.md), [출처·수집 및 공개 범위](DATA_SOURCES.md), [인수인계](HANDOFF.md).
분석 표는 `outputs/analysis/`, 그래프는 `outputs/figures/`에 생성됩니다.
분석 실행은 기존 입력을 보존하고 해당 출력만 갱신합니다.
검증 환경은 Python 3.14.7입니다. 예측은 1주 앞 과거 평가이며 현재 가격을 예측하는 서비스가 아닙니다.

## 로컬 대시보드

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory dashboard
```

브라우저에서 `http://127.0.0.1:8765`를 엽니다. 종료는 Ctrl+C입니다.
[시연·스크린샷 시나리오](DASHBOARD_DEMO.md)에 제출 증빙 준비 방법을 기록했습니다.
실제 브라우저 화면 검증·캡처는 아직 완료하지 못했습니다.

## 데이터와 GitHub 공개

재배포 조건이 미확인인 원자료·파생 CSV·그래프·대시보드 데이터는 `.gitignore`에서 제외했습니다.
처음 받는 사용자는 [수집 안내](DATA_SOURCES.md)에 따라 CSV를 준비한 뒤 전처리부터 실행해야 합니다.
현재 분석값·보고서와 화면의 공개 가능 범위도 업로드 전에 확인해야 합니다.
API 키를 담은 파일·요청 URL을 커밋하지 않습니다.
