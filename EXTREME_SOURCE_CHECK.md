# 급변 구간 외부 수치 표본 대조

검토일: 2026-10-06 (Asia/Seoul)

이 문서는 각 지표의 절대 주간 변화 상위 3개를 원자료에서 다시 집계한 내부 점검과 별도로, 대표 일별 값 일부를 공개된 외부 자료와 대조한 기록이다. 표본 검토이므로 전체 원자료·18개 급변 주간을 외부 검증했다고 볼 수 없다. 날짜·관측시각·현물/선물·종가/장중·평균기간이 다르면 숫자가 다를 수 있어 “불일치”를 곧바로 오류로 판단하지 않는다.

| 지표·로컬 날짜 | 로컬 값 | 외부 공개값/출처 | 판단 |
|---|---:|---|---|
| 두바이유 2026-03-19 | $166.80/bbl | Reuters 인용 보도: Cash Dubai May-loading cargo assessment $166.80 | 숫자는 일치. 다만 Opinet의 싱가포르 거래 Dubai 현물 추정값과 Reuters의 May-loading cargo assessment가 같은 평가물·시점인지는 미확인. |
| 두바이유 2026-03-09 | $125.00/bbl | Bloomberg 자료를 인용한 필리핀 DOF 게시 자료: Dubai spot $96.30 | $28.70 차이. 두 자료 모두 Dubai/spot 표현을 쓰지만 Opinet의 T+1 조사 시차와 외부 표의 평가시점·방법론이 동일한지 확인되지 않았다. 사용자 다운로드 오류나 Opinet 원자료 오류로 결론 내릴 수 없음. |
| 두바이유 2026-03-10 주 시작 | 주간 평균 $127.932/bbl (3/9~15, 관측 5일) | IEA 2026-03-12 보고서의 Dubai Mth 1 (Singapore close) 주간 비교값 $107.33/bbl | 기준물이 Mth 1·Singapore close인 기간 통계라 Opinet Dubai 현물 일별 평균과 직접 같은 값이 아님. 참고 비교이며 오류 판단 근거로 쓰지 않음. |
| USD/KRW 2022-11-11 | 1,318.4원 | 국내 외환시장 종가 보도 1,318.4원 | 정확히 일치. 별도 일일 환율 제공 사이트는 날짜 기준값 1,314.13원 등을 제시해 마감시각/환율 시리즈 차이가 존재함을 확인. 로컬 ECOS 15:30 정의와 국내 종가 보도가 더 가까운 비교 기준. |
| 국고채 3년 2022-06-17 | 연 3.745% | 당시 채권시장 종가 보도 3.745% | 정확히 일치. |
| 전국 보통휘발유 2022-03-15 | 2,000.95원/L | 오피넷을 인용한 당일 보도: 오후 4시 전국 평균 2,000.95원/L | 수치 일치. 보도도 오피넷을 원출처로 하므로 독립 수집원 검증이라기보다 날짜·단위·전사 확인. |
| KOSPI 2026-05-08 | 7,498.00 | KRX 종가 보도 및 Yahoo Finance 일별 이력 7,498.00 | 정확히 일치. |
| KOSPI 2026-07-31 | 6,595.45 | 당일 종가 보도 6,595.45 | 정확히 일치. |
| 금 2026-03 | 로컬 2026-02-27 $5,177.31 → 2026-03-31 $4,518.50 (-12.72%) | World Gold Council의 LBMA Gold PM 기준 3월 수익률 -11.8% | 하락 방향은 부합하지만 가격 기준·관측일이 달라 정확값 검증은 아님. Alpha Vantage 주말 522개 관측의 정의는 계속 미확인. |

## 출처

- [Alpha Vantage 공식 API 문서](https://www.alphavantage.co/documentation/) — 역사 금·은 가격 함수. 일/주/월 주기는 설명하지만 주말 날짜 관측의 기준시각·생성방식은 명시하지 않음.
- [오피넷 원유 조회·도움말](https://www.opinet.co.kr/glopcoilSelect.do) — Dubai(현물)는 싱가포르 거래 가격 추정값이며 현지 시차로 T일 가격을 T+1일 조사한다고 안내.
- [Reuters 보도(Investing.com 재게시), Cash Dubai $166.80](https://www.investing.com/news/commodities-news/middle-east-oil-premiums-surge-to-record-highs-amid-iranisrael-conflict-93CH-4570421)
- [필리핀 DOF 게시자료(Bloomberg source 표시), Dubai spot $96.30](https://www.dof.gov.ph/download/pse-investph-2026march-17-2026/)
- [IEA 2026년 3월 Oil Market Report](https://www.iea.org/reports/oil-market-report-march-2026) — Dubai Mth 1 Singapore close의 별도 기준값.
- [2022-11-11 원/달러 1,318.4원 종가 보도](https://www.dailian.co.kr/news/view/1172355/%EC%9B%90%EB%8B%AC%EB%9F%AC-%ED%99%98%EC%9C%A8-13184%EC%9B%90-%EB%A7%88%EA%B0%90-591-2022); [비교용 일일 환율 표](https://www.exchangerates.org.uk/USD-KRW-spot-exchange-rates-history-2022.html)
- [2022-06-17 국고채 3년 종가 3.745%](https://view.asiae.co.kr/article/2022061717592732319)
- [2022-03-15 전국 휘발유 2,000.95원/L](https://www.newsis.com/view/NISX20220315_0001794483)
- [Yahoo Finance KOSPI 이력](https://finance.yahoo.com/quote/%5EKS11/history/?frequency=1d) 및 [2026-07-31 종가 보도](https://www.donga.com/news/Economy/article/all/20260731/134401617/1)
- [World Gold Council 2026년 3월 금 시장 논평](https://www.gold.org/goldhub/research/gold-market-commentary-march-2026)

## 해석 및 조치

사용자는 `시장지표_6개_원자료_확보_통합_설명서_수정본.md`의 절차대로 다운로드했다고 확인했다. 안내 조건(오피넷 국제원유, Dubai 현물, 일간, 달러/배럴)과 실제 원본 CSV의 `기간,Dubai` 열은 일치하므로 다운로드 설정을 다시 확인하거나 재수집할 필요는 없다.

오피넷 공식 도움말은 Dubai(현물)를 “싱가포르에서 거래된 Dubai(현물) 가격 추정값”으로 정의하고, 화~토 조사 및 현지 시차로 T일 가격을 T+1일에 조사한다고 설명한다([오피넷 원유 조회·도움말](https://www.opinet.co.kr/glopcoilSelect.do)). 그러므로 Bloomberg/Reuters의 Dubai 표기와 날짜만 맞춰 수치를 비교해 정확·오류를 판정할 수 없다. 공개된 참고값의 차이는 기록하되, 같은 시점·평가방법인지 알 수 없어 **사용자 다운로드 오류나 원자료 이상으로 해석하지 않는다**. 표본 대조의 범위가 제한적이라는 점만 남기고 원자료는 유지한다.
