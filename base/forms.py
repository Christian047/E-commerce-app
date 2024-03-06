from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm




class CustomerCreationForm(UserCreationForm):
    is_vendor = forms.BooleanField(label='Are you a vendor?', required=False)

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('email', 'is_vendor')

# This form collects the forms to be put in the views
class Roomform(ModelForm):
    # Class Meta is used for the appearance of the form
    class Meta:
        model = Room
        # Fields takes care of how many of the model parts to display
        fields = '__all__'
        # Exclude method is used to exclude certain parts from the list
        exclude = ['host', 'participants']
   
        
# Create a form to display the user model
class Userform(ModelForm):
    # Class Meta is used for the appearance of the form
    class Meta:
        model = User
        #  A list of Username and email are necessary for the field
        fields = ['username','email']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category' ,'image','description']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']