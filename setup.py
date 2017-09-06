from setuptools import setup, find_packages

setup(
    name='django-google-auth',
    version=__import__('google_auth').__version__,
    description=__import__('google_auth').__doc__,
    long_description=open('README.md').read(),
    author='Felipe Cavalcanti',
    author_email='fjfcavalcanti@gmail.com',
    url='https://github.com/felipejfc/django-google-auth',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'oauth2client>=4.1.2',
        'requests>=2.18.4',
        'djangorestframework>=3.0.1',
        ],
    include_package_data=True,
    zip_safe=False,
)
