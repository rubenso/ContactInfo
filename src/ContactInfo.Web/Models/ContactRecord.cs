namespace ContactInfo.Web.Models;

public class ContactRecord
{
    public int Id { get; set; }

    public string FullName { get; set; } = string.Empty;

    public string? BirthNumber { get; set; }

    public DateOnly BirthDate { get; set; }

    public string Gender { get; set; } = string.Empty;

    public string Email { get; set; } = string.Empty;

    public string Nationality { get; set; } = string.Empty;

    public bool GdprConsent { get; set; }

    public DateTime CreatedAtUtc { get; set; }
}
