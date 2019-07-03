from django.db.models import Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView

import pandas as pd
import numpy as np

from .models import Order, OrderItem

# Create your views here.
class ReportView(TemplateView):
    template_name = 'report/index.html'

    def get(self, request, *args, **kwargs):
        content = {
            'shipping_rate': self.get_shipping_rate(),
            'product_sum': self.get_product_sum(),
            'cohort': self.get_cohort()
        }

        return render(request, self.template_name, content)

    @staticmethod
    def get_shipping_rate() -> (list):
        '''
        output: [
            { 'name': str, 'value': int },
            ...
        ]
        '''
        shipping_count = Order.objects.values('shipping').annotate(count=Count('order_id'))
        shipping_data = []
        for item in shipping_count:
            shipping_data.append({ 'name':  str(item['shipping']) + '元', 'value': item['count']})

        return shipping_data

    @staticmethod
    def get_product_sum() -> (list):
        '''
        output: {
            'name': [str, ...],
            'value': [int, ...]
        }
        '''
        product_group_by = OrderItem.objects.values('product_name').annotate(sum=Sum('qty')).order_by('-sum')

        group_data = {
            'name': [],
            'value': []
        }
        for item in product_group_by:
            group_data['name'].append(item['product_name'])
            group_data['value'].append(item['sum'])
        return group_data

    @staticmethod
    def get_cohort() -> (dict):
        '''
        output: {
            'index': [str, ...],
            'value': [list, ...]
        }
        '''
        order_df = pd.DataFrame(list(Order.objects.values()))
        order_df['date'] = order_df['created_at'].apply(lambda x: x.date)
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
        
        index = ['Total', *list(date.strftime('%Y-%m-%d')  for date in date_group.groups.keys())]
        value = [total, *cohort_array.tolist()]
        index.reverse()
        value.reverse()
        cohort_data = {
            'index': index,
            'value': value
        }

        return cohort_data
