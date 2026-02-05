"""
Django model to map Supabase users to Django users
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SupabaseUserMapping(models.Model):
    """
    Maps Supabase authentication users to Django users
    Supabase handles auth, Django handles data and business logic
    """
    # Django user (main user model)
    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supabase_mapping'
    )
    
    # Supabase user ID (UUID from Supabase auth.users)
    supabase_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='UUID from Supabase auth.users table'
    )
    
    # Email from Supabase (for verification)
    supabase_email = models.EmailField(
        db_index=True,
        help_text='Email from Supabase auth'
    )
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    # Flags
    is_active = models.BooleanField(
        default=True,
        help_text='Can this user authenticate?'
    )
    
    class Meta:
        db_table = 'supabase_user_mapping'
        verbose_name = 'Supabase User Mapping'
        verbose_name_plural = 'Supabase User Mappings'
        indexes = [
            models.Index(fields=['supabase_id']),
            models.Index(fields=['supabase_email']),
        ]
    
    def __str__(self):
        return f'{self.django_user.username} <-> {self.supabase_id[:8]}...'
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login_at = timezone.now()
        self.save(update_fields=['last_login_at'])
    
    @classmethod
    def get_django_user_by_supabase_id(cls, supabase_id):
        """
        Get Django user by Supabase ID
        Returns None if not found
        """
        try:
            mapping = cls.objects.select_related('django_user').get(
                supabase_id=supabase_id,
                is_active=True
            )
            return mapping.django_user
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def create_mapping(cls, django_user, supabase_id, supabase_email):
        """
        Create a new mapping between Django user and Supabase user
        """
        return cls.objects.create(
            django_user=django_user,
            supabase_id=supabase_id,
            supabase_email=supabase_email
        )

# ------------------------------------------------------------------------------
# Password Reset Code (OTP)
# ------------------------------------------------------------------------------
import uuid
import datetime

class PasswordResetCode(models.Model):
    """
    Store 6-digit numeric codes for password reset.
    Valid for 15 minutes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_code'
        indexes = [
            models.Index(fields=['email', 'code']),
        ]

    def is_valid(self):
        return (
            not self.used and
            self.expires_at > timezone.now() and
            self.attempts < 3
        )
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiry to 15 minutes from now
            self.expires_at = timezone.now() + datetime.timedelta(minutes=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ResetCode({self.email} - {self.code})"
