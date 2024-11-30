from .models import Category, Tag

def related(request):
    context = {
        'category_list': Category.objects.all(),
        'tag_list': Tag.objects.all(),
    }
    return context