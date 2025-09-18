using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using ContactInfo.Web.Data;
using ContactInfo.Web.Models;
using ContactInfo.Web.Resources.Shared;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Localization;

namespace ContactInfo.Web.Pages;

public class IndexModel : PageModel
{
    private readonly ContactInfoContext _context;
    private readonly IWebHostEnvironment _environment;
    private readonly IStringLocalizer<SharedResource> _sharedLocalizer;

    public IndexModel(ContactInfoContext context, IWebHostEnvironment environment, IStringLocalizer<SharedResource> sharedLocalizer)
    {
        _context = context;
        _environment = environment;
        _sharedLocalizer = sharedLocalizer;
    }

    [BindProperty]
    public InputModel Input { get; set; } = new();

    public bool Saved { get; private set; }

    public string? ExportFileName { get; private set; }

    public IReadOnlyList<string> GenderOptions { get; } = new[] { "Male", "Female", "Other" };

    public IReadOnlyList<string> NationalityOptions { get; } = new[]
    {
        "CzechRepublic",
        "Slovakia",
        "Poland",
        "Germany",
        "Austria",
        "Other"
    };

    public void OnGet()
    {
        if (!Input.NoBirthNumber &&
            !string.IsNullOrWhiteSpace(Input.BirthNumber) &&
            TryParseBirthNumber(Input.BirthNumber, out var birthDate, out var normalized))
        {
            Input.BirthNumber = normalized;
            Input.BirthDate ??= birthDate;
        }
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!Input.NoBirthNumber)
        {
            if (string.IsNullOrWhiteSpace(Input.BirthNumber))
            {
                ModelState.AddModelError($"{nameof(Input)}.{nameof(Input.BirthNumber)}", _sharedLocalizer["BirthNumberRequired"]);
            }
            else if (TryParseBirthNumber(Input.BirthNumber, out var parsedDate, out var normalizedBirthNumber))
            {
                Input.BirthNumber = normalizedBirthNumber;
                Input.BirthDate ??= parsedDate;
                var birthDateKey = $"{nameof(Input)}.{nameof(Input.BirthDate)}";
                if (ModelState.ContainsKey(birthDateKey))
                {
                    ModelState.Remove(birthDateKey);
                    ModelState.SetModelValue(birthDateKey, new ValueProviderResult(Input.BirthDate!.Value.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)));
                }
            }
            else
            {
                ModelState.AddModelError($"{nameof(Input)}.{nameof(Input.BirthNumber)}", _sharedLocalizer["BirthNumberInvalid"]);
            }
        }
        else
        {
            Input.BirthNumber = null;
            var birthNumberKey = $"{nameof(Input)}.{nameof(Input.BirthNumber)}";
            if (ModelState.ContainsKey(birthNumberKey))
            {
                ModelState.Remove(birthNumberKey);
            }
        }

        if (!ModelState.IsValid)
        {
            return Page();
        }

        var record = new ContactRecord
        {
            FullName = Input.FullName.Trim(),
            BirthNumber = Input.BirthNumber,
            BirthDate = Input.BirthDate!.Value,
            Gender = Input.Gender,
            Email = Input.Email.Trim(),
            Nationality = Input.Nationality,
            GdprConsent = Input.GdprConsent,
            CreatedAtUtc = DateTime.UtcNow
        };

        _context.Contacts.Add(record);
        await _context.SaveChangesAsync();

        ExportFileName = await SaveJsonAsync(record);

        Saved = true;
        ModelState.Clear();
        Input = new InputModel();

        return Page();
    }

    private async Task<string> SaveJsonAsync(ContactRecord record)
    {
        var exportDirectory = Path.Combine(_environment.ContentRootPath, "exports");
        Directory.CreateDirectory(exportDirectory);
        var fileName = $"contact_{record.Id}_{DateTime.UtcNow:yyyyMMddHHmmss}.json";
        var filePath = Path.Combine(exportDirectory, fileName);

        var jsonOptions = new JsonSerializerOptions
        {
            WriteIndented = true
        };

        await System.IO.File.WriteAllTextAsync(filePath, JsonSerializer.Serialize(new
        {
            record.FullName,
            record.BirthNumber,
            BirthDate = record.BirthDate.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture),
            record.Gender,
            record.Email,
            record.Nationality,
            record.GdprConsent,
            record.CreatedAtUtc
        }, jsonOptions));

        return fileName;
    }

    public static bool TryParseBirthNumber(string? rawValue, out DateOnly birthDate, out string? normalizedBirthNumber)
    {
        birthDate = default;
        normalizedBirthNumber = null;
        if (string.IsNullOrWhiteSpace(rawValue))
        {
            return false;
        }

        var digits = new string(rawValue.Where(char.IsDigit).ToArray());
        if (digits.Length != 9 && digits.Length != 10)
        {
            return false;
        }

        if (digits.Length == 10)
        {
            if (!long.TryParse(digits, out var numericValue))
            {
                return false;
            }

            var remainder = numericValue % 11;
            var controlDigit = digits[^1] - '0';
            if (remainder != 0 && !(remainder == 10 && controlDigit == 0))
            {
                return false;
            }
        }

        if (!int.TryParse(digits[..2], out var yearPart) ||
            !int.TryParse(digits.Substring(2, 2), out var monthPart) ||
            !int.TryParse(digits.Substring(4, 2), out var dayPart))
        {
            return false;
        }

        if (monthPart > 70 && monthPart < 83)
        {
            monthPart -= 70;
        }
        else if (monthPart > 50)
        {
            monthPart -= 50;
        }
        else if (monthPart > 20 && monthPart < 33)
        {
            monthPart -= 20;
        }

        var fullYear = 1900 + yearPart;
        if (digits.Length == 10 && fullYear < 1954)
        {
            fullYear += 100;
        }

        if (digits.Length == 9 && fullYear > DateTime.UtcNow.Year)
        {
            fullYear -= 100;
        }

        try
        {
            birthDate = new DateOnly(fullYear, monthPart, dayPart);
            normalizedBirthNumber = NormalizeBirthNumber(digits);
            return true;
        }
        catch
        {
            return false;
        }
    }

    private static string NormalizeBirthNumber(string digits)
    {
        var suffix = digits[6..];
        return $"{digits[..6]}/{suffix}";
    }

    public class InputModel
    {
        [Required(ErrorMessage = "NameRequired")]
        public string FullName { get; set; } = string.Empty;

        public string? BirthNumber { get; set; }

        public bool NoBirthNumber { get; set; }

        [Required(ErrorMessage = "BirthDateRequired")]
        [DataType(DataType.Date)]
        public DateOnly? BirthDate { get; set; }

        [Required(ErrorMessage = "GenderRequired")]
        public string Gender { get; set; } = string.Empty;

        [Required(ErrorMessage = "EmailRequired")]
        [EmailAddress(ErrorMessage = "EmailInvalid")]
        public string Email { get; set; } = string.Empty;

        [Required(ErrorMessage = "NationalityRequired")]
        public string Nationality { get; set; } = string.Empty;

        [Range(typeof(bool), "true", "true", ErrorMessage = "GdprRequired")]
        public bool GdprConsent { get; set; }
    }
}
