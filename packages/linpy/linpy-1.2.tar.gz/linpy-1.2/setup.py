from setuptools import setup, find_packages


setup(
    name='linpy',
    version='1.02',
    license='MIT',
    author="linpy",
    author_email='linpy@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='',
    install_requires=[
          'sympy',
          'numpy'
      ],

)
