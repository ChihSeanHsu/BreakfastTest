from django.test import TestCase
from .views import ReportView

# Create your tests here.
class DataInitMixin:
    fixtures = ['init_data.json']

class TestShipping(DataInitMixin, TestCase):

    def test_shipping_rate(self):
        shipping_rate = ReportView.get_shipping_rate()
        self.assertIsInstance(shipping_rate, list)
        self.assertEqual(shipping_rate[0]['value'], 10)


class TestTopThree(DataInitMixin, TestCase):
    
    def test_get_product_sum(self):
        product_sum = ReportView.get_product_sum()
        self.assertIsInstance(product_sum, dict)
        product_list = [
            '[Aronia] 有機野櫻莓果醬(無添加糖) (225g/罐)',
            '[137 degrees] 咖啡拿鐵杏仁堅果奶 (180ml/罐) {賞味期限: 2018-10-05}',
            '[澳思] 初榨椰子油 (650ml/罐) {賞味期限: 2019-08-23}'
        ]
        qty_list = [
            53,
            19,
            18
        ]
        for idx, (product, qty) in enumerate(zip(product_list, qty_list)):
            self.assertEqual(product_sum['name'][idx], product)
            self.assertEqual(product_sum['value'][idx], qty)


class TestCohort(DataInitMixin, TestCase):
    
    def test_cohort(self):
        cohort = ReportView.get_cohort()
        row1 = [27.0, 15.0, 15.0, 12.0, 10.0, 8.0, 7.0, 5.0, 5.0, 4.0, 4.0, 4.0, 3.0, 2.0, 1.0]

        self.assertIsInstance(cohort, dict)
        self.assertIn('value', cohort)
        self.assertEqual(cohort['value'][-1], row1)

class TestReportView(DataInitMixin, TestCase):

    def test_report(self):
        res = self.client.get('/report/')
        self.assertTemplateUsed(res, 'report/index.html')
        self.assertIn('[Aronia] 有機野櫻莓果醬(無添加糖) (225g/罐)', res.content.decode('utf8'))
        self.assertIn('barChart', res.content.decode('utf8'))
        self.assertIn('productTable', res.content.decode('utf8'))
        self.assertIn('cohortChart', res.content.decode('utf8'))

        