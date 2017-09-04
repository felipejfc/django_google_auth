from setuptools import setup, find_packages

setup(
    name='django-google-auth',
    version=__import__('google-auth').__version__,
    description=__import__('google-auth').__doc__,
    long_description=open('README.md').read(),
    author='Felipe Cavalcanti',
    author_email='fjfcavalcanti@gmail.com',
    url='https://github.com/felipejfc/django-google-auth',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Development Status :: Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
