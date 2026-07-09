#!/usr/bin/env python3

from datetime import datetime
import os
from pathlib import Path
import sys


def get_user_data_dir_1():
    columns = ['id', 'value', 'iu/ml', 'log', 'result_type', 'created at']
    frow = ''
    for c in columns:
        if c == columns[len(columns) - 1]:
            frow = frow + c
        else:
            frow = frow + c + ' , '
    print(frow)
    path = os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'ViralLoadCalculator') + f'/{str(datetime.now().date())}.csv'
    p = Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        f.write(frow)
    return {
        'platform': sys.platform,
        'user_data_dir': os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'ViralLoadCalculator')
    }

print(get_user_data_dir_1())