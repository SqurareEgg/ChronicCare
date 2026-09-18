using Microsoft.Data.SqlClient;

namespace ChronicCare.Data;

public class DatabaseHelper
{
    private readonly string _connectionString;

    public DatabaseHelper(IConfiguration config)
    {
        _connectionString = config.GetConnectionString("DefaultConnection")
            ?? throw new InvalidOperationException("ConnectionString 'DefaultConnection'이 없습니다.");
    }

    public SqlConnection GetConnection() => new SqlConnection(_connectionString);
}
