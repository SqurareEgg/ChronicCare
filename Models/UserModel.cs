namespace ChronicCare.Models;

public class UserModel
{
    public int UserId { get; set; }
    public string LoginId { get; set; } = "";
    public string Password { get; set; } = "";
    public string Name { get; set; } = "";
    public string Role { get; set; } = "";
}
