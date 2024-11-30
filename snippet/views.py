from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from .models import Category, Tag, Code, UserProfile
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class RelatedDataMixin:
    @staticmethod
    def get_related_context():
        return {
            'categories': Category.objects.all(),
            'tags': Tag.objects.all()
        }

class TopView(TemplateView):
    template_name = "top.html"

    def get_queryset(self):
        queryset = Code.objects.order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['category_key'] = Category.objects.all()
        context['code_list'] = Code.objects.order_by('-id')
        return context
    
class CodeListView(ListView):
    model = Code
    template_name = "list.html"

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            results = Code.objects.filter(
                Q(code__icontains=query)|
                Q(title__icontains=query)|
                Q(description__icontains=query)
            )
        else:
            results = Code.objects.all()
        return results
    
class CategoryView(ListView):
    model = Code
    template_name = "list.html"

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        queryset = Code.objects.order_by('-id').filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_key'] = self.kwargs['category']
        return context

class TagView(ListView):
    model = Code
    template_name = "list.html"

    def get_queryset(self):
        tag = Tag.objects.get(name=self.kwargs['tag'])
        queryset = Code.objects.order_by('-id').filter(tag=tag)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_key'] = self.kwargs['tag']
        return context

class CodeCreateView(CreateView):
    model = Code
    fields = '__all__'
    template_name = "code_form.html"

    def form_valid(self, form):
        code = form.save(commit=False)

        new_category_name = self.request.POST.get('new_category')
        if new_category_name:
            new_category, created = Category.objects.get_or_create(name=new_category_name)
            form.instance.category = new_category

        code.save()

        selected_tags = self.request.POST.getlist('tags')
        if selected_tags:
            form.save()
            form.instance.tag.set(selected_tags)

        new_tags = self.request.POST.get('new_tags')
        if new_tags:
            tag_names = [tag.strip() for tag in new_tags.split(',')]
            tag_objects = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            form.instance.tag.add(*tag_objects) 

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(RelatedDataMixin.get_related_context())
        return context

class CodeUpdateView(UpdateView):
    model = Code
    fields = '__all__'
    template_name = "code_update_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(RelatedDataMixin.get_related_context())
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)

        tags = self.request.POST.getlist('tag')
        if tags:
            self.object.tag.set(tags)
        else:
            self.object.tag.clear()

        return response

class CodeDetailView(DetailView):
    model = Code
    template_name = "code_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.tag.all()
        return context

class FollowCodeView(LoginRequiredMixin, View):
    template_name = 'favorites.html'

    def get(self, request, *args, **kwargs):
        # お気に入りコードを取得
        favorite_codes = request.user.profile.favorite_codes.all()
        context = {'favorite_codes': favorite_codes}
        context.update(RelatedDataMixin.get_related_context())
        return render(request, self.template_name, context)

    def post(self, request, code_id):
        
        if not hasattr(request.user, 'profile'):
            UserProfile.objects.create(user=request.user)
        
        user_profile = request.user.profile
        code = get_object_or_404(Code, id=code_id)

        if code in user_profile.favorite_codes.all():
            user_profile.favorite_codes.remove(code)
        else:
            user_profile.favorite_codes.add(code)

        return redirect('top')