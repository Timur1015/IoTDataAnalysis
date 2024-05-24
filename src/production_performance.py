from src.classes.OEE import OEE
from src.classes.ErrorMessagesAcc import ErrorMessagesAcc
from src.classes.Package_ import Package_
import pandas as pd
from src.classes.IoTStandardPlotter import IoTStandardPlotter
from src.classes.Utility import Utility

solution_path = '../solutions'
use_case_num = 1
oee_df = OEE().df
planned_cycles = 10
last_months = 2

cycles = oee_df[['timestamp', 'expected_cycles_per_minute', 'actual_cycles_per_minute']].copy()

# convert to timeseries by setting index and convert timestamps to date format
Utility.convert_to_ts(cycles, 'timestamp')

# get data from last 2 months
filtered_cycles = Utility.filter_by_months(cycles, last_months)

# calculate mean to get the average cycles
avg_actual_cycles = Utility.calc_mean(filtered_cycles['actual_cycles_per_minute'])
avg_expected_cycles = Utility.calc_mean(filtered_cycles['expected_cycles_per_minute'])

# plot
standard_plotter = IoTStandardPlotter()
standard_plotter.add_scatter(filtered_cycles['actual_cycles_per_minute'], 'green')
standard_plotter.add_scatter(filtered_cycles['expected_cycles_per_minute'], 'blue')
standard_plotter.add_hline(avg_actual_cycles, 'green', 'mean')
standard_plotter.add_hline(avg_expected_cycles, 'blue', 'mean')
standard_plotter.add_hline(planned_cycles, 'red', 'planned')
standard_plotter.set_title(
    'Actual vs expected cycles (last months: ' + str(last_months) + ')')
standard_plotter.set_ylabel('Actual cycles / Expected cycles per minute')
standard_plotter.show()
standard_plotter.save_plot(use_case_num, solution_path)

# view each month separately
cycles_months = Utility.spit_into_months(cycles)
for month in cycles_months:
    month_n = Utility.get_month_name(month)
    avg_actual_cycles = Utility.calc_mean(month['actual_cycles_per_minute'])
    avg_expected_cycles = Utility.calc_mean(month['expected_cycles_per_minute'])
    standard_plotter.clear_plot()
    standard_plotter.add_scatter(month['actual_cycles_per_minute'], 'green')
    standard_plotter.add_scatter(month['expected_cycles_per_minute'], 'blue')
    standard_plotter.add_hline(avg_actual_cycles, 'green', 'mean')
    standard_plotter.add_hline(avg_expected_cycles, 'blue', 'mean')
    standard_plotter.add_hline(planned_cycles, 'red', 'planned')
    standard_plotter.set_title(
        'Actual vs expected cycles (' + month_n + ')')
    standard_plotter.set_ylabel('Actual cycles / Expected cycles per minute')
    standard_plotter.show()
    standard_plotter.save_plot(use_case_num, solution_path)

# get error data to see why the actual cycles are not as bad as the planned cycles
errors_acc = ErrorMessagesAcc().df
dead_time = errors_acc[['timestamp', 'accumulated_dead_time', 'identifier']].copy()
# seconds to minutes
dead_time['accumulated_dead_time'] = dead_time['accumulated_dead_time'] / 60
Utility.convert_to_ts(dead_time, 'timestamp')

# get data from last 2 months
dead_time = Utility.filter_by_months(dead_time, last_months)

# merge data and scale properly
oee_and_errors = pd.merge_asof(dead_time, filtered_cycles, left_index=True, right_index=True)

# plot
standard_plotter.clear_plot()
standard_plotter.add_scatter(oee_and_errors['actual_cycles_per_minute'], 'green')
standard_plotter.add_scatter(oee_and_errors['expected_cycles_per_minute'], 'blue')
standard_plotter.add_plot(oee_and_errors['accumulated_dead_time'], 'red')
standard_plotter.set_title('Cycles per minute & Dead time')
standard_plotter.set_ylabel('Actual cycles / Expected cycles per minute / Accumulated dead time (min)')
standard_plotter.show()
standard_plotter.save_plot(use_case_num, solution_path)

# Amount of produced packages
package_df = Package_().df
packages = package_df[['timestamp', 'good_packs', 'reject_packs']].copy()

# convert to timeseries by setting index and convert timestamps to date format
Utility.convert_to_ts(packages, 'timestamp')

# split into months
package_months = Utility.spit_into_months(packages)
months = []
good_packs = []
reject_packs = []
for month in package_months:
    months.append(Utility.get_month_name(month))
    good_packs.append(month['good_packs'].sum())
    reject_packs.append(month['reject_packs'].sum())
standard_plotter = IoTStandardPlotter()
standard_plotter.add_bar(good_packs, months, 'green', 'Good Packs', None)
standard_plotter.add_bar(reject_packs, months, 'red', 'Reject Packs', good_packs)
standard_plotter.set_title('Amount of packages per month')
standard_plotter.set_ylabel('produced packages')
standard_plotter.show()
standard_plotter.save_plot(use_case_num, solution_path)
