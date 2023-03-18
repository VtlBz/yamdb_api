from django.core.management.base import BaseCommand

from reviews.management.commands import _fillyamdb_main
from reviews.management.commands import _fillyamdb_input_config as conf


class Command(BaseCommand):
    help = 'Creating model objects according the file folder path specified'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            type=str,
            help='Defines the path to folder with imported files',
            default=conf.DEFAULT_PATH
        )

    def handle(self, *args, **options):
        _fillyamdb_main.confirmation()
        _fillyamdb_main.run(options['p'])
        print('Complete!')
