namespace ChronicCare.Models;

public static class RiskCalculator
{
    public static (int Score, string Level) Calculate(int? glucose, int? systolic, int? diastolic)
    {
        int score = 0;

        if (glucose.HasValue)
        {
            if (glucose >= 126) score += 2;
            else if (glucose >= 100) score += 1;
        }

        if (systolic.HasValue)
        {
            if (systolic >= 140) score += 2;
            else if (systolic >= 120) score += 1;
        }

        if (diastolic.HasValue)
        {
            if (diastolic >= 90) score += 2;
            else if (diastolic >= 80) score += 1;
        }

        string level = score switch
        {
            >= 4 => "위험",
            >= 2 => "주의",
            _    => "정상"
        };

        return (score, level);
    }

    public static string RiskBadgeClass(string level) => level switch
    {
        "위험" => "badge bg-danger",
        "주의" => "badge bg-warning text-dark",
        _     => "badge bg-success"
    };

    public static string RiskRowClass(string level) => level switch
    {
        "위험" => "table-danger",
        "주의" => "table-warning",
        _     => ""
    };
}
