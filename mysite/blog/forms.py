# from django import forms
# from .models import Post, Comment
#
#
# class PostForm(forms.ModelForm):
#     class Meta():
#         model = Post
#         fields = ('author','title','text',)
#         #attrs attributes
#         #bice povezano sa tri klase editable, medium-editor-textarea,postcontent
#         widgets = {
#             'title': forms.TextInput(attrs={'class':'textinputclass'}),
#             'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
#         }
#
# class CommentForm(forms.ModelForm):
#     class Meta():
#         model = Comment
#         field=('author','text',)
#
#         widgets = {
#             'author': forms.TextInput(attrs={'class': ' textinputclass'}),
#             #klase ispod su CSS klase, nisu nase kreirane
#             'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
#         }
#


from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
