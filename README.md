# ContactInfo

Webová aplikace ASP.NET Core 9 (Razor Pages) poskytující online vstupní dotazník pro sběr kontaktních údajů.

## Spuštění

1. Nainstalujte .NET SDK 9.0 (preview) dle souboru `global.json`.
2. V kořenové složce projektu spusťte příkaz:
   ```bash
   dotnet run --project src/ContactInfo.Web/ContactInfo.Web.csproj
   ```
3. Aplikace je dostupná na adrese `https://localhost:5001` (nebo jiné dle konfigurace).

## Databáze

- Připojovací řetězec je definován v `src/ContactInfo.Web/appsettings.json`.
- Strukturu databáze lze vytvořit pomocí skriptu `database/create.sql`.

## Funkce

- Formulář pro zadání kontaktních údajů s validacemi a podporou GDPR.
- Automatické doplnění data narození po zadání rodného čísla.
- Uložení záznamu do databáze Microsoft SQL Server.
- Export odeslaných dat do JSON souboru v adresáři `exports`.
- Přepínání jazyků mezi češtinou a angličtinou.
