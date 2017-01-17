from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
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
from .forms import ItemForm, SearchForm


def home(request):
    published_items = Item.objects.filter(is_published=True).count()
    fb_profile_clicks = sum(item.renters.count() for item in Item.objects.all())
    context = dict(
        published_items=published_items,
        fb_profile_clicks=fb_profile_clicks,
    )
    if request.method != 'GET':
        context['form'] = SearchForm()
        return render(request, 'app/index.html', context)

    form = SearchForm(request.GET)
    if not form.is_valid():
        return render(request, 'app/index.html', context)

    context['form'] = form
    what = form.cleaned_data['what'].strip()
    where = form.cleaned_data['where'].strip()
    if not what and not where:
        return render(request, 'app/index.html', context)

    items = Item.objects.annotate(search=SearchVector('name', 'description'))
    items.filter(is_published=True)
    if what:
        for what_kw in what.split(' '):
            items = items.filter(search=what_kw)
    if where:
        for where_kw in where.replace(', ', ' ').replace(',', '').split(' '):
            items = items.filter(place__search=where_kw)
    table = ItemTable(items)
    RequestConfig(request).configure(table)
    context['table'] = table
    return render(request, 'app/index.html', context)


@method_decorator(login_required, name='dispatch')
class ItemAddView(FormView):
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'app/add_item.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if len(Item.objects.filter(user=request.user)) > 500:
            return redirect('home')
        form = self.form_class(request.POST)

        if form.is_valid():
            item_data = {k: v for k, v in form.cleaned_data.items() if 'image' not in k}
            item_data['user'] = request.user
            categories = item_data.pop('categories')
            item = Item(**item_data)
            item.save()

            item.categories = categories
            item.save()

            images_data = {k: v for k, v in form.cleaned_data.items() if 'image' in k}
            for key in sorted(k for k, v in images_data.items() if v):
                url = images_data[key]
                image = Image(item=item, url=url)
                image.save()

            send_emails(request, item)
            response = redirect('view_item', item.id)
            response['Location'] += '?new=true'
            return response
        else:
            return render(request, 'app/add_item.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ItemDetailView(DetailView):
    template_name = 'app/item_details.html'
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(Item, id=item_id) if item_id else None
        if item.is_published or item.user == request.user or request.user.is_staff:
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
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(Item, id=item_id) if item_id else None
        if item and (item.user != request.user or request.user.is_staff):
            return super().post(request, *args, **kwargs)
        return redirect('view_item', item.id)


@staff_member_required
def publish_item(request, *args, **kwargs):
    item_id = kwargs.get('pk')
    item = get_object_or_404(Item, id=item_id) if item_id else None
    item.is_published = True
    item.save()
    return redirect('view_item', item.id)


@staff_member_required
def unpublish_item(request, *args, **kwargs):
    item_id = kwargs.get('pk')
    item = get_object_or_404(Item, id=item_id) if item_id else None
    item.is_published = False
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
    if not item.renters.filter(id=request.user.id) and request.user != item.user:
        item.renters.add(request.user)
        item.save()
    return redirect(item.user.profile.facebook_url)
