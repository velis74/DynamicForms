#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys

from pathlib import Path


def write_ver_to_init(file_name, version, search, replacement):
    with open(file_name, "r") as file:
        content = file.read()
    content = re.sub(f"^{search}.*", replacement, content, flags=re.MULTILINE)
    with open(file_name, "w") as file:
        file.write(content)


def get_version(version_arg):
    if not re.match(r"^\d+\.\d+\.\d+$", version_arg):
        raise ValueError("Invalid version format. Should be x.y.z (all numbers)")
    return version_arg


def sync_requirements(requirements_file="requirements.txt", pyproject_file="pyproject.toml"):
    if not Path(requirements_file).exists():
        raise FileNotFoundError(f"Requirements file '{requirements_file}' not found.")

    with open(requirements_file, "r") as f:
        requirements = "".join(
            (f'\n    "{line.strip()}",' for line in f if line.strip() and not line.strip().startswith("#"))
        )

    with open(pyproject_file, "r") as f:
        content = f.read()

    dependencies_start = content.index("dependencies = [")
    dependencies_end = content.index("]", dependencies_start) + 1

    before_dependencies = content[: dependencies_start + len("dependencies = [")]
    after_dependencies = content[dependencies_end + 1 :]

    new_content = f"{before_dependencies}{requirements}\n]\n{after_dependencies}"

    with open(pyproject_file, "w") as f:
        f.writelines(new_content)

    print(f"Updated dependencies in {pyproject_file} with requirements from {requirements_file}")


def main():
    parser = argparse.ArgumentParser(description="Publish script for DynamicForms")
    parser.add_argument("version", help="Version to publish (format: x.y.z)")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    args = parser.parse_args()

    def run_command(command, dry_run=args.dry_run, cwd=None):
        if dry_run:
            print(f"[DRY RUN] Would run: {' '.join(command)}")
        else:
            subprocess.run(command, check=True, cwd=cwd)

    try:
        version = get_version(args.version)
    except ValueError as e:
        print(str(e))
        sys.exit(1)

    run_command("pip install -U setuptools wheel twine build pkginfo".split(" "))

    sync_requirements()

    files_to_update = [
        ("dynamicforms/__init__.py", "__version__", f"__version__ = '{version}'"),
        ("vue/dynamicforms/package.json", '  "version":', f'  "version": "{version}",'),
        ("pyproject.toml", "version =", f'version = "{version}"'),
    ]

    for file_name, search, replacement in files_to_update:
        write_ver_to_init(file_name, version, search, replacement)

    run_command(["git", "add", "pyproject.toml", "dynamicforms/__init__.py", "vue/dynamicforms/package.json"])
    run_command(["git", "commit", "-m", f"Bump version to {version}"])

    run_command(["tox", "-e", "check"])
    run_command(["npm", "run", "test"])

    run_command(["npm", "run", "build"], dry_run=False)
    run_command(["npm", "publish"], cwd="vue/dynamicforms")
    run_command(["python", "-m", "build"], dry_run=False)
    run_command(["twine", "upload", "dist/*"])

    for dir_to_remove in ["build", "dist", "DynamicForms.egg-info"]:
        if os.path.exists(dir_to_remove):
            subprocess.run(["rm", "-rf", dir_to_remove])

    if not args.dry_run:
        run_command(["git", "tag", "-a", version, "-m", f"version {version}"])
        run_command(["git", "push", "origin", "main"])
        run_command(["git", "push", "--tags"])

    print("Build and publish process completed successfully!")
    if args.dry_run:
        print("This was a dry run. No actual changes were made or packages published.")


if __name__ == "__main__":
    main()
