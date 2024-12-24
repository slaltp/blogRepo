
from django import forms
from .models import Profile
from .models import Comment, Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'password','password1', 'contact_number', 'profile_picture']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','post_img']
    def clean_post_img(self):
        post_img = self.cleaned_data.get('post_img')
        if not post_img:
            raise forms.ValidationError("Image is required for the post.")
        return post_img