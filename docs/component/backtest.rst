.. _backtest:
============================================
Intraday Trading: Model&Strategy Testing
============================================
.. currentmodule:: qlib

Introduction
===================

The ``Backtest`` module uses ``Order Executor`` to trade and execute orders produced by ``Strategy``.

The ``Backtest`` module could be used to test models and strategies. By ``Backtest``, users can check the performance of custom model/strategy.



Example
===========================

Users need to generate a prediction score(a pandas DataFrame) with MultiIndex<instrument, datetime> and a `score` column. And users need to assign a strategy used in backtest, if strategy is not assigned,
a `TopkAmountStrategy` strategy with `(topk=20, buffer_margin=150, risk_degree=0.95, limit_threshold=0.0095)` will be used.
If ``Strategy`` module is not user's interested part, `TopkAmountStrategy` is enough. 

The simple example with default strategy is as follows.

.. code-block:: python

    from qlib.contrib.evaluate import backtest
    # pred_score is the prediction score
    report, positions = backtest(pred_score, topk=50, margin=0.5, verbose=False, limit_threshold=0.0095)

To know more about backtesting with specific strategy, please refer to `Strategy <strategy.html>`_.

To know more about the prediction score `pred_score` output by ``Model``, please refer to `Interday Model: Model Training & Prediction <model.html>`_.

Prediction Score
-----------------

The prediction score is a pandas DataFrame. Its index is <instrument(str), datetime(pd.Timestamp)> and it must
contains a `score` column.

A prediction sample is shown as follows.

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

``Model`` module can make predictions, please refer to `Model <model.html>`_.

Backtest Result
------------------

The backtest results are in the following form:

.. code-block:: python

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

- `sub_bench`
    Returns of the portfolio without deduction of fees

- `sub_cost`
    Returns of the portfolio with deduction of fees

- `mean`
    Mean value of the returns sequence(difference sequence of assets).

- `std`
    Standard deviation of the returns sequence(difference sequence of assets).

- `annual`
    Average annualized returns of the portfolio.

-  `ir`
    Information Ratio, please refer to `Information Ratio – IR <https://www.investopedia.com/terms/i/informationratio.asp>`_.

- `mdd`
    Maximum Drawdown, please refer to `Maximum Drawdown (MDD) <https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp>`_.


REFERENCE
==============
To know more about ``Backtest``, please refer to `Backtest API <../reference/api.html>`_.
