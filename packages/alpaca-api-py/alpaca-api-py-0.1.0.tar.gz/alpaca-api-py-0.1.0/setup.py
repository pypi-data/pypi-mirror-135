from setuptools import setup

setup(
    name='alpaca-api-py',
    version='0.1.0',
    description='Alpaca API interface',
    url='https://github.com/shuds13/pyexample',
    author='Kekoa Yamaguchi',
    author_email='example@email.com',
    license='BSD 2-clause',
    packages=['alpaca_api'],
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      'requests',
                      'pandas'
                      ],
)
