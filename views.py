from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ingredient, Recipe, RecipeIngredient

@login_required
def dashboard(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'recipes': recipes})

@login_required
def add_recipe(request):
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        recipe = Recipe.objects.create(
            user=request.user,
            recipe_name=request.POST['recipe_name']
        )
        for ing in ingredients:
            qty = request.POST.get(f'qty_{ing.id}')
            if qty and float(qty) > 0:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ing,
                    quantity=float(qty)
                )
        return redirect('result', recipe.id)
    return render(request, 'add_recipe.html', {'ingredients': ingredients})

@login_required
def result(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    items = RecipeIngredient.objects.filter(recipe=recipe)
    total = {'cal': 0, 'protein': 0, 'carbs': 0, 'fats': 0}
    for item in items:
        factor = item.quantity / 100
        total['cal'] += item.ingredient.calories * factor
        total['protein'] += item.ingredient.protein * factor
        total['carbs'] += item.ingredient.carbs * factor
        total['fats'] += item.ingredient.fats * factor
    return render(request, 'result.html', {'recipe': recipe, 'total': total})
