# 🛠️ Technical Troubleshooting Report (기술팀 오류 및 해결 보고서)

본 프로젝트의 구현 과정에서 발생한 주요 기술적 결함과 이를 해결하기 위해 수행한 기술팀의 조치 내역을 상세히 보고합니다.

## 1. 하드웨어 및 라이브러리 호환성 오류 (DevOps)

### ❌ 오류 1: `AssertionError: Torch not compiled with CUDA enabled`
- **원인**: 사용자의 기본 Python 환경에 GPU를 지원하지 않는 CPU 전용 PyTorch가 설치되어 있었습니다.
- **해결**: 
    1. Python 3.13의 최신 버전 라이브러리 불안정성을 고려하여, 안정적인 **Python 3.10 가상환경(`art_therapy`)**을 신규 생성했습니다.
    2. Conda 및 PyTorch 공식 인덱스를 사용하여 **CUDA 12.1 전용 PyTorch**를 강제 재설치했습니다.

### ❌ 오류 2: `DLL load failed: 지정된 프로시저를 찾을 수 없습니다.` (xformers 충돌)
- **원인**: 메모리 최적화 라이브러리인 `xformers`가 현재 설치된 PyTorch 버전 또는 Windows 시스템의 특정 DLL과 충돌을 일으켰습니다.
- **해결**: `xformers`가 없어도 SDXL 구동이 가능하므로, 충돌의 원인이 되는 **`xformers` 패키지를 완전히 제거**하고 기본 Attention 메커니즘을 사용하도록 설정을 변경하여 안정성을 확보했습니다.

---

## 2. 소프트웨어 로직 및 UI 연동 오류 (Development)

### ❌ 오류 3: 인페인팅(2단계) 버튼 동작 불가 (Indentation Bug)
- **원인**: `src/app.py` 작성 과정에서 `mod_btn.click` 이벤트 핸들러가 다른 함수의 코드 블록 내부에 잘못 포함(Indentation 오류)되어, 버튼 클릭 시 이벤트가 트리거되지 않았습니다.
- **해결**: 코드 구조를 전수 조사하여 **함수 스코프(Scope)를 정상화**하고, Gradio의 이벤트 루프에 버튼이 정확히 등록되도록 수정했습니다.

---

## 3. 실행 환경 및 경로 오류 (QA/System)

### ❌ 오류 4: `ModuleNotFoundError` 및 경로 인식 불가
- **원인**: 터미널의 현재 작업 디렉토리(CWD)가 프로젝트 루트(`Workshop1`)가 아닐 경우, `src` 폴더 내의 모듈을 인식하지 못하는 현상이 발생했습니다.
- **해결**: 사용자에게 정확한 실행 경로와 명령어를 가이드했으며, `model_engine.py`에서 상대 경로 대신 절대 경로를 인식할 수 있도록 보강했습니다.

### ❌ 오류 5: 환경 격리 실패 (Conda Run Isolation)
- **원인**: `conda run` 명령어가 특정 상황에서 가상환경이 아닌 Base 환경의 라이브러리를 우선적으로 참조하는 현상이 있었습니다.
- **해결**: `pip install --force-reinstall`을 통해 가상환경 내의 라이브러리 우선순위를 강제로 높여 환경 격리를 완벽히 구현했습니다.

---
**기술팀 총평**: 본 프로젝트는 로컬 Windows GPU 환경이라는 특수한 제약 조건 속에서 발생할 수 있는 거의 모든 라이브러리 충돌 케이스를 해결했습니다. 현재 배포된 버전은 매우 견고한(Stable) 상태입니다.
