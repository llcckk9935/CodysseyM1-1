# CodysseyM1-1 — 시장지표 시계열 분석

두바이유·원/달러 환율·국고채 3년 금리·국내 휘발유·국제 금·KOSPI의 과거 흐름을 주간 단위로 분석하고, 결과를 대시보드로 살펴보는 프로젝트입니다.

## 목차

### 1. 프로젝트 한눈에 보기

- [프로젝트 소개](#1-프로젝트-한눈에-보기)
- [기술과 처리 흐름](#2-기술과-처리-흐름)

### 2. 설치와 실행

- [원하는 사용 방법 고르기](#3-원하는-사용-방법-고르기)
- [준비물과 프로젝트 폴더](#4-준비물과-프로젝트-폴더)
- [원자료 준비](#5-원자료-준비)
- [Python 환경 설치](#6-python-환경-설치)
- [분석 실행](#7-분석-실행)
- [대시보드 열기](#8-대시보드-열기)

### 3. 결과와 참고

- [생성되는 결과](#9-생성되는-결과)
- [데이터·분석 기준](#10-데이터분석-기준)
- [문제 해결](#11-문제-해결)
- [관련 문서](#12-관련-문서)

## 1. 프로젝트 한눈에 보기

이 프로젝트는 여섯 시장지표의 과거 데이터를 표준화하고 주간 단위로 비교합니다. 상관관계와 시차 관계를 계산하고, 휘발유 가격의 1주 앞 예측을 과거 자료에서 평가합니다. 결과는 표·그래프와 로컬 대시보드로 확인할 수 있습니다.

> **빠른 실행:** `data/raw/`에 원자료 7개가 있고 Python 환경이 준비되어 있다면 [7. 분석 실행](#7-분석-실행)으로 이동하세요.

## 2. 기술과 처리 흐름

| 구분 | 사용 기술 | 역할 |
| --- | --- | --- |
| 데이터 처리·분석 | Python, pandas, NumPy, SciPy | 원자료 전처리, 통계·시차·예측 분석 |
| 그래프 | Matplotlib | 분석 결과 시각화 |
| 대시보드 | HTML, CSS, JavaScript, SVG | 분석 결과 조회와 필터 변경 |
| 로컬 실행 | Python HTTP 서버 | 브라우저에 대시보드 제공 |

**처리 흐름:** 원자료 → 전처리 → 분석·예측 → 대시보드 자료 생성 → 브라우저에서 결과 확인.

## 3. 원하는 사용 방법 고르기

| 원하는 작업 | 따라갈 항목 | 필요한 준비 |
| --- | --- | --- |
| 내 컴퓨터에서 처음 실행 | 4번부터 순서대로 | 원자료 7개, Python 3.10 이상 |
| 이미 설치된 프로젝트에서 결과 갱신 | 7번 → 8번 | 원자료와 가상환경 |
| 분석 결과만 살펴보기 | 9번과 [분석 리포트](REPORT.md) | 생성된 결과 파일 |
| 대시보드 계산 점검 | 11번의 선택 테스트 | Node.js |

## 4. 준비물과 프로젝트 폴더

- Windows와 PowerShell
- Python 3.10 이상 (전체 파이프라인은 개발 환경 Python 3.14.7에서 확인)
- 프로젝트 파일
- 분석에 사용할 원자료 7개
- 선택 사항: 대시보드 계산 테스트용 Node.js

GitHub에서 처음 받는 경우 저장소의 **Code → Download ZIP**으로 내려받아 압축을 풉니다. 이미 프로젝트 폴더를 연 상태라면 아래 확인 명령을 실행합니다.

```powershell
Get-Location
```

경로 끝이 `codysseyM1-1`이 아니라면 실제 폴더 경로로 이동합니다.

```powershell
cd "C:\경로\codysseyM1-1"
```

## 5. 원자료 준비

공개 저장소에는 재배포 조건을 확인하지 못한 원본 데이터와 분석용 CSV가 포함되지 않습니다. 사용할 권한과 이용 조건을 확인한 뒤 [데이터 출처 및 수집 안내](DATA_SOURCES.md)에 있는 파일명·형식대로 원자료 7개를 준비하세요. 금 자료는 원본 JSON과 CSV가 각각 필요할 수 있습니다.

프로젝트 루트에서 `data/raw/` 폴더를 준비합니다.

```powershell
New-Item -ItemType Directory -Force data\raw
```

받은 파일을 `data/raw/`에 직접 넣은 뒤 목록을 확인합니다.

```powershell
Get-ChildItem data\raw -File
```

목록에 파일이 7개 있어야 전체 분석이 시작됩니다. Alpha Vantage API 키는 문서·GitHub·명령 기록에 입력하지 마세요.

## 6. Python 환경 설치

PowerShell에서 프로젝트 루트에 있는지 확인하고, 아래 명령을 **각 코드 블록에서 한 번에 하나씩** 위에서부터 실행합니다. 가상환경은 프로젝트 라이브러리를 별도로 설치하는 공간입니다.

### 6-1. Python 버전 확인

```powershell
python --version
```

표시된 버전이 3.10 이상인지 확인합니다.

### 6-2. 가상환경 생성

```powershell
python -m venv .venv
```

### 6-3. 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

성공하면 PowerShell 프롬프트 앞에 `(.venv)`가 표시됩니다. 실행 정책 오류가 나면 현재 PowerShell 창에서만 아래 명령을 실행하고, 6-3을 다시 실행합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 6-4. 패키지 설치

```powershell
python -m pip install -r requirements.txt
```

작업을 마치고 가상환경을 나갈 때 실행합니다.

```powershell
deactivate
```

## 7. 분석 실행

원자료 7개를 준비하고 가상환경을 활성화한 뒤, 프로젝트 루트에서 실행합니다.

```powershell
python scripts/run_pipeline.py
```

파이프라인은 다음 작업을 순서대로 진행합니다.

1. 원자료 날짜와 값을 표준화하고 일별·주간 자료 생성
2. 기초 통계, 상관관계, 시차 관계 분석과 그래프 생성
3. 휘발유 가격의 1주 앞 과거 예측 성능 평가
4. 대시보드 데이터 생성
5. 결과 파일과 데이터 조건 검증

성공하면 완료 메시지와 함께 `data/processed/`, `outputs/`, `dashboard/data.json`의 결과가 생성 또는 갱신됩니다. 원자료는 수정하지 않습니다. 중간 단계에서 오류가 나면 메시지와 [문제 해결](#11-문제-해결), [데이터 출처 안내](DATA_SOURCES.md)를 대조하세요.

### 단계별로 실행하고 싶을 때 (선택)

전체 파이프라인 대신 단계를 하나씩 실행할 수 있습니다. 명령은 프로젝트 루트에서 실행하며 각 줄을 따로 실행합니다.

```powershell
python scripts/preprocess.py
```

```powershell
python scripts/analyze.py
```

```powershell
python scripts/forecast.py
```

```powershell
python scripts/build_dashboard.py
```

```powershell
python scripts/verify.py
```

## 8. 대시보드 열기

분석 실행이 성공한 뒤, 프로젝트 루트에서 아래 명령으로 로컬 서버를 시작합니다. 서버가 켜져 있는 동안 이 PowerShell 창을 열어 둡니다.

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory dashboard
```

브라우저에서 [http://127.0.0.1:8765](http://127.0.0.1:8765)를 엽니다. 기간·지표·수준 또는 주간 변화 선택을 바꾸어 결과를 확인할 수 있습니다. 서버를 종료하려면 서버가 실행 중인 PowerShell 창에서 `Ctrl+C`를 누릅니다.

HTML 파일을 직접 더블클릭하면 대시보드 자료를 불러오지 못할 수 있습니다. 위 로컬 서버 방식으로 여세요. 서버는 이 컴퓨터에서만 접속할 수 있도록 설정되어 있습니다.

## 9. 생성되는 결과

| 위치 | 내용 |
| --- | --- |
| `data/processed/` | 표준화된 일별 자료와 주간 자료 |
| `outputs/analysis/` | 분석 표와 예측 평가 결과 |
| `outputs/figures/` | 보고서용 분석 그래프 |
| `dashboard/data.json` | 대시보드가 읽는 자료 |
| [REPORT.md](REPORT.md) | 결과 설명, 해석과 한계 |

대시보드의 휘발유 예측 화면은 **과거 자료로 평가한 결과**입니다. 현재의 미래 가격 예측 기능은 아니며, 금·환율 예측도 제공하지 않습니다.

## 10. 데이터·분석 기준

- 분석 기간: `2021-10-01`부터 `2026-09-30`까지
- 주간 구분: 일요일 종료(`W-SUN`)
- 주간 평균은 실제 관측값으로 계산하며 빠진 날짜를 임의로 채우지 않습니다.
- 첫 주와 마지막 주는 부분 주간입니다. `2026-10-04` 라벨 주간에는 9월 30일까지의 자료만 들어갑니다.
- `*_obs_days` 열은 주간 평균에 포함된 실제 관측일 수입니다.
- 상관관계는 함께 움직인 정도를 나타내며 인과관계를 뜻하지 않습니다.
- 금 데이터는 Alpha Vantage `GOLD_SILVER_HISTORY`, `GOLD`, `daily`의 USD/트로이온스 종가입니다. 주말 값의 시장 기준과 산출 시각은 확인되지 않았습니다.

수집 조건과 재배포 범위는 [DATA_SOURCES.md](DATA_SOURCES.md)를, 금 자료 주말 값과 외부 비교 한계는 [DATA_VALIDATION.md](DATA_VALIDATION.md)를 참고하세요.

## 11. 문제 해결

| 문제 | 확인할 내용 |
| --- | --- |
| `python` 명령을 찾을 수 없음 | Python 설치 여부와 PATH 설정을 확인한 뒤 새 PowerShell 창을 엽니다. |
| 원자료가 7개가 아니라고 표시됨 | 필요한 파일이 `data/raw/` 바로 아래에 있고 파일명이 안내와 일치하는지 확인합니다. |
| `ModuleNotFoundError` 또는 패키지 오류 | 프로젝트 루트와 가상환경을 확인하고 아래 설치 명령을 다시 실행합니다. |
| `data.json`이 필요하다고 표시됨 | 7번 분석을 먼저 성공적으로 완료합니다. |
| 대시보드 주소가 열리지 않음 | 서버 명령이 실행 중인지 확인하고, 종료했다면 8번 명령으로 다시 시작합니다. |

```powershell
python -m pip install -r requirements.txt
```

대시보드 계산을 별도로 확인하려면 Node.js를 설치한 뒤 실행합니다. 이 검사는 화면 모양이나 배포 상태를 점검하지 않습니다.

```powershell
node scripts/check_dashboard.cjs
```

## 12. 관련 문서

- [분석 리포트](REPORT.md)
- [데이터 출처·수집·이용 안내](DATA_SOURCES.md)
- [원자료 확보 상세 안내](시장지표_6개_원자료_확보_통합_설명서_수정본.md)
- [데이터 검증 기록](DATA_VALIDATION.md)
- [급변 구간 외부값 대조](EXTREME_SOURCE_CHECK.md)
- [대시보드 실행 및 시연 시나리오](DASHBOARD_DEMO.md)
