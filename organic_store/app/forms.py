from django import forms
from . models import register,suppliers,delivery_agent,product,category

class registerform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    address=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    forms.Textarea(attrs={'rows': 2, 'cols': 15}),
    class Meta():
         model= register
         fields=('firstname','lastname','address','phone_no','state','district','city','email','password',)

class Editcustomerform(forms.ModelForm):
    class Meta():
        address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,}))
        model= register
        fields=('firstname','lastname','address','phone_no','state','district','city','password')


class Loginform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    class Meta():
        model = register
        fields = ('email','password')

class addDeliveryAgentForm(forms.ModelForm):
    class Meta():
        model = delivery_agent
        fields = ('name','email','id_proof')

class addCategoryForm(forms.ModelForm):
    class Meta():
        model = category
        fields = ('category_name',)


class editCategoryForm(forms.ModelForm):
    class Meta():
        model = category
        fields = ('category_name',)

class suppliersform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    address=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
         model= suppliers
         fields=('firstname','lastname','address','phone_no','state','district','city','email','password','id')

class Editsuppliersform(forms.ModelForm):
    address=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= register
         fields=('firstname','lastname','address','phone_no','state','district','city','password')


class Deliveryagentform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    class Meta():
         model= delivery_agent
         fields=('name','email','password',)


class Addproductsform(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= product
         fields=('categories','name','description','price','image')

class editproductsform(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= product
         fields=('categories','name','description','price','image')



