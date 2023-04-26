import argparse
import os
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate Field classes from DRF with applied DynamicForms mixins"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "command",
            type=str,
            default="serve",
            action="store",
            nargs="?",
            help='command to run, e.g. "build" or "serve". default: "serve"',
        )
        parser.add_argument("cmd_params", nargs=argparse.REMAINDER)

    def handle(self, *args, **options):
        cmd = options.get("command")
        pth = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        pth = os.path.join(pth, "dynamicforms", "vue")
        print(["npm", "run", cmd] + options.get("cmd_params"))
        p = subprocess.Popen(["npm", "run", cmd] + options.get("cmd_params"), cwd=pth)
        p.wait()
