from django.db import models
from accounts.models import Profile
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
# Create your models here.


fs = FileSystemStorage(location='/static/elem_images')

class Card(models.Model):
    name = models.CharField(max_length=50)
    elements = models.ManyToManyField('Element')
    image = models.URLField()
    rarity = models.IntegerField(default=0)
    poke_id = models.IntegerField()
    profiles = models.ManyToManyField(Profile, related_name='deck')

    def __str__(self):
        return self.name

    @classmethod
    def deal_cards(cls):
        cards = cls.objects.all().order_by('rarity')
        a = cards.count() / 10
        deck = random.sample(list(cards[0:a]), k=2)
        deck += random.sample(list(cards[a:a * 3]), k=5)
        deck += random.sample(list(cards[a * 3:a * 6]), k=20)
        deck += random.sample(list(cards[a * 6:a * 10]), k=40)
        return deck


class Element(models.Model):
    name = models.CharField(max_length=50)
    elem_id = models.IntegerField()
    image = models.ImageField(storage=fs,null=True)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('C', 'Closed')
    ]
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='O')
    datetime = models.DateTimeField(auto_now_add=True)

    def accepted_offer(self):
        return self.offer_set.filter(status='A').first()


class Offer(models.Model):
    STATUS_CHOICES = [
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('P', 'Pending')
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='P')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        cards = Card.deal_cards()
        profile.deck.add(*cards)

