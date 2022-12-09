from .models import Ad
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad
    # By convention:
    # template_name = "ads/ad_list.html"


class AdDetailView(OwnerDetailView):
    model = Ad
    # By convention:
    # template_name = "ads/ad_detail.html"


class AdCreateView(OwnerCreateView):
    model = Ad
    # List the fields to copy from the Ad model to the Ad form
    fields = ['title', 'price', 'text']
    # By convention:
    # template_name = "ads/ad_form.html"


class AdUpdateView(OwnerUpdateView):
    model = Ad
    # List the fields to copy from the Ad model to the Ad form
    fields = ['title', 'price', 'text']
    # By convention:
    # template_name = "ads/ad_form.html"


class AdDeleteView(OwnerDeleteView):
    model = Ad
    # By convention:
    # template_name = "ads/ad_confirm_delete.html"
