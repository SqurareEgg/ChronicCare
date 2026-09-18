using System.Data;
using Dapper;
using ChronicCare.Models;

namespace ChronicCare.Data;

public class AlertRepository
{
    private readonly DatabaseHelper _db;
    public AlertRepository(DatabaseHelper db) => _db = db;

    public async Task<List<AlertModel>> GetAllAsync(string? status = null)
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<AlertModel>(
            "usp_Alert_SelectAll",
            new { Status = status },
            commandType: CommandType.StoredProcedure);
        return result.ToList();
    }

    public async Task UpdateStatusAsync(int alertId, string status, int checkedBy)
    {
        using var conn = _db.GetConnection();
        await conn.ExecuteAsync(
            "usp_Alert_UpdateStatus",
            new { AlertId = alertId, Status = status, CheckedBy = checkedBy },
            commandType: CommandType.StoredProcedure);
    }
}
