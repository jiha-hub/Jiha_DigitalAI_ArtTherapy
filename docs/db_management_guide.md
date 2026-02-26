# 🗄️ MindPalette v4.0: DB 관리 지침서 (Database Management Guide)

이 문서는 MindPalette의 영속성 계층인 `gallery_log.json` 및 파일 시스템 DB를 관리, 백업, 복구하는 방법을 기술합니다.

---

## 1. DB 시스템 개요
MindPalette는 복잡한 성능 오버헤드를 줄이기 위해 **JSON 기반 파일 DB** 방식을 사용합니다. 

- **DB 파일**: `C:\Users\asia\Desktop\Workshop1\outputs\gallery\gallery_log.json`
- **장점**: 별도의 SQL 서버 불필요, 백업/이동 용이, 프라이버시 최적화.

---

## 2. `gallery_log.json` 상세 구조

```json
[
  {
    "id": "20240220_123456",
    "title": "평화로운 숲",
    "diary": "복잡했던 마음이 초록색 선을 그리며 차분해졌다.",
    "path": "outputs/gallery/result_20240220_123456.png",
    "sketch_path": "outputs/gallery/sketch_20240220_123456.png",
    "heart_rate": 72,
    "lora_style": "Soft Watercolor",
    "timestamp": "2024-02-20 12:34:56",
    "comments": ["정말 평온해 보입니다!", "색감이 따뜻하네요."],
    "likes": 5
  }
]
```

---

## 3. DB 관리 작업 (Operating Procedures)

### 3.1 백업 (Backup)
매주 또는 중요 세션 이후 다음 폴더 전체를 압축하여 별도 저장소(외장 하드 등)에 보관하는 것을 권장합니다.
- **경로**: `C:\Users\asia\Desktop\Workshop1\outputs\gallery\`

### 3.2 복구 (Restore/Migration)
1. 새로운 PC에 MindPalette를 설치합니다.
2. 백업한 `gallery` 폴더의 내용물을 동일한 경로에 덮어씌웁니다.
3. 앱을 실행하면 `gallery_log.json`을 읽어 자동으로 아카이브가 복원됩니다.

### 3.3 정합성 검사 (Integrity Check)
로그 파일과 실제 이미지가 일치하지 않을 경우(`File Not Found` 등), 다음 절차를 수행합니다.
- `gallery_log.json`을 열어 존재하지 않는 파일 경로가 포함된 JSON 객체를 삭제하거나 수정하십시오.

---

## 4. 데이터 유지 관리 API (src/utils.py)
백엔드 로직에 반영된 주요 DB 처리 함수입니다.

| 함수명 | 역할 | 비고 |
| :--- | :--- | :--- |
| `save_to_gallery()` | 새로운 작품 정보와 이미지를 DB에 추가 | 중복 ID 방지 |
| `load_gallery_data()` | `gallery_log.json`을 파싱하여 리스트로 반환 | 데코레이터를 통한 캐싱 고려 가능 |
| `add_comment()` | 특정 인덱스의 작품에 댓글 배열 추가 | JSON 쓰기/닫기 원자성 보장 |

---

## 5. 관리자 주의사항
> [!WARNING]
> `gallery_log.json` 파일의 구문(Syntax)이 깨질 경우(쉼표 누락 등), 갤러리 탭이 로드되지 않을 수 있습니다. 수동 수정 시 반드시 JSON Validator를 활용하십시오.

---
**작성일**: 2026-02-20 | **관리책임**: MindPalette 시스템 운영팀
