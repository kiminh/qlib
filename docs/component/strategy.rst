.. _strategy:
==========================
Strategy: Portfolio Management
==========================
.. currentmodule:: qlib

Introduction
===================

By ``Strategy``, users can adopt different trading strategies, which means that users can use different algorithms to generate investment portfolios based on the predicted scores of the ``Model`` module.

``Qlib`` provides several trading strategy classes, users can customize strategies according to their own needs also.

Base Class & Interface
=====================

BaseStrategy
------------------

Qlib provides a base class ``qlib.contrib.strategy.BaseStrategy``. All strategy classes need to inherit the base class and implement its interface.

- `get_risk_degree`
    Return the proportion of your total value you will use in investment. Dynamically risk_degree will result in Market timing.

- `generate_order_list`
    Rerturn the order list. 

User can inherit 'BaseStrategy' to costomize their strategy class.

WeightStrategyBase
--------------------

Qlib alse provides a class ``qlib.contrib.strategy.WeightStrategyBase`` that is a subclass of `BaseStrategy`. 

`WeightStrategyBase` only focuses on the target positions, and automatically generates an order list based on positions. It provides the `generate_target_weight_position` interface.

- `generate_target_weight_position`
    According to the current position and trading date to generate the target position.
     
    .. note:: The cash is not considered.
    Return the target position.

    .. note::
        Here the `target position` means percentage of total assets.

`WeightStrategyBase` implements the interface `generate_order_list`, whose process is as follows.

- Call `generate_target_weight_position` method to generate the target position.
- Generate the target amount of stocks from the target position.
- Generate the order list from the target amount

User can inherit `WeightStrategyBase` and implement the inteface `generate_target_weight_position` to costomize their strategy class, which focuses on the target positions.

Implemented Strategy
====================

Qlib provides several implemented strategy classes, such as `TopkWeightStrategy`, `TopkAmountStrategy` and `TopkDropoutStrategy`.

TopkWeightStrategy
------------------
`TopkWeightStrategy` is a subclass of `WeightStrategyBase` and implements the interface `generate_target_weight_position`.

The implemented interface `generate_target_weight_position` adopts the ``Topk-Margin`` algorithm to calculate the target position, it ensures that the weight of each stock is as even as possible.

.. note:: 
    ``Topk-Margin`` algorithm: 

    - `Topk`: The number of stocks held
    - `margin`: Score rank threshold
    

    Currently, the number of held stocks is `Topk`.
    On each trading day, the held stocks with scores outside the threshold `margin` will be sold, and the same number of unheld stocks with best scores will be bought. 

    .. image:: ../_static/img/topk_margin.png
        :alt: Topk-Margin




TopkAmountStrategy
------------------
`TopkAmountStrategy` is a subclass of `BaseStrategy` and implement the interface `generate_order_list` whose process is as follows.

- Adopt the the ``Topk-Margin`` algorithm to calculate the target amount of each stock
- Generate the order list from the target amount



TopkDropoutStrategy
------------------
`TopkDropoutStrategy` is a subclass of `BaseStrategy` and implement the interface `generate_order_list` whose process is as follows.

- Adopt the the ``TopkDrop`` algorithm to calculate the target amount of each stock

    .. note::
        ``TopkDrop`` algorithm：

        - `Topk`: The number of stocks held
        - `Drop`: The number of stocks sold on each trading day
        
        Currently, the number of held stocks is `Topk`.
        On each trading day, the `Drop` number of held stocks with worst scores will be sold, and the same number of unheld stocks with best scores will be bought.
        
        .. image:: ../_static/img/topk_drop.png
            :alt: Topk-Drop

        ``TopkDrop`` algorithm sells `Drop` stocks every trading day, which guarantees a fixed turnover rate.
        
- Generate the order list from the target amount

Example
====================
``Strategy`` can be specified in the ``Backtest`` module, the example is as follows.

.. code-block:: python

    from qlib.contrib.strategy.strategy import TopkAmountStrategy
    from qlib.contrib.evaluate import backtest
    STRATEGY_CONFIG = {
        "topk": 50,
        "buffer_margin": 230,
    }
    BACKTEST_CONFIG = {
        "verbose": False,
        "limit_threshold": 0.095,
        "account": 100000000,
        "benchmark": BENCHMARK,
        "deal_price": "vwap",
    }

    # use default strategy
    # custom Strategy, refer to: TODO: Strategy api url
    strategy = TopkAmountStrategy(**STRATEGY_CONFIG)
    report_normal, positions_normal = backtest(
        pred_score, strategy=strategy, **BACKTEST_CONFIG
    )

Also, the above example has been given in ``examples.estimator.train_backtest_analyze.ipynb``.

To know more about ``Backtest``, please refer to `Backtest: Model&Strategy Testing <backtest.html>`_.

Api
===================
Please refer to `Strategy Api <../reference/api.html>`_.
