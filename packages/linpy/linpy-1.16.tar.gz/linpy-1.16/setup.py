from setuptools import setup, find_packages


# python setup.py sdist
# pip install twine
# twine upload dist/*


setup(
    name='linpy',
    version='1.16',
    license='MIT',
    author="linpy",
    author_email='linpy@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='',
    install_requires=[
          'sympy',
          'numpy',
          'ipython'
      ],

)
