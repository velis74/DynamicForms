import os
import subprocess
from argparse import ArgumentParser

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate Field classes from DRF with applied DynamicForms mixins'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('command', type=str, default='serve', action='store', nargs='?',
                            help='command to run, e.g. "build" or "serve". default: "serve"')

    def handle(self, *args, **options):
        cmd = options.get('command')
        pth = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', '..', '..'))
        pth = os.path.join(pth, 'dynamicforms', 'df-vue-components')
        p = subprocess.Popen(['npm', 'run', cmd], cwd=pth)
        p.wait()
