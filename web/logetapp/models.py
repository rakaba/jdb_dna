from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル

    usernameを使わず、emailアドレスをユーザー名として使うようにしています。

    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    storeid = models.CharField(max_length=100, null=True, blank=True)
    styletestid = models.CharField(max_length=100, null=True, blank=True)
    styletestpass = models.CharField(max_length=100, null=True, blank=True)
    stylecheckcode = models.CharField(max_length=100, null=True, blank=True)
    styleansno = models.CharField(max_length=100, null=True, blank=True)
    styletestername = models.CharField(max_length=100, null=True, blank=True)
    skintestid = models.CharField(max_length=100, null=True, blank=True)
    skintestpass = models.CharField(max_length=100, null=True, blank=True)
    skincheckcode = models.CharField(max_length=100, null=True, blank=True)
    skinansno = models.CharField(max_length=100, null=True, blank=True)
    skintestername = models.CharField(max_length=100, null=True, blank=True)
    muscletestid = models.CharField(max_length=100, null=True, blank=True)
    muscletestpass = models.CharField(max_length=100, null=True, blank=True)
    musclecheckcode = models.CharField(max_length=100, null=True, blank=True)
    muscleansno = models.CharField(max_length=100, null=True, blank=True)
    muscletestername = models.CharField(max_length=100, null=True, blank=True)
    headtestid = models.CharField(max_length=100, null=True, blank=True)
    headtestpass = models.CharField(max_length=100, null=True, blank=True)
    headcheckcode = models.CharField(max_length=100, null=True, blank=True)
    headansno = models.CharField(max_length=100, null=True, blank=True)
    headtestername = models.CharField(max_length=100, null=True, blank=True)
    floralighttestid = models.CharField(max_length=100, null=True, blank=True)
    floralighttestpass = models.CharField(max_length=100, null=True, blank=True)
    floralightcheckcode = models.CharField(max_length=100, null=True, blank=True)
    floralightansno = models.CharField(max_length=100, null=True, blank=True)
    floralighttestername = models.CharField(max_length=100, null=True, blank=True)
    floraexperttestid = models.CharField(max_length=100, null=True, blank=True)
    floraexperttestpass = models.CharField(max_length=100, null=True, blank=True)
    floraexpertcheckcode = models.CharField(max_length=100, null=True, blank=True)
    floraexpertansno = models.CharField(max_length=100, null=True, blank=True)
    floraexperttestername = models.CharField(max_length=100, null=True, blank=True)
    foodproteintestid = models.CharField(max_length=100, null=True, blank=True)
    foodproteintestpass = models.CharField(max_length=100, null=True, blank=True)
    foodproteincheckcode = models.CharField(max_length=100, null=True, blank=True)
    foodproteinansno = models.CharField(max_length=100, null=True, blank=True)
    foodproteintestername = models.CharField(max_length=100, null=True, blank=True)
    othertestid = models.CharField(max_length=100, null=True, blank=True)
    othertestpass = models.CharField(max_length=100, null=True, blank=True)
    othercheckcode = models.CharField(max_length=100, null=True, blank=True)
    otheransno = models.CharField(max_length=100, null=True, blank=True)
    othertestername = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

class StoreModel(models.Model):
    storeid = models.CharField(max_length=100, unique=True)
    storename = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.storename

class StyleDnaModel(models.Model):
    styletestid = models.CharField(max_length=100, unique=True)
    styletestpass = models.CharField(max_length=100)
    styleansno = models.CharField(max_length=100, null=True, blank=True)
    stylecheckcode = models.CharField(max_length=100, null=True, blank=True)
    stylename = models.CharField(max_length=100, null=True, blank=True)
    stylestoreid = models.CharField(max_length=100, null=True, blank=True)
    styledate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.styletestid

class SkinDnaModel(models.Model):
    skintestid = models.CharField(max_length=100, unique=True)
    skintestpass = models.CharField(max_length=100)
    skinansno = models.CharField(max_length=100, null=True, blank=True)
    skincheckcode = models.CharField(max_length=100, null=True, blank=True)
    skinname = models.CharField(max_length=100, null=True, blank=True)
    skinstoreid = models.CharField(max_length=100, null=True, blank=True)
    skindate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.skintestid

class MuscleDnaModel(models.Model):
    muscletestid = models.CharField(max_length=100, unique=True)
    muscletestpass = models.CharField(max_length=100)
    muscleansno = models.CharField(max_length=100, null=True, blank=True)
    musclecheckcode = models.CharField(max_length=100, null=True, blank=True)
    musclename = models.CharField(max_length=100, null=True, blank=True)
    musclestoreid = models.CharField(max_length=100, null=True, blank=True)
    muscledate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.muscletestid

class HeadDnaModel(models.Model):
    headtestid = models.CharField(max_length=100, unique=True)
    headtestpass = models.CharField(max_length=100)
    headansno = models.CharField(max_length=100, null=True, blank=True)
    headcheckcode = models.CharField(max_length=100, null=True, blank=True)
    headname = models.CharField(max_length=100, null=True, blank=True)
    headstoreid = models.CharField(max_length=100, null=True, blank=True)
    headdate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.headtestid

class FloraLightModel(models.Model):
    floralighttestid = models.CharField(max_length=100, unique=True)
    floralighttestpass = models.CharField(max_length=100)
    floralightansno = models.CharField(max_length=100, null=True, blank=True)
    floralightcheckcode = models.CharField(max_length=100, null=True, blank=True)
    floralightname = models.CharField(max_length=100, null=True, blank=True)
    floralightstoreid = models.CharField(max_length=100, null=True, blank=True)
    floralightdate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.floralighttestid

class FloraExpertModel(models.Model):
    floraexperttestid = models.CharField(max_length=100, unique=True)
    floraexperttestpass = models.CharField(max_length=100)
    floraexpertansno = models.CharField(max_length=100, null=True, blank=True)
    floraexpertcheckcode = models.CharField(max_length=100, null=True, blank=True)
    floraexpertname = models.CharField(max_length=100, null=True, blank=True)
    floraexpertstoreid = models.CharField(max_length=100, null=True, blank=True)
    floraexpertdate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.floraexperttestid

class FoodProteinModel(models.Model):
    foodproteintestid = models.CharField(max_length=100, unique=True)
    foodproteintestpass = models.CharField(max_length=100)
    foodproteinansno = models.CharField(max_length=100, null=True, blank=True)
    foodproteincheckcode = models.CharField(max_length=100, null=True, blank=True)
    foodproteinname = models.CharField(max_length=100, null=True, blank=True)
    foodproteinstoreid = models.CharField(max_length=100, null=True, blank=True)
    foodproteindate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.foodproteintestid

class OtherModel(models.Model):
    othertestid = models.CharField(max_length=100, unique=True)
    othertestpass = models.CharField(max_length=100)
    otheransno = models.CharField(max_length=100, null=True, blank=True)
    othercheckcode = models.CharField(max_length=100, null=True, blank=True)
    othername = models.CharField(max_length=100, null=True, blank=True)
    otherstoreid = models.CharField(max_length=100, null=True, blank=True)
    otherdate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.othertestid
