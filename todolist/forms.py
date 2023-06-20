from django import forms

from todolist.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content"]  # еще можно добавить "tags"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            # "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
