using System.Data;
using Dapper;
using ChronicCare.Models;

namespace ChronicCare.Data;

public class PatientRepository
{
    private readonly DatabaseHelper _db;
    public PatientRepository(DatabaseHelper db) => _db = db;

    public async Task<List<PatientModel>> GetAllAsync()
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<PatientModel>(
            "usp_Patient_SelectAll", commandType: CommandType.StoredProcedure);
        return result.ToList();
    }

    public async Task<PatientModel?> GetByIdAsync(int patientId)
    {
        using var conn = _db.GetConnection();
        return await conn.QuerySingleOrDefaultAsync<PatientModel>(
            "usp_Patient_GetById",
            new { PatientId = patientId },
            commandType: CommandType.StoredProcedure);
    }

    public async Task<int> InsertAsync(PatientModel p)
    {
        using var conn = _db.GetConnection();
        return await conn.QuerySingleAsync<int>(
            "usp_Patient_Insert",
            new
            {
                p.Name, p.Gender, p.BirthDate, p.Phone,
                p.Address, p.DiseaseType, p.DoctorUserId
            },
            commandType: CommandType.StoredProcedure);
    }

    public async Task UpdateAsync(PatientModel p)
    {
        using var conn = _db.GetConnection();
        await conn.ExecuteAsync(
            "usp_Patient_Update",
            new
            {
                p.PatientId, p.Name, p.Gender, p.BirthDate, p.Phone,
                p.Address, p.DiseaseType, p.DoctorUserId
            },
            commandType: CommandType.StoredProcedure);
    }

    public async Task DeleteAsync(int patientId)
    {
        using var conn = _db.GetConnection();
        await conn.ExecuteAsync(
            "usp_Patient_Delete",
            new { PatientId = patientId },
            commandType: CommandType.StoredProcedure);
    }

    public async Task<List<UserModel>> GetDoctorsAsync()
    {
        using var conn = _db.GetConnection();
        var result = await conn.QueryAsync<UserModel>(
            "SELECT UserId, Name, Role FROM Users WHERE Role = N'의사' ORDER BY Name");
        return result.ToList();
    }
}
