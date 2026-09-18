from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ── 색상 팔레트 ──────────────────────────────
BLUE_DARK   = RGBColor(0x1B, 0x3A, 0x6B)
BLUE_MID    = RGBColor(0x1E, 0x57, 0x99)
BLUE_LIGHT  = RGBColor(0xD6, 0xE4, 0xF7)
RED         = RGBColor(0xDC, 0x35, 0x45)
ORANGE      = RGBColor(0xFD, 0x7E, 0x14)
GREEN       = RGBColor(0x19, 0x87, 0x54)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_LIGHT  = RGBColor(0xF8, 0xF9, 0xFA)
GRAY_TEXT   = RGBColor(0x49, 0x55, 0x6B)
BLACK       = RGBColor(0x21, 0x25, 0x29)

BLANK = prs.slide_layouts[6]   # 완전 빈 레이아웃

# ── 헬퍼 함수 ───────────────────────────────
def add_rect(slide, l, t, w, h, fill=None, line=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, l, t, w, h,
             size=18, bold=False, color=BLACK, align=PP_ALIGN.LEFT,
             wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def slide_header(slide, title, subtitle=""):
    """상단 헤더 바 + 제목"""
    add_rect(slide, 0, 0, 13.33, 1.1, fill=BLUE_DARK)
    add_text(slide, title, 0.4, 0.1, 10, 0.7,
             size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.72, 10, 0.35,
                 size=13, color=RGBColor(0xAA, 0xC4, 0xE8), align=PP_ALIGN.LEFT)
    # 하단 푸터
    add_rect(slide, 0, 7.2, 13.33, 0.3, fill=BLUE_DARK)
    add_text(slide, "만성질환 모니터링 & 위험도 예측 시스템   |   객체지향프로그래밍 & 빅데이터처리실습 기말과제",
             0.3, 7.21, 12, 0.25, size=9, color=RGBColor(0xAA, 0xC4, 0xE8))

def add_bullet_box(slide, items, l, t, w, h,
                   bg=GRAY_LIGHT, border=None, title=None, title_bg=BLUE_MID):
    add_rect(slide, l, t, w, h, fill=bg, line=border or RGBColor(0xCC,0xCC,0xCC))
    y = t + 0.08
    if title:
        add_rect(slide, l, t, w, 0.32, fill=title_bg)
        add_text(slide, title, l+0.12, t+0.04, w-0.2, 0.26,
                 size=12, bold=True, color=WHITE)
        y = t + 0.38
    for item in items:
        add_text(slide, item, l+0.18, y, w-0.3, 0.28, size=11, color=GRAY_TEXT)
        y += 0.27

def add_code_box(slide, code, l, t, w, h, title=None):
    add_rect(slide, l, t, w, h, fill=RGBColor(0x1E,0x1E,0x1E))
    if title:
        add_text(slide, title, l+0.12, t+0.05, w-0.2, 0.22,
                 size=10, bold=True, color=RGBColor(0x56,0x9C,0xD6))
        code_t = t + 0.28
        code_h = h - 0.28
    else:
        code_t = t + 0.1
        code_h = h - 0.1
    txBox = slide.shapes.add_textbox(
        Inches(l+0.15), Inches(code_t), Inches(w-0.25), Inches(code_h-0.1))
    tf = txBox.text_frame
    tf.word_wrap = False
    first = True
    for line in code.split('\n'):
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(9.5)
        run.font.name = "Consolas"
        run.font.color.rgb = RGBColor(0xD4,0xD4,0xD4)

# ════════════════════════════════════════════
# 슬라이드 1 — 표지
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, fill=BLUE_DARK)
add_rect(sl, 0, 2.7, 13.33, 2.3, fill=BLUE_MID)
add_text(sl, "💊", 5.8, 0.4, 2, 1.0, size=52, align=PP_ALIGN.CENTER, color=WHITE)
add_text(sl, "만성질환 모니터링 & 위험도 예측 시스템",
         1.0, 1.6, 11.33, 1.0, size=30, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Chronic Disease Monitoring & Risk Prediction System",
         1.0, 2.5, 11.33, 0.5, size=15, color=RGBColor(0xAA,0xC4,0xE8), align=PP_ALIGN.CENTER, italic=True)
add_text(sl, "객체지향프로그래밍 & 빅데이터처리실습  |  기말과제",
         1.0, 3.05, 11.33, 0.45, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "기술 스택 :  MSSQL  +  Blazor Server  (.NET 10)  +  Dapper",
         1.0, 3.5, 11.33, 0.4, size=13, color=BLUE_LIGHT, align=PP_ALIGN.CENTER)
add_rect(sl, 3.5, 4.3, 6.33, 0.002, fill=WHITE)
add_text(sl, "제출일 : 2026년 6월 21일   |   발표 : 2026년 6월 22일 10시",
         1.0, 4.4, 11.33, 0.4, size=12, color=RGBColor(0xAA,0xC4,0xE8), align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════
# 슬라이드 2 — 목차
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "목  차", "Table of Contents")
sections = [
    ("01", "프로젝트 개요",    "목적 · 요약 · 개발 범위"),
    ("02", "업무 분석",        "업무 Flow · 기능 요구사항"),
    ("03", "DB 설계",          "테이블 구조 · ERD · 저장 프로시저"),
    ("04", "화면 설계",        "전체 화면 구성 · 페이지별 상세"),
    ("05", "핵심 구현",        "위험도 알고리즘 · 인증 · CRUD · 통계"),
    ("06", "테스트 시나리오",  "실행 흐름 · 주요 기능 검증"),
    ("07", "느낀점 & 결론",    "배운 점 · 개선 방향"),
]
for i, (num, title, desc) in enumerate(sections):
    col = i % 2
    row = i // 2
    lx = 0.5 + col * 6.4
    ty = 1.25 + row * 1.45
    add_rect(sl, lx, ty, 6.1, 1.3, fill=WHITE, line=RGBColor(0xCC,0xCC,0xCC))
    add_rect(sl, lx, ty, 0.65, 1.3, fill=BLUE_MID)
    add_text(sl, num, lx+0.04, ty+0.3, 0.58, 0.7,
             size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, title, lx+0.75, ty+0.12, 5.2, 0.45,
             size=15, bold=True, color=BLUE_DARK)
    add_text(sl, desc,  lx+0.75, ty+0.58, 5.2, 0.4,
             size=11, color=GRAY_TEXT)

# ════════════════════════════════════════════
# 슬라이드 3 — 프로젝트 개요
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "01  프로젝트 개요")
add_text(sl, "프로젝트 목적", 0.4, 1.2, 6.0, 0.35, size=14, bold=True, color=BLUE_DARK)
add_bullet_box(sl, [
    "✔  의료진이 만성질환(당뇨·고혈압) 환자의 혈당·혈압 측정값을 등록·조회",
    "✔  규칙 기반 알고리즘으로 위험도(정상/주의/위험)를 자동 산정",
    "✔  고위험군 환자를 우선적으로 모니터링할 수 있도록 지원",
    "✔  알림 자동 생성 및 통계 화면으로 전체 추이 파악",
], 0.4, 1.55, 6.0, 1.35)

add_text(sl, "기술 스택", 0.4, 3.0, 6.0, 0.35, size=14, bold=True, color=BLUE_DARK)
techs = [
    ("DB",      "Microsoft SQL Server 2025",   BLUE_DARK),
    ("Backend", "Blazor Web App  (.NET 10)",   BLUE_MID),
    ("ORM",     "Dapper  +  저장 프로시저",   GREEN),
    ("UI",      "Bootstrap 5  +  Bootstrap Icons", ORANGE),
]
for j, (label, val, clr) in enumerate(techs):
    lx = 0.4 + (j % 2) * 3.1
    ty = 3.4 + (j // 2) * 0.55
    add_rect(sl, lx, ty, 2.9, 0.45, fill=clr)
    add_text(sl, f"{label}  :  {val}", lx+0.12, ty+0.06, 2.75, 0.35,
             size=11, bold=True, color=WHITE)

add_text(sl, "시스템 흐름 요약", 6.6, 1.2, 6.3, 0.35, size=14, bold=True, color=BLUE_DARK)
flow_items = [
    ("1", "의료진 로그인",           BLUE_DARK),
    ("2", "환자 등록 / 조회 / 수정", BLUE_MID),
    ("3", "측정값 입력 (혈당·혈압)", BLUE_MID),
    ("4", "위험도 자동 계산",        RED),
    ("5", "위험 시 알림 자동 생성",  RED),
    ("6", "통계 화면으로 추이 파악", GREEN),
]
for j, (num, text, clr) in enumerate(flow_items):
    ty = 1.55 + j * 0.72
    add_rect(sl, 6.6, ty, 0.45, 0.52, fill=clr)
    add_text(sl, num, 6.6, ty+0.05, 0.45, 0.42,
             size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(sl, 7.1, ty, 5.7, 0.52, fill=GRAY_LIGHT,
             line=RGBColor(0xCC,0xCC,0xCC))
    add_text(sl, text, 7.22, ty+0.1, 5.5, 0.35, size=12, color=GRAY_TEXT)
    if j < 5:
        add_text(sl, "▼", 6.77, ty+0.56, 0.3, 0.2,
                 size=9, color=BLUE_MID, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════
# 슬라이드 4 — 업무 분석 / Flow
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "02  업무 분석  —  업무 Flow")
add_text(sl, "[의료진 로그인]", 5.9, 1.15, 2.5, 0.45,
         size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_rect(sl, 5.9, 1.15, 2.5, 0.42, fill=BLUE_DARK)
add_text(sl, "[의료진 로그인]", 5.9, 1.2, 2.5, 0.35,
         size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "▼", 7.0, 1.6, 0.4, 0.35, size=14, bold=True,
         color=BLUE_DARK, align=PP_ALIGN.CENTER)
add_rect(sl, 4.2, 1.95, 5.0, 0.42, fill=BLUE_MID)
add_text(sl, "[메인 메뉴  —  전체 기능 한 화면 노출]", 4.2, 2.0, 5.0, 0.35,
         size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

boxes = [
    (0.4,  3.0, 3.0, "환자 관리",      ["신규 환자 등록","조회 / 수정 / 삭제"],                    BLUE_DARK),
    (3.7,  3.0, 3.0, "측정기록 관리",  ["혈당·혈압 입력","위험도 자동 계산","Alert 자동 생성"],   RED),
    (7.0,  3.0, 2.5, "알림 관리",      ["미확인 알림 조회","확인 / 처리완료"],                     ORANGE),
    (9.8,  3.0, 3.1, "통계 / 집계",    ["위험군 분포 통계","월별 측정 추이"],                      GREEN),
]
for lx, ty, w, title, items, clr in boxes:
    add_rect(sl, lx, ty-0.05, w, 0.42, fill=clr)
    add_text(sl, title, lx+0.1, ty, w-0.15, 0.35,
             size=12, bold=True, color=WHITE)
    bh = 0.32 * len(items) + 0.1
    add_rect(sl, lx, ty+0.38, w, bh, fill=GRAY_LIGHT,
             line=RGBColor(0xCC,0xCC,0xCC))
    for k, item in enumerate(items):
        add_text(sl, f"• {item}", lx+0.15, ty+0.45+k*0.32, w-0.2, 0.3,
                 size=10.5, color=GRAY_TEXT)

add_text(sl, "핵심 포인트 :  측정값 입력 → RiskCalculator 자동 계산 → 위험 시 Alert 자동 INSERT (SP 내 트랜잭션)",
         0.4, 6.75, 12.5, 0.35, size=11, bold=True, color=RED)

# ════════════════════════════════════════════
# 슬라이드 5 — DB 설계 (테이블)
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "03  DB 설계  —  테이블 구조")
tables = [
    ("Users",        "UserId (PK)\nLoginId  UNIQUE\nPassword\nName\nRole\nCreatedAt",                                          BLUE_DARK),
    ("Patients",     "PatientId (PK)\nName / Gender / BirthDate\nPhone / Address\nDiseaseType  (당뇨|고혈압|둘다)\nDoctorUserId (FK→Users)\nIsActive",  BLUE_MID),
    ("Measurements", "MeasurementId (PK)\nPatientId (FK→Patients)\nMeasureDate / MeasureType\nGlucoseLevel / SystolicBP\nDiastolicBP / HeartRate\nRiskScore / RiskLevel\nCreatedBy (FK→Users)",  RED),
    ("Alerts",       "AlertId (PK)\nPatientId (FK→Patients)\nMeasurementId (FK→Meas.)\nAlertDate / RiskLevel\nAlertMessage / Status\nCheckedBy (FK→Users)\nCheckedDate",                         ORANGE),
]
for i, (name, cols, clr) in enumerate(tables):
    lx = 0.35 + i * 3.22
    add_rect(sl, lx, 1.15, 3.0, 0.38, fill=clr)
    add_text(sl, name, lx+0.1, 1.18, 2.8, 0.32,
             size=13, bold=True, color=WHITE)
    lines = cols.split('\n')
    bh = 0.29 * len(lines) + 0.12
    add_rect(sl, lx, 1.53, 3.0, bh, fill=WHITE,
             line=RGBColor(0xCC,0xCC,0xCC))
    for k, line in enumerate(lines):
        add_text(sl, line, lx+0.15, 1.6+k*0.29, 2.8, 0.27,
                 size=9.5, color=GRAY_TEXT)

# ERD 관계 화살표 설명
add_text(sl, "ERD 관계", 0.35, 5.0, 12.6, 0.35, size=13, bold=True, color=BLUE_DARK)
add_rect(sl, 0.35, 5.35, 12.6, 0.6, fill=BLUE_LIGHT)
add_text(sl,
    "Users ←─── Patients (DoctorUserId)     │     Patients ←─── Measurements (PatientId)     │     Measurements ←─── Alerts (MeasurementId)     │     Patients ←─── Alerts (PatientId)",
    0.5, 5.42, 12.3, 0.45, size=10.5, color=BLUE_DARK)
add_text(sl, f"시드 데이터  :  Users 10명  │  Patients 30명  │  Measurements 90건 (위험:30 / 주의:30 / 정상:30)  │  Alerts 30건",
         0.35, 6.1, 12.6, 0.38, size=11, bold=True, color=GRAY_TEXT)

# ════════════════════════════════════════════
# 슬라이드 6 — 저장 프로시저
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "03  DB 설계  —  저장 프로시저 (15개)")
sps = [
    ("SELECT", [
        "usp_User_Login",
        "usp_Patient_SelectAll",
        "usp_Patient_GetById",
        "usp_Measurement_SelectAll",
        "usp_Measurement_SelectByPatient",
        "usp_Stat_RiskDistribution",
        "usp_Stat_MonthlyTrend",
    ], BLUE_DARK),
    ("INSERT", [
        "usp_Patient_Insert",
        "usp_Measurement_Insert\n  ↳ 위험 시 Alert 자동 INSERT",
    ], GREEN),
    ("UPDATE", [
        "usp_Patient_Update",
        "usp_Measurement_Update",
        "usp_Alert_UpdateStatus",
    ], ORANGE),
    ("DELETE", [
        "usp_Patient_Delete\n  ↳ Alerts → Measurements\n     → Patient 순 삭제",
        "usp_Measurement_Delete",
    ], RED),
]
for i, (op, items, clr) in enumerate(sps):
    lx = 0.35 + i * 3.24
    add_rect(sl, lx, 1.15, 3.1, 0.4, fill=clr)
    add_text(sl, op, lx+0.1, 1.18, 3.0, 0.33,
             size=14, bold=True, color=WHITE)
    bh = max(0.32 * len(items) + 0.25, 1.4)
    add_rect(sl, lx, 1.55, 3.1, bh, fill=GRAY_LIGHT,
             line=RGBColor(0xCC,0xCC,0xCC))
    for k, sp in enumerate(items):
        add_text(sl, f"• {sp}", lx+0.15, 1.62+k*0.55, 2.9, 0.52,
                 size=10, color=GRAY_TEXT)

add_code_box(sl, """\
CREATE PROCEDURE usp_Measurement_Insert
    @PatientId INT, @MeasureDate DATETIME,
    @GlucoseLevel INT=NULL, @SystolicBP INT=NULL, @DiastolicBP INT=NULL,
    @RiskScore INT, @RiskLevel NVARCHAR(10), ...
AS BEGIN
    BEGIN TRANSACTION;
    INSERT INTO Measurements (...) VALUES (...);
    DECLARE @NewId INT = SCOPE_IDENTITY();

    IF @RiskLevel = N'위험'   -- ← 위험 시 Alert 자동 생성
    BEGIN
        INSERT INTO Alerts (PatientId, MeasurementId, RiskLevel, AlertMessage, Status)
        VALUES (@PatientId, @NewId, @RiskLevel, N'[위험] ' + @PName + ..., N'미확인');
    END
    SELECT @NewId AS NewId;
    COMMIT;
END""",
0.35, 3.7, 12.6, 3.2, title="핵심 SP — usp_Measurement_Insert (트랜잭션 + 자동 알림)")

# ════════════════════════════════════════════
# 슬라이드 7 — 화면 설계
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "04  화면 설계  —  전체 구성")
screens = [
    ("/login",                    "로그인",         "admin / 1234  인증",           BLUE_DARK),
    ("/",                         "대시보드",       "요약 카드 · 위험군 분포 · 알림 · 우선순위 큐", BLUE_MID),
    ("/patients",                 "환자 목록",      "검색 · 필터 · 테이블",         BLUE_DARK),
    ("/patients/create",          "환자 등록",      "폼 입력 · 유효성 검사",        BLUE_MID),
    ("/patients/edit/{id}",       "환자 수정",      "기존 데이터 로드 · 수정 저장", BLUE_DARK),
    ("/measurements",             "측정 목록",      "환자별·위험도별 필터",         RED),
    ("/measurements/create",      "측정 등록",      "실시간 위험도 계산 · 기준표",  RED),
    ("/alerts",                   "알림 관리",      "상태 필터 · 확인/처리완료 변경", ORANGE),
    ("/statistics/distribution",  "위험군 분포",    "카드 · 프로그레스바 · 위험환자 목록", GREEN),
    ("/statistics/trend",         "월별 추이",      "환자 선택 · 테이블 · 텍스트 차트", GREEN),
]
for i, (url, title, desc, clr) in enumerate(screens):
    col = i % 2
    row = i // 2
    lx = 0.35 + col * 6.5
    ty = 1.2 + row * 1.18
    add_rect(sl, lx, ty, 6.2, 1.1, fill=WHITE,
             line=RGBColor(0xCC,0xCC,0xCC))
    add_rect(sl, lx, ty, 6.2, 0.38, fill=clr)
    add_text(sl, title, lx+0.12, ty+0.06, 3.5, 0.3,
             size=12, bold=True, color=WHITE)
    add_text(sl, url, lx+3.5, ty+0.08, 2.6, 0.26,
             size=9, color=RGBColor(0xAA,0xC4,0xE8), align=PP_ALIGN.RIGHT)
    add_text(sl, desc, lx+0.15, ty+0.46, 5.9, 0.5,
             size=10.5, color=GRAY_TEXT)

# ════════════════════════════════════════════
# 슬라이드 8 — 핵심 구현 : 위험도 알고리즘
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "05  핵심 구현  —  위험도 자동 계산 알고리즘")

add_text(sl, "RiskCalculator.cs", 0.4, 1.15, 7.5, 0.35,
         size=13, bold=True, color=BLUE_DARK)
add_code_box(sl, """\
public static class RiskCalculator
{
    public static (int Score, string Level)
        Calculate(int? glucose, int? systolic, int? diastolic)
    {
        int score = 0;

        if (glucose  >= 126) score += 2;   // 당뇨 위험
        else if (glucose  >= 100) score += 1;   // 당뇨 주의

        if (systolic >= 140) score += 2;   // 혈압 위험
        else if (systolic >= 120) score += 1;   // 혈압 주의

        if (diastolic >= 90)  score += 2;  // 혈압 위험
        else if (diastolic >= 80)  score += 1;  // 혈압 주의

        string level = score switch {
            >= 4 => "위험",   // 빨강 — 알림 자동 생성
            >= 2 => "주의",   // 노랑
            _    => "정상"    // 초록
        };
        return (score, level);
    }
}""", 0.4, 1.5, 7.5, 4.8)

add_text(sl, "위험도 산정 기준표", 8.2, 1.15, 4.8, 0.35,
         size=13, bold=True, color=BLUE_DARK)
criteria = [
    ("항목",     "정상 (0점)", "주의 (+1점)", "위험 (+2점)", BLUE_DARK),
    ("혈당",     "< 100",      "100 ~ 125",  "≥ 126",       None),
    ("수축기 BP","< 120",      "120 ~ 139",  "≥ 140",       None),
    ("이완기 BP","< 80",       "80 ~ 89",    "≥ 90",        None),
]
for k, (item, n, w, d, hdr) in enumerate(criteria):
    ty = 1.52 + k * 0.48
    bg = BLUE_DARK if hdr else (GRAY_LIGHT if k % 2 == 0 else WHITE)
    fc = WHITE if hdr else GRAY_TEXT
    add_rect(sl, 8.2, ty, 4.8, 0.46, fill=bg,
             line=RGBColor(0xCC,0xCC,0xCC))
    for j, val in enumerate([item, n, w, d]):
        add_text(sl, val, 8.2+j*1.2, ty+0.09, 1.18, 0.3,
                 size=10, bold=(k==0), color=fc, align=PP_ALIGN.CENTER)

add_rect(sl, 8.2, 3.5, 4.8, 0.48, fill=RED)
add_text(sl, "합산 ≥ 4점 : 위험  →  알림 자동 생성", 8.3, 3.58, 4.6, 0.35,
         size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_rect(sl, 8.2, 4.0, 4.8, 0.48, fill=ORANGE)
add_text(sl, "합산 2~3점 : 주의  →  경고 표시", 8.3, 4.08, 4.6, 0.35,
         size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_rect(sl, 8.2, 4.5, 4.8, 0.48, fill=GREEN)
add_text(sl, "합산 0~1점 : 정상  →  녹색 표시", 8.3, 4.58, 4.6, 0.35,
         size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(sl, "예시)  혈당 145 (+2점) + 수축기 155 (+2점) + 이완기 98 (+2점)  =  6점  →  위험  →  알림 생성",
         0.4, 6.65, 12.5, 0.38, size=11, bold=True, color=RED)

# ════════════════════════════════════════════
# 슬라이드 9 — 핵심 구현 : 인증 + CRUD
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "05  핵심 구현  —  인증 서비스 & CRUD 패턴")

add_text(sl, "AuthService.cs  (Scoped — 회로 단위 세션 유지)",
         0.4, 1.15, 6.3, 0.35, size=12, bold=True, color=BLUE_DARK)
add_code_box(sl, """\
// Scoped 서비스 → SignalR 회로 동안 상태 유지
public class AuthService
{
    public UserModel? CurrentUser { get; private set; }
    public bool IsAuthenticated => CurrentUser != null;

    public async Task<bool> LoginAsync(string id, string pw)
    {
        var user = await conn.QuerySingleOrDefaultAsync<UserModel>(
            "usp_User_Login",
            new { LoginId=id, Password=pw },
            commandType: StoredProcedure);

        if (user == null) return false;
        CurrentUser = user;
        return true;
    }
}""", 0.4, 1.5, 6.3, 3.4)

add_text(sl, "PatientRepository.cs  (Dapper + SP 호출)",
         6.9, 1.15, 6.1, 0.35, size=12, bold=True, color=BLUE_DARK)
add_code_box(sl, """\
public class PatientRepository
{
    // List<T> — 전체 목록 조회
    public async Task<List<PatientModel>> GetAllAsync()
    {
        var result = await conn.QueryAsync<PatientModel>(
            "usp_Patient_SelectAll",
            commandType: StoredProcedure);
        return result.ToList();
    }

    // Insert — SP 호출 후 신규 ID 반환
    public async Task<int> InsertAsync(PatientModel p)
    {
        return await conn.QuerySingleAsync<int>(
            "usp_Patient_Insert",
            new { p.Name, p.Gender, p.BirthDate,
                  p.DiseaseType, p.DoctorUserId },
            commandType: StoredProcedure);
    }
}""", 6.9, 1.5, 6.1, 3.85)

add_text(sl, "Collection 자료구조 활용", 0.4, 5.0, 12.5, 0.35,
         size=12, bold=True, color=BLUE_DARK)
coll_items = [
    ("List<MeasurementModel>",        "환자별 측정 이력 목록 표시",                     BLUE_MID),
    ("Dictionary<int, PatientModel>", "환자 캐시 — 알림/대시보드에서 이름 빠른 조회",  BLUE_DARK),
    ("SortedList (우선순위 큐)",       "오늘의 모니터링 우선순위 — 위험도 내림차순",     RED),
]
for j, (name, desc, clr) in enumerate(coll_items):
    lx = 0.4 + j * 4.2
    add_rect(sl, lx, 5.38, 4.0, 0.38, fill=clr)
    add_text(sl, name, lx+0.1, 5.43, 3.8, 0.3,
             size=10, bold=True, color=WHITE)
    add_text(sl, desc, lx+0.1, 5.8, 3.8, 0.35,
             size=9.5, color=GRAY_TEXT)

# ════════════════════════════════════════════
# 슬라이드 10 — 통계 기능
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "05  핵심 구현  —  통계 기능 2종")

add_text(sl, "① 위험군 분포 통계  —  usp_Stat_RiskDistribution",
         0.4, 1.15, 12.5, 0.35, size=13, bold=True, color=BLUE_DARK)
add_code_box(sl, """\
-- 환자별 가장 최근 측정값 기준으로 위험등급 집계
SELECT m.RiskLevel, COUNT(*) AS Cnt
FROM Measurements m
INNER JOIN (
    SELECT PatientId, MAX(MeasureDate) AS LastDate
    FROM Measurements GROUP BY PatientId
) latest ON m.PatientId=latest.PatientId
       AND m.MeasureDate=latest.LastDate
GROUP BY m.RiskLevel
ORDER BY CASE m.RiskLevel
    WHEN N'위험' THEN 1 WHEN N'주의' THEN 2 ELSE 3 END;""",
0.4, 1.52, 6.2, 2.5)

# 위험군 분포 시각화 예시
for j, (label, cnt, clr) in enumerate([("위험",10,RED),("주의",10,ORANGE),("정상",10,GREEN)]):
    lx = 6.8 + j * 2.15
    ty = 1.52
    add_rect(sl, lx, ty, 2.0, 0.4, fill=clr)
    add_text(sl, label, lx, ty+0.06, 2.0, 0.3,
             size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, f"{cnt}명 (33%)", lx, ty+0.45, 2.0, 0.35,
             size=12, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_rect(sl, lx+0.2, ty+0.83, 1.6, 0.45, fill=clr)

add_text(sl, "② 월별 측정 추이  —  usp_Stat_MonthlyTrend",
         0.4, 4.15, 12.5, 0.35, size=13, bold=True, color=BLUE_DARK)
add_code_box(sl, """\
SELECT FORMAT(MeasureDate,'yyyy-MM') AS YearMonth,
       AVG(CAST(GlucoseLevel AS FLOAT)) AS AvgGlucose,
       AVG(CAST(SystolicBP  AS FLOAT))  AS AvgSystolic,
       AVG(CAST(DiastolicBP AS FLOAT))  AS AvgDiastolic,
       COUNT(*) AS MeasureCnt
FROM Measurements
WHERE (@PatientId IS NULL OR PatientId = @PatientId)
GROUP BY FORMAT(MeasureDate,'yyyy-MM')
ORDER BY YearMonth;""",
0.4, 4.52, 6.2, 2.3)

# 월별 추이 표 예시
cols_h = ["연월","평균 혈당","평균 수축기","평균 이완기","건수"]
rows_d = [
    ["2026-01","88.0","112.0","70.0","30"],
    ["2026-04","111.7","126.0","80.7","30"],
    ["2026-06","119.3","138.7","90.0","30"],
]
add_rect(sl, 6.8, 4.52, 6.1, 0.38, fill=BLUE_DARK)
for j, h in enumerate(cols_h):
    add_text(sl, h, 6.8+j*1.22, 4.57, 1.2, 0.3,
             size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
for r, row in enumerate(rows_d):
    bg = GRAY_LIGHT if r%2==0 else WHITE
    add_rect(sl, 6.8, 4.9+r*0.38, 6.1, 0.37, fill=bg,
             line=RGBColor(0xCC,0xCC,0xCC))
    for j, val in enumerate(row):
        clr_text = RED if (j in [1,2] and float(val.replace(',','')) > 120) else GRAY_TEXT
        add_text(sl, val, 6.8+j*1.22, 4.95+r*0.38, 1.2, 0.28,
                 size=9.5, color=clr_text, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════
# 슬라이드 11 — 테스트 시나리오
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "06  테스트 시나리오  —  발표 실행 흐름")
steps = [
    ("STEP 1", "로그인",
     "• URL : http://localhost:5221/login\n• ID: admin  /  PW: 1234\n• 로그인 성공 → 대시보드 이동",
     BLUE_DARK),
    ("STEP 2", "대시보드 확인",
     "• 전체 환자 30명 / 위험 환자 10명 / 미확인 알림 10건\n• 위험군 분포 프로그레스바 확인\n• 오늘의 모니터링 우선순위 큐 확인",
     BLUE_MID),
    ("STEP 3", "환자 등록",
     "• [환자 등록] 메뉴 → 신규 환자 입력\n• 이름·성별·생년월일·질환 유형·담당의 선택\n• 저장 → 목록에서 신규 환자 확인",
     GREEN),
    ("STEP 4", "측정 등록 & 위험도 확인",
     "• [측정 등록] → 방금 등록한 환자 선택\n• 혈당 130, 수축기 145, 이완기 92 입력\n• 우측 패널에 RiskScore 6점 / 위험 즉시 표시\n• 저장 → 알림 자동 생성 확인",
     RED),
    ("STEP 5", "알림 처리",
     "• [알림 관리] → 미확인 알림 확인\n• '확인' 버튼 → '처리완료' 버튼 클릭\n• 상태 변경 확인",
     ORANGE),
    ("STEP 6", "통계 확인",
     "• [위험군 분포] → 위험 10명 반영 확인\n• [월별 추이] → 전체 환자 또는 개별 환자 선택\n• 월별 평균 혈당·혈압 추이 테이블 확인",
     BLUE_DARK),
]
for i, (step, title, desc, clr) in enumerate(steps):
    col = i % 2
    row = i // 2
    lx = 0.35 + col * 6.5
    ty = 1.2 + row * 1.88
    add_rect(sl, lx, ty, 6.2, 1.8, fill=WHITE,
             line=RGBColor(0xCC,0xCC,0xCC))
    add_rect(sl, lx, ty, 6.2, 0.42, fill=clr)
    add_text(sl, step, lx+0.12, ty+0.08, 1.1, 0.3,
             size=10, bold=True, color=WHITE)
    add_text(sl, title, lx+1.2, ty+0.09, 4.8, 0.3,
             size=12, bold=True, color=WHITE)
    add_text(sl, desc, lx+0.15, ty+0.5, 5.9, 1.2,
             size=10, color=GRAY_TEXT)

# ════════════════════════════════════════════
# 슬라이드 12 — 느낀점 & 결론
# ════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "07  느낀점 & 결론")

add_text(sl, "배운 점", 0.4, 1.2, 5.8, 0.38, size=14, bold=True, color=BLUE_DARK)
add_bullet_box(sl, [
    "✦ 저장 프로시저로 비즈니스 로직을 DB에 캡슐화하면",
    "    C# 코드가 단순해지고 유지보수가 편리해짐",
    "",
    "✦ RiskCalculator를 별도 static 클래스로 분리하여",
    "    재사용성과 테스트 용이성을 높임",
    "",
    "✦ Scoped AuthService를 통해 ASP.NET Identity 없이도",
    "    Blazor Server 세션 인증 구현 가능함을 확인",
    "",
    "✦ Dictionary / SortedList 등 컬렉션 자료구조로",
    "    성능 최적화 및 우선순위 정렬을 실제 적용",
], 0.4, 1.6, 5.8, 3.8)

add_text(sl, "개선 방향", 6.5, 1.2, 6.4, 0.38, size=14, bold=True, color=BLUE_DARK)
add_bullet_box(sl, [
    "◆ 비밀번호 해싱 (bcrypt) 적용으로 보안 강화",
    "",
    "◆ Chart.js 연동하여 통계를 실제 그래프로 시각화",
    "",
    "◆ ML.NET 기반 머신러닝 위험도 예측 모델 도입",
    "",
    "◆ 모바일 반응형 UI 개선",
    "",
    "◆ 실시간 알림 (SignalR 브로드캐스트) 구현",
], 6.5, 1.6, 6.4, 3.8)

add_rect(sl, 0.4, 5.6, 12.5, 0.002, fill=BLUE_DARK)
add_rect(sl, 0.4, 5.65, 12.5, 1.2, fill=BLUE_DARK)
add_text(sl,
    "MSSQL 저장 프로시저 15개 + Blazor Server 인터랙티브 UI + 규칙 기반 위험도 알고리즘의 결합으로\n"
    "실무 수준의 만성질환 모니터링 시스템을 성공적으로 구현하였습니다.",
    0.6, 5.75, 12.1, 0.95,
    size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════
# 저장
# ════════════════════════════════════════════
out = r"C:\Users\kjw52\OneDrive\Desktop\work\blazor\만성질환_모니터링_시스템_기말과제.pptx"
prs.save(out)
print(f"저장 완료: {out}")
print(f"슬라이드 수: {len(prs.slides)}")
