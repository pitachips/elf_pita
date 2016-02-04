from django import forms
from .models import Store, Review, Comment


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = ('name', 'address', 'tel', 'intro', 'hours', 'website', 'photo', 'area', 'sub_area', 'categories', 'sub_categories', 'parking', 'menu' )
        widgets = {
            'intro': forms.Textarea(attrs={'style':'resize:none; width:500px; height:100px;', }),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('user_rating', 'content', 'photo', )
        widgets = {
            'content': forms.Textarea(attrs={'style':'resize:none; width:500px; height:100px;', }),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )