import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Item

class Command(BaseCommand):
    help = 'Imports products from JSON file into database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as file:
            products = json.load(file)
            
            for product in products:
                Item.objects.create(
                    item_name=product['item_name'],
                    item_price=product['item_price'],
                    item_description=product['item_description'],
                    item_image=product['item_image'],
                    item_brand=product['item_brand'],
                    item_type=product['item_type'],
                    item_quantity=product['item_quantity'],
                    created_at=timezone.now()
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} products'))