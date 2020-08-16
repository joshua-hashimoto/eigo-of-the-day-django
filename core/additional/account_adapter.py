from django.http import Http404
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    A custom account adapter to disable signup
    functionality from django-allauth
    """

    def is_open_for_signup(self, request):
        raise Http404
        return False
