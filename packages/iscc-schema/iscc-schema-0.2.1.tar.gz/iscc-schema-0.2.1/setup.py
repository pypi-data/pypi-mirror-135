# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_schema']

package_data = \
{'': ['*'], 'iscc_schema': ['models/*', 'reference/*']}

install_requires = \
['jcs>=0.2,<0.3', 'pydantic>=1.9,<2.0']

setup_kwargs = {
    'name': 'iscc-schema',
    'version': '0.2.1',
    'description': 'OpenAPI representation of the ISCC data model',
    'long_description': '# **ISCC** - Schema\n\n*OpenAPI representation of the ISCC data model*\n\n[![Build](https://github.com/iscc/iscc-schema/actions/workflows/tests.yml/badge.svg)](https://github.com/iscc/iscc-schema/actions/workflows/tests.yml)\n[![Version](https://img.shields.io/pypi/v/iscc-schema.svg)](https://pypi.python.org/pypi/iscc-schema/)\n\n## Introduction\n\nThis repository hosts all schema definitions of the ISCC. Schemas are defined in\n[OpenAPI v3.1.0](https://spec.openapis.org/oas/v3.1.0.html) format and serve as a\nsingle source of truth for auto-generated [JSON Schema](https://json-schema.org/)\ndefinitions, [JSON-LD](https://json-ld.org/) contexts, and other schema related\nartifacts.\n\n## Generated files\n\nThe source of code generation are the files at `iscc_schema/models/*`.\nThe outputs produced when running `poe build` are:\n\n- [`docs/schema/iscc.json`](https://github.com/iscc/iscc-schema/blob/main/docs/schema/iscc.json) - JSON Schema for ISCC Metadata\n- [`docs/schema/index.md`](https://github.com/iscc/iscc-schema/blob/main/docs/schema/index.md) - JSON Schema Markdown documentation\n- [`docs/context/iscc.jsonld`](https://github.com/iscc/iscc-schema/blob/main/docs/context/iscc.jsonld) - JSON-LD context for ISCC Metadata\n- [`docs/terms/index.md`](https://github.com/iscc/iscc-schema/blob/main/docs/context/index.md) - ISCC Metadata Vocabulary documentation\n- [`iscc_schema/schema.py`](https://github.com/iscc/iscc-schema/blob/main/iscc_schema/schema.py) - Pydantic models for ISCC Metadata\n\n## Published files\n\nThe generated files are published under the following canonical URLs:\n\n- [`http://purl.org/iscc/schema`](http://purl.org/iscc/schema) - JSON Schema latest version\n- [`http://purl.org/iscc/context`](http://purl.org/iscc/context) - JSON-LD Context latest version\n- [`http://purl.org/iscc/terms`](http://purl.org/iscc/terms) - ISCC Metadata Vocabulary latest version\n- [`http://pypi.org/project/iscc-schema`](http://pypi.org/project/iscc-schema) - Python package with pydantic models\n\n## OpenAPI Extensions\n\nThe OpenAPI Specification allows for\n[extending](https://spec.openapis.org/oas/latest.html#specification-extensions) the\nspecification with custom fields. Extensions must start with `x-`.\nAll ISCC extensions start with `x-iscc-`:\n\n- `x-iscc-context` - for documenting JSON-LD contexts.\n- `x-iscc-schema-doc` - for original descriptions from [schema.org](https://schema.org)\n\n\n## Changelog\n\n### 0.2.1 - 2022-01-19\n- Tweak code generator\n- Cleanup dependencies\n\n### 0.2.0 - 2022-01-17\n- Added generator field\n- Changed properties field to support base64\n- Changed iscc validation to support Semantic-Code\n\n\n### 0.1.0 - 2022-01-05\n- Initial release\n',
    'author': 'Titusz',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iscc/iscc-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
