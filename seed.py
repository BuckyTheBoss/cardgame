import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'card_game.settings')
django.setup()

import random
from trading_post.models import *
from django.core.files import File


def create_pokemon(num_of_pokemon):
    if Card.objects.count() >= num_of_pokemon:
        print(f'{num_of_pokemon} already exist in the db')
        return

    for num in range(1, num_of_pokemon+1):
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}/')
        if r.status_code == 200:
            data = r.json()
            print(f"Pokemon: {data['name']}")
            card, created = Card.objects.get_or_create(poke_id=data['id'], name=data['name'], image=f'https://pokeres.bastionbot.org/images/pokemon/{data["id"]}.png')
            if created:
                for elem in data['types']:
                    element, created = Element.objects.get_or_create(name=elem['type']['name'], elem_id=elem['type']['url'].split('/')[6])
                    card.elements.add(element)

            species_r = requests.get(data['species']['url'])
            if species_r.status_code == 200:
                card.rarity = species_r.json()['capture_rate']
            else:
                card.rarity = random.randint(1, 100)
            card.save()

        else:
            print(f'Pokemon with ID {num} not found or the api responded with another status code: {r.status_code}')


def fix_rarity():
    for card in Card.objects.exclude(pk=1):
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{card.poke_id}/')
        if r.status_code == 200:
            data = r.json()
            card, created = Card.objects.get_or_create(poke_id=data['id'], name=data['name'],
                                                       image=f'https://pokeres.bastionbot.org/images/pokemon/{data["id"]}.png')

            species_r = requests.get(data['species']['url'])
            print(species_r)
            if species_r.status_code == 200:
                card.rarity = species_r.json()['capture_rate']
                card.save()



def populate_element_images():
    elems = Element.objects.all()
    images_dir = 'trading_post/static/elem_images/'
    for filename in os.listdir(images_dir):
        print(filename)
        for elem in elems:
            if elem.name == filename.split('.')[0]:
                f = open(images_dir+filename)
                file = File(f)
                elem.image.save(filename, file)
                file.close()

