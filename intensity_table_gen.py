import rm_est
import numpy as np
import pandas as pd
# itemgetter returns the dictionary values of multiple keys
from operator import itemgetter

# generate the first row of an intensity chart (always RPE 10.0) using the rep range in "reps_to_map"
# the use_method arg can accept a tuple of multiple methods
def first_row_gen(base_weight = 150, reps_to_map = 12, use_method='Average'):
    # arbritrary values can be used as seed set for RM estimate calculations
    # but will change intensity values slightly, can be adjusted depending on exercise
    # true PR set recommended
    reps_to_estimate = 1
    first_row = dict()

    for rep_value in reps_to_map:
        # add the intensity (estimated percentage of max lift) to the first row
        first_row.setdefault(rep_value, base_weight / rm_est.blind_r_rm((base_weight, rep_value), reps_to_estimate, use_method=use_method, return_set=False))

    return first_row

# generate each of "other" (non-first) rows with whole RPE values (9.0, 8.0, etc)
def whole_row_diag_gen(first_row, reps_to_map, rpes_to_map):
    # initialize data table
    whole_row_diag_table = list()
    # add first row to table
    whole_row_diag_table.append(first_row)
    # find all non-first rows that correspond to a whole RPE value (e.g. 9, 8, 7, etc)
    non_max_whole_rpe_rows = ((row_num, rpe) for (row_num, rpe) in enumerate(reversed(rpes_to_map)) if (rpe.is_integer()) and (rpe < max(rpes_to_map)))
    # separate the whole row numbers from the corresponding whole rpe values
    non_max_whole_rows, non_max_whole_rpes = zip(*non_max_whole_rpe_rows)

    # generate table diagonals
    for counter, non_max_whole_row in enumerate(non_max_whole_rows):
        # step through a count of the whole rows
        # e.g. 2 <> RPE 9.0, 3 <> RPE 8.0, etc
        whole_row_count = counter + non_max_whole_rows[0]
        # the lookup keys are offset by the whole row count
        # e.g. whole row 2 (RPE 9.0) includes values from column 2 (reps = 2) of the first row onward
        lookup_keys = tuple(range(whole_row_count, len(reps_to_map)+1))
        # the values pulled from the first row will always be inserted at column 1
        store_keys = tuple(range(1, len(lookup_keys)+1))
        # pull values corresponding to each lookup key
        offset_values = itemgetter(*lookup_keys)(first_row)
        # associate appropriate row keys with the values pulled from the first row
        offset_items = dict(zip(store_keys, offset_values))
        # insert offset data at the specified row location
        whole_row_diag_table.insert(non_max_whole_row, offset_items)
        
    # print(pd.DataFrame(whole_row_table, index = (max(rpes_to_map), *non_max_whole_rpes)))

    return whole_row_diag_table

# fill in missing values in whole row table
# uses extrapolation / "dead reckoning"
# e.g. filling = anchor_value + norm_factor*(anchor_value - step_value) where norm_factor = (filling_col - anchor_col) / (anchor_col - step_col)
# e.g. norm_factor = (12 - 10) / (10 - 9)
def whole_row_filler(whole_row_diag_table, reps_to_map):
    # find number of columns
    columns = len(reps_to_map)
    # skipping the first row, step through the table rows

    for row in range(1, len(whole_row_diag_table)):
        # find columns needing filling
        columns_to_fill = range(columns + 1 - row, columns + 1)

        for column in columns_to_fill:
            # calculate normalization factor
            norm_factor = (reps_to_map[column-1] - reps_to_map[column-2]) / (reps_to_map[column-2] - reps_to_map[column-3])
            # find anchor value
            anchor_value = whole_row_diag_table[row][reps_to_map[column-2]]
            # find step value
            step_value = whole_row_diag_table[row][reps_to_map[column-3]]
            # calculate the filler value
            filling = anchor_value + norm_factor*(anchor_value - step_value)
            # fill table with filler value
            whole_row_diag_table[row].setdefault(column, filling)

    # return with filler values added
    return whole_row_diag_table

# generate intermediate RPE rows (9.5, 8.5, etc)
def inter_row_gen(whole_row_table, reps_to_map, rpes_to_map):
    # find all rows that correspond to intermediate RPE values (e.g. 9.5, 8.5, etc)
    inter_rpe_rows = tuple(((row_num, rpe) for (row_num, rpe) in enumerate(reversed(rpes_to_map)) if not(rpe.is_integer())))
    # separate the intermediate row numbers from the corresponding intermediate rpe values
    inter_rows, inter_rpes = zip(*inter_rpe_rows)

    # check if the smallest RPE to map is a whole number
    # if so, the values of the last intermediate row can be found with interpolation between the rows above and below
    if min(rpes_to_map).is_integer():
        # calculate intermediate values for all intermediate rows
        for inter_row in inter_rows:
            # pull values from the row above
            above_values = tuple(whole_row_table[inter_row - 1].values())
            # pull values from the row below
            below_values = tuple(whole_row_table[inter_row].values())
            # calculate intermediate row values
            inter_values = np.mean((above_values, below_values), axis=0)
            # associate row keys with the intermediate values
            inter_items = dict(zip(reps_to_map, inter_values))
            # insert intermediate row at specified location
            whole_row_table.insert(inter_row, inter_items)
    
    # if not, the values of the final row (which is an intermediate row) must be found with extrapolation
    else:
        # calculate intermediate values for all but the last intermediate row
        for inter_row in inter_rows[:-1]:
            # pull values from the row above
            above_values = tuple(whole_row_table[inter_row - 1].values())
            # pull values from the row below
            below_values = tuple(whole_row_table[inter_row].values())
            # calculate intermediate row values
            inter_values = np.mean((above_values, below_values), axis=0)
            # associate row keys with the intermediate values
            inter_items = dict(zip(reps_to_map, inter_values))
            # insert intermediate row at specified location
            whole_row_table.insert(inter_row, inter_items)

        # calculate the values of the last intermediate row using extrapolation
        # e.g. last_inter_values = 2*anchor_row_values - step_row_values
        # find anchor row values
        anchor_row_values = np.asarray(tuple(whole_row_table[inter_rows[-1] - 1].values()))
        # find step value
        step_row_values = np.asarray(tuple(whole_row_table[inter_rows[-1] - 2].values()))
        # calculate the last intermediate row values
        last_inter_values = tuple(2*anchor_row_values - step_row_values)
        # associate row keys with last intermediate row values
        last_inter_items = dict(zip(reps_to_map, last_inter_values))
        # insert last intermediate row at specified location
        whole_row_table.insert(inter_rows[-1], last_inter_items)

    # return with intermediate values added
    return whole_row_table

# generates an intensity table and copies it the the clipboard
def generate_intensity_table(base_weight = 150, rep_num = 12, rpe_min = 6.5, rpe_increment = 0.5, use_method = 'Average'):
    """Generate an intensity table where each row corresponds to a RPE (rate of perceived exhaustion)
    and each column maps to the number of reps completed.
    
    Inputs -
        - base_weight: a seed weight used to generate the intensity table (default = 150).
            - the default can be used, but a true PR weight (regardless of rep count) should be used for better prediction accuracy.
        - rep_num: the max repetions represented in the table, integer (default = 12)
        - rpe_min: the minimum RPE represented in the table (default = 6.5)
        - rpe_increment: the increment between RPE levels represented in the table
        - use_method: the intensity / one rep max calculation method to use (default = 'Average')
            - available methods: 'Average', 'Bryzcki', 'Epley', 'Lander', 'Lombardi', 'Mayhew', 'OConner', 'Wathan'
    
    Output -
        - a dataframe containing the intensities as percentages
            - index name: 'Rate of Perceived Exhaustion (RPE)'
            - column prefix = 'Reps Completed: '"""

    # generate tuple of reps_to_map
    reps_to_map = tuple(range(1, rep_num + 1))
    # generate tuple RPE values to map
    rpes_to_map = tuple(rpe_min + rpe_count*rpe_increment for rpe_count in range(0, int((10-rpe_min)/rpe_increment) + 1))

    # generate first row using 'Average' RM estimate method
    first_row = first_row_gen(base_weight, reps_to_map, use_method=use_method)

    # generate data table of all unfilled whole RPE (10.0, 9.0, 8.0, etc) rows 
    whole_row_diag_table = whole_row_diag_gen(first_row, reps_to_map, rpes_to_map)

    # fills unfilled whole RPE (9.0, 8.0, etc) rows
    whole_row_table = whole_row_filler(whole_row_diag_table, reps_to_map)

    # generate data table of all (10.0, 9.5, 8.0, etc) rows
    intensity_table = inter_row_gen(whole_row_table, reps_to_map, rpes_to_map)

    # store intensity table as data frame and copy to clipboard
    df = pd.DataFrame(intensity_table, index = tuple(reversed(rpes_to_map)))
    # df.index.name = index_name
    # columns = ('{}: {}'.format(column_name_prefix, column_name) for column_name in df.columns)
    # df.columns = columns
    return df

if __name__ == "__main__":
    # simply copy the intesity table to the clipboard for verification and further manipulation in Excel
    # TODO
    # implement tool as flask & react.js web app
    weight_pr = 135
    intensity_df = generate_intensity_table(base_weight=weight_pr)
    intensity_df.to_clipboard(excel=True)