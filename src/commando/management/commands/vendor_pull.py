import helpers
from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')
VENDOR_STATICFILES = {
    "saas-theme.min.css": ""
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js",
    "flowbite.min.js.map": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js.map"
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Downloading vendor staticfiles")

        completed_urls =[]
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f"failed to download {url}")
                )
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS("succesfully updated vendor static files")
            )
        else:
            self.stdout.write(
                self.style.WARNING("some files were not updated")
            )