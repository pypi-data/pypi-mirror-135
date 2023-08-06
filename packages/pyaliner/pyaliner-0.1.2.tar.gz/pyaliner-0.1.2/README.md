# Pyaliner

Library for aligning and visually comparing sequential data in the terminal.

## paired ground-truth vs predicted comparison

### compact

![Compact paired ground-truth vs predicted](/images/paired-2way.png)

### classic

![Classic paired ground-truth vs predicted](/images/classic-paired-2way.png)

## inlined ground-truth vs predicted comparison 

### compact

![Compact inlined ground-truth vs predicted](/images/inlined-2way.png)

### classic

![Classic inlined ground-truth vs predicted](/images/classic-inlined-2way.png)

## paired input vs ground-truth vs predicted comparison

### compact

![Compact paired input vs ground-truth vs predicted](/images/paired-3way.png)

### classic

![Classic paired input vs ground-truth vs predicted](/images/classic-paired-3way.png)

## paired ground-truth vs 1st predicted vs 2nd predicted comparison

![Classic paired ground-truth vs 1st predicted vs 2nd predicted](/images/classic-paired-tpp.png)

## alignment

```python

>>> from pyaliner import align, COMPACT

>>> align('Example invalid invalid sentence'.split(), 'Example sentence'.split())
(('Example', 'invalid', 'invalid', 'sentence'), ('Example', '⎵', '⎵', 'sentence'))

>>> align('Example invalid invalid sentence'.split(), 'Example sentence'.split(), kind=COMPACT)
(('Example', 'invalid∙invalid', 'sentence'), ('Example', '⎵', 'sentence'))

```

# Limitations

*  Three-way alignment uses a slow heuristic.
*  Wide characters, e.g., East Asian scripts,  are not properly aligned with narrow ones

# Installing

Install with pip:

```shell
pip install pyaliner
```

# Testing

Unit tests are written with [pytest](https://docs.pytest.org/en/stable) and [hypothesis](https://hypothesis.works/). 
Run with:

```shell
pip install pytest hypothesis

pytest
```

# Changelog

Check the [Changelog](https://github.com/JoseLlarena/pyaliner/blob/master/CHANGELOG.md) for fixes and enhancements of each version.

# License

Copyright Jose Llarena 2022

Distributed under the terms of the [MIT](https://github.com/JoseLlarena/pyaliner/blob/master/LICENSE) license, Pyaliner is free 
and open source software.