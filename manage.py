#!/usr/bin/env python
import os
import sys
import warnings

if __name__ == "__main__":  # pragma: no cover
    warnings.filterwarnings("default", category=DeprecationWarning)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    params = list(sys.argv)
    if len(params) >= 2 and params[1] == "makemessages":
        params.extend(("-i", "node_modules", "-i", "static", "-i", "coverage", "-i", "dynamicforms_legacy"))
        params.extend(("-i", "tests", "-i", "setup", "-i", "examples", "-i", "dynamicforms_dev", "-i", "dist"))
        print("Modified makemessages: will process both django and djangojs domains")
        execute_from_command_line(params + ["-d", "djangojs", "-e", "js,ts,vue"])

    execute_from_command_line(params)
