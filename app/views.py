from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic.edit import DeleteView
from django_tables2 import RequestConfig
from geopy.distance import distance

from app.models import Item, Image
from app.tables import ItemTable
from app.varia import send_emails
from .forms import S3DirectUploadForm, ItemForm, ProfileLocationForm


def home(request):
    published_items = Item.objects.filter(published=True).count()
    fb_profile_clicks = sum(item.renters.count() for item in Item.objects.all())

    if hasattr(request.user, 'profile') and request.user.profile.place:
        form_data = dict(place=request.user.profile.place, location=request.user.profile.location)
        form = ProfileLocationForm(form_data)
    else:
        form = ProfileLocationForm()

    table = ItemTable(Item.objects.filter(published=True))
    RequestConfig(request).configure(table)
    context = dict(
        published_items=published_items,
        fb_profile_clicks=fb_profile_clicks,
        form=form,
        table=table,
    )
    return render(request, 'app/index.html', context)


@method_decorator(login_required, name='dispatch')
class ItemAddView(FormView):
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
        if request.user.is_staff or item.user == request.user:
            return super().get(request, *args, **kwargs)
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.profile.location:
            distance_in_miles = distance(self.request.user.profile.location, self.object.location).miles
            context['distance'] = distance_in_miles
        if self.request.GET.get('new'):
            context['new'] = self.request.GET['new'] == 'true'
        return context


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
            send_emails(request, item)
            response = redirect('view_item', item.id)
            response['Location'] += '?new=true'
            return response
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


@login_required
def contact_owner(request, pk):
    if not pk:
        return redirect('home')
    item = get_object_or_404(Item, id=pk) if pk else None
    if not item.renters.filter(id=request.user.id):
        item.renters.add(request.user)
        item.save()
    return redirect(item.user.profile.facebook_url)


@login_required
def add_location(request, *args, **kwargs):
    if request.method != 'POST':
        return redirect('home')
    form = ProfileLocationForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        profile.place = form.cleaned_data['place']
        profile.location = form.cleaned_data['location']
        profile.save()
    return redirect('home')
