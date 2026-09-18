namespace ChronicCare.Models;

public class MeasurementModel
{
    public int MeasurementId { get; set; }
    public int PatientId { get; set; }
    public DateTime MeasureDate { get; set; } = DateTime.Now;
    public string MeasureType { get; set; } = "둘다";
    public int? GlucoseLevel { get; set; }
    public int? SystolicBP { get; set; }
    public int? DiastolicBP { get; set; }
    public int? HeartRate { get; set; }
    public int RiskScore { get; set; }
    public string RiskLevel { get; set; } = "정상";
    public string? Note { get; set; }
    public int? CreatedBy { get; set; }

    // JOIN으로 채워지는 표시용 필드
    public string PatientName { get; set; } = "";
}
