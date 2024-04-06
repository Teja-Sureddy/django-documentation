from django.db import models


class Invoice(models.Model):
    sender_name = models.CharField(max_length=150)
    sender_address_line1 = models.CharField(max_length=150)
    sender_address_line2 = models.CharField(max_length=150, blank=True, null=True)
    sender_country = models.CharField(max_length=150)

    invoice_number = models.CharField(max_length=50)
    order_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipient_name = models.CharField(max_length=150)
    recipient_address_line1 = models.CharField(max_length=150)
    recipient_address_line2 = models.CharField(max_length=150, blank=True, null=True)
    recipient_country = models.CharField(max_length=150)
    recipient_phone = models.CharField(max_length=20)

    shipping_type = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.invoice_number} - {self.order_number}'


class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
