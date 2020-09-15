#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT License.

import sys
from pathlib import Path

import qlib
import pandas as pd
from qlib.config import REG_CN
from qlib.contrib.model.gbdt import LGBModel
from qlib.contrib.estimator.handler import QLibDataHandlerV1
from qlib.contrib.strategy.strategy import TopkAmountStrategy
from qlib.contrib.evaluate import (
    backtest as normal_backtest,
    long_short_backtest,
    risk_analysis,
)
from qlib.utils import exists_qlib_data


if __name__ == "__main__":

    # use default data
    mount_path = "~/.qlib/qlib_data/cn_data"  # target_dir
    if not exists_qlib_data(mount_path):
        print(f"Qlib data is not found in {mount_path}")
        sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath("scripts")))
        from get_data import GetData

        GetData().qlib_data_cn(mount_path)

    qlib.init(mount_path=mount_path, region=REG_CN)

    MARKET = "CSI500"
    BENCHMARK = "SH000905"

    ###################################
    # train model
    ###################################
    DATA_HANDLER_CONFIG = {
        "dropna_label": True,
        "start_date": "2007-01-01",
        "end_date": "2020-08-01",
        "market": MARKET,
    }

    TRAINER_CONFIG = {
        "train_start_date": "2007-01-01",
        "train_end_date": "2014-12-31",
        "validate_start_date": "2015-01-01",
        "validate_end_date": "2016-12-31",
        "test_start_date": "2017-01-01",
        "test_end_date": "2020-08-01",
    }

    # use default DataHandler
    # custom DataHandler, refer to: TODO: DataHandler api url
    x_train, y_train, x_validate, y_validate, x_test, y_test = QLibDataHandlerV1(**DATA_HANDLER_CONFIG).get_split_data(
        **TRAINER_CONFIG
    )

    MODEL_CONFIG = {
        "loss": "mse",
        "colsample_bytree": 0.8879,
        "learning_rate": 0.0421,
        "subsample": 0.8789,
        "lambda_l1": 205.6999,
        "lambda_l2": 580.9768,
        "max_depth": 8,
        "num_leaves": 210,
        "num_threads": 20,
    }
    # use default model
    # custom Model, refer to: TODO: Model api url
    model = LGBModel(**MODEL_CONFIG)
    model.fit(x_train, y_train, x_validate, y_validate)
    _pred = model.predict(x_test)
    _pred = pd.DataFrame(_pred, index=x_test.index, columns=y_test.columns)

    # backtest requires pred_score
    pred_score = pd.DataFrame(index=_pred.index)
    pred_score["score"] = _pred.iloc(axis=1)[0]

    # save pred_score to file
    pred_score_path = Path("~/tmp/qlib/pred_score.pkl").expanduser()
    pred_score_path.parent.mkdir(exist_ok=True, parents=True)
    pred_score.to_pickle(pred_score_path)

    ###################################
    # backtest
    ###################################
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
        "open_cost": 0.0005,
        "close_cost": 0.0015,
        "min_cost": 5,
    }

    # use default strategy
    # custom Strategy, refer to: TODO: Strategy api url
    strategy = TopkAmountStrategy(**STRATEGY_CONFIG)
    report_normal, positions_normal = normal_backtest(pred_score, strategy=strategy, **BACKTEST_CONFIG)

    # long short backtest
    long_short_reports = long_short_backtest(pred_score, topk=50)

    ###################################
    # analyze
    # If need a more detailed analysis, refer to: examples/train_and_bakctest.ipynb
    ###################################
    analysis = dict()
    analysis["pred_long"] = risk_analysis(long_short_reports["long"])
    analysis["pred_short"] = risk_analysis(long_short_reports["short"])
    analysis["pred_long_short"] = risk_analysis(long_short_reports["long_short"])
    analysis["sub_bench"] = risk_analysis(report_normal["return"] - report_normal["bench"])
    analysis["sub_cost"] = risk_analysis(report_normal["return"] - report_normal["bench"] - report_normal["cost"])
    analysis_df = pd.concat(analysis)  # type: pd.DataFrame
    print(analysis_df)