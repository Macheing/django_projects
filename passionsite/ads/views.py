# django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

# app imports
from ads.forms import CreateForm, CommentForm
from ads.utils import dump_queries
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
# database models
from ads.models import Ad, Comment, Fav



# Create your views here.

# Ad list view
class AdListView(OwnerListView):
    model = Ad
    # By convention:
    template_name = "ads/ad_list.html"

    def get(self, request) :
        ad_list = Ad.objects.all()
        # ad favorites
        favorites = list()
        # search bar
        search_value =  request.GET.get("search", False)

        #check whether user is authenticated or not
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        # search query
        if search_value:
            # Simple title-only search
            # objects = Ad.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]
            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=search_value)
            query.add(Q(text__icontains=search_value), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]

        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the ad_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)



        context = {'ad_list' : ad_list, 'favorites': favorites, 'search': search_value}
        return render(request, self.template_name, context)


# Ad detail view
class AdDetailView(OwnerDetailView):
    model = Ad
    # By convention:
    template_name = "ads/ad_detail.html"

    def get(self, request, pk):
        data = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=data).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': data, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)

# ad create view
class AdCreateView(LoginRequiredMixin, View):
    model = Ad
    fields = ['title','price', 'text','picture']

    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    # get form data
    def get(self, request, pk=None):
        form = CreateForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    # post form data
    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        # Add owner to the model before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()

        return redirect(self.success_url)

# ad update view
class AdUpdateView(LoginRequiredMixin, View):
    model = Ad
    #fields = ['title', 'price', 'text','picture','comments']

    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        ad = form.save(commit=False)
        ad.save()
        return redirect(self.success_url)

# ad delete view
class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ads/ad_confirm_delete.html"


# stream_file view for uploading, viewing, updating of pictures with ads.
def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response

# comment create view for creating comments
class CommentCreateView(LoginRequiredMixin, View):
    model = Comment
    fields = ['text','ad','owner']
    #template_name = 'ads/ad_detail.html'
    #success_url = reverse_lazy('ads:all')

    def post(self, request, pk) :
        data = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'],
                            owner=request.user, ad=data)

        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

# comment delete view for deleting comments
class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/ad_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        data = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=data)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        data = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=data).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


