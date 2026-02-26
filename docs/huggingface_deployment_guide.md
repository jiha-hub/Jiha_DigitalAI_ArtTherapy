# 🚀 마인드팔레트: 허깅페이스(Hugging Face) 배포 가이드

마인드팔레트를 전 세계 사용자가 접속할 수 있도록 허깅페이스 스페이스(Spaces)에 배포하는 단계별 기술 지침입니다.

## 1. 스페이스 생성 (Creation)
1. [Hugging Face Spaces](https://huggingface.co/spaces)에 접속하여 **"Create new Space"**를 클릭합니다.
2. **Space Name**: `mindpalette` (원하는 이름)
3. **SDK**: **Gradio** 선택
4. **Hardware**: 
    - **무료**: CPU Basic (속도가 매우 느림)
    - **추천**: **T4 Small (GPU)** 또는 **A10G Small** (부드러운 치료 경험을 위해 권장)
5. **Visibility**: Public (또는 Private) 선택 후 생성.

## 2. 파일 업로드 (가장 쉬운 방법: 웹 UI 이용)
스크린샷에 보이는 화면에서 파일을 올리는 **'Drag & Drop'** 방법입니다.
1. 상단 메뉴의 **"Files and versions"** 탭을 클릭합니다.
2. **"Add file" > "Upload files"**를 선택합니다.
3. **중요**: 로컬 `Workshop1` 폴더 안에 있는 다음 파일들을 **최상위(Root)** 에 끌어다 놓으세요.
    - `src/app.py` -> (Space의 최상위 경로에 `app.py`라는 이름으로 있어야 합니다.)
    - `src/model_engine.py`
    - `src/utils.py`
    - `requirements.txt`
4. 화면 하단의 **"Commit changes to main"** 버튼을 누르면 배포가 시작됩니다.

## 3. 파일 구조 가이드 (Hugging Face 전용)
허깅페이스는 기본적으로 **최상위 경로**에 있는 `app.py`를 찾아 실행합니다. 
따라서 `src/app.py`가 아니라, `app.py` 파일이 바로 보여야 합니다.
```text
mindpalette/ (Space Root)
├── app.py           <-- src 폴더 안에 넣지 말고 밖에 바로 두세요!
├── model_engine.py
├── utils.py
└── requirements.txt
```

## 5. 최적화 팁 (Optimization)
- **low_vram 모드**: `app.py`에서 `model = ArtTherapyModel(device=device, low_vram=True)` 설정을 유지하여 GPU 메모리 부족 현상을 방지하세요.
- **Privacy**: 의료 및 생체 데이터는 민감하므로, 실제 상용화 시에는 허깅페이스의 `Settings > Variables and secrets` 기능을 통해 DB 연결 문자열 등을 보호해야 합니다.

---
**마인드팔레트 배포 지원팀 (Antigravity AI)**
