// GlobeTrek Adventures — Frontend JS

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss flash messages after 5s
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });

    // Smooth scroll for in-page anchors
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Set minimum date on date inputs to today
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"].future-only').forEach(function (input) {
        if (!input.min) input.min = today;
    });

    // Confirm dialogs on delete buttons
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });

    // Mock payment - auto-format card number with spaces
    const cardInput = document.getElementById('id_card_number');
    if (cardInput) {
        cardInput.addEventListener('input', function (e) {
            let v = this.value.replace(/\s/g, '').replace(/[^0-9]/g, '');
            this.value = v.match(/.{1,4}/g)?.join(' ') || v;
        });
    }
});
