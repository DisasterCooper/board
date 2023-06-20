import django_filters

from todolist.models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    content = django_filters.CharFilter(lookup_expr="icontains")
    date_from = django_filters.DateTimeFilter(field_name="created", lookup_expr="gte")

    class Meta:
        model = Post
        fields = ["title", "content", "created"]
