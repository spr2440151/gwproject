from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, Step, Review
 
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'category', 'servings', 'cooking_time', 'point']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'レシピ名'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'レシピの説明'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '例: 4'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '例: 30 (分)'}),
            'point': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '調理のポイント'}),
        }
 
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '材料名'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '分量'}),
        }
 
class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ['step_number', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '手順の説明'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
 
#材料フォームセット
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True
)
 
#手順フォームセット
StepFormSet = inlineformset_factory(
    Recipe, Step,
    form=StepForm,
    extra=3,
    can_delete=True
)

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    phone = forms.CharField(label='電話番号')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #フィールド内のplaceholderにメッセージを登録
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください'
        #フィールドを出力、<input>タグのclass属性を設定
        self.fields['name'].widget.attrs['class'] = 'form-control'
        #以下それぞれ繰り返し
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = '電話番号を入力してください'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} 星") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }