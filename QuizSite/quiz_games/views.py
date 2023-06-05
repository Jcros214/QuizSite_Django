import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.templatetags.static import static

import requests as req
from random import shuffle


# Create your views here.
def index(request):
    return render(request, 'quiz_games/index.html')


def match_verse(request):
    return render(request, 'quiz_games/match_verse.html')


def match_verse_backend(request):
    if request.method == 'GET':
        material = json.loads(req.get('http://localhost:8000' + static('summer_spectacular2023_material.json')).content)

        # Filter material
        material = [verse for verse in material['verses'] if int(verse['chapter']) == 5]

        # Get random verse
        import random
        verse = random.choice(material)
        verse_text = verse['text']
        verse_ref = f"{verse['chapter']}:{verse['verse']}"

        # verse_ref_options = [verse['verse_ref'] for verse in material if verse['text'] != verse]

        other_options = [f"{new_verse['chapter']}:{new_verse['verse']}" for new_verse in material if
                         (new_verse['text'] != verse_text) and (new_verse['chapter'] == verse['chapter'])]

        shuffle(other_options)

        verse_ref_options = [verse_ref, *other_options[:3]]

        shuffle(verse_ref_options)

        data = {
            'verse': verse_text,
            'verse_ref_options': verse_ref_options,

        }
        response = HttpResponse(
            json.dumps(data), content_type='application/json',
        )
        response.set_cookie('verse_ref', verse_ref)
        return response

    elif request.method == 'POST':
        data = {
            'result': 'Correct!' if request.COOKIES.get('verse_ref') == request.POST.get(
                'verse_ref') else f'Incorrect: You said: {request.POST.get("verse_ref")}, but it\'s actually {request.COOKIES.get("verse_ref")}',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse("?")
