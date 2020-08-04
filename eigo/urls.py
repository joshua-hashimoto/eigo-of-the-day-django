from django.urls import path

from .views import PhraseDetailView, PhraseCreateView, PhraseUpdateView

app_name = 'eigo'

urlpatterns = [
    path('<uuid:pk>/edit/', PhraseUpdateView.as_view(), name='eigo_edit'),
    path('<uuid:pk>/', PhraseDetailView.as_view(), name='eigo_detail'),
    path('new/', PhraseCreateView.as_view(), name='eigo_new'),
]