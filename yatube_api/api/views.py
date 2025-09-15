from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Follow, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        # при создании поста записываем автора
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        # поддерживаем пагинацию через limit и offset
        if 'limit' in request.query_params or 'offset' in request.query_params:
            paginator = LimitOffsetPagination()
            queryset = paginator.paginate_queryset(
                self.queryset, request, view=self
            )
            serializer = self.get_serializer(queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    # для групп только чтение, без создания
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        # получаем пост и возвращаем его комментарии
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        # сохраняем автора и сам пост
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        # показываем только подписки текущего пользователя
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # user берём из запроса
        serializer.save(user=self.request.user)
