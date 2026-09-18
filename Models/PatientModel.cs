namespace ChronicCare.Models;

public class PatientModel
{
    public int PatientId { get; set; }
    public string Name { get; set; } = "";
    public string Gender { get; set; } = "M";
    public DateTime BirthDate { get; set; } = DateTime.Today.AddYears(-50);
    public string? Phone { get; set; }
    public string? Address { get; set; }
    public string DiseaseType { get; set; } = "당뇨";
    public int? DoctorUserId { get; set; }
    public DateTime RegisteredDate { get; set; }
    public bool IsActive { get; set; } = true;

    // JOIN으로 채워지는 표시용 필드
    public string DoctorName { get; set; } = "";

    public int Age => DateTime.Today.Year - BirthDate.Year -
        (DateTime.Today < BirthDate.AddYears(DateTime.Today.Year - BirthDate.Year) ? 1 : 0);
}
