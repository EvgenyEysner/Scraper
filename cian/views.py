import os
from io import BytesIO
from threading import Thread

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa

from .forms import ApartmentEditForm, ImageForm, ProfileEditForm
from .models import Apartment, Image, Task, Profile
from .scraper import save_data, get_page_data


class IndexView(LoginRequiredMixin, ListView):
    model = Apartment
    template_name = 'cian/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartments_list'] = Apartment.objects.filter(owner=self.request.user.id)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = 'cian/apartment.html'
    context_object_name = 'apartments'

    def get_context_data(self, *args, **kwargs):
        self.object_list = super().get_queryset()
        context = super().get_context_data(**kwargs)
        context['image'] = Image.objects.all()
        return context


class ApartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    templates = 'cian/apartment_confirm_delete.html'
    success_url = reverse_lazy('apartments:home')


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('apartments:home')
    templates = 'cian/index.html'


class ApartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Apartment
    form_class = ApartmentEditForm
    success_url = reverse_lazy('apartments:home')
    template_name = 'cian/apartment_update.html'


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageForm
    success_url = reverse_lazy('apartments:home')
    template_name = 'cian/image_update.html'
    context_object_name = 'image'


class UserProfile(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'cian/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context

    def post(self, request):
        user = self.request.user
        if self.request.POST.get('form_type') == 'form_1':
            url = request.POST['url']
            t = Task(url=url, user=user)
            t.save()
            return redirect('apartments:profile')

        elif self.request.POST.get('form_type') == 'form_2':
            qs = Task.objects.filter(user=user)
            for url in qs:
                apartments = get_page_data(url)
                save_items = Thread(target=save_data, args=(apartments, user, ))
                save_items.start()
            return redirect('apartments:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'cian/edit.html'
    success_url = reverse_lazy('apartments:profile')


def fetch_pdf_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

@login_required
def apartments_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    apartment = get_object_or_404(Apartment, pk=pk)
    user = Profile.objects.get(user=request.user.id)

    template_path = 'cian/report.html'
    context = {
        'apartment': apartment,
        'user': user,
    }
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    # create a pdf
    pdf = pisa.pisaDocument(BytesIO(html.encode(
        'UTF-8')), result, encoding='UTF-8', link_callback=fetch_pdf_resources)
    apartment.delete() # remove object after file creation
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None