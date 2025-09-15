from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    """Отдельная группа для объединения постов."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """Основная публикация пользователя."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    # Пост можно привязать к группе, но это необязательно
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='posts',
        blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарий к конкретному посту."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    # индекс по дате ускоряет выборку последних комментариев
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    """Подписка одного пользователя на другого."""

    # тот, кто подписывается
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    # на кого подписываются
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            # одна пара подписчик/автор должна быть уникальна
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            )
        ]
