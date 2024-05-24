from src.classes.Package_ import Package_
from src.classes.Recipe import Recipe
import pandas as pd
from src.classes.IoTStandardPlotter import IoTStandardPlotter
from src.classes.Utility import Utility
from src.classes.ErrorMessagesTl import ErrorMessagesTl


def process_data_and_plot(dataframes, item_name, categories, sp: IoTStandardPlotter):
    reject_packs = []
    good_packs = []
    errorcodes = []

    for df in dataframes:
        if item_name in df.index:
            sticks = df.loc[df.index == item_name]
            reject_packs.append(sticks['reject_packs_count'].values[0])
            good_packs.append(sticks['good_packs_count'].values[0])
            errorcodes.append(sticks['error_1019_count'].values[0])
        else:
            reject_packs.append(0)
            good_packs.append(0)
            errorcodes.append(0)

    sp.add_bar(good_packs, categories, 'green', 'good packs', None)
    sp.add_bar(reject_packs, categories, 'red', 'reject packs', good_packs)
    sp.add_bar(errorcodes, categories, 'blue', 'error', None)
    return sp


solution_path = '../solutions'
use_case_num = 2
package_df = Package_().df
Utility.convert_to_ts(package_df, 'timestamp')
recipe_df = Recipe().df
Utility.convert_to_ts(recipe_df, 'timestamp')

# get all rejected packages of vegan parmesan
packs_and_recipes = pd.merge_asof(package_df, recipe_df, left_index=True, right_index=True)
vegan_parmesan = packs_and_recipes.loc[packs_and_recipes['recipe'] == 'vegan parmesan']

# get the amount of rejected packages of vegan parmesan by month
package_months = Utility.spit_into_months(vegan_parmesan)
months = []
reject_packs = []
for month in package_months:
    months.append(Utility.get_month_name(month))
    reject_packs.append(month['reject_packs'].sum())

# plot vegan parmesan by month
standard_plotter = IoTStandardPlotter()
standard_plotter.add_bar(reject_packs, months, 'red', 'Reject Packs', None)
standard_plotter.set_title('Rejected vegan parmesan packages per month')
standard_plotter.set_ylabel('rejected packages')
standard_plotter.show()
standard_plotter.save_plot(2, solution_path)

# plot vegan parmesan by timestamps
standard_plotter.clear_plot()
standard_plotter.add_plot(vegan_parmesan['reject_packs'], 'green')
standard_plotter.set_title('All rejected vegan parmesan packages by time')
standard_plotter.set_ylabel('rejected packages')
standard_plotter.show()
standard_plotter.save_plot(2, solution_path)

errors_tl = ErrorMessagesTl().df
Utility.convert_to_ts(errors_tl, 'start_ts')
code_1019 = errors_tl.loc[errors_tl['code'] == 1019]

packages = Package_().df
Utility.convert_to_ts(packages, 'timestamp')

recipes = Recipe().df
Utility.convert_to_ts(recipes, 'timestamp')

# join the recipes to the packages and split the result into months
packs_recipes = pd.merge_asof(packages, recipes, left_index=True, right_index=True)
packs_recipes_months = Utility.spit_into_months(packs_recipes)

# join the errors with code 1019 to the merged packages with its recipes
errors_packs_recipes = pd.merge_asof(errors_tl, packs_recipes, left_index=True, right_index=True)
filtered_epc = errors_packs_recipes.loc[errors_packs_recipes['code'] == 1019]
filtered_epc_month = Utility.spit_into_months(filtered_epc)

res = []
months = []

for i in range(len(packs_recipes_months)):
    # get the specific name of the month from timestamp
    months.append(Utility.get_month_name(packs_recipes_months[i]))
    # group all good packages by its recipe
    recipe_good_packs = packs_recipes_months[i].groupby('recipe')['good_packs'].sum().rename('good_packs_count')
    # group all rejected packages by its recipe
    recipe_reject_packs = packs_recipes_months[i].groupby('recipe')['reject_packs'].sum().rename('reject_packs_count')
    # group all errors by its recipe
    recipe_errors = filtered_epc_month[i].groupby('recipe').size().rename('error_1019_count')
    # merge everything together
    cor = pd.concat([recipe_errors, recipe_good_packs, recipe_reject_packs], axis=1)
    cor.fillna(0, inplace=True)
    res.append(cor)
    print(cor.head())

# plot every product by month and with its produced packages and the errors
sp = IoTStandardPlotter()
sp = process_data_and_plot(res, 'vegan cheese sticks', months, sp)
sp.set_title('Vegan cheese sticks')
sp.set_ylabel('Amount')
sp.show()
sp.save_plot(use_case_num, solution_path)
sp.clear_plot()
sp = process_data_and_plot(res, 'vegan parmesan', months, sp)
sp.set_title('Vegan parmesan')
sp.set_ylabel('Amount')
sp.show()
sp.save_plot(use_case_num, solution_path)
sp.clear_plot()
sp = process_data_and_plot(res, 'vegan hero 150g', months, sp)
sp.set_title('Vegan hero 150g')
sp.set_ylabel('Amount')
sp.show()
sp.save_plot(use_case_num, solution_path)
