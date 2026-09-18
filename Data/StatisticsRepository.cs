using System.Data;
using Dapper;
using ChronicCare.Models;

namespace ChronicCare.Data;

public class StatisticsRepository
{
    private readonly DatabaseHelper _db;
    public StatisticsRepository(DatabaseHelper db) => _db = db;

    public async Task<List<RiskDistributionItem>> GetRiskDistributionAsync()
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<RiskDistributionItem>(
            "usp_Stat_RiskDistribution", commandType: CommandType.StoredProcedure);
        return result.ToList();
    }

    public async Task<List<MonthlyTrendItem>> GetMonthlyTrendAsync(int? patientId = null)
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<MonthlyTrendItem>(
            "usp_Stat_MonthlyTrend",
            new { PatientId = patientId },
            commandType: CommandType.StoredProcedure);
        return result.ToList();
    }
}
