from django.db import models
from accounts.models import CustomUser
 
class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.title
 
class Recipe(models.Model):
   
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )
   
    title = models.CharField(
        verbose_name='レシピ名',
        max_length=100)
   
    description = models.TextField(
        verbose_name='レシピ紹介'
    )
   
    category = models.ManyToManyField(
        Category,
        verbose_name='カテゴリー',
        related_name='recipes'
    )
   
    image = models.ImageField(
        verbose_name='イメージ',
        upload_to='photos'
    )
   
    servings = models.IntegerField(
        verbose_name='提供人数',
        default=1
    )
   
    cooking_time = models.IntegerField(
        verbose_name='調理時間(分)'
    )
   
    point = models.TextField(
        verbose_name='ポイント'
    )
   
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )
   
    update_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )
   
    def __str__(self):
        return self.title
 
class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='レシピ',
        related_name='ingredients'
    )
   
    name = models.CharField(
        verbose_name='材料名',
        max_length=100
    )
   
    quantity = models.CharField(
        verbose_name='分量',
        max_length=10
    )
   
    def __str__(self):
        return f'{self.name} ({self.quantity})'
 
class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='レシピ',
        related_name='steps'
    )
   
    step_number = models.PositiveIntegerField(
        verbose_name='手順番号',
        unique=False
    )
   
    description = models.TextField(
        verbose_name='手順説明',
        default=''
    )
   
    image = models.ImageField(
        verbose_name='イメージ',
        upload_to='photos',
        null=True,
        blank=True
    )
    
    def save(self,*args, **kwargs):
        if not self.step_number:
            max_step_number = Step.objects.filter(recipe=self.recipe).aggregate(
                models.Max('step_number')
            )['step_number__max']
            self.step_number = (max_step_number or 0) + 1
        super().save(*args, **kwargs)
   
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'step_number'], name = 'unique_step_per_recipe')]
        ordering = ['step_number']
   
    def __str__(self):
        return f'Step {self.step_number}: {self.description}'
 
class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='レシピ',
        related_name='reviews'
    )
   
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='ユーザー'
    )
   
    rating = models.IntegerField(
        verbose_name='評価',
        choices=[(i, str(i)) for i in range(1, 6)]
    )
   
    comment = models.TextField(
        verbose_name='コメント',
        blank=True
    )
   
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )
   
    def __str__(self):
        return f"{self.user.username}'s review for {self.recipe.title}"
   