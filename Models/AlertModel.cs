namespace ChronicCare.Models;

public class AlertModel
{
    public int AlertId { get; set; }
    public int PatientId { get; set; }
    public int MeasurementId { get; set; }
    public DateTime AlertDate { get; set; }
    public string RiskLevel { get; set; } = "";
    public string? AlertMessage { get; set; }
    public string Status { get; set; } = "미확인";
    public int? CheckedBy { get; set; }
    public DateTime? CheckedDate { get; set; }

    // JOIN으로 채워지는 표시용 필드
    public string PatientName { get; set; } = "";
    public string CheckedByName { get; set; } = "";
}
