import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from analytics.models import SalesData

class Command(BaseCommand):
    help = 'Import Superstore CSV data'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        SalesData.objects.all().delete()
        rows = []
        with open(options['csv_file'], encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(SalesData(
                    row_id=int(r['Row ID']),
                    order_id=r['Order ID'],
                    order_date=datetime.strptime(r['Order Date'], '%m/%d/%Y').date(),
                    ship_date=datetime.strptime(r['Ship Date'], '%m/%d/%Y').date(),
                    ship_mode=r['Ship Mode'],
                    customer_id=r['Customer ID'],
                    customer_name=r['Customer Name'],
                    segment=r['Segment'],
                    country=r['Country/Region'],
                    city=r['City'],
                    state=r['State/Province'],
                    postal_code=str(r['Postal Code']),
                    region=r['Region'],
                    product_id=r['Product ID'],
                    category=r['Category'],
                    sub_category=r['Sub-Category'],
                    product_name=r['Product Name'],
                    sales=float(r['Sales']),
                    quantity=int(r['Quantity']),
                    discount=float(r['Discount']),
                    profit=float(r['Profit']),
                ))
        SalesData.objects.bulk_create(rows, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f'Imported {len(rows)} rows successfully!'))
