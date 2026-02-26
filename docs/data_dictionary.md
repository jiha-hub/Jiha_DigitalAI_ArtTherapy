# 📊 MindPalette v4.0: 데이터 정의서 (Data Dictionary)

이 문서는 MindPalette v4.0에서 관리되는 모든 데이터 요소의 정의, 형식 및 치료적 의미를 기술합니다.

---

## 1. 개요
MindPalette는 **Privacy-First (개인정보 보호 우선)** 원칙에 따라 모든 데이터를 사용자의 로컬 환경(`outputs/gallery/`)에 저장하며, 관계형 DB 대신 경량화된 JSON 파일 기반의 NoSQL 구조를 채택하여 이식성을 극대화했습니다.

---

## 2. 핵심 데이터 엔티티

### 2.1 사용자 정서 데이터 (Emotional Context)
| 필드명 | 데이터 타입 | 설명 | 치료적 의미 |
| :--- | :---: | :--- | :--- |
| `title` | String | 작품 제목 | 내면의 감정을 명사화(Labeling)하는 핵심 과정 |
| `diary` | String | 내러티브 일기 | 비언어적 이미지를 언어적 서사로 통합하는 과정 |
| `mood_tag` | List | 감정 키워드 | 세션 당시의 주요 정서 상태 필터링 |
| `timestamp` | DateTime | 생성 일시 | 시간 흐름에 따른 정서 변화(Timeline) 추적 |

### 2.2 바이오 피드백 (Biometrics)
| 필드명 | 데이터 타입 | 설명 | 치료적 의미 |
| :--- | :---: | :--- | :--- |
| `heart_rate` | Number | 실시간 심박수 (BPM) | 발산 전후의 신체적 긴장도 객관화 지표 |
| `hrv` | Number | 심박 변이도 | 스트레스 저항력 및 자율신경계 안정성 평가 |

### 2.3 AI 아트 메타데이터 (System Artifacts)
| 필드명 | 데이터 타입 | 설명 | 비고 |
| :--- | :---: | :--- | :--- |
| `image_path` | Path | 최종 결과물 경로 | `outputs/gallery/result_*.png` |
| `sketch_path` | Path | 원본 스케치 경로 | `outputs/gallery/sketch_*.png` |
| `prompt` | String | 사용된 긍정 프롬프트 | 치유적 상징물(Symbol) 기록 |
| `neg_prompt` | String | 배제된 부정 프롬프트 | 회피하고자 하는 정서적 요소 기록 |
| `lora_style` | String | 적용된 치료 화풍 | Watercolor, Pastel 등 선택된 LoRA |
| `adapter_scale` | Float | 스케치 보존 강도 | 사용자 원본성(Agency) 유지 지수 |

### 2.4 소셜 인터랙션 (Social Interaction)
| 필드명 | 데이터 타입 | 설명 | 비고 |
| :--- | :---: | :--- | :--- |
| `comments` | List[Dict] | 지지적 댓글 목록 | 익명 기반의 사회적 지지망 구축 |
| `likes` | Integer | 공감 수 | 정서적 연대감 수치화 |
| `privacy` | Boolean | 프라이버시 모드 여부 | `True`일 경우 갤러리 등록 제외 |

---

## 3. 데이터 저장 구조 (File System)

```text
C:\Users\asia\Desktop\Workshop1\outputs\gallery\
├── gallery_log.json         # 전체 메타데이터 DB (Index)
├── result_20240220_1.png    # 최종 작품 이미지
├── sketch_20240220_1.png    # 원본 스케치 (대조용)
└── masked_20240220_1.png    # 인페인팅 구역 (분석용)
```

---

## 4. 보안 및 보존 정책
1. **로컬 격리**: 데이터는 외부 서버가 아닌 로컬 폴더에만 존재함.
2. **무결성**: `gallery_log.json` 훼손 시 이미지 기반 복구 프로토콜 지원.
3. **익명성**: 소셜 기능 이용 시에도 원본 사용자 정보는 마스킹 처리됨.

---
**작성일**: 2026-02-20 | **버전**: v4.0 (Final)
