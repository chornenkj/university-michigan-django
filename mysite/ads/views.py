from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse

from .models import Ad, Comment
from .owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from .forms import CreateForm, CommentForm


class AdListView(OwnerListView):
    model = Ad
    # By convention:
    # template_name = "ads/ad_list.html"


class AdDetailView(OwnerDetailView):
    model = Ad
    def get(self, request, pk):
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)
    # By convention:
    # template_name = "ads/ad_detail.html"


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
