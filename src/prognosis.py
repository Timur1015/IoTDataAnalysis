import pandas as pd

from src.classes.Utility import Utility
from src.classes.Recipe import Recipe
from src.classes.Package_ import Package_


def exponential_smoothing(series, alpha):
    smoothed_series = [series[0]]
    for i in range(1, len(series)):
        smoothed_value = smoothed_series[i - 1] + alpha * (series[i - 1] - smoothed_series[i - 1])
        smoothed_series.append(smoothed_value)
    return smoothed_series


recipes = Recipe().df
packages = Package_().df
Utility.convert_to_ts(recipes, 'timestamp')
Utility.convert_to_ts(packages, 'timestamp')

packs_recipes = pd.merge_asof(packages, recipes, left_index=True, right_index=True)
packs_recipes_months = Utility.spit_into_months(packs_recipes)
months = []
recipe_good_packs_by_month = []
for m in packs_recipes_months:
    months.append(Utility.get_month_name(m))
    month_data = m.groupby('recipe')['good_packs'].sum()
    recipe_good_packs_by_month.append(month_data)

for recipe in recipe_good_packs_by_month:
    print(recipe)

alpha = 0.2

smoothed_recipe_good_packs_by_month = []
for recipe in recipe_good_packs_by_month:
    smoothed_good_packs = exponential_smoothing(recipe, alpha)
    smoothed_recipe_good_packs_by_month.append(smoothed_good_packs)


for g in smoothed_recipe_good_packs_by_month:
    print(g)

