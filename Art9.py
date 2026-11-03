from django.db import models
from django.conf import settings


class HighLevelData(models.Model):
    id = models.AutoField(primary_key=True)
    header_data = models.TextField(null=True, blank=True)
    request = models.ForeignKey(
        "RequestorTeam",
        on_delete=models.CASCADE,
        db_column="sgp_id",
        to_field="sgp_id",
        related_name="high_level_data",
        null=True,
        blank=True,
    )
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1, db_index=True)

    class Meta:
        db_table = "high_level_data"
        indexes = [
            models.Index(fields=["request", "is_active"]),
            models.Index(
                fields=[
                    "request",
                    "is_active",
                    "-created_date",
                ]
            ),
        ]

    def get_processed_header_data(self):
        if not self.header_data:
            return self.header_data
        app_url = settings.DOMAIN_URL
        value = self.header_data
        replacements = {
            "/kpmgivtm/public/img/first_page_side.png": f"{app_url}/backend/img/first_page_side.png",
            "/kpmgivtm/public/img/first_page_sar.png": f"{app_url}/backend/img/first_page_sar.jpg",
            "/kpmgivtm/public/img/first_page_sar.jpg": f"{app_url}/backend/img/first_page_sar.jpg",
            "https://abc.kworld.abc.com/abcivtm/public/storage/result_storage/architecture_img": f"{app_url}/backend/result_storage/architecture_img",
            "/kpmgivtm/public/storage/result_storage/architecture_img": f"{app_url}/backend/result_storage/architecture_img",
            "/kpmgivtm/public/img/logo_new.png": f"{app_url}/backend/img/logo_new.png",
        }
        for old_path, new_path in replacements.items():
            value = value.replace(old_path, new_path)
        return value
