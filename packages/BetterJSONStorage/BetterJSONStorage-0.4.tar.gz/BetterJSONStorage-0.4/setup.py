from setuptools import setup, find_packages

setup(
    name='BetterJSONStorage',
    version='0.4',
    license='MIT',
    author="Thomas Eeckout",
    author_email='thomas.eeckout@outlook.be',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='tinyDB python orjson compressed database',
    install_requires=[
          'orjson',
          'blosc'
      ],
)