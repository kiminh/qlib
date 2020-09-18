.. _data:
============================
Data: Data Framework&Usage
============================

Introduction
============================

``Qlib Data`` supports constructing data sets from raw data, and the ``Qlib Data`` framework includes three layers as follows.

- Raw Data
- Data API
- Data Handler



Raw Data 
============================

``Qlib`` provides the script 'scripts/get_data.py' to download the raw data that will be used to initialize the qlib package, please refer to `Initialization <../start/initialization.rst>`_.

When ``Qlib`` is initialized, users can choose A-share mode or US stocks mode, please refer to `Initialization <../start/initialization.rst>`_.

A-share Mode
--------------------------------

If users use ``Qlib`` in A-share mode, A-share data is required. The script'scripts/get_data.py' provides methods to download A-share data. If users want to use A-share mode, they need to do as follows.

- Download data in qlib format
    Run the following command to download A-share data in csv format. 

    .. code-block:: bash

        python scripts/get_data.py qlib_data_cn --target_dir ~/.qlib/qlib_data/cn_data

    Users can find A-share data in qlib format in the'~/.qlib/csv_data/cn_data' directory.

- Initialize Qlib in A-share Mode
    Users only need to initialize ``Qlib`` as follows.
    
    .. code-block:: python

        from qlib.config import REG_CN
        qlib.init(mount_path='~/.qlib/qlib_data/cn_data', region=REG_CN)
        

Please refer to `Script API <../reference/api.html>`_.

US Stock Mode
-------------------------
If users use ``Qlib`` in US Stock mode, US stock data is required. Qlib does not mention script to download US stock data. If users want to use Qlib in US stock mode, they need to do as follows.

- Prepare data in csv format
    Users need to prepare US stock data in csv format by themselves, which is in the same format as the A-share data in csv format. Please download the A-share csv data as follows to know more about the format. 

    .. code-block:: bash

        python scripts/get_data.py csv_data_cn --target_dir ~/.qlib/csv_data/cn_data
    

- Convert data from csv format to Qlib format
    Qlib provides the 'scripts/dump_bin.py' to convert data from csv format to qlib format.
    Assuming that the users store the US Stock data in csv format in path '~/.qlib/csv_data/us_data', they need to execute the following command to convert the data from csv format to Qlib format:

    .. code-block:: bash

        python scripts/dump_bin.py dump --csv_path  ~/.qlib/csv_data/us_data --qlib_dir ~/.qlib/qlib_data/us_data --include_fields open,close,high,low,volume,factor

- Initialize ``Qlib`` in US stock mode
    Users only need to initialize ``Qlib`` as follows.
    
    .. code-block:: python

        from qlib.config import REG_US
        qlib.init(mount_path='~/.qlib/qlib_data/us_data', region=REG_US)
        

Please refer to `Script API <../reference/api.html>`_ for more details.

Data API
========================

Data Retrieval
---------------
Users can use APIs in `qlib.data` to retrieve data, please refer to `Data Retrieval <../start/getdata.html>`_.

Filter
-------------------
``Qlib`` provides `NameDFilter` and `ExpressionDFilter` to filter the instruments according to users' need.

- `NameDFilter`
    Name dynamic instrument filter. Filter the instruments based on a regulated name format. A name rule regular expression is required.

- `ExpressionDFilter`
    Expression dynamic instrument filter. Filter the instruments based on a certain expression. An expression rule indicating a certain feature field is required.
    
    - `basic features filter`: rule_expression = '$close/$open>5'
    - `cross-sectional features filter` : rule_expression = '$rank($close)<10'
    - `time-sequence features filter`: rule_expression = '$Ref($close, 3)>100'

To know more about ``Filter``, please refer to `Filter API <../reference/api.html>`_.

Feature
------------------

``Qlib`` provides `Feature` and `ExpressionOps` to fetch the features according to users' need.

- `Feature`
    Load data from data provider.

- `ExpressionOps`
    `ExpressionOps` will use operator for feature construction.
    To know more about  ``Operator``, please refer to `Operator API <../reference/api.html>`_.

To know more about  ``Feature``, please refer to `Feature API <../reference/api.html>`_.




Data Handler
=================

``Data Handler`` is a part of ``estimator`` and can also be used as a single module. 

``Data Handler`` can be used to load raw data, prepare features and label columns, preprocess data(standardization, remove NaN, etc.), split training, validation, and test sets. It is a subclass of ``qlib.contrib.estimator.handler.BaseDataHandler``, which provides some interfaces, for example:

Base Class & Interface
----------------------

Qlib provides a base class `qlib.contrib.estimator.BaseDataHandler <../reference/api.html#class-qlib.contrib.estimator.BaseDataHandler>`_, which provides the following interfaces:

- `setup_feature`    
    Implement the interface to load the data features.

- `setup_label`   
    Implement the interface to load the data labels and calculate user's labels. 

- `setup_processed_data`    
    Implement the interface for data preprocessing, such as preparing feature columns, discarding blank lines, and so on.

Qlib also provides two functions to help user init the data handler, user can override them for user's need.

- `_init_kwargs`
    User can init the kwargs of the data handler in this function, some kwargs may be used when init the raw df.
    Kwargs are the other attributes in data.args, like dropna_label, dropna_feature

- `_init_raw_df`
    User can init the raw df, feature names and label names of data handler in this function. 
    If the index of feature df and label df are not same, user need to override this method to merge them (e.g. inner, left, right merge).

If users want to load features and labels by config, users can inherit `qlib.contrib.estimator.handler.ConfigDataHandler`, Qlib also have provided some preprocess method in this subclass.
If users want to use qlib data, `QLibDataHandler` is recommended. Users can inherit their custom class from `QLibDataHandler`, which is also a subclass of `ConfigDataHandler`.


Usage
--------------
'Data Handler' can be used as a single module, which provides the following mehtod:

- `get_split_data`
    - According to the start and end dates, return features and labels of the pandas DataFrame type used for the 'Model'

- `get_rolling_data`
    - According to the start and end dates, and `rolling_period`, an iterator is returned, which can be used to traverse the features and labels used for rolling.




Example
--------------

``Data Handler`` can be run with ``estimator`` by modifying the configuration file, and can also be used as a single module. 

Know more about how to run ``Data Handler`` with ``estimator``, please refer to `Estimator <estimator.html#about-data>`_.

Qlib provides implemented data handler `QLibDataHandlerV1`. The following example shows how to run 'QLibDataHandlerV1' as a single module. 

.. note:: User needs to initialize package qlib with qlib.init first, please refer to `initialization <initialization.rst>`_.


.. code-block:: Python

    from qlib.contrib.estimator.handler import QLibDataHandlerV1
    from qlib.contrib.model.gbdt import LGBModel

    DATA_HANDLER_CONFIG = {
        "dropna_label": True,
        "start_date": "2007-01-01",
        "end_date": "2020-08-01",
        "market": "csi500",
    }

    TRAINER_CONFIG = {
        "train_start_date": "2007-01-01",
        "train_end_date": "2014-12-31",
        "validate_start_date": "2015-01-01",
        "validate_end_date": "2016-12-31",
        "test_start_date": "2017-01-01",
        "test_end_date": "2020-08-01",
    }

    exampleDataHandler = QLibDataHandlerV1(**DATA_HANDLER_CONFIG)

    # example of 'get_split_data'
    x_train, y_train, x_validate, y_validate, x_test, y_test = exampleDataHandler.get_split_data(**TRAINER_CONFIG)

    # example of 'get_rolling_data'

    for (x_train, y_train, x_validate, y_validate, x_test, y_test) in exampleDataHandler.get_rolling_data(**TRAINER_CONFIG):
        print(x_train, y_train, x_validate, y_validate, x_test, y_test) 


.. note:: (x_train, y_train, x_validate, y_validate, x_test, y_test) can be used as arguments for the ``fit``, ``predict``, and ``score`` methods of the 'Model' , please refer to `Model <model.html#Interface>`_.

Also, the above example has been given in ``examples.estimator.train_backtest_analyze.ipynb``.

To know more abot 'Data Handler', please refer to `Data Handler API <../reference/api.html#handler>`_.


