from django.http import Http404


def get_list_or_404(klass, *args, **kwargs):
    obj_list = list(klass.objects.filter(*args, **kwargs))
    if not obj_list:
        raise Http404()
    return obj_list


def get_object_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404()
