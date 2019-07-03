from django.db import models

# Create your models here.
class Order(models.Model):

    order_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    shipping = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        indexes = [
            models.Index(fields=['customer_id'])
        ]


class OrderItem(models.Model):

    order_id = models.ForeignKey(Order, models.CASCADE)
    product_name = models.CharField(max_length=100)
    qty = models.IntegerField()

    class Meta:
        db_table = 'order_item'
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['product_name'])
        ]