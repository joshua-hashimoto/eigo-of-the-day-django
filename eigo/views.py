from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, NamedFormsetsMixin

from .forms import ExampleInlineFormSet, SnapInlineFormSet
from .models import Phrase


class PhraseListView(LoginRequiredMixin, ListView):
    """
    list all objects to template.
    Login is required.

    Attributes:
        model (Phrase): target model to fetch data from.
        template_name (str): a path to template that is responsible to render objects
        context_object_name (str): to override context object name used in template.
                                   for ListView's it defaults to 'object_list'
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Phrase
    template_name = 'eigo/eigo_list.html'
    context_object_name = 'eigo_list'
    login_url = 'account_login'

    def get_queryset(self):
        """
        override this method to add custom search functionalities.
        in this case, it has 2 parts:

        1. see if url contains 'search' query params(?search=)
           if so, get that value and search through the data using .search()
        2. see if url contains 'ordering' query params(?ordering=)
           if so, changed the ordering of the listed objects using .order_by()

        Returns:
            queryset: return filtered_ordered object list to template.
        """
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
    pass object to template.
    Login is required.

    Attributes:
        model (Phrase): target model to fetch data from.
        template_name (str): a path to template that is responsible to render objects
        context_object_name (str): to override context object name used in template.
                                   for DetailView's it defaults to 'object'
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Phrase
    template_name = 'eigo/eigo_detail.html'
    context_object_name = 'eigo'
    login_url = 'account_login'


class PhraseCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    """
    passes form class for creating new object.
    Login is required.

    Attributes:
        model (Phrase): target model to fetch data from.
        inlines (List): set inlineformsets to the view.
                        this is for CreateWithInlinesView
        inlines_names (List): set custom names for inlineformsets included in inlines attribute.
                              this is for CreateWithInlinesView but only can be used because
                              NamedFormsetsMixin is set
        fields (Tuple): set fields to render to template. for default CreateView
        template_name (str): a path to template that is responsible to render objects
        success_url (str): a url to render after creation is successful
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Phrase
    inlines = [ExampleInlineFormSet, SnapInlineFormSet]
    inlines_names = ['example_formset', 'snap_formset']
    fields = ('phrase',)
    template_name = 'eigo/eigo_new.html'
    success_url = reverse_lazy('eigo:eigo_list')
    login_url = 'account_login'

    def form_valid(self, form):
        """
        default function for CreateView that is called when
        the form user submits is valid.
        override to set current login user to user field in model.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhraseUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    """
    passes form class for updating objects.
    Login is required.

    Attributes:
        model (Phrase): target model to fetch data from.
        inlines (List): set inlineformsets to the view.
                        this is for UpdateWithInlinesView
        inlines_names (List): set custom names for inlineformsets included in inlines attribute.
                              this is for UpdateWithInlinesView but only can be used because
                              NamedFormsetsMixin is set
        fields (Tuple): set fields to render to template. for default UpdateView
        template_name (str): a path to template that is responsible to render objects
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin
    """
    model = Phrase
    inlines = [ExampleInlineFormSet, SnapInlineFormSet]
    inlines_names = ['example_formset', 'snap_formset']
    fields = ('phrase',)
    template_name = 'eigo/eigo_edit.html'
    login_url = 'account_login'

    def form_valid(self, form):
        """
        default function for UpdateView that is called when
        the form user submits is valid.
        override to set current login user to user field in model.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        default function for UpdateView that is called when
        the update is successful.
        override to give a url to render.
        """
        return reverse_lazy('eigo:eigo_detail', kwargs={'pk': self.object.pk})


class PhraseDeleteView(LoginRequiredMixin, DeleteView):
    """
    passes form class for object deletion.
    Login is required.

    Attributes:
        model (Phrase): target model to fetch data from.
        template_name (str): a path to template that is responsible to render objects
        success_url (str): a url to render after creation is successful
        login_url (str): a django named path to login page.
                         needed because this view is login required by LoginRequiredMixin

    Note:
        originally designed to only disable object by changing
        is_active field to False. However due to the model Phrase
        needs to be unique, it will create more problems then
        the benifit it will give to the user. This might change.
    """
    model = Phrase
    template_name = 'eigo/eigo_delete.html'
    success_url = reverse_lazy('eigo:eigo_list')
    login_url = 'account_login'
