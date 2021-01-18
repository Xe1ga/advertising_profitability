from django.db import models


class Orders(models.Model):
    order_id = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    affiliate_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'orders'


class Statistic(models.Model):
    date = models.DateField()
    clicks_uniq = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'statistic'
