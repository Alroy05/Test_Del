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


class Role(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_DELETED = 3

    ROLE_TYPE_AU = 1
    ROLE_TYPE_RQ = 2
    ROLE_TYPE_SS = 3
    ROLE_TYPE_TL = 6
    ROLE_TYPE_SECURITY_OFFICER = 12

    # Deprecated
    ROLE_TYPE_SUPPORT = 13
    ROLE_TYPE_CLIENT_AU = 14
    ROLE_TYPE_READ_ONLY_LEADERSHIP = 15

    # Demistro
    ROLE_TYPE_DEMISTRO_TEAM = 16

    # ADO
    ROLE_TYPE_ADO_TEAM = 17

    #Role to access the analysis card only
    ROLE_TYPE_SOL_ARCHITECT = 18

    #GSSR System role
    ROLE_TYPE_SYSTEM_ROLE = 19

    # ServiceNow
    ROLE_TYPE_SERVICE_NOW_TEAM = 20

    HIDDEN_USER_ROLE_IDS = [
        ROLE_TYPE_DEMISTRO_TEAM,
        ROLE_TYPE_ADO_TEAM,
        ROLE_TYPE_SERVICE_NOW_TEAM,
        ROLE_TYPE_SYSTEM_ROLE,
    ]
    
    ROLE_TYPE_LIST = {
        ROLE_TYPE_AU: "System Super Admin",
        ROLE_TYPE_RQ: "Solution Team",
        ROLE_TYPE_SS: "Coordinator",
        ROLE_TYPE_TL: "Security Resource",
        ROLE_TYPE_SECURITY_OFFICER: "GISG Leadership",
        ROLE_TYPE_SOL_ARCHITECT: "Solution Architect",
        ROLE_TYPE_SUPPORT: "Support Team", #Deprecated
        ROLE_TYPE_CLIENT_AU: "Client Admin", #Deprecated
        ROLE_TYPE_READ_ONLY_LEADERSHIP: "Leadership Read only", #Deprecated
    }

    ROLE_TYPE_VAR_LIST = {
        ROLE_TYPE_AU: "super_admin",
        ROLE_TYPE_RQ: "solution_team",
        ROLE_TYPE_SS: "coordinator",
        ROLE_TYPE_TL: "security_resource",
        ROLE_TYPE_SECURITY_OFFICER: "security_leadership",
        ROLE_TYPE_SOL_ARCHITECT: "solution_architect",
    }

    ACTION_PENDING_CHOICES = {
        ROLE_TYPE_RQ: "Solution Team",
        ROLE_TYPE_SS: "Coordinator",
        ROLE_TYPE_SECURITY_OFFICER: "GISG Leadership",
        ROLE_TYPE_TL: "Security Resource",
        ROLE_TYPE_SOL_ARCHITECT: "Solution Architect",
    }

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.IntegerField(
        default=STATUS_ACTIVE,
        choices=[
            (STATUS_ACTIVE, "Active"),
            (STATUS_INACTIVE, "Inactive"),
            (STATUS_DELETED, "Deleted"),
        ],
    )
    permissions = models.ManyToManyField(
        "Permission", blank=True, db_table="app_role_permissions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

    def get_role_type_as_string(self):
        return self.ROLE_TYPE_LIST.get(self.id, "-")

    def get_role_type_as_string_var(self):
        return self.ROLE_TYPE_VAR_LIST.get(self.id, "-")

    @classmethod
    def get_role_type_list(cls):
        return cls.ROLE_TYPE_LIST

    @classmethod
    def get_role_type_var_list(cls):
        return cls.ROLE_TYPE_VAR_LIST

    @classmethod
    def get_status_as_string_by_id(cls, role_id):
        return cls.ROLE_TYPE_LIST.get(role_id, "-")

    @classmethod
    def get_status_as_string_var_by_id(cls, role_id):
        return cls.ROLE_TYPE_VAR_LIST.get(role_id, "-")
