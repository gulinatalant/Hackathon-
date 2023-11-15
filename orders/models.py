from django.db import models
from django.contrib.auth import get_user_model
from events.models import Events
import uuid

User = get_user_model()


class Order(models.Model):
    event  = models.ManyToManyField(Events, through='OrderItem')
    order_number = models.CharField(max_length=100,unique=True, default=uuid.uuid4, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'event: {self.event}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='items')
    event = models.ForeignKey(Events, on_delete=models.RESTRICT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'order_items'
