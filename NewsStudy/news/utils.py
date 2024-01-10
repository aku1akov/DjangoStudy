from .models import ViewCount


def get_ip(request):
    http_xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_xff:
        ip = http_xff.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ViewCountMixin:
    def get_object(self):
        obj = super().get_object()
        ip = get_ip(self.request)
        ViewCount.objects.get_or_create(article=obj, ip=ip)
        return obj
