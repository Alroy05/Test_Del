from django.conf import settings
from django.db import models


class SarTemplateJsonData(models.Model):

    STATUS_DRAFT = 1
    STATUS_COMPLETED = 2

    STATUS_LABELS = {
        STATUS_DRAFT: "DRAFT",
        STATUS_COMPLETED: "COMPLETED"
    }

    STATUS_VALUES = {label: value for value, label in STATUS_LABELS.items()}

    id = models.AutoField(primary_key=True)
    header_name = models.CharField(
        max_length=50,
        db_index=True,
        null=True,
        blank=True,
    )
    json_data = models.JSONField(
        default=dict,
        blank=True,
    )
    request = models.ForeignKey(
        "RequestorTeam",
        on_delete=models.CASCADE,
        db_column="sgp_id",
        to_field="sgp_id",
        related_name="sar_template_json_data",
        null=True,
        blank=True,
    )
    section_status = models.PositiveSmallIntegerField(
        default=STATUS_DRAFT,
    )
    needs_refresh = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="created_by",
        related_name="sar_template_json_data_created",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(
        default=1,
        db_index=True,
    )
    class Meta:
        db_table = "sar_template_json_data"
        indexes = [
            models.Index(
                fields=["request", "is_active"],
                name="sar_json_request_idx",
            ),
            models.Index(
                fields=[
                    "request",
                    "is_active",
                    "header_name",
                    "-created_date",
                ],
                name="sar_json_lookup_idx",
            ),
        ]
        ordering = ["header_name"]

    def __str__(self):
        return (
            f"{self.request_id or 'No request'} - "
            f"{self.header_name or 'No header'}"
        )




import os
import time
from random import randint
from datetime import datetime
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from app.crypto import decrypt_field, encrypt_field, hash_field
from .role import Role


def generate_id():
    now = datetime.now()
    formatted = now.strftime("%Y-%m%d-%H%M%S-%f")
    return f"UID-{formatted}"


class UserDataManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        try:
            admin_role = Role.objects.get(id=Role.ROLE_TYPE_AU)
            user.roles.add(admin_role)
        except Role.DoesNotExist:
            raise Exception(
                "The 'System Super Admin' role (ID 1) must exist in the 'roles' table."
            )

        user.save(using=self._db)
        return user


class UserData(AbstractBaseUser):
    id = models.CharField(
        primary_key=True,
        default=generate_id,
        max_length=32,
        editable=False,
        unique=True,
    )
    _email = models.CharField(max_length=255, unique=True, db_column="email")
    email_hash = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    roles = models.ManyToManyField("Role", blank=True)
    permissions = models.ManyToManyField("Permission", blank=True)
    workload = models.IntegerField(default=0)
    first_login = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    permissions_updated_at = models.DateTimeField(null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    last_failed_attempt = models.DateTimeField(null=True, blank=True)
    captcha = models.CharField(max_length=6, null=True, blank=True)
    otp_code = models.CharField(max_length=4, blank=True, null=True)
    otp_expiry = models.FloatField(blank=True, null=True)
    otp_attempts = models.IntegerField(default=3)
    previous_passwords = models.JSONField(default=list)
    password_expiry = models.FloatField(blank=True, null=True)
    request_type = models.CharField(max_length=35, blank=True, null=True)
    user_type: int | None = models.PositiveSmallIntegerField(blank=True, null=True)  # type: ignore
    token_version = models.IntegerField(default=0)
    source = models.PositiveSmallIntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3")],
        default=1,
    )

    objects = UserDataManager()
    USERNAME_FIELD = "_email"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_staff(self):
        return self.roles.filter(id=Role.ROLE_TYPE_AU).exists()

    @property
    def is_superuser(self):
        return self.roles.filter(id=Role.ROLE_TYPE_AU).exists()

    @property
    def email(self):
        try:
            return decrypt_field(self._email)
        except:
            return ""

    @property
    def current_role(self):
        return Role.ROLE_TYPE_LIST.get(self.user_type, "Unknown")  # type: ignore

    @email.setter
    def email(self, value):
        self._email = encrypt_field(value)
        self.email_hash = hash_field(value)

    def set_password(self, raw_password):
        if self.password:
            prev_passwords = (
                self.previous_passwords[-4:] if self.previous_passwords else []
            )
            prev_passwords.append(self.password)
            self.previous_passwords = prev_passwords

        self.password = make_password(raw_password)
        self.password_expiry = time.time() + int(
            os.environ.get("PASSWORD_EXPIRY", 31536000)
        )

    def is_password_expired(self):
        if not self.password_expiry:
            return False
        return time.time() > self.password_expiry

    def generate_otp(self):
        self.otp_code = str(randint(1000, 9999))
        self.otp_expiry = time.time() + 300
        self.otp_attempts = 3
        self.save(update_fields=["otp_code", "otp_expiry", "otp_attempts"])

    def __str__(self):
        try:
            return self.email
        except:
            return self.id

    class Meta:  # type: ignore
        db_table = "app_userdata"
        verbose_name = "User"
        verbose_name_plural = "Users"



from django.db import models
from django.conf import settings


class SarTemplateData(models.Model):
    id = models.AutoField(primary_key=True)
    header_name = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    header_data = models.TextField(null=True, blank=True)
    request = models.ForeignKey(
        "RequestorTeam",
        on_delete=models.CASCADE,
        db_column="sgp_id",
        to_field="sgp_id",
        related_name="sar_template_data",
        null=True,
        blank=True,
    )
    comment = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="created_by",
        related_name="sar_template_data_created",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1, db_index=True)

    class Meta:
        db_table = "sar_template_data"
        indexes = [
            models.Index(fields=["request", "is_active"]),
            models.Index(
                fields=["request", "is_active", "header_name", "-created_date"],
                name="sar_lookup_idx",
            ),
        ]
        ordering = ["header_name"]

    def __str__(self):
        return f"{self.request} - {self.header_name}"

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

