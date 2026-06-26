# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/nfb2021/polychromae/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                          |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| packages/chromophore/src/chromophore/\_\_init\_\_.py          |        5 |        0 |    100% |           |
| packages/chromophore/src/chromophore/\_colormap.py            |       67 |       16 |     76% |9-10, 18-21, 75-86 |
| packages/chromophore/src/chromophore/\_palettes.py            |        3 |        0 |    100% |           |
| packages/chromophore/tests/test\_colormap.py                  |       69 |        0 |    100% |           |
| packages/pytochrome/src/pytochrome/\_\_init\_\_.py            |       92 |       40 |     57% |90, 95, 100-102, 120-121, 130-131, 158-189, 207, 223, 227, 230, 239, 279-283, 301-302 |
| packages/pytochrome/src/pytochrome/\_backends/\_\_init\_\_.py |        4 |        0 |    100% |           |
| packages/pytochrome/src/pytochrome/\_backends/\_base.py       |       40 |       14 |     65% |41-45, 71-74, 81-84, 88 |
| packages/pytochrome/src/pytochrome/\_backends/\_mpl.py        |       73 |       57 |     22% |26-28, 35, 43-168, 176-178, 185 |
| packages/pytochrome/src/pytochrome/\_backends/\_plotly.py     |       56 |       38 |     32% |18, 37, 54, 104-105, 110, 130-134, 142-153, 161-168, 176-195, 198 |
| packages/pytochrome/src/pytochrome/\_cmaps.py                 |       21 |        7 |     67% |11-14, 19, 27-28 |
| packages/pytochrome/src/pytochrome/\_tokens.py                |       30 |        0 |    100% |           |
| packages/pytochrome/tests/test\_tokens.py                     |       45 |        1 |     98% |        62 |
| **TOTAL**                                                     |  **505** |  **173** | **66%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/nfb2021/polychromae/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/nfb2021/polychromae/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/nfb2021/polychromae/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/nfb2021/polychromae/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fnfb2021%2Fpolychromae%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/nfb2021/polychromae/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.