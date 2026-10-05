# 분석 그래프 공개 조건 검토

확인일: 2026-10-05. 대상: 비상업적 학습 프로젝트의 공개 GitHub REPORT.md에 직접 제작한 PNG를 삽입하는 행위.
원자료 CSV/JSON 재배포, 대시보드의 수치 데이터 공개는 별도 사안이다. 이 문서는 법률 판단이나 제공자의 허락을 대신하지 않는다.

## 공식 근거와 현재 판단

### 사용자 확인에 따른 공개 결정

2026-10-05 사용자가 오피넷·ECOS·Alpha Vantage 세 곳 모두 공개를 허용했다고 전달했다.
직전 질문의 범위인 공개 GitHub의 직접 제작한 정적 분석 그래프 공개로 해석하여 PNG 9개를 포함한다.
답변 원문·담당자·개별 추가 조건은 전달받지 않았고 AI가 제공자의 답변을 독립 확인한 것은 아니다.
아래 공식 정책 검토 표는 사용자 확인 이전의 조사 기록이다. 원자료·파생 CSV·대시보드 수치 공개 허가로
확대하지 않으며, 답변 원문에 추가 표시 조건이 있으면 추후 반영한다. 문의 초안은 AI가 발송하지 않았다.

| 제공자 | 확인한 공식 근거 | 남은 확인 |
|---|---|---|
| 한국석유공사 오피넷 | [저작권정책이 포함된 공식 페이지](https://www.opinet.co.kr/searchViewS.do): 콘텐츠·DB의 권리 및 무단 복제·배포 주의, 수익 또는 그에 상응하는 혜택을 위한 사용은 사전 협의 안내 | 전국 보통휘발유와 두바이유를 주간 집계해 만든 교육용 정적 그래프의 공개 허용 여부. 원자료별 별도 조건도 확인 필요 |
| 한국은행 ECOS | [공식 ECOS 소개](https://www.bok.or.kr/portal/bbs/B0000522/view.do?menuNo=201692&nttId=10070977): 자체 통계와 외부 기관 통계를 함께 제공 | 원/달러·국고채 3년·KOSPI 각각의 원작성기관/이용 조건. ECOS 다운로드만으로 일괄 재배포 허가를 추정하지 않음 |
| 한국은행 스냅샷 | [정보 이용 지침](https://snapshot.bok.or.kr/guideline): 출처를 표시한 비상업적 데이터·그래프 이용 및 배포 안내, 원작성기관 정책 확인 요구 | 스냅샷 지침을 현재 ECOS에서 받은 파일에 자동 적용할 수 없음. 동일 지표/시계열 여부와 적용 범위를 확인해야 함 |
| Alpha Vantage | [공식 약관](https://www.alphavantage.co/terms_of_service/) 2항: 개인·비상업적 사용, 별도 서면 합의 가능. 개인적 활동을 넘어서는 목적을 commercial use 정의에 포함 | GOLD_SILVER_HISTORY 금 가격으로 만든 공개 교육용 그래프에 서면 동의가 필요한지. 연락 안내: premium@alphavantage.co |

**확인되지 않음은 금지 확정이 아니다.** 원자료의 재배포 제한을 자체 제작한 모든 분석 그래프의 금지로 단정하지 않았다.
반대로 출처만 기재하거나 교육 목적이라는 이유만으로 모든 이용 조건을 충족했다고 단정하지 않는다.
검색에서 발견한 다른 데이터셋의 공공누리/무제한 표시는 이 프로젝트 원자료에 전용하지 않았다.

## 그래프별 확인 대상

| 파일 | 사용 데이터 | 공개 전 확인할 제공자 |
|---|---|---|
| 01_levels_ma.png / 02_weekly_changes.png / 03_normalized_levels.png | 6개 지표 | 오피넷, ECOS 및 원작성기관, Alpha Vantage |
| 04_q1_lags.png / 07_q1_yearly_lags.png / 08_q1_influence.png | 두바이유·휘발유 | 오피넷 및 해당 원자료 권리자 |
| 05_q3_rolling.png | 국고채 3년·KOSPI | ECOS 및 원작성기관 |
| 06_q2_scatter.png | 환율·금·KOSPI | ECOS 및 원작성기관, Alpha Vantage |
| 09_forecast.png | 휘발유 실제값·휘발유 이력 기반 예측 | 오피넷 |

초기 공식 정책 조사만으로는 그래프 공개 허용을 확정하지 못했다. 이후 위 사용자 확인에 따라
9개 PNG만 `.gitignore` 예외로 지정했다. 로컬 원자료는 보존하며 수치 파일 제외를 유지한다.

## 다음 진행 순서

1. 기존 다운로드 화면/통계 메타데이터에 개별 이용 조건이 있는지 확인한다.
2. 조건으로 해결되지 않는 범위는 아래 문의를 제공자에게 보내 서면 답변을 확보한다. **아직 발송하지 않았다.**
3. 허용된 PNG만 명시적으로 Git 추적하고 출처·집계·변환 설명을 REPORT.md에 추가한다.
4. GitHub에서 이미지 링크가 실제로 열리는지 검증한다. CSV/JSON과 웹 대시보드 데이터 공개는 별도 검토한다.
5. 불허 또는 허락 확보 불가 시, 공개 가능한 대체 출처를 사용자와 결정하고 재수집·재분석한다. 임의로 데이터를 교체하지 않는다.

## 문의 초안 — 오피넷 / ECOS

안녕하세요. 개인 비상업적 교육 과제로 2021-10-01~2026-09-30의 시계열을 분석하고 있습니다.
오피넷 문의 대상은 두바이유 현물 일별 가격과 전국 보통휘발유 일별 평균 판매가격이며,
ECOS 문의 대상은 원/달러 종가(15:30), 국고채 3년 금리, KOSPI입니다.
원본 파일 및 다운로드 가능한 수치 데이터는 공개하지 않고, 주간 평균·변화율·상관분석을 통해
직접 만든 정적 PNG와 설명을 https://github.com/llcckk9935/CodysseyM1-1 에 공개하려 합니다.
출처와 분석기간, 집계 방법을 명시하고 제공기관의 공식 분석이 아님을 표시할 예정입니다.
이러한 그래프 공개가 허용되는지, 필요한 표시 문구나 별도 허가 및 원작성기관 확인이 있는지 안내 부탁드립니다.
위 기간의 데이터 제공 여부와 지표별 정확한 원출처도 확인 부탁드립니다.

## 문의 초안 — Alpha Vantage

Subject: Permission clarification for educational static charts (GOLD_SILVER_HISTORY)

Hello, I am working on an individual, non-commercial educational time-series project.
I used GOLD_SILVER_HISTORY with symbol GOLD and interval daily for 2021-10-01 through 2026-09-30.
May I publish original static PNG charts of weekly averages, percentage changes, and correlations
in a public GitHub educational report, with attribution, without publishing the raw JSON/CSV or downloadable price data?
Repository: https://github.com/llcckk9935/CodysseyM1-1
Please clarify whether written permission or a different license is required and the required attribution.
Separately, could you clarify the definition and timezone of the daily observations, including dates on weekends?
No API key is included in this request or the repository. Thank you.
