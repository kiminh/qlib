Qlib is an AI-oriented quantitative investment platform, which aims to realize the potential, empower the research, and create the value of AI technologies in quantitative investment.

With Qlib, you can easily apply your favorite model to create a better Quant investment strategy.


- [Framework of Qlib](#framework-of-qlib)
- [Quick start](#quick-start)
  - [Installation](#installation)
  - [Get Data](#get-data)
  - [Auto Quant research workflow with _estimator_](#auto-quant-research-workflow-with-estimator)
  - [Customized Quant research workflow by code](#customized-quant-research-workflow-by-code)
- [More About Qlib](#more-about-qlib)
  - [Offline mode and online mode](#offline-mode-and-online-mode)
  - [Performance of Qlib Data Server](#performance-of-qlib-data-server)
- [Contributing](#contributing)



# Framework of Qlib
![framework](docs/_static/img/framework.png)

At the module level, Qlib is a platform that consists of the above components. Each component is loose-coupling and can be used stand-alone.

| Name                | Description                                                                                                                                                                                                                                                   |
| ------              | -----                                                                                                                                                                                                                                                         |
| _Data layer_        | _DataServer_ focus on providing high performance infrastructure  for user to retrieve and get raw data. _DataEnhancement_ will preprocess the data and provide the best dataset to be fed in to the models                                                    |
| _Interday Model_    | _Interday model_ focus on producing forecasting signals(aka. _alpha_). Models are trained by _Model Creator_ and managed by _Model Manager_. User could choose one or multiple models for forecasting. Multiple models could be combined with _Ensemble_ module |
| _Interday Strategy_ | _Portfolio Generator_ will take forecasting signals as input and output the orders based on current position to achieve target portfolio                                                                                                                      |
| _Intraday Trading_  | _Order Executor_ is responsible for executing orders produced by _Interday Strategy_ and returning the executed results.                                                                                                                                        |
| _Analysis_          | User could get detailed analysis report of forecasting signal and portfolio in this part.                                                                                                                                                                     |

* The modules with hand-drawn style is under development and will be  released in the future.
* The modules with dashed border is highly user-customizable and extendible.


# Quick start

## Installation

To install Qlib from source you need _Cython_ in addition to the normal dependencies above:

```bash
pip install numpy
pip install --upgrade  cython
```

Clone the repository and then run:
```bash
python setup.py install
```


## Get Data
- Load and prepare the Data: execute the following command to load the stock data:
  ```bash
  python scripts/get_data.py qlib_data_cn --target_dir ~/.qlib/qlib_data/cn_data
  ```
<!-- 
- Run the initialization code and get stock data:

  ```python
  import qlib
  from qlib.data import D
  from qlib.config import REG_CN

  # Initialization
  mount_path = "~/.qlib/qlib_data/cn_data"  # target_dir
  qlib.init(mount_path=mount_path, region=REG_CN)

  # Get stock data by Qlib
  # Load trading calendar with the given time range and frequency
  print(D.calendar(start_time='2010-01-01', end_time='2017-12-31', freq='day')[:2])

  # Parse a given market name into a stockpool config
  instruments = D.instruments('csi500')
  print(D.list_instruments(instruments=instruments, start_time='2010-01-01', end_time='2017-12-31', as_list=True)[:6])

  # Load features of certain instruments in given time range
  instruments = ['SH600000']
  fields = ['$close', '$volume', 'Ref($close, 1)', 'Mean($close, 3)', '$high-$low']
  print(D.features(instruments, fields, start_time='2010-01-01', end_time='2017-12-31', freq='day').head())
  ```
 -->

## Auto Quant research workflow with _estimator_
Qlib provides a tool named `estimator` to run whole workflow automatically(including building dataset, train models, backtest, analysis)

1. Run _estimator_ (_config.yaml_ for: [estimator_config.yaml](example/estimator/estimator_config.yaml)):

    ```bash
    estimator -c example/estimator/estimator_config.yaml
    ```
  
    Estimator result:
  
    ```bash

                          risk
    sub_bench mean    0.000662
              std     0.004487
              annual  0.166720
              sharpe  2.340526
              mdd    -0.080516
    sub_cost  mean    0.000577
              std     0.004482
              annual  0.145392
              sharpe  2.043494
              mdd    -0.083584
    ```
    See the full documnents for [Use _Estimator_ to Start An Experiment](TODO:URL).

2. Analysis

    Run `examples/estimator/analyze_from_estimator.ipynb` in `jupyter notebook`
    1.  forecasting signal analysis
        - Model Performance
        ![Model Performance](docs/_static/img/model_performance.png)

    2.  portfolio analysis
        - Report
        ![Report](docs/_static/img/report.png)
        <!-- 
        - Score IC
        ![Score IC](docs/_static/img/score_ic.png)
        - Cumulative Return
        ![Cumulative Return](docs/_static/img/cumulative_return.png)
        - Risk Analysis
        ![Risk Analysis](docs/_static/img/risk_analysis.png)
        - Rank Label
        ![Rank Label](docs/_static/img/rank_label.png)
        -->

## Customized Quant research workflow by code
Automatic workflow may not suite the research workflow of all Quant researchers. To support flexible Quant research workflow, Qlib also provide modularized interface to allow researchers to build their own workflow. [Here](TODO_URL) is a demo for customized Quant research workflow by code



# More About Qlib
The detailed documents are organized in [docs](docs).
[Sphinx](http://www.sphinx-doc.org) and the readthedocs theme is required to build the documentation in html formats. 
```bash
cd docs/
conda install sphinx sphinx_rtd_theme -y
# Otherwise, you can install them with pip
# pip install sphinx sphinx_rtd_theme
make html
```
You can also view the [latest document](TODO_URL) online directly.



## Offline mode and online mode
The data server of Qlib can both deployed as offline mode and online mode. The default mode is offline mode.

Under offline mode, the data will be deployed locally. 

Under online mode, the data will be deployed as a shared data service. The data and their cache will be shared by clients. The data retrieving performance is expected to be improved due to a higher rate of cache hits. It will use less disk space, too. The documents of the online mode can be found in [Qlib-Server](TODO_link). The online mode can be deployed automatically with [Azure CLI based scripts](TODO_link)

## Performance of Qlib Data Server
The performance of data processing is important to data-driven methods like AI technologies. As an AI-oriented platform, Qlib provides a solution for data storage and data processing. To demonstrate the performance of Qlib, We
compare Qlib with several other solutions. 

We evaluate the performance of several solutions by completing the same task,
which creates a dataset(14 features/factors) from the basic OHLCV daily data of a stock market(800 stocks each day from 2007 to 2020). The task involves data queries and processing.

|                         | HDF5      | MySQL     | MongoDB   | InfluxDB  | Qlib -E -D  | Qlib +E -D   | Qlib +E +D  |
| --                      | ------    | ------    | --------  | --------- | ----------- | ------------ | ----------- |
| Total (1CPU) (seconds)  | 184.4±3.7 | 365.3±7.5 | 253.6±6.7 | 368.2±3.6 | 147.0±8.8   | 47.6±1.0     | **7.4±0.3** |
| Total (64CPU) (seconds) |           |           |           |           | 8.8±0.6     | **4.2±0.2**  |             |
* `+(-)E` indicates with(out) `ExpressionCache`
* `+(-)D` indicates with(out) `DatasetCache`

Most general-purpose databases take too much time on loading data. After looking into the underlying implementation, we find that data go through too many layers of interfaces and unnecessary format transformations in general-purpose database solutions.
Such overheads greatly slow down the data loading process.
Qlib data are stored in a compact format, which is efficient to be combined into arrays for scientific computation.





# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
