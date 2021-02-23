from django import forms
from .models import Topic, Enrty

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic#topic models
        fields=['text']
        lables={'text':''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Enrty
        fields=['text']
        lables={'text': ' '}
        widgets={'text':forms.Textarea(attrs={'cols':80})}