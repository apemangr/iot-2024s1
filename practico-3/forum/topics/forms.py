
from django import forms
from .models import Topic, Response

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content', 'author_name']
