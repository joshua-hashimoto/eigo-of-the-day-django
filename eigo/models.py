from django.contrib.auth import get_user_model
from django.db import models
from martor.models import MartorField

from core.additional.models import CoreModel


class Phrase(CoreModel):
    """
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phrase = models.CharField(max_length=255)
    memo = MartorField(blank=True)


class Example(CoreModel):
    """
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='examples')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    example = models.TextField()
    memo = MartorField(blank=True)


def upload_image_to(instance, filename):
    asset_path = f'{str(instance.phrase.phrase)}/images/{filename}'
    return asset_path


class Snap(CoreModel):
    """
    """
    phrase = models.ForeignKey(
        Phrase, on_delete=models.CASCADE, related_name='snaps')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    snap = models.ImageField(upload_to=upload_image_to)
