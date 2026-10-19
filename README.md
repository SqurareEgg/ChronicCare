# ChronicCare — 만성질환 모니터링 시스템

Blazor Server 기반의 만성질환자 관리 웹 애플리케이션입니다. 환자 등록, 측정값(혈압/혈당 등) 기록, 위험도 계산, 이상 알림, 통계 대시보드를 제공하는 학기말 과제로 제작했습니다.

- **기간**: 2026-06-21 (단기 과제)
- **인원**: 개인 프로젝트 (학기말 과제)
- **담당 역할**: 기획/설계/개발 전체 담당 (100%)

## 기술 스택

- .NET 10.0, Blazor Server
- Dapper + Microsoft.Data.SqlClient (MS SQL Server, Raw SQL 기반 데이터 접근)
- Bootstrap 5

## 핵심 기능

- **환자 관리**: 환자 등록/수정/목록 (`Patients/`)
- **측정값 기록**: 혈압·혈당 등 측정값 등록 및 이력 조회 (`Measurements/`)
- **위험도 계산**: `RiskCalculator`로 측정값 기반 위험도 산출
- **알림**: 이상 수치 발생 시 알림 목록 제공 (`Alerts/`)
- **통계**: 월별 추이(`MonthlyTrend`), 위험군 분포(`RiskDistribution`) 대시보드
- **인증**: `AuthService` 기반 로그인

## DB 스키마

`SQL/ChronicCareDB_Setup.sql` 참고 (MS SQL Server, `ChronicCareDB`)

## 실행 방법

```sh
# SQL/ChronicCareDB_Setup.sql를 로컬 MS SQL Server에 실행해 DB 생성
dotnet run
```

- 접속 문자열은 `appsettings.json`의 `ConnectionStrings:DefaultConnection` 참고 (Windows 통합 인증, `localhost`)
- .NET 10.0 SDK 필요

## 성과 및 회고

- (작성 예정)

## 발표자료

<img width="1280" height="720" alt="슬라이드1" src="https://github.com/user-attachments/assets/c6362797-d718-4913-a63e-04be58f06c1d" />

<img width="1280" height="720" alt="슬라이드2" src="https://github.com/user-attachments/assets/4ac6cec2-8971-4527-b605-7202abee5b3a" />

<img width="1280" height="720" alt="슬라이드3" src="https://github.com/user-attachments/assets/944acac2-c51b-4c59-96d2-79efa1927560" />

<img width="1280" height="720" alt="슬라이드4" src="https://github.com/user-attachments/assets/32cc56c1-c559-4ef7-b8ce-6e4c4463e765" />

<img width="1280" height="720" alt="슬라이드5" src="https://github.com/user-attachments/assets/3f16e652-c0dd-4556-805a-2a9f99383d28" />

<img width="1280" height="720" alt="슬라이드6" src="https://github.com/user-attachments/assets/209701d8-ca00-4b69-9f5b-01520cc069c6" />

<img width="1280" height="720" alt="슬라이드7" src="https://github.com/user-attachments/assets/075d34db-d828-48ce-9374-ecfdc7aeac5f" />

<img width="1280" height="720" alt="슬라이드8" src="https://github.com/user-attachments/assets/98632abc-6ad3-44e5-b676-f004ed28a480" />

<img width="1280" height="720" alt="슬라이드9" src="https://github.com/user-attachments/assets/441041c4-c21c-4780-a15d-9b97d87d27df" />

<img width="1280" height="720" alt="슬라이드10" src="https://github.com/user-attachments/assets/f7292663-aaf0-43b5-9c69-f21104bd8deb" />

<img width="1280" height="720" alt="슬라이드11" src="https://github.com/user-attachments/assets/6f5c310c-b037-43fa-9773-d870fedecc0c" />
