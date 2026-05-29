"""Context processors — inject company-wide variables into every template."""
from django.conf import settings


def site_meta(request):
    """Make company info available in every template."""
    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
    }
