from django import forms
from django.forms import ModelForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES,
    CHOICES_CONDICAO, SubmissaoModel
    )


class PreSubmissaoForm(ModelForm):
    error_css_class = "error"

    class Meta:
        model = SubmissaoModel
        fields = ('problema', 'equipe')

        labels = {
            'problema': 'Problema:',
            'equipe': 'Equipe  :',
        }
        widgets = {
            'problema': forms.Select(choices=CHOICES_PROBLEMAS),
            'equipe': forms.Select(choices=CHOICES_EQUIPES),
        }

    def clean_problema(self):
        if not self.cleaned_data['problema']:
            return False
        return self.cleaned_data['problema']

    def clean_equipe(self):
        if not self.cleaned_data['equipe']:
            return False
        return self.cleaned_data['equipe']


class SubmissaoForm(ModelForm):
    error_css_class = "error"

    class Meta:
        model = SubmissaoModel
        fields = ('problema', 'equipe')
        fields = fields + ('tempo', 'status')

        labels = {
            'problema': 'Problema:',
            'equipe': 'Equipe  :',
            'tempo': 'Tempo  :',
            'status': 'Aceito ? ',
        }
        widgets = {
            'problema': forms.Select(choices=CHOICES_PROBLEMAS),
            'equipe': forms.Select(choices=CHOICES_EQUIPES),
            'status': forms.Select(choices=CHOICES_CONDICAO),
            'tempo': forms.NumberInput(),
        }

    def clean_problema(self):
        if not self.cleaned_data['problema']:
            return False
        return self.cleaned_data['problema']

    def clean_equipe(self):
        if not self.cleaned_data['equipe']:
            return False
        return self.cleaned_data['equipe']

    def clean_status(self):
        if not self.cleaned_data['status']:
            return False
        return self.cleaned_data['status']

    def clean_tempo(self):
        tempo = self.cleaned_data['tempo']
        if not tempo and int(tempo) > 0:
            return False
        return tempo
