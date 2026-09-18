-- ============================================================
-- ChronicCareDB 전체 설정 스크립트
-- DB 생성 → 테이블 → 저장프로시저 → 시드데이터
-- ============================================================

USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = N'ChronicCareDB')
BEGIN
    ALTER DATABASE ChronicCareDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE ChronicCareDB;
END
GO

CREATE DATABASE ChronicCareDB;
GO

USE ChronicCareDB;
GO

-- ============================================================
-- 1. 테이블 생성
-- ============================================================

CREATE TABLE Users (
    UserId    INT IDENTITY(1,1) PRIMARY KEY,
    LoginId   VARCHAR(50)   NOT NULL,
    Password  VARCHAR(100)  NOT NULL,
    Name      NVARCHAR(50)  NOT NULL,
    Role      NVARCHAR(20)  NOT NULL DEFAULT N'간호사',
    CreatedAt DATETIME      NOT NULL DEFAULT GETDATE(),
    CONSTRAINT UQ_Users_LoginId UNIQUE (LoginId)
);
GO

CREATE TABLE Patients (
    PatientId      INT IDENTITY(1,1) PRIMARY KEY,
    Name           NVARCHAR(50)  NOT NULL,
    Gender         CHAR(1)       NOT NULL,
    BirthDate      DATE          NOT NULL,
    Phone          VARCHAR(20)   NULL,
    Address        NVARCHAR(200) NULL,
    DiseaseType    NVARCHAR(20)  NOT NULL,
    DoctorUserId   INT           NULL,
    RegisteredDate DATETIME      NOT NULL DEFAULT GETDATE(),
    IsActive       BIT           NOT NULL DEFAULT 1,
    CONSTRAINT FK_Patients_Users FOREIGN KEY (DoctorUserId) REFERENCES Users(UserId)
);
CREATE INDEX IX_Patients_DiseaseType ON Patients(DiseaseType);
CREATE INDEX IX_Patients_DoctorUserId ON Patients(DoctorUserId);
GO

CREATE TABLE Measurements (
    MeasurementId INT IDENTITY(1,1) PRIMARY KEY,
    PatientId     INT           NOT NULL,
    MeasureDate   DATETIME      NOT NULL DEFAULT GETDATE(),
    MeasureType   NVARCHAR(20)  NOT NULL,
    GlucoseLevel  INT           NULL,
    SystolicBP    INT           NULL,
    DiastolicBP   INT           NULL,
    HeartRate     INT           NULL,
    RiskScore     INT           NOT NULL DEFAULT 0,
    RiskLevel     NVARCHAR(10)  NOT NULL DEFAULT N'정상',
    Note          NVARCHAR(200) NULL,
    CreatedBy     INT           NULL,
    CONSTRAINT FK_Measurements_Patients FOREIGN KEY (PatientId) REFERENCES Patients(PatientId),
    CONSTRAINT FK_Measurements_Users    FOREIGN KEY (CreatedBy)  REFERENCES Users(UserId)
);
CREATE INDEX IX_Measurements_PatientId   ON Measurements(PatientId);
CREATE INDEX IX_Measurements_MeasureDate ON Measurements(MeasureDate);
CREATE INDEX IX_Measurements_RiskLevel   ON Measurements(RiskLevel);
GO

CREATE TABLE Alerts (
    AlertId       INT IDENTITY(1,1) PRIMARY KEY,
    PatientId     INT           NOT NULL,
    MeasurementId INT           NOT NULL,
    AlertDate     DATETIME      NOT NULL DEFAULT GETDATE(),
    RiskLevel     NVARCHAR(10)  NOT NULL,
    AlertMessage  NVARCHAR(200) NULL,
    Status        NVARCHAR(20)  NOT NULL DEFAULT N'미확인',
    CheckedBy     INT           NULL,
    CheckedDate   DATETIME      NULL,
    CONSTRAINT FK_Alerts_Patients     FOREIGN KEY (PatientId)     REFERENCES Patients(PatientId),
    CONSTRAINT FK_Alerts_Measurements FOREIGN KEY (MeasurementId) REFERENCES Measurements(MeasurementId),
    CONSTRAINT FK_Alerts_Users        FOREIGN KEY (CheckedBy)      REFERENCES Users(UserId)
);
CREATE INDEX IX_Alerts_Status    ON Alerts(Status);
CREATE INDEX IX_Alerts_PatientId ON Alerts(PatientId);
GO

-- ============================================================
-- 2. 저장 프로시저
-- ============================================================

-- SP1: 로그인 검증
CREATE PROCEDURE usp_User_Login
    @LoginId  VARCHAR(50),
    @Password VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT UserId, LoginId, Name, Role
    FROM Users
    WHERE LoginId = @LoginId AND Password = @Password;
END
GO

-- SP2: 환자 전체 조회 (담당의 이름 포함)
CREATE PROCEDURE usp_Patient_SelectAll
AS
BEGIN
    SET NOCOUNT ON;
    SELECT p.PatientId, p.Name, p.Gender, p.BirthDate, p.Phone, p.Address,
           p.DiseaseType, p.DoctorUserId, p.RegisteredDate, p.IsActive,
           u.Name AS DoctorName
    FROM Patients p
    LEFT JOIN Users u ON p.DoctorUserId = u.UserId
    WHERE p.IsActive = 1
    ORDER BY p.RegisteredDate DESC;
END
GO

-- SP3: 환자 단건 조회
CREATE PROCEDURE usp_Patient_GetById
    @PatientId INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT p.PatientId, p.Name, p.Gender, p.BirthDate, p.Phone, p.Address,
           p.DiseaseType, p.DoctorUserId, p.RegisteredDate, p.IsActive,
           u.Name AS DoctorName
    FROM Patients p
    LEFT JOIN Users u ON p.DoctorUserId = u.UserId
    WHERE p.PatientId = @PatientId;
END
GO

-- SP4: 환자 등록 (Insert)
CREATE PROCEDURE usp_Patient_Insert
    @Name         NVARCHAR(50),
    @Gender       CHAR(1),
    @BirthDate    DATE,
    @Phone        VARCHAR(20) = NULL,
    @Address      NVARCHAR(200) = NULL,
    @DiseaseType  NVARCHAR(20),
    @DoctorUserId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Patients (Name, Gender, BirthDate, Phone, Address, DiseaseType, DoctorUserId)
    VALUES (@Name, @Gender, @BirthDate, @Phone, @Address, @DiseaseType, @DoctorUserId);
    SELECT CAST(SCOPE_IDENTITY() AS INT) AS NewId;
END
GO

-- SP5: 환자 수정 (Update)
CREATE PROCEDURE usp_Patient_Update
    @PatientId    INT,
    @Name         NVARCHAR(50),
    @Gender       CHAR(1),
    @BirthDate    DATE,
    @Phone        VARCHAR(20) = NULL,
    @Address      NVARCHAR(200) = NULL,
    @DiseaseType  NVARCHAR(20),
    @DoctorUserId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Patients
    SET Name = @Name, Gender = @Gender, BirthDate = @BirthDate,
        Phone = @Phone, Address = @Address, DiseaseType = @DiseaseType,
        DoctorUserId = @DoctorUserId
    WHERE PatientId = @PatientId;
END
GO

-- SP6: 환자 삭제 (Delete — 연관 레코드 먼저 삭제 후 소프트 삭제)
CREATE PROCEDURE usp_Patient_Delete
    @PatientId INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        DELETE FROM Alerts WHERE PatientId = @PatientId;
        DELETE FROM Measurements WHERE PatientId = @PatientId;
        UPDATE Patients SET IsActive = 0 WHERE PatientId = @PatientId;
        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END
GO

-- SP7: 측정기록 전체 조회 (환자명 포함)
CREATE PROCEDURE usp_Measurement_SelectAll
AS
BEGIN
    SET NOCOUNT ON;
    SELECT m.MeasurementId, m.PatientId, m.MeasureDate, m.MeasureType,
           m.GlucoseLevel, m.SystolicBP, m.DiastolicBP, m.HeartRate,
           m.RiskScore, m.RiskLevel, m.Note, m.CreatedBy,
           p.Name AS PatientName
    FROM Measurements m
    INNER JOIN Patients p ON m.PatientId = p.PatientId
    ORDER BY m.MeasureDate DESC;
END
GO

-- SP8: 환자별 측정 이력 조회
CREATE PROCEDURE usp_Measurement_SelectByPatient
    @PatientId INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT m.MeasurementId, m.PatientId, m.MeasureDate, m.MeasureType,
           m.GlucoseLevel, m.SystolicBP, m.DiastolicBP, m.HeartRate,
           m.RiskScore, m.RiskLevel, m.Note, m.CreatedBy,
           p.Name AS PatientName
    FROM Measurements m
    INNER JOIN Patients p ON m.PatientId = p.PatientId
    WHERE m.PatientId = @PatientId
    ORDER BY m.MeasureDate DESC;
END
GO

-- SP9: 측정기록 등록 (Insert) — RiskLevel='위험'이면 Alert 자동 생성
CREATE PROCEDURE usp_Measurement_Insert
    @PatientId    INT,
    @MeasureDate  DATETIME,
    @MeasureType  NVARCHAR(20),
    @GlucoseLevel INT = NULL,
    @SystolicBP   INT = NULL,
    @DiastolicBP  INT = NULL,
    @HeartRate    INT = NULL,
    @RiskScore    INT,
    @RiskLevel    NVARCHAR(10),
    @Note         NVARCHAR(200) = NULL,
    @CreatedBy    INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        INSERT INTO Measurements
            (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, Note, CreatedBy)
        VALUES
            (@PatientId, @MeasureDate, @MeasureType, @GlucoseLevel, @SystolicBP, @DiastolicBP, @HeartRate, @RiskScore, @RiskLevel, @Note, @CreatedBy);

        DECLARE @NewMeasId INT = CAST(SCOPE_IDENTITY() AS INT);

        IF @RiskLevel = N'위험'
        BEGIN
            DECLARE @PName NVARCHAR(50);
            SELECT @PName = Name FROM Patients WHERE PatientId = @PatientId;
            INSERT INTO Alerts (PatientId, MeasurementId, RiskLevel, AlertMessage, Status)
            VALUES (@PatientId, @NewMeasId, @RiskLevel,
                    N'[위험] ' + @PName + N' 환자의 측정 수치가 위험 수준입니다.',
                    N'미확인');
        END

        SELECT @NewMeasId AS NewId;
        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END
GO

-- SP10: 측정기록 수정 (Update)
CREATE PROCEDURE usp_Measurement_Update
    @MeasurementId INT,
    @MeasureDate   DATETIME,
    @MeasureType   NVARCHAR(20),
    @GlucoseLevel  INT = NULL,
    @SystolicBP    INT = NULL,
    @DiastolicBP   INT = NULL,
    @HeartRate     INT = NULL,
    @RiskScore     INT,
    @RiskLevel     NVARCHAR(10),
    @Note          NVARCHAR(200) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Measurements
    SET MeasureDate = @MeasureDate, MeasureType = @MeasureType,
        GlucoseLevel = @GlucoseLevel, SystolicBP = @SystolicBP,
        DiastolicBP = @DiastolicBP, HeartRate = @HeartRate,
        RiskScore = @RiskScore, RiskLevel = @RiskLevel, Note = @Note
    WHERE MeasurementId = @MeasurementId;
END
GO

-- SP11: 측정기록 삭제 (Delete)
CREATE PROCEDURE usp_Measurement_Delete
    @MeasurementId INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        DELETE FROM Alerts WHERE MeasurementId = @MeasurementId;
        DELETE FROM Measurements WHERE MeasurementId = @MeasurementId;
        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH
END
GO

-- SP12: 알림 전체 조회
CREATE PROCEDURE usp_Alert_SelectAll
    @Status NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT a.AlertId, a.PatientId, a.MeasurementId, a.AlertDate,
           a.RiskLevel, a.AlertMessage, a.Status, a.CheckedBy, a.CheckedDate,
           p.Name AS PatientName,
           u.Name AS CheckedByName
    FROM Alerts a
    INNER JOIN Patients p ON a.PatientId = p.PatientId
    LEFT JOIN Users u ON a.CheckedBy = u.UserId
    WHERE (@Status IS NULL OR a.Status = @Status)
    ORDER BY a.AlertDate DESC;
END
GO

-- SP13: 알림 상태 변경 (Update)
CREATE PROCEDURE usp_Alert_UpdateStatus
    @AlertId    INT,
    @Status     NVARCHAR(20),
    @CheckedBy  INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Alerts
    SET Status = @Status, CheckedBy = @CheckedBy, CheckedDate = GETDATE()
    WHERE AlertId = @AlertId;
END
GO

-- SP14: 통계① 위험군 분포 (환자별 최신 측정값 기준)
CREATE PROCEDURE usp_Stat_RiskDistribution
AS
BEGIN
    SET NOCOUNT ON;
    SELECT m.RiskLevel, COUNT(*) AS Cnt
    FROM Measurements m
    INNER JOIN (
        SELECT PatientId, MAX(MeasureDate) AS LastDate
        FROM Measurements
        GROUP BY PatientId
    ) latest ON m.PatientId = latest.PatientId AND m.MeasureDate = latest.LastDate
    GROUP BY m.RiskLevel
    ORDER BY
        CASE m.RiskLevel WHEN N'위험' THEN 1 WHEN N'주의' THEN 2 ELSE 3 END;
END
GO

-- SP15: 통계② 월별 평균 혈당/혈압 추이
CREATE PROCEDURE usp_Stat_MonthlyTrend
    @PatientId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT FORMAT(MeasureDate, 'yyyy-MM') AS YearMonth,
           AVG(CAST(GlucoseLevel AS FLOAT)) AS AvgGlucose,
           AVG(CAST(SystolicBP  AS FLOAT))  AS AvgSystolic,
           AVG(CAST(DiastolicBP AS FLOAT))  AS AvgDiastolic,
           COUNT(*) AS MeasureCnt
    FROM Measurements
    WHERE (@PatientId IS NULL OR PatientId = @PatientId)
    GROUP BY FORMAT(MeasureDate, 'yyyy-MM')
    ORDER BY YearMonth;
END
GO

-- ============================================================
-- 3. 시드 데이터
-- ============================================================

-- 사용자 (10명)
INSERT INTO Users (LoginId, Password, Name, Role) VALUES
('admin',   '1234', N'관리자',  N'관리자'),
('doctor1', '1234', N'김철수',  N'의사'),
('doctor2', '1234', N'이영희',  N'의사'),
('doctor3', '1234', N'박민준',  N'의사'),
('doctor4', '1234', N'정수현',  N'의사'),
('doctor5', '1234', N'최지원',  N'의사'),
('nurse1',  '1234', N'한소희',  N'간호사'),
('nurse2',  '1234', N'강나연',  N'간호사'),
('nurse3',  '1234', N'윤지혜',  N'간호사'),
('nurse4',  '1234', N'임채원',  N'간호사');
GO

-- 환자 (30명): 당뇨 10명 / 고혈압 10명 / 둘다 10명
INSERT INTO Patients (Name, Gender, BirthDate, Phone, DiseaseType, DoctorUserId) VALUES
(N'김민수', 'M', '1968-03-15', '010-1111-2001', N'당뇨', 2),
(N'이서연', 'F', '1972-07-22', '010-1111-2002', N'당뇨', 3),
(N'박준호', 'M', '1955-11-08', '010-1111-2003', N'당뇨', 4),
(N'최지영', 'F', '1963-05-30', '010-1111-2004', N'당뇨', 5),
(N'정현석', 'M', '1948-09-12', '010-1111-2005', N'당뇨', 6),
(N'강미라', 'F', '1975-02-18', '010-1111-2006', N'당뇨', 2),
(N'윤태민', 'M', '1960-06-25', '010-1111-2007', N'당뇨', 3),
(N'장수현', 'F', '1952-08-03', '010-1111-2008', N'당뇨', 4),
(N'임동욱', 'M', '1945-04-17', '010-1111-2009', N'당뇨', 5),
(N'한지수', 'F', '1980-12-09', '010-1111-2010', N'당뇨', 6),
(N'오민재', 'M', '1958-01-21', '010-1111-2011', N'고혈압', 2),
(N'신혜린', 'F', '1966-10-14', '010-1111-2012', N'고혈압', 3),
(N'권성훈', 'M', '1943-07-28', '010-1111-2013', N'고혈압', 4),
(N'문지현', 'F', '1970-03-05', '010-1111-2014', N'고혈압', 5),
(N'배철호', 'M', '1953-09-19', '010-1111-2015', N'고혈압', 6),
(N'유나영', 'F', '1977-05-11', '010-1111-2016', N'고혈압', 2),
(N'안상민', 'M', '1961-11-23', '010-1111-2017', N'고혈압', 3),
(N'송다인', 'F', '1949-02-07', '010-1111-2018', N'고혈압', 4),
(N'홍준서', 'M', '1935-08-30', '010-1111-2019', N'고혈압', 5),
(N'전미경', 'F', '1964-04-16', '010-1111-2020', N'고혈압', 6),
(N'차재원', 'M', '1956-12-02', '010-1111-2021', N'둘다', 2),
(N'황수민', 'F', '1968-07-14', '010-1111-2022', N'둘다', 3),
(N'노준혁', 'M', '1950-01-26', '010-1111-2023', N'둘다', 4),
(N'서유진', 'F', '1973-06-08', '010-1111-2024', N'둘다', 5),
(N'고태연', 'M', '1940-10-20', '010-1111-2025', N'둘다', 6),
(N'류민정', 'F', '1960-03-12', '010-1111-2026', N'둘다', 2),
(N'성이준', 'M', '1947-08-24', '010-1111-2027', N'둘다', 3),
(N'마지원', 'F', '1955-05-06', '010-1111-2028', N'둘다', 4),
(N'백상훈', 'M', '1962-11-18', '010-1111-2029', N'둘다', 5),
(N'천하영', 'F', '1958-02-25', '010-1111-2030', N'둘다', 6);
GO

-- 측정기록 및 알림 시드 데이터
-- 그룹 A (환자 1~10):  정상→주의→위험 (최신=위험, 알림=미확인)
-- 그룹 B (환자 11~20): 정상→위험→주의 (최신=주의, 알림=확인)
-- 그룹 C (환자 21~30): 위험→주의→정상 (최신=정상, 알림=처리완료)
DECLARE @i    INT = 1;
DECLARE @uid  INT;
DECLARE @mid  INT;
DECLARE @pnm  NVARCHAR(50);

WHILE @i <= 30
BEGIN
    SET @uid = ((@i - 1) % 5) + 2;  -- doctor UserId 2~6 순환
    SELECT @pnm = Name FROM Patients WHERE PatientId = @i;

    IF @i <= 10
    BEGIN
        -- 측정1: 정상 (4개월 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -4, GETDATE()), N'둘다', 92, 114, 72, 74, 0, N'정상', @uid);

        -- 측정2: 주의 (2개월 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -2, GETDATE()), N'둘다', 115, 126, 83, 78, 3, N'주의', @uid);

        -- 측정3: 위험 (3일 전) → 알림 생성
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(DAY, -3, GETDATE()), N'둘다', 145, 155, 98, 92, 6, N'위험', @uid);
        SET @mid = CAST(SCOPE_IDENTITY() AS INT);

        INSERT INTO Alerts (PatientId, MeasurementId, RiskLevel, AlertMessage, Status)
        VALUES (@i, @mid, N'위험', N'[위험] ' + @pnm + N' 환자의 혈당·혈압 수치가 위험 수준입니다.', N'미확인');
    END
    ELSE IF @i <= 20
    BEGIN
        -- 측정1: 정상 (5개월 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -5, GETDATE()), N'둘다', 88, 112, 70, 72, 0, N'정상', @uid);

        -- 측정2: 위험 (2개월 전) → 알림 생성
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -2, GETDATE()), N'둘다', 130, 148, 95, 88, 6, N'위험', @uid);
        SET @mid = CAST(SCOPE_IDENTITY() AS INT);

        INSERT INTO Alerts (PatientId, MeasurementId, RiskLevel, AlertMessage, Status)
        VALUES (@i, @mid, N'위험', N'[위험] ' + @pnm + N' 환자의 혈당·혈압 수치가 위험 수준입니다.', N'확인');

        -- 측정3: 주의 (5일 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(DAY, -5, GETDATE()), N'둘다', 112, 128, 82, 80, 3, N'주의', @uid);
    END
    ELSE
    BEGIN
        -- 측정1: 위험 (5개월 전) → 알림 생성 (처리완료)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -5, GETDATE()), N'둘다', 158, 160, 102, 96, 6, N'위험', @uid);
        SET @mid = CAST(SCOPE_IDENTITY() AS INT);

        INSERT INTO Alerts (PatientId, MeasurementId, RiskLevel, AlertMessage, Status, CheckedBy, CheckedDate)
        VALUES (@i, @mid, N'위험', N'[위험] ' + @pnm + N' 환자의 혈당·혈압 수치가 위험 수준입니다.', N'처리완료', @uid, DATEADD(MONTH, -4, GETDATE()));

        -- 측정2: 주의 (2개월 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(MONTH, -2, GETDATE()), N'둘다', 110, 124, 80, 76, 2, N'주의', @uid);

        -- 측정3: 정상 (10일 전)
        INSERT INTO Measurements (PatientId, MeasureDate, MeasureType, GlucoseLevel, SystolicBP, DiastolicBP, HeartRate, RiskScore, RiskLevel, CreatedBy)
        VALUES (@i, DATEADD(DAY, -10, GETDATE()), N'둘다', 95, 116, 74, 70, 0, N'정상', @uid);
    END

    SET @i = @i + 1;
END
GO

-- 결과 확인
SELECT '사용자' AS 테이블, COUNT(*) AS 건수 FROM Users
UNION ALL SELECT '환자', COUNT(*) FROM Patients
UNION ALL SELECT '측정기록', COUNT(*) FROM Measurements
UNION ALL SELECT '알림', COUNT(*) FROM Alerts;
GO
