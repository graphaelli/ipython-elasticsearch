from setuptools import setup, find_packages


version = '0.2'

install_requires = [
    'requests',
]

setup(name='ipython-elasticsearch',
      version=version,
      description="Elasticearch access via IPython",
      long_description="Elasticearch access via IPython",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Topic :: Database',
          'Topic :: Database :: Front-Ends',
          'Programming Language :: Python :: 3',
      ],
      keywords='database ipython elasticsearch',
      author='Gilad Raphaelli',
      author_email='g@raphaelli',
      url='pypi.python.org/pypi/ipython-elasticsearch',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=['nose', 'responses'],
)
