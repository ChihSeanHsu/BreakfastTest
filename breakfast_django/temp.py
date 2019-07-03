#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 23:33:39 2019

@author: Sean
"""

import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('./db.sqlite3')
order_df = pd.read_sql('SELECT *, date(created_at) date FROM "order";', conn)

order_df = order_df.drop('created_at', axis=1)

date_group = order_df.groupby('date')

group_num = len(date_group)
cohort_array = np.zeros([group_num, group_num])

for idx_row, (group_row, df_row) in enumerate(date_group):
    customer_set_row = set(df_row['customer_id'])
    idx_col = 0
    
    for idx, (group_col, df_col) in enumerate(date_group):
        if idx_col >= group_num or idx < idx_row:
            continue
        customer_set_col = set(df_col['customer_id'])
        return_cus =  customer_set_col & customer_set_row
        cohort_array[idx_row][idx_col] = len(return_cus)
        idx_col += 1

total = []
for i in range(group_num):
    total.append(sum(cohort_array[:, i]))
             

