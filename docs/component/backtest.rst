.. _backtest:
===================================
Backtest: Model&Strategy Evaluation
===================================
.. currentmodule:: qlib

Introduction
===================

The ``Backtest`` module is used to evaluate models and strategies. By ``Backtest``, users can check the performance of custom model/strategy.


Example
===========================

Users need to generate a score file(a pandas DataFrame) with MultiIndex<instrument, datetime> and a `score` column. And users need to assign a strategy used in backtest, if strategy is not assigned,
a `TopkAmountStrategy` strategy with(topk=20, buffer_margin=150, risk_degree=0.95, limit_threshold=0.0095) will be used.
If ``Strategy`` module is not user's interested part, `TopkAmountStrategy` is enough. 

The simple example with default strategy is as follows.

.. code-block:: python

    from qlib.contrib.evaluate import backtest
    report, positions = backtest(pred_test, topk=50, margin=0.5, verbose=False, limit_threshold=0.0095)

To know more about backtesting with specific strategy, please refer to `Strategy <strategy.html>`_.

Score File
--------------

The score file is a pandas DataFrame, its index is <instrument(str), datetime(pd.Timestamp)> and it must
contains a "score" column.

A score file sample is shown as follows.

.. code-block:: python

    instrument datetime   score
    SH600000   2019-01-04 -0.505488
    SZ002531   2019-01-04 -0.320391
    SZ000999   2019-01-04  0.583808
    SZ300569   2019-01-04  0.819628
    SZ001696   2019-01-04 -0.137140
    ...                         ...
    SZ000996   2019-04-30 -1.027618
    SH603127   2019-04-30  0.225677
    SH603126   2019-04-30  0.462443
    SH603133   2019-04-30 -0.302460
    SZ300760   2019-04-30 -0.126383

``Model`` module can produce the score file, please refer to `Model <model.html>`_.

Backtest Result
------------------

The backtest results are in the following form:

.. code-block:: python

    sub_bench       mean    0.000953
                    std     0.004688
                    annual  0.240123
                    ir      3.226878
                    mdd    -0.064588
    sub_cost        mean    0.000718
                    std     0.004694
                    annual  0.181003
                    ir      2.428964
                    mdd    -0.072977

- `sub_bench`
    Income without deduction of fees

- `sub_cost`
    Income with deduction of fees

- `mean`
    Mean value of the income sequence(difference sequence of assets).

- `std`
    Standard deviation of the income sequence(difference sequence of assets).

- `annual`
    Average annualized income of the portfolio.

-  `ir`
    Information Ratio, please refer to `Information Ratio – IR <https://www.investopedia.com/terms/i/informationratio.asp>`_.

- `mdd`
    Maximum Drawdown, please refer to `Maximum Drawdown (MDD) <https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp>`_.


Api
==============
Please refer to `Backtest Api <../reference/api.html>`_.