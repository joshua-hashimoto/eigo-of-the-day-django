from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, NamedFormsetsMixin

from .forms import ExampleInlineFormSet, SnapInlineFormSet
from .models import Phrase


class PhraseListView(LoginRequiredMixin, ListView):
    """
    """
    model = Phrase
    template_name = 'eigo/eigo_list.html'
    context_object_name = 'eigo_list'
    login_url = 'account_login'

    def get_queryset(self):
        queryset = Phrase.objects.all()
        if (query := self.request.GET.get('search')):
            queryset = Phrase.objects.search(query)
        if (ordering := self.request.GET.get('ordering')):
            if ordering == 'up':
                queryset = queryset.order_by('-phrase')
            if ordering == 'down':
                queryset = queryset.order_by('phrase')
        return queryset


class PhraseDetailView(LoginRequiredMixin, DetailView):
    """
    """
    model = Phrase
    template_name = 'eigo/eigo_detail.html'
    context_object_name = 'eigo'
    login_url = 'account_login'


class PhraseCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    """
    """
    model = Phrase
    inlines = [ExampleInlineFormSet, SnapInlineFormSet]
    inlines_names = ['example_formset', 'snap_formset']
    fields = ('phrase',)
    template_name = 'eigo/eigo_new.html'
    success_url = reverse_lazy('eigo:eigo_list')
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhraseUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    """
    """
    model = Phrase
    inlines = [ExampleInlineFormSet, SnapInlineFormSet]
    inlines_names = ['example_formset', 'snap_formset']
    fields = ('phrase',)
    template_name = 'eigo/eigo_edit.html'
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eigo:eigo_detail', kwargs={'pk': self.object.pk})


class PhraseDeleteView(LoginRequiredMixin, DeleteView):
    model = Phrase
    template_name = 'eigo/eigo_delete.html'
    success_url = reverse_lazy('eigo:eigo_list')
    login_url = 'account_login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
