# 일반 · 공학용 PC 계산기

Python 3.10 이상과 Tkinter로 만든 데스크톱 앱입니다. 외부 Python 패키지는 필요하지 않습니다.

## 실행

저장소 폴더에서 `python -m calculator`를 실행하세요. macOS/Linux에서는 `python3 -m calculator`도 가능합니다.
Windows에서는 Python 설치 시 Tcl/Tk를 포함하세요. Ubuntu/Debian에서 Tkinter가 없다면 `sudo apt install python3-tk`가 필요합니다. 그래픽 데스크톱이 있어야 창이 열립니다.

## 사용

- 일반/공학 모드를 전환해 같은 입력창을 사용합니다. Enter는 계산, Escape는 초기화입니다.
- 삼각·역삼각 함수, DEG/RAD, 로그, 제곱근, 거듭제곱, 팩토리얼, π/e를 지원합니다.
- `sin(30)`, `sqrt(9)+2^3`, `log(100)`, `fact(5)`처럼 닫는 괄호까지 입력하세요. 곱셈은 `2*pi`처럼 명시합니다.
- `%` 버튼은 `/100`을 입력합니다. `200*10/100`은 20입니다. 직접 입력하는 `%`와 `mod` 버튼은 나머지 연산입니다.
- Ans는 마지막 성공한 결과이며 ±는 전체 수식의 부호를 바꿉니다.
- 최근 100개 기록을 더블클릭해 수식을 재사용합니다. 기록은 메모리에만 저장됩니다. 재사용 시 현재 DEG/RAD 설정이 적용됩니다.
- 실수만 지원하며 화면은 유효숫자 12자리, 내부 계산은 Python 부동소수점을 사용합니다.

## 구조와 테스트

`calculator/engine.py`는 화면에 의존하지 않는 계산 엔진입니다. AST 허용 목록으로 수식을 해석하고 임의 코드 실행을 사용하지 않습니다. `calculator/ui.py`는 생성자로 엔진을 전달받으며 화면 상태를 관리합니다. 엔진과 화면의 상태는 각 클래스 내부에 캡슐화했습니다.

테스트: `python -m unittest discover -s tests -v`

## 실행 파일 배포 (선택)

### 단일 Windows EXE 다운로드

`main`에 코드를 푸시하면 GitHub Actions의 **Build Windows EXE**가 자동 실행됩니다. 저장소의 **Actions → Build Windows EXE → 성공한 실행 → Artifacts → Calculator-Windows**에서 ZIP을 다운로드하고 압축을 풀어 `Calculator.exe`를 실행하세요. 다운로드에는 GitHub 로그인이 필요할 수 있습니다. EXE 하나만 전달하면 되며 사용자의 PC에는 Python 설치가 필요하지 않습니다. 빌드는 Windows x64용이며 서명되지 않은 파일이라 Windows에서 게시자 확인 경고가 표시될 수 있습니다.

Actions의 **Run workflow**로 다시 빌드할 수도 있습니다. 아티팩트는 90일 동안 보관됩니다. Windows PC에서 직접 만들려면 Python 3.10 이상을 설치한 뒤 `build-windows.bat`를 더블클릭하세요. 결과는 `dist/Calculator.exe`입니다.

빌드 스크립트는 `py -3`, `python`, `python3` 순으로 Python 3.10 이상을 찾습니다. Python Launcher(`py`)는 필수가 아닙니다. 어떤 명령도 없다면 python.org에서 Python을 설치하면서 **Add python.exe to PATH**와 **Tcl/Tk**를 포함한 뒤 스크립트를 다시 실행하세요. 이미 설치한 경우 설치 프로그램의 Modify로 Tcl/Tk를, 설치 옵션으로 PATH 등록을 확인하세요. 패키지를 내려받기 위한 인터넷 연결도 필요합니다.

대상 운영체제에서 `python -m pip install pyinstaller` 후 `python -m PyInstaller --onefile --windowed --name Calculator desktop.py`를 실행하세요. 결과는 `dist/`에 생성됩니다. Windows용은 Windows에서, macOS용은 macOS에서 빌드해야 합니다. PyInstaller는 배포할 때만 필요한 선택 의존성입니다.
