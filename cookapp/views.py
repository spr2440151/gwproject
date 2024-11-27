from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.urls import reverse_lazy
from .forms import RecipeForm, IngredientForm, StepForm, ContactForm, ReviewForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Recipe, Review
from django.views.generic import DetailView
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMessage


 
class IndexView(ListView):
    template_name = 'index.html'
    queryset = Recipe.objects.order_by('-posted_at')[:3]

@method_decorator(login_required, name='dispatch')
class CreateRecipeView(CreateView):
    form_class = RecipeForm
    template_name = "post_recipe.html"
    success_url = reverse_lazy('cook:post_ingredient')
 
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        recipe.save()
        self.request.session['recipe_id'] = recipe.id  # セッションに保存
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CreateIngredientView(CreateView):
    form_class = IngredientForm
    template_name = 'post_ingredient.html'
    success_url = reverse_lazy('cook:post_step')
    
    def form_valid(self, form):
        ingredient = form.save(commit=False)
        recipe_id = self.request.session.get('recipe_id')  # セッションから取得
        if not recipe_id:
            # recipe_idが見つからない場合はエラーを返す
            form.add_error(None, "レシピが見つかりませんでした。最初からやり直してください。")
            return self.form_invalid(form)
        ingredient.recipe_id = recipe_id
        ingredient.user = self.request.user
        ingredient.save()
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class CreateStepView(CreateView):
    form_class = StepForm
    template_name = 'post_step.html'
    success_url = reverse_lazy('cook:post_success')
    
    def form_valid(self, form):
        step = form.save(commit=False)
        recipe_id = self.request.session.get('recipe_id')  # セッションから取得
        if not recipe_id:
            # recipe_idが見つからない場合はエラーを返す
            form.add_error(None, "レシピが見つかりませんでした。最初からやり直してください。")
            return self.form_invalid(form)
        step.recipe_id = recipe_id
        step.user = self.request.user
        step.save()
        return super().form_valid(form)



class PostSuccessView(TemplateView):
    template_name = 'post_success.html'


class RecipeListView(ListView):
    template_name = 'cooks_list.html'
    queryset = Recipe.objects.order_by('-posted_at')
    paginate_by = 9
    
class FaqView(TemplateView):
    template_name = 'faq.html'

class ContactView(TemplateView):
    template_name = 'contact.html'


class CategoryView(ListView):
    template_name = 'index.html'
    
    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = Recipe.objects.filter(category=category_id).order_by('-posted_at')
        return categories

class DetailView(DetailView):
    template_name  = 'detail.html'
    model = Recipe
    context_object_name = 'recipe'

def recipe_search(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(point__icontains=query)
        )

    return render(request, 'recipe_list.html', {'object_list': recipes})

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('cook:contact')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']
        message = \
            '送信者名: {0}\nメールアドレス: {1}\n 電話番号:{2}\n メッセージ:\n{3}' \
            .format(name, email, phone, message)
        from_email = 'spr2440151@stu.o-hara.ac.jp'
        to_lite = ['spr2440151@stu.o-hara.ac.jp']
        message = EmailMessage(subject=f'{name} さんからのお問い合わせ',
                               body=message,
                               from_email=from_email,
                               to=to_lite,
                               )
        message.send()
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)

@login_required
def write_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.save()
            return redirect('cook:recipe_detail', pk=recipe.id)
    else:
        form = ReviewForm()
    
    return render(request, 'write_review.html', {'form': form, 'recipe': recipe})