from django.core.management.base import BaseCommand, CommandError

from pathlib import Path


class Command(BaseCommand):
    help = "Creates test products"

    def handle(self, *args, **options):
        path = Path(__file__).resolve().parent / 'products.json'

