from functools import reduce
import operator
import itertools

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from martor.models import MartorField

from core.additional.models import CoreModel


class PhraseQueryset(models.QuerySet):

    def all(self):
        return self.filter(is_active=True)

    def search(self, query):
        query_list = [i.split(',') for i in query.split(' ')]
        query_list = list(itertools.chain.from_iterable(query_list))
        query_list = [i for i in query_list if i != '']
        lookup = reduce(operator.or_, (Q(is_active=True) & Q(
            phrase__icontains=option) for option in query_list))
        return self.filter(lookup)


class PhraseManager(models.Manager):

    def get_queryset(self):
        return PhraseQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Phrase(CoreModel):
    """
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phrase = models.CharField(max_length=255, unique=True)

    objects = PhraseManager()

    def __str__(self):
        return self.phrase

    def get_absolute_url(self):
        return reverse("eigo:eigo_detail", kwargs={"pk": self.pk})


class Example(CoreModel):
    """
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='examples')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    example = models.TextField()

    def __str__(self):
        return self.example


def upload_image_to(instance, filename):
    asset_path = f'{str(instance.phrase.phrase)}/{filename}'
    return asset_path


class Snap(CoreModel):
    """
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='snaps')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    snap = models.ImageField(upload_to=upload_image_to, blank=True,)

    def __str__(self):
        return self.snap.name
