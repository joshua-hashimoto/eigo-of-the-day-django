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
    """
    custom queryset for model Phrase
    """

    def all(self):
        """
        Returns:
            queryset: return all object with is_active=True
        """
        return self.filter(is_active=True)

    def search(self, query):
        """
        custom search for the model.
        it works for search that include space ' ' and ',' in the search form.

        Returns:
            queryset: return filtered queryset using user input.
        """
        query_list = [i.split(',') for i in query.split(' ')]
        query_list = list(itertools.chain.from_iterable(query_list))
        query_list = [i for i in query_list if i != '']
        lookup = reduce(operator.or_, (Q(is_active=True) & Q(
            phrase__icontains=option) for option in query_list))
        return self.filter(lookup)


class PhraseManager(models.Manager):
    """
    custom manager for model Phrase using PhraseQuerySet.
    """

    def get_queryset(self):
        """
        set custom queryset

        Returns:
            PhraseQueryset: return PhraseQueryset using model Phrase
        """
        return PhraseQueryset(self.model, using=self._db)

    def all(self):
        """
        calls custom queryset's all() method

        Returns:
            queryset: return all object with is_active=True
        """
        return self.get_queryset().all()

    def search(self, query=None):
        """
        if argument query is set to None, return .none().
        if there is a value, pass it to custom queryset's search method.

        Args:
            query (str): user input query string

        Returns:
            queryset: return filtered queryset
        """
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Phrase(CoreModel):
    """
    model to save Phrases

    Attributes:
        user (ForeignKey): one-to-one relation to set user to model
        phrase (CharField): field to save the actual phrase. max length to 255 charactors
        objects (PhraseManager): set custom Manager to model
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phrase = models.CharField(max_length=255, unique=True)

    objects = PhraseManager()

    class Meta:
        """
        Attributes:
            ordering (List): use to determine the ordering of model objects when listed
        """
        ordering = ['-timestamp', '-updated', ]

    def __str__(self):
        """
        determine which field of the model should be representing the model object.
        mainly used in admin site.

        Returns:
            str: returns phrase field.
        """
        return self.phrase

    def get_absolute_url(self):
        """
        determine to absolute url of the model.
        mainly used to call each object through urls in template.
        """
        return reverse("eigo:eigo_detail", kwargs={"pk": self.pk})


class ExampleQueryset(models.QuerySet):
    """
    custom queryset for model Example
    """

    def all(self):
        """
        Returns:
            queryset: return all object with is_active=True
        """
        return self.filter(is_active=True)


class ExampleManager(models.Manager):
    """
    custom manager for model Example using ExampleQuerySet.
    """

    def get_queryset(self):
        """
        set custom queryset

        Returns:
            ExampleQueryset: return ExampleQueryset using model Example
        """
        return ExampleQueryset(self.model, using=self._db)

    def all(self):
        """
        calls custom queryset's all() method

        Returns:
            queryset: return all object with is_active=True
        """
        return self.get_queryset().all()


class Example(CoreModel):
    """
    model to save Example

    Attributes:
        phrase (ForeignKey): one-to-one relation to set phrase to model
        example (TextField): field to save the actual phrase
        objects (ExampleManager): set custom Manager to model
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='examples')
    example = models.TextField()

    objects = ExampleManager()

    def __str__(self):
        """
        determine which field of the model should be representing the model object.
        mainly used in admin site.

        Returns:
            str: returns example field.
        """
        return self.example


class SnapQueryset(models.QuerySet):
    """
    custom queryset for model Snap
    """

    def all(self):
        """
        Returns:
            queryset: return all object with is_active=True
        """
        return self.filter(is_active=True)


class SnapManager(models.Manager):
    """
    custom manager for model Snap using SnapQuerySet.
    """

    def get_queryset(self):
        """
        set custom queryset

        Returns:
            SnapQueryset: return SnapQueryset using model Snap
        """
        return SnapQueryset(self.model, using=self._db)

    def all(self):
        """
        calls custom queryset's all() method

        Returns:
            queryset: return all object with is_active=True
        """
        return self.get_queryset().all()


def upload_image_to(instance, filename):
    asset_path = f'{str(instance.phrase.phrase)}/{filename}'
    return asset_path


class Snap(CoreModel):
    """
    model to save Snap

    Attributes:
        phrase (ForeignKey): one-to-one relation to set phrase to model
        snap (ImageField): field to save the actual phrase
        objects (SnapManager): set custom Manager to model
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='snaps')
    snap = models.ImageField(upload_to=upload_image_to,)

    objects = SnapManager()

    def __str__(self):
        """
        determine which field of the model should be representing the model object.
        mainly used in admin site.

        Returns:
            str: returns name of the snap field.
        """
        return self.snap.name
