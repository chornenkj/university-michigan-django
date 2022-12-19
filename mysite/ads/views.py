from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse

from .models import Ad, Comment, Fav
from .owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from .forms import CreateForm, CommentForm


class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    def get(self, request) :
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'ad_list' : ad_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    def get(self, request, pk):
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        # Create unbound CreateForm instance to pass to template
        form = CreateForm()
        ctx = {'form': form}
        ctx['edit'] = False
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        # Read form data from the POST data
        form = CreateForm(request.POST, request.FILES or None)

        # If form is not valid return to enter valid data
        # The form will contain previous data from the POST data
        if not form.is_valid():
            ctx = {'form': form}
            ctx['edit'] = False
            return render(request, self.template_name, ctx)

        # If form is valid add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        # And now save data to database
        pic.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        # Get instance with pk passed to create CreateFrom with
        # data from database
        x = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=x)
        ctx = {'form': form}
        ctx['edit'] = True
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        # Read data from database for pk passed
        x = get_object_or_404(Ad, id=pk, owner=self.request.user)
        # Create form and read data from the POST data for this instance
        form = CreateForm(request.POST, request.FILES or None, instance=x)

        # If form is not valid return to enter valid data
        # The form will contain previous data from the POST data
        if not form.is_valid():
            ctx = {'form': form}
            ctx['edit'] = True
            return render(request, self.template_name, ctx)

        # If form is valid save form data to database
        form.save()
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    # By convention:
    # template_name = "ads/ad_confirm_delete.html"


# The view to show picture only
def stream_file(request, pk):
    x = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = x.content_type
    response['Content-Length'] = len(x.picture)
    response.write(x.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # Generate success_url dynamically to return to the ad page
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
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


