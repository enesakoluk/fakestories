import django_filters
from app.models import PostModel
class PostFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = PostModel
        fields = ['title',"isVideo","user__username","user__id"]