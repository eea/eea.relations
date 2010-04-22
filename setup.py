from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='eea.relations',
      version=version,
      description="EEA Possible Relations",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea relations widget reference browser referencebrowserwidget faceted facetednavigation plone zope python',
      author='Alin Voinea',
      author_email='alin.voinea@eaudeweb.ro',
      url='http://eea.europa.eu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea',],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pydot',
          'eea.facetednavigation',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
