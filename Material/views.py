from django.shortcuts import render, redirect
from django import forms
import os
import random


# Create your views here.

# def index(request):
#     return render(request, 'Material/index.html', )
#

def render_material(request, name):
    return render(request, f'Material/{name}.html')


def current_material(request):
    return render_material(request, 'matthew_5_7')


def matthew(request):
    return render_material(request, 'matthew')


class MaterialForm(forms.Form):
    material_set = forms.MultipleChoiceField(choices=(("Matthew_5-7", "Matthew 5-7"),))
    chapters = forms.MultipleChoiceField(
        choices=(("Matthew_5", "Matthew 5"), ("Matthew_6", "Matthew 6"), ("Matthew_7", "Matthew 7")))


def audio_verses(request):
    # on GET, load page
    if request.method == 'GET':
        # get a random verse
        print(os.getcwd())
        file = random.choice(os.listdir("Material/static/audio/Matthew_5-7/Matthew_5/"))

        material_sets = os.listdir("Material/static/audio/")
        chapters = [os.listdir(f'Material/static/audio/{material_set}') for material_set in material_sets]

        chapter = 'Matthew_5'
        material_set = 'Matthew_5-7'

        return render(request, 'Material/audio_verses.html',
                      {
                          'file': file,
                          'chapter': chapter,
                          'material_set': material_set,
                          'chapters': chapters,
                          'material_sets': material_sets,
                      })
    else:
        if request.POST.get('chapters'):
            material_set = request.POST.get('material_set')
            chapter = request.POST.get('chapters')
        else:
            return redirect('material:audio')
