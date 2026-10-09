# 시장지표 시계열 분석 — 설치 및 실행 안내

이 프로젝트는 두바이유·원/달러 환율·국고채 3년 금리·국내 휘발유·국제 금·KOSPI의 과거 흐름을 주간 단위로 비교합니다. 이 문서는 프로젝트를 처음 사용하는 분이 필요한 자료를 준비하고, 분석을 실행한 뒤, 대시보드를 여는 순서를 안내합니다.

## 먼저 알아둘 점

- 이 저장소에는 프로그램 코드와 설명서, 분석 그래프가 들어 있습니다.
- 원본 데이터 7개와 분석 결과 CSV, 대시보드용 데이터 파일은 공개 저장소에 포함되어 있지 않습니다. 데이터 재배포 조건을 확인하지 못했기 때문입니다.
- 따라서 GitHub에서 처음 내려받은 경우, 분석을 시작하기 전에 본인이 사용할 수 있는 원자료를 `data/raw/` 폴더에 준비해야 합니다. 어떤 자료를 어떤 형식으로 준비하는지는 [데이터 출처 및 수집 안내](DATA_SOURCES.md)를 읽어 주세요.
- 원본 데이터가 이미 이 프로젝트의 `data/raw/` 폴더에 있는 컴퓨터에서는 아래 4번부터 진행하면 됩니다.
- 원자료는 실행 중 수정하지 않습니다. 분석 결과와 대시보드 데이터는 실행할 때 새로 만들거나 갱신합니다.

## 1. 준비물 확인하기

다음 항목을 준비합니다.

1. Windows 컴퓨터와 인터넷 연결
2. Python 3.10 이상
3. GitHub 저장소의 프로젝트 파일
4. 분석에 사용할 원자료 7개
5. 대시보드 계산 테스트까지 할 경우 Node.js (선택 사항)

프로젝트는 Python 3.14.7이 설치된 개발 컴퓨터에서 전체 실행을 확인했습니다. 다른 Python 버전에서도 동작할 수 있도록 `requirements.txt`에 필요한 라이브러리를 적어 두었지만, 모든 Python 버전에서 테스트한 것은 아닙니다.

## 2. 프로젝트를 컴퓨터에 준비하기

이미 프로젝트 폴더가 있다면 이 단계를 건너뛰세요. 처음 내려받는다면 GitHub 저장소 페이지에서 **Code → Download ZIP**을 선택해 압축을 푼 뒤, 압축을 푼 `codysseyM1-1` 폴더를 찾습니다.

1. 파일 탐색기에서 `codysseyM1-1` 프로젝트 폴더를 엽니다.
2. 탐색기 위쪽의 주소 표시줄을 클릭하고 `powershell`이라고 입력한 뒤 Enter를 눌러 해당 폴더 위치에서 PowerShell을 엽니다.
3. PowerShell에 아래 명령을 입력하고 Enter를 누릅니다.

```powershell
Get-Location
```

화면에 표시된 경로 끝이 `codysseyM1-1`인지 확인합니다. 다른 위치라면 아래 명령에서 경로를 프로젝트 폴더 위치에 맞게 바꿔 입력하세요.

```powershell
cd "C:\경로\codysseyM1-1"
```

## 3. 원자료 7개 준비하기

GitHub에서 내려받은 폴더에는 원자료가 없으므로, 데이터를 사용할 권한과 이용 조건을 확인한 뒤 준비해야 합니다. 다운로드 조건과 파일 형식은 [DATA_SOURCES.md](DATA_SOURCES.md)를 확인하세요.

1. 프로젝트 안에 `data/raw/` 폴더가 있는지 확인합니다. 없다면 프로젝트 폴더에서 다음 명령으로 만듭니다.

```powershell
New-Item -ItemType Directory -Force data\raw
```

2. 출처 안내에 따라 받은 원자료 파일 7개를 `data/raw/` 폴더에 넣습니다. 파일 이름과 형식이 스크립트가 예상하는 것과 일치해야 합니다. 이 프로젝트는 금 자료의 원본 JSON과 CSV를 각각 요구할 수 있으므로, 안내서의 파일 목록을 그대로 확인하세요.
3. Alpha Vantage API를 이용해 금 자료를 새로 받는 경우 API 키를 공개 문서, GitHub, 명령 기록 등에 올리지 마세요.
4. 원자료 파일이 몇 개인지 확인하려면 다음 명령을 실행합니다.

```powershell
Get-ChildItem data\raw -File
```

원자료가 7개가 아니면 전체 분석 실행이 시작되지 않습니다. 무엇이 빠졌는지 [데이터 출처 및 수집 안내](DATA_SOURCES.md)의 목록과 대조하세요.

## 4. Python 가상환경 만들기

가상환경은 이 프로젝트에서 쓸 Python 라이브러리를 별도 공간에 설치하는 방법입니다. 다른 Python 작업에 영향을 덜 주도록 프로젝트마다 한 번 만들어 사용합니다.

PowerShell에서 프로젝트 폴더에 있는지 확인한 뒤 아래 명령을 순서대로 실행하세요.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`python --version`에서 3.10 이상이 표시되어야 합니다. 설치가 끝나면 PowerShell 프롬프트 앞에 `(.venv)`가 나타납니다. 이후 이 프로젝트 명령을 실행할 때는 가상환경을 활성화한 상태로 진행하세요.

PowerShell이 스크립트 실행을 막아 `.venv\Scripts\Activate.ps1` 단계에서 오류가 나면, 현재 PowerShell 창에서만 아래 명령을 실행한 뒤 활성화 명령을 다시 실행하세요.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

이 설정은 현재 PowerShell 창에만 적용됩니다. 작업을 마치고 가상환경을 나가려면 다음 명령을 실행합니다.

```powershell
deactivate
```

## 5. 분석과 대시보드 자료 만들기

원자료 7개를 준비하고 가상환경을 활성화한 상태에서 다음 명령을 실행합니다.

```powershell
python scripts/run_pipeline.py
```

이 명령 하나가 다음 작업을 차례로 진행합니다.

1. 원자료를 읽어 날짜·값 형식을 맞추고 일별 및 주간 자료를 만듭니다.
2. 기초 통계, 시차 관계, 상관관계와 시각화 결과를 계산합니다.
3. 휘발유의 1주 앞 과거 예측 성능을 평가합니다.
4. 대시보드가 읽을 자료를 만듭니다.
5. 주요 결과와 파일 연결을 확인합니다.

각 작업이 끝날 때까지 기다려 주세요. 어떤 단계에서 오류가 발생하면 그 오류를 보여주고 나머지 작업은 진행하지 않습니다. 오류가 나오면 원자료 파일을 임의로 바꾸지 말고, 메시지를 복사해 [데이터 수집 안내](DATA_SOURCES.md) 및 아래 문제 해결 항목과 대조하세요. 실행 전후 원자료 파일이 바뀌지 않았는지도 확인합니다.

성공하면 전처리 결과는 `data/processed/`, 분석 표와 그래프는 `outputs/`, 대시보드 자료는 `dashboard/data.json`에 생성됩니다. 해당 결과 파일이 이미 있다면 다시 생성되거나 갱신될 수 있습니다. 원자료는 보존됩니다.

## 6. 대시보드 열기

5번 분석 실행이 성공한 뒤, 같은 프로젝트 폴더의 PowerShell에서 아래 명령을 실행합니다.

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory dashboard
```

1. 브라우저(Edge, Chrome 등)를 엽니다.
2. 주소창에 `http://127.0.0.1:8765`를 입력하고 Enter를 누릅니다.
3. 기간, 지표, 수준·주간 변화 선택을 바꾸어 결과를 살펴봅니다.
4. 대시보드를 닫을 때는 서버 명령이 실행 중인 PowerShell 창으로 돌아와 `Ctrl+C`를 누릅니다.

HTML 파일을 파일 탐색기에서 직접 더블클릭하면 대시보드 자료를 불러오지 못할 수 있으므로 위 방법으로 열어 주세요. 이 서버는 내 컴퓨터 안에서만 접속하도록 설정되어 있습니다.

## 7. 생성된 결과와 예측 해석하기

- 분석 설명과 그래프는 [REPORT.md](REPORT.md)에서 확인합니다. 현재 보고서는 1차 탐색 분석 초안이며, 데이터 정의의 미확인 사항과 해석 한계를 함께 기록하고 있습니다.
- `outputs/figures/`에는 보고서용 그래프가, `outputs/analysis/`에는 분석 표가 저장됩니다.
- 대시보드의 예측 화면은 휘발유 가격을 1주 앞서 예측하는 방식으로 **과거 자료에서 성능을 평가한 결과**입니다. 현재 시점의 미래 가격을 알려주거나, 금·환율 예측을 제공하는 기능은 아닙니다.
- 금 자료의 주말 값 정의와 일부 외부 비교 기준은 아직 확인되지 않았습니다. 관련 주의사항은 [데이터 검증 기록](DATA_VALIDATION.md)에서 확인하세요.

## 8. 자주 생기는 문제

### `python` 명령을 찾지 못한다는 메시지가 나옵니다

Python이 설치되어 있는지 확인하고, 설치 중 **Add Python to PATH** 옵션을 선택했는지 확인하세요. 설치 후 PowerShell을 새로 열어 `python --version`을 다시 실행합니다.

### 원자료가 7개가 아니라고 나옵니다

`data/raw/` 안에 필요한 파일이 모두 있는지, 하위 폴더가 아니라 바로 그 폴더 안에 들어 있는지 확인합니다. 파일별 조건은 [DATA_SOURCES.md](DATA_SOURCES.md)에 있습니다.

### `ModuleNotFoundError` 또는 라이브러리 오류가 나옵니다

PowerShell 경로가 프로젝트 폴더인지 확인하고 가상환경을 활성화한 뒤 다음 명령을 다시 실행합니다.

```powershell
python -m pip install -r requirements.txt
```

### 대시보드에 `data.json`을 만들라는 안내가 나옵니다

분석 결과 생성 단계가 아직 실행되지 않았거나 성공하지 않은 상태입니다. 5번의 `python scripts/run_pipeline.py`를 먼저 실행하세요.

### 대시보드 주소가 열리지 않습니다

PowerShell에서 서버 명령이 계속 실행 중인지 확인합니다. 창을 닫았거나 `Ctrl+C`를 눌렀다면 서버 명령을 다시 실행한 다음 주소를 엽니다.

## 9. 분석 단계별로 따로 실행하기 (선택)

각 결과를 단계별로 만들고 싶거나 오류가 어느 단계에서 발생했는지 확인하려면 프로젝트 폴더에서 아래 명령을 순서대로 실행할 수 있습니다. 원자료 7개와 설치된 라이브러리가 필요합니다.

```powershell
python scripts/preprocess.py
python scripts/analyze.py
python scripts/forecast.py
python scripts/build_dashboard.py
python scripts/verify.py
```

대부분의 사용자는 5번의 `python scripts/run_pipeline.py`만 사용하면 됩니다.

대시보드 계산 테스트는 별도 선택 사항이며 Node.js가 설치되어 있어야 합니다.

```powershell
node scripts/check_dashboard.cjs
```

이 테스트는 기간·지표 선택 시 계산이 예상대로 바뀌는지를 확인합니다. 실제 브라우저의 화면 모양이나 배포 상태를 확인하는 테스트는 아닙니다.

## 데이터·분석 기준

- 분석 기간: 2021-10-01~2026-09-30
- 주간 자료: 일요일 종료 주차 기준(`W-SUN`)
- 주간 평균은 실제 관측값만 사용하며 빠진 날짜를 임의로 채우지 않습니다.
- 첫 주와 마지막 주는 분석 기간에 걸친 부분 주간입니다. 마지막 라벨 `2026-10-04`에는 2026-09-30까지의 데이터만 포함됩니다.
- `*_obs_days` 열은 각 주간 평균에 사용된 실제 관측일 수입니다.
- 상관관계는 두 값이 함께 오르거나 내린 정도를 요약할 뿐, 한 값이 다른 값의 원인이라는 뜻은 아닙니다.

## 데이터 출처와 이용 주의

분석 지표는 오피넷의 두바이유·국내 휘발유, 한국은행 ECOS의 원/달러 환율·국고채 3년 금리·KOSPI, Alpha Vantage의 국제 금입니다. 수집 조건·파일 형식·재배포 범위는 [DATA_SOURCES.md](DATA_SOURCES.md)를 참고하세요.

국제 금 데이터는 Alpha Vantage의 `GOLD_SILVER_HISTORY` 함수, `GOLD` 심볼, `daily` 간격을 사용했습니다. 단위는 USD/트로이온스이며, 주말 값의 산출 방법과 기준 시각은 확인되지 않았습니다. API 키를 저장소나 공개 문서에 올리지 마세요.

## 더 읽을 자료

- [분석 리포트](REPORT.md)
- [미션 요구사항 점검](MISSION_REVIEW.md)
- [출처·수집·이용 안내](DATA_SOURCES.md)
- [데이터 검증 기록](DATA_VALIDATION.md)
- [대시보드 실행 및 시연](DASHBOARD_DEMO.md)
- [프로젝트 인수인계 기록](HANDOFF.md)
