from setuptools import setup, find_packages

setup(
    name='adfmapping',
    version='0.1.2',
    author='Gaurav Lotekar',
    author_email='gauravnlotekar@gmail.com',
    url='https://github.com/gogi2811/adfmapping',
    keywords='Azure ADF mapping ADF mapping JSON json',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=['adfmapping'],
    install_requires=[
        'Click',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'adfmapping = adfmapping:get_dynamic_mapping',
        ],
    },
)