from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import Count


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_user(self, user, other_email):  # get_or_create
        email = user.email
        if email == other_email:
            return None
        qlookup1 = Q(first__email=email) & Q(second__email=other_email)
        qlookup2 = Q(first__email=other_email) & Q(second__email=email)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False


class Thread(models.Model):
    first = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first',
                              verbose_name='Первый пользователь')
    second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second',
                               verbose_name='Второй пользователь')
    new_messages = models.IntegerField(blank=True, null=True, verbose_name='Непрочитанные сообщения')
    time = models.IntegerField(default=0, verbose_name='Время чата')
    access = models.BooleanField(default=False, verbose_name='Доступ')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    objects = ThreadManager()

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return '{}'.format(self.first)

    def unreaded(self):
        messages_count = ChatMessage.objects.filter(status=False).count()
        self.messages_count = messages_count
        self.save()
        return self.messages_count


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Комната', related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.TextField(blank=True, null=True, verbose_name='Сообщение')
    audio = models.FileField(upload_to='messages/audio-file/', blank=True, null=True, verbose_name='Аудио')
    image = models.ImageField(upload_to='messages/image-file/', blank=True, null=True, verbose_name='Картинки')
    video = models.FileField(upload_to='messages/video-file/', blank=True, null=True, verbose_name='Видео')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return '{}'.format(self.user)
