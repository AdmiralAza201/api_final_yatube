from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    # автора подставляем автоматически, его менять нельзя
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    # автора и связанный пост менять нельзя
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп, логики нет."""

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    # user подставляем из запроса
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    # following выбираем по username из базы
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        # достаём текущего пользователя из контекста
        user = self.context['request'].user
        following = attrs.get('following')
        # нельзя подписаться на себя
        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        # и нельзя подписываться дважды на одного и того же человека
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return attrs
