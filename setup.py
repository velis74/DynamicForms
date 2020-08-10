import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()
with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="DynamicForms",
    version="0.9.22",
    author="Jure Erznožnik",
    author_email="jure@velis.si",
    description="DynamicForms performs all the visualisation & data entry of your DRF Serializers & ViewSets and adds "
                "some candy of its own: It is a django library that gives you the power of dynamically-shown form "
                "fields, auto-filled default values, dynamic record loading and similar candy with little effort. "
                "To put it differently: once defined, a particular ViewSet / Serializer can be rendered in multiple "
                "ways allowing you to perform viewing and authoring operations on the data in question.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/velis74/DynamicForms",
    packages=setuptools.find_packages(include=('dynamicforms',)),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.4',
    license='BSD-3-Clause',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)
