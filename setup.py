from setuptools import setup, find_packages

setup(
    name='covid19norway',
    version='1.0.4',
    description='',
    long_description=open('README.md').read().strip(),
    author='Jens Markussen',
    author_email='jens.markussen@knowit.no',
    packages=find_packages(),
    license='MIT License',
    install_requires=[
        'requests', 'pandas', 'numpy'],
    zip_safe=False)
