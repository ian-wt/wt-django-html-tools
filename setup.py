from setuptools import setup, find_packages


setup(
    name='wt-django-html-tools',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'django>=4.0',
        'bleach>=6.0',
        'bs4'
    ],
    python_requires=">=3.8"
)
