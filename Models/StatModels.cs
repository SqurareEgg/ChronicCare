namespace ChronicCare.Models;

public class RiskDistributionItem
{
    public string RiskLevel { get; set; } = "";
    public int Cnt { get; set; }
}

public class MonthlyTrendItem
{
    public string YearMonth { get; set; } = "";
    public double? AvgGlucose { get; set; }
    public double? AvgSystolic { get; set; }
    public double? AvgDiastolic { get; set; }
    public int MeasureCnt { get; set; }
}
