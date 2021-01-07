"""SNaP OneDrive Report Aggregator

# Running
1. Replace onedrive_dir_path with your path
2. Run Python script

# Troubleshooting problems
1. "Permission denied"
Solution: Make sure the OneDrive program is running on your computer.

"""
import os
import pandas as pd
import re

from datetime import datetime
from openpyxl import load_workbook
from typing import List


# Necessary config options
onedrive_dir_path = '/Users/joeflack4/OneDrive/'

# Optional config options
input_dir_regexp = 'SNAP_TAM_[0-9]{3}'
worksheet_name = 'Data Entry Log'
duration_colnames = ['Duration', 'Total Interaction Duration']
output_dirname = 'SNAP_TAM_Aggregated'
print_progress = False

# Other variables
valid_extensions = ['.xls', '.xlsx', '.xlsm']
output_path = os.path.join(onedrive_dir_path, output_dirname)


def run():
    """Run"""
    onedrive_root_contents: List[str] = os.listdir(onedrive_dir_path)
    snap_dirs: List[str] = [
        os.path.join(onedrive_dir_path, x) for x in onedrive_root_contents
        if re.match(input_dir_regexp, x)]

    snap_files: List[str] = []
    for folder in snap_dirs:
        candidates = [
            y for y in os.listdir(folder)
            if any([y.endswith(ext) for ext in valid_extensions])]
        for candidate in candidates:
            path = os.path.join(folder, candidate)
            snap_files.append(path)

    # Enable permission to read (may not be necessary)
    workbooks = {}
    for file in snap_files:
        os.chmod(file, 0o777)
        wb = load_workbook(filename=file, read_only=True)
        workbooks[file] = wb

    worksheets = {}
    for file, wb in workbooks.items():
        ws = wb[worksheet_name]
        worksheets[file] = ws

    headers: List[str] = None
    duration_col_indices = []
    data: List[List] = []
    n_worksheets = len(worksheets)
    ws_num = 0
    for _, ws in worksheets.items():
        row_num = 0
        ws_num += 1
        if print_progress:
            print(
                'Processing file ' + str(ws_num) + ' of ' + str(n_worksheets))

        for row in ws:
            row_num += 1
            if not any(cell.value for cell in row):
                break
            row_vals = [cell.value for cell in row]
            n_cols = len(row_vals)
            if row_num == 1:
                if ws_num > 1:
                    continue
                headers = row_vals
                # identify 'duration' cols for empty test
                for i in range(n_cols):
                    if headers[i] in duration_colnames:
                        duration_col_indices.append(i)
                continue
            # check if row is 'effectively' empty
            is_empty_row = False
            if not row_vals[0]:
                for i in range(n_cols):
                    if i in duration_col_indices and \
                            row_vals[i] not in [None, 0]:
                        is_empty_row = True
                        break
                    if row_vals[i]:
                        is_empty_row = True
                        break
            if is_empty_row:
                break
            data.append(row_vals)

    df = pd.DataFrame(data, columns=headers)
    filename = (str(datetime.now()) + '.csv').replace(':', '-')
    outpath = os.path.join(output_path, filename)
    df.to_csv(outpath, index=False)
    if print_progress:
        print('Done')


if __name__ == '__main__':
    run()
