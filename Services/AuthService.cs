using System.Data;
using Dapper;
using ChronicCare.Data;
using ChronicCare.Models;

namespace ChronicCare.Services;

public class AuthService
{
    private readonly DatabaseHelper _db;

    public UserModel? CurrentUser { get; private set; }
    public bool IsAuthenticated => CurrentUser != null;

    public AuthService(DatabaseHelper db) => _db = db;

    public async Task<bool> LoginAsync(string loginId, string password)
    {
        using var conn = _db.GetConnection();
        var user = await conn.QuerySingleOrDefaultAsync<UserModel>(
            "usp_User_Login",
            new { LoginId = loginId, Password = password },
            commandType: CommandType.StoredProcedure);

        if (user == null) return false;

        CurrentUser = user;
        return true;
    }

    public void Logout() => CurrentUser = null;
}
