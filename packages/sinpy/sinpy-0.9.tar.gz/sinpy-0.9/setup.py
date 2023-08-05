from setuptools import setup, find_packages


setup(
    name='sinpy',
    version='0.9',
    license='MIT',
    author="sinpy",
    author_email='sinpy@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='',
    install_requires=[
          'sympy',
          'numpy'
      ],

)
