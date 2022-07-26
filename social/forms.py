from django import forms
from .models import Genre, Thread


class CreateThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ('title', 'genre',)
        labels = {
            'title': 'スレッドのタイトル',
            'genre': 'スレッドのジャンル'
        }