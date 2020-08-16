from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_client, is_consultant, is_staff, is_active, is_superuser,
                     **extra_fields):
        if email:
            email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email,
            is_client=is_client,
            is_consultant=is_consultant,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_consultant(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, True, False, False, False, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, False, False, True, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, True, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, blank=False, verbose_name=_('Почта'))
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('Пароль'))
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=30, blank=False, null=False, verbose_name=_('Фамилия'))
    photo = models.ImageField(upload_to='profile-photo/', blank=True, null=True, verbose_name=_('Фотография'))
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Телефон'))
    is_active = models.BooleanField(default=False, verbose_name=_('Активный'))
    is_client = models.BooleanField(default=False, verbose_name=_('Клиент'))
    is_consultant = models.BooleanField(default=False, verbose_name=_('Исполнитель'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Сотрудник'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата регистрации'))

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Consultant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Заголовок'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    comment = models.TextField(max_length=200, blank=True, null=True, verbose_name=_('Комментарии'))

    class Meta:
        verbose_name = _('Консультант')
        verbose_name_plural = _('Консультанты')

    def __str__(self):
        return '{}'.format(self.user)

    def short_description(self):
        return truncatechars(self.description, 270)

    short_description.short_description = 'О себе'


class ImageConsultant(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, blank=False, null=False,
                                   related_name='certificates',
                                   verbose_name=_('Консультант'))
    certificate_image = models.ImageField(upload_to='certificate-image/', blank=True, null=True,
                                          verbose_name=_('Сертификаты'))

    class Meta:
        verbose_name = _('Сертификат')
        verbose_name_plural = _('Сертификаты')

    def __str__(self):
        return '{}'.format(self.consultant)

    def get_certificate(self):
        return self.certificate_image.url

    def certificate_tag(self):
        return mark_safe('<img src="%s" width="300" height="450"/>' % self.get_certificate())

    certificate_tag.short_description = 'Сертификаты'


class RatingStart(models.Model):
    value = models.SmallIntegerField(default=0, verbose_name=_('Значение'))

    def __str__(self):
        return '{}'.format(self.value)

    class Meta:
        verbose_name = _("Звезда рейтинга")
        verbose_name_plural = _("Звезды рейтинга")
        ordering = ["-value"]


class Reviews(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    email = models.EmailField()
    text = models.TextField(max_length=5000, verbose_name=_('Сообщение'))
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, verbose_name=_('Консультант'),
                                   related_name='reviews')
    star = models.ForeignKey(RatingStart, on_delete=models.CASCADE, verbose_name=_('Звезда'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
