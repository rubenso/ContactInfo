(function () {
    const form = document.querySelector('form[data-birth-date-target]');
    if (!form) {
        return;
    }

    const birthNumberInput = form.querySelector('[data-rc-input="true"]');
    const birthDateTargetId = form.getAttribute('data-birth-date-target');
    const birthDateInput = birthDateTargetId ? document.getElementById(birthDateTargetId) : null;
    const noBirthNumberCheckbox = form.querySelector('[data-no-rc-toggle="true"]');

    function normalizeBirthNumber(digits) {
        return `${digits.substring(0, 6)}/${digits.substring(6)}`;
    }

    function parseBirthNumber(value) {
        if (!value) {
            return null;
        }

        const digits = value.replace(/\D/g, '');
        if (digits.length !== 9 && digits.length !== 10) {
            return null;
        }

        if (digits.length === 10) {
            let remainder = 0;
            for (let i = 0; i < digits.length; i += 1) {
                remainder = (remainder * 10 + Number.parseInt(digits[i], 10)) % 11;
            }

            const controlDigit = Number.parseInt(digits.substring(9), 10);
            if (Number.isNaN(controlDigit)) {
                return null;
            }

            if (remainder !== 0 && !(remainder === 10 && controlDigit === 0)) {
                return null;
            }
        }

        const yearPart = parseInt(digits.substring(0, 2), 10);
        let monthPart = parseInt(digits.substring(2, 4), 10);
        const dayPart = parseInt(digits.substring(4, 6), 10);

        if (Number.isNaN(yearPart) || Number.isNaN(monthPart) || Number.isNaN(dayPart)) {
            return null;
        }

        if (monthPart > 70 && monthPart < 83) {
            monthPart -= 70;
        } else if (monthPart > 50) {
            monthPart -= 50;
        } else if (monthPart > 20 && monthPart < 33) {
            monthPart -= 20;
        }

        let year = 1900 + yearPart;
        if (digits.length === 10 && year < 1954) {
            year += 100;
        }
        const currentYear = new Date().getUTCFullYear();
        if (digits.length === 9 && year > currentYear) {
            year -= 100;
        }

        const date = new Date(Date.UTC(year, monthPart - 1, dayPart));
        if (date.getUTCFullYear() !== year || date.getUTCMonth() !== monthPart - 1 || date.getUTCDate() !== dayPart) {
            return null;
        }

        return {
            birthDate: date.toISOString().substring(0, 10),
            normalized: normalizeBirthNumber(digits)
        };
    }

    function toggleBirthNumberAvailability() {
        if (!birthNumberInput) {
            return;
        }

        const disabled = noBirthNumberCheckbox && noBirthNumberCheckbox.checked;
        birthNumberInput.disabled = disabled;
        if (disabled) {
            birthNumberInput.value = '';
            if (birthDateInput) {
                birthDateInput.value = '';
            }
        }
    }

    if (birthNumberInput && birthDateInput) {
        const handleBirthNumberChange = function () {
            const result = parseBirthNumber(birthNumberInput.value);
            if (result) {
                birthDateInput.value = result.birthDate;
                birthNumberInput.value = result.normalized;
            }
        };

        birthNumberInput.addEventListener('change', handleBirthNumberChange);
        birthNumberInput.addEventListener('input', handleBirthNumberChange);
    }

    if (noBirthNumberCheckbox) {
        noBirthNumberCheckbox.addEventListener('change', toggleBirthNumberAvailability);
        toggleBirthNumberAvailability();
    }
})();
