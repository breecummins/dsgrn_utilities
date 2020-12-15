from distutils.core import setup

setup(
    name='dsgrn_utilities',
    package_dir={'':'src'},
    packages = ['dsgrn_utilities'],
    install_requires=["networkx","DSGRN"],
    author="Bree Cummins",
    url='https://github.com/breecummins/dsgrn_utilities'
    )