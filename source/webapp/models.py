from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='UserInfo', verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Имя")
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(max_length=50, verbose_name="Почта")

    def __str__(self):
        return self.user.get_full_name()


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Текст статьи")
    author = models.ForeignKey(User, blank=True, verbose_name="Автор", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images', blank=True, null=True, verbose_name="Картинка")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время создания")

    def __str__(self):
        return f"{self.pk}. {self.title} | {self.author.username}"

    def get_absolute_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Comment(models.Model):
    text = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Текст комментария")
    author = models.ForeignKey(User, blank=True, verbose_name="Автор", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время создания")
    article = models.ForeignKey(Article, related_name="comments", blank=True, verbose_name="Статья", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.article.id})

    def __str__(self):
        return f"{self.pk}. {self.text} | {self.author.username}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Rate(models.Model):
    rate = models.IntegerField(max_length=2, null=True, blank=True, verbose_name="Оценка")
    user = models.ForeignKey(User, blank=True, related_name="rates", verbose_name="Пользователь", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="rates", blank=True, verbose_name="Статья", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        unique_together = ('user', 'article')
