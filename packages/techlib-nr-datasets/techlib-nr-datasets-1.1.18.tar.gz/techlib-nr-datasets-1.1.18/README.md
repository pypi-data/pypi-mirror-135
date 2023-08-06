# NR-Datasets

[![Build Status](https://travis-ci.org/Narodni-repozitar/nr-datasets.svg?branch=master)](https://travis-ci.org/Narodni-repozitar/nr-datasets)
[![Coverage Status](https://coveralls.io/repos/github/Narodni-repozitar/nr-datasets/badge.svg?branch=master)](https://coveralls.io/github/Narodni-repozitar/nr-datasets?branch=master)


Disclaimer: The library is part of the Czech National Repository, and therefore the README is written in Czech.
General libraries extending [Invenio](https://github.com/inveniosoftware) are concentrated under the [Oarepo
 namespace](https://github.com/oarepo).

  ## Instalace

 Nejedná se o samostatně funkční knihovnu, proto potřebuje běžící Invenio a závislosti Oarepo.
 Knihovna se instaluje ze zdroje.

 ```bash
git clone git@github.com:Narodni-repozitar/nr-datasets.git
cd nr-datasets
pip install poetry
poetry install
```

Pro testování a/nebo samostané fungování knihovny je nutné instalovat tests z extras.

```bash
poetry install --extras tests
```

:warning: Pro instalaci se používá Manažer závilostí **Poetry** více infromací lze naleznout v
[dokumentaci](https://python-poetry.org/docs/)
