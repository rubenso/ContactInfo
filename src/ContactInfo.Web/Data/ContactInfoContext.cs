using ContactInfo.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace ContactInfo.Web.Data;

public class ContactInfoContext : DbContext
{
    public ContactInfoContext(DbContextOptions<ContactInfoContext> options)
        : base(options)
    {
    }

    public DbSet<ContactRecord> Contacts => Set<ContactRecord>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ContactRecord>(entity =>
        {
            entity.ToTable("Contacts");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.FullName).IsRequired().HasMaxLength(200);
            entity.Property(e => e.BirthNumber).HasMaxLength(20);
            entity.Property(e => e.Email).IsRequired().HasMaxLength(254);
            entity.Property(e => e.Nationality).IsRequired().HasMaxLength(100);
            entity.Property(e => e.Gender).IsRequired().HasMaxLength(20);
            entity.Property(e => e.GdprConsent).IsRequired();
            entity.Property(e => e.CreatedAtUtc).IsRequired();
        });
    }
}
