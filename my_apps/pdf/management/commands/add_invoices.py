from django.core.management.base import BaseCommand
from my_apps.pdf.models import Invoice, Item


class Command(BaseCommand):
    help = 'Inserts dummy Invoices'

    def handle(self, *args, **options):
        data = [
            {
                'invoice': {
                    'sender_name': 'HomeStore', 'sender_address_line1': '6162 Honey Bluff Parkway',
                    'sender_address_line2': 'Calder, Michigan, 34567-8912', 'sender_country': 'United States',
                    'invoice_number': '000000006', 'order_number': '110000000006',
                    'recipient_name': 'Veronica Costello', 'recipient_address_line1': '6162 Honey Bluff Parkway',
                    'recipient_address_line2': 'Calder, Michigan, 34567-8912', 'recipient_country': 'United States',
                    'recipient_phone': '(555) 321-4567', 'shipping_type': 'Flat Rate - Fixed',
                    'payment_type': 'Check / Money order'
                },
                'items': [
                    {'name': 'Clamber Watch', 'sku': '24-WG03', 'quantity': 2, 'price': 100, 'discount': 10},
                    {'name': 'Olivia 1/4 Zip Light Jacket', 'sku': 'WJ12-M-Purple', 'quantity': 1, 'price': 77,
                     'discount': 8},
                    {'name': 'Rival Field Messenger', 'sku': '24-MB06', 'quantity': 1, 'price': 145, 'discount': 7}
                ]
            },
            {
                'invoice': {
                    'sender_name': 'ElectroGadgets', 'sender_address_line1': '1234 Tech Avenue',
                    'sender_address_line2': 'Silicon Valley, California, 90210', 'sender_country': 'United States',
                    'invoice_number': '000000007', 'order_number': '110000000007',
                    'recipient_name': 'John Doe', 'recipient_address_line1': '5678 Main Street',
                    'recipient_address_line2': 'Anytown, Texas, 76543', 'recipient_country': 'United States',
                    'recipient_phone': '(123) 456-7890', 'shipping_type': 'Express Delivery',
                    'payment_type': 'Credit Card'
                },
                'items': [
                    {'name': 'Smartphone X', 'sku': 'SGP-X123', 'quantity': 1, 'price': 899},
                    {'name': 'Wireless Earbuds', 'sku': 'WB-456', 'quantity': 2, 'price': 79, 'discount': 5},
                    {'name': 'Portable Power Bank', 'sku': 'PB-789', 'quantity': 1, 'price': 49},
                    {'name': 'Classic Black Dress', 'sku': 'DRESS-CB001', 'quantity': 1, 'price': 150},
                    {'name': 'Leather Handbag', 'sku': 'HB-LTH123', 'quantity': 1, 'price': 200, 'discount': 10},
                    {'name': 'Stylish Sunglasses', 'sku': 'SG-XY456', 'quantity': 1, 'price': 50}
                ]
            },
            {
                'invoice': {
                    'sender_name': 'BookEmporium', 'sender_address_line1': '9876 Library Lane',
                    'sender_address_line2': 'Booktown, New York, 54321', 'sender_country': 'United States',
                    'invoice_number': '000000008', 'order_number': '110000000008',
                    'recipient_name': 'Alice Smith', 'recipient_address_line1': '4321 Reading Road',
                    'recipient_address_line2': 'Novelville, Florida, 87654', 'recipient_country': 'United States',
                    'recipient_phone': '(987) 654-3210', 'shipping_type': 'Standard Shipping',
                    'payment_type': 'PayPal'
                },
                'items': [
                    {'name': 'The Great Gatsby', 'sku': 'BK-TGG01', 'quantity': 3, 'price': 12},
                ]
            }
        ]

        for obj in data:
            invoice = Invoice.objects.create(**obj['invoice'])
            for item in obj['items']:
                Item(**item, invoice=invoice).save()

        self.stdout.write(self.style.SUCCESS('Successfully inserted invoice data.'))
