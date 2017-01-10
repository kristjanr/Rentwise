from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic.edit import DeleteView

from app.models import Item, Image
from .forms import S3DirectUploadForm, ItemForm


@method_decorator(login_required, name='dispatch')
class ItemView(FormView):
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'app/add_item.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if len(Item.objects.filter(user=request.user)) > 500:
            return redirect('home')
        if form.is_valid():
            item_data = form.cleaned_data
            item_data['user'] = request.user
            if item_data.get('published'):
                del item_data['published']
            categories = item_data.pop('categories')
            item = Item(**item_data)
            item.save()
            item.categories = categories
            item.save()
            return redirect('upload_images', item.id)
        else:
            return render(request, 'app/add_item.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ItemDetailView(DetailView):
    template_name = 'app/item_details.html'
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(Item, id=item_id) if item_id else None
        if item.user != request.user:
            return redirect('home')
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ImageUploadView(FormView):
    template_name = 'app/upload_images.html'
    form_class = S3DirectUploadForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        item_id = kwargs.get('pk')
        item = get_object_or_404(Item, id=item_id) if item_id else None
        if not item or item.user != request.user:
            return redirect('home')

        if form.is_valid():
            for key in sorted(k for k, v in form.cleaned_data.items() if v):
                url = form.cleaned_data[key]
                image = Image(item=item, url=url)
                image.save()
            return redirect('view_item', item.id)
        else:
            return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(Item, id=item_id) if item_id else None
        if not item or item.user != request.user:
            return redirect('view_item', item.id)
        return super().post(request, *args, **kwargs)


@staff_member_required
def publish_item(request, *args, **kwargs):
    item_id = kwargs.get('pk')
    item = get_object_or_404(Item, id=item_id) if item_id else None
    item.published = True
    item.save()
    return redirect('view_item', item.id)


@staff_member_required
def unpublish_item(request, *args, **kwargs):
    item_id = kwargs.get('pk')
    item = get_object_or_404(Item, id=item_id) if item_id else None
    item.published = False
    item.save()
    return redirect('view_item', item.id)


def logout_view(request):
    logout(request)
    return redirect('home')
