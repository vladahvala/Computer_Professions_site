from django import forms
from .models import Comment

class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Comment here...', 'class':'form-control'}))
    #placeholder - текст, який пишеться перед тим як користувач ставить туди курсор
    class Meta:
        model = Comment
        fields = ['content']