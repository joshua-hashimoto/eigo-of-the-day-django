from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import PhraseForm, ExampleFormSet, SnapFormSet
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


class PhraseCreateView(LoginRequiredMixin, CreateView):
    """
    """
    model = Phrase
    template_name = 'eigo/eigo_form.html'
    form_class = PhraseForm
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['examples'] = ExampleFormSet(self.request.POST)
            context['snaps'] = SnapFormSet(
                self.request.POST, self.request.FILES)
        else:
            context['examples'] = ExampleFormSet()
            context['snaps'] = SnapFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
        examples = context['examples']
        if examples.is_valid():
            examples.instance = self.object
            presaved_examples = examples.save(commit=False)
            for pre_example in presaved_examples:
                pre_example.user = self.request.user
                pre_example.save()
        snaps = context['snaps']
        if snaps.is_valid():
            snaps.instance = self.object
            presaved_snaps = snaps.save(commit=False)
            for pre_snap in presaved_snaps:
                pre_snap.user = self.request.user
                pre_snap.save()
        return super(PhraseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eigo:eigo_detail', kwargs={'pk': self.object.pk})


class PhraseUpdateView(LoginRequiredMixin, UpdateView):
    """
    """
    model = Phrase
    template_name = 'eigo/eigo_form.html'
    form_class = PhraseForm
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['examples'] = ExampleFormSet(
                self.request.POST, instance=self.object)
            context['snaps'] = SnapFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['examples'] = ExampleFormSet(instance=self.object)
            context['snaps'] = SnapFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
        examples = context['examples']
        if examples.is_valid():
            examples.instance = self.object
            presaved_examples = examples.save(commit=False)
            for pre_example in presaved_examples:
                pre_example.user = self.request.user
                pre_example.save()
        snaps = context['snaps']
        if snaps.is_valid():
            snaps.instance = self.object
            presaved_snaps = snaps.save(commit=False)
            for pre_snap in presaved_snaps:
                pre_snap.user = self.request.user
                pre_snap.save()
        return super(PhraseUpdateView, self).form_valid(form)

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
