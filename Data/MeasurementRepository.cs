using System.Data;
using Dapper;
using ChronicCare.Models;

namespace ChronicCare.Data;

public class MeasurementRepository
{
    private readonly DatabaseHelper _db;
    public MeasurementRepository(DatabaseHelper db) => _db = db;

    public async Task<List<MeasurementModel>> GetAllAsync()
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<MeasurementModel>(
            "usp_Measurement_SelectAll", commandType: CommandType.StoredProcedure);
        return result.ToList();
    }

    public async Task<List<MeasurementModel>> GetByPatientAsync(int patientId)
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<MeasurementModel>(
            "usp_Measurement_SelectByPatient",
            new { PatientId = patientId },
            commandType: CommandType.StoredProcedure);
        return result.ToList();
    }

    public async Task<int> InsertAsync(MeasurementModel m)
    {
        using var conn = _db.GetConnection();
        return await conn.QuerySingleAsync<int>(
            "usp_Measurement_Insert",
            new
            {
                m.PatientId, m.MeasureDate, m.MeasureType,
                m.GlucoseLevel, m.SystolicBP, m.DiastolicBP,
                m.HeartRate, m.RiskScore, m.RiskLevel, m.Note, m.CreatedBy
            },
            commandType: CommandType.StoredProcedure);
    }

    public async Task UpdateAsync(MeasurementModel m)
    {
        using var conn = _db.GetConnection();
        await conn.ExecuteAsync(
            "usp_Measurement_Update",
            new
            {
                m.MeasurementId, m.MeasureDate, m.MeasureType,
                m.GlucoseLevel, m.SystolicBP, m.DiastolicBP,
                m.HeartRate, m.RiskScore, m.RiskLevel, m.Note
            },
            commandType: CommandType.StoredProcedure);
    }

    public async Task DeleteAsync(int measurementId)
    {
        using var conn = _db.GetConnection();
        await conn.ExecuteAsync(
            "usp_Measurement_Delete",
            new { MeasurementId = measurementId },
            commandType: CommandType.StoredProcedure);
    }
}
