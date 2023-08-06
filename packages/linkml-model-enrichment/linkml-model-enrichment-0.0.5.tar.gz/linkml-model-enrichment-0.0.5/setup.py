# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkml_model_enrichment',
 'linkml_model_enrichment.annotators',
 'linkml_model_enrichment.dosdp',
 'linkml_model_enrichment.importers',
 'linkml_model_enrichment.jsonschema',
 'linkml_model_enrichment.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'funowl>=0.1.10,<0.2.0',
 'jsonpatch>=1.32,<2.0',
 'linkml-runtime>=1.1.10,<2.0.0',
 'linkml>=1.1.13,<2.0.0',
 'mkdocs>=1.2.3,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'quantulum3>=0.7.9,<0.8.0',
 'rdflib==5.0.0',
 'requests>=2.26.0,<3.0.0',
 'strsimpy>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['curated_to_enums = '
                     'linkml_model_enrichment.annotators.curated_to_enums:curated_to_enums',
                     'enum_annotator = '
                     'linkml_model_enrichment.annotators.enum_annotator:enum_annotator',
                     'enums_to_curateable = '
                     'linkml_model_enrichment.annotators.enums_to_curateable:enums_to_curateable',
                     'tsv2linkml = '
                     'linkml_model_enrichment.importers.csv_import_engine:tsv2model']}

setup_kwargs = {
    'name': 'linkml-model-enrichment',
    'version': '0.0.5',
    'description': 'Infer models, enrich with meaning for terms including enum permissible values',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
