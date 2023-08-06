# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['featureclass']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'featureclass',
    'version': '0.3.0',
    'description': 'Feature engineering library that helps you keep track of feature dependencies, documentation and schema',
    'long_description': '# featureclass\n\nFeature engineering library that helps you keep track of feature dependencies, documentation and schema  \n\n# Installation \nUsing pip\n\n```bash\npip install featureclass\n```\n\n# Motivation\n\nThis library helps define a featureclass.  \nfeatureclass is inspired by dataclass, and is meant to provide alternative way to define features engineering classes.  \n\nI have noticed that the below code is pretty common when doing feature engineering:  \n\n```python\nfrom statistics import variance\nfrom math import sqrt\nclass MyFeatures:\n    def calc_all(self, datapoint):\n        out = {}\n        out[\'var\'] = self.calc_var(datapoint),\n        out[\'stdev\'] = self.calc_std(out[\'var\'])\n        return out\n        \n    def calc_var(self, data) -> float:\n        return variance(data)\n\n    def calc_stdev(self, var) -> float:\n        return sqrt(var)\n```\n\nSome things were missing for me from this type of implementation:  \n1. Implicit dependencies between features  \n2. No simple schema  \n3. No documentation for features  \n4. Duplicate declaration of the same feature - once as a function and one as a dict key  \n\n\nThis is why I created this library.  \nI turned the above code into this:  \n```python\nfrom featureclass import feature, featureclass, feature_names, feature_annotations, asdict, as_dataclass\nfrom statistics import variance\nfrom math import sqrt\n\n@featureclass\nclass MyFeatures:\n    def __init__(self, datapoint):\n        self.datapoint = datapoint\n    \n    @feature()\n    def var(self) -> float:\n        """Calc variance"""\n        return variance(self.datapoint)\n\n    @feature()\n    def stdev(self) -> float:\n        """Calc stdev"""\n        return sqrt(self.var)\n\nprint(feature_names(MyFeatures)) # (\'var\', \'stdev\')\nprint(feature_annotations(MyFeatures)) # {\'var\': float, \'stdev\': float}\nprint(asdict(MyFeatures([1,2,3,4,5]))) # {\'var\': 2.5, \'stdev\': 1.5811388300841898}\nprint(as_dataclass(MyFeatures([1,2,3,4,5]))) # MyFeatures(stdev=1.5811388300841898, var=2.5)\n```\n\nThe feature decorator is using cached_property to cache the feature calculation,   \nmaking sure that each feature is calculated once per datapoint\n\n',
    'author': 'Itay Azolay',
    'author_email': 'itayazolay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Itayazolay/featureclass',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
