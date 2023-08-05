import datetime
import getpass
import json
import logging
import os

# import psutil
import socket
from pathlib import Path

import numpy as np
import tensorflow as tf
from scikit_learn import metrics
from tensorflow import keras
from tensorflow.keras import layers

"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Embedding, LSTM, Dense, Sequential
#
"""
from tensorflow.keras.callbacks import (
    CSVLogger,
    EarlyStopping,
    ModelCheckpoint,
    TensorBoard,
)
from tensorflow.keras.layers import LSTM, Dense, Embedding


def create_model(input_shape=(2,), output_shape=1):
    # Instantiate a Sequential model
    model = keras.Sequential()

    # Add a Dense layer with 50 neurons and an input of 1 neuron
    model.add(Dense(50, input_shape=input_shape, activation="relu"))

    # Add two Dense layers with 50 neurons and relu activation
    model.add(Dense(200, activation="relu"))
    model.add(Dense(100, activation="relu"))
    model.add(Dense(50, activation="relu"))
    model.add(Dense(100, activation="relu"))
    model.add(Dense(100, activation="relu"))

    # End your model with a Dense layer and no activation
    model.add(Dense(output_shape))

    # Summarise your model

    print(model.summary())

    # Compile your model
    model.compile(
        optimizer="adam",
        loss="mae",
        metrics=[
            #'MeanSquaredError',
            "RootMeanSquaredError",
            "MeanAbsoluteError",
        ],
    )
    return model


def train_sequential(
    model,
    X,
    y,
    where_to_save,
    log_dir="logs/",
    fit_params=None,
    monitor="val_loss",
):
    # TODO: DOCUMENT once thoroughly tested
    # Watch out: where_to_save might be inside fit_params
    logging_TB = TensorBoard(log_dir=log_dir)

    checkpoint = ModelCheckpoint(
        log_dir + "ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5",
        monitor="val_loss",
        save_weights_only=True,
        save_best_only=True,
    )
    csv_logger = CSVLogger(log_dir + "/log.csv", append=True, separator=";")

    if fit_params is None:
        fit_params = {
            "batch_size": 32,
            "epochs": 100,
            "verbose": True,
            "validation_split": 0.3,
            "callbacks": [
                logging_TB,
                csv_logger,
                EarlyStopping(verbose=True, patience=10, monitor=monitor),
                ModelCheckpoint(
                    where_to_save,
                    monitor=monitor,
                    verbose=True,
                    save_best_only=True,
                ),
            ],
        }
    print("Fitting! Hit CTRL-C to stop early...")
    history = "Nothing to show"
    try:
        history = model.fit(X, y, **fit_params)
    except KeyboardInterrupt:
        print("Training stopped early!")
        history = model.history
    return history


def main_train(X_train, y_train, input_shape=(2,), checkpoint_path=None):
    model = create_model(input_shape=input_shape, output_shape=1)
    if checkpoint_path is None:
        now = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        # now.strftime("%Y%m%d%I%M%S")
        checkpoint_path = Path("./dl-models/" + now + "/")
        checkpoint_path.mkdir(parents=True, exist_ok=True)

    history = train_sequential(
        model=model,
        X=X_train,
        y=y_train,
        where_to_save=checkpoint_path,
        log_dir=str(checkpoint_path),
        fit_params=None,
        monitor="val_loss",
    )

    return model, history


def main_train_sites(dataset):
    # df = dataset[(dataset.mask_coh == 0) & (dataset.mask_kz == 0)]
    df = dataset
    for site in df.site.unique():

        X_train = df[(df.label == "train") & (df.site == site)][
            ["coherence", "kz"]
        ]
        y_train = df[(df.label == "train") & (df.site == site)][
            [
                "lvis_rh100",
            ]
        ]

        now = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        # now.strftime("%Y%m%d%I%M%S")
        checkpoint_path = Path(
            "./dl-models/2-inputs.v2/" + site + "/" + now + "/"
        )
        checkpoint_path.mkdir(parents=True, exist_ok=True)

        main_train(X_train, y_train, checkpoint_path=checkpoint_path)
    # General Model with all sites
    X_train = df[(df.label == "train")][["coherence", "kz"]]
    y_train = df[(df.label == "train")][
        [
            "lvis_rh100",
        ]
    ]

    now = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
    # now.strftime("%Y%m%d%I%M%S")
    checkpoint_path = Path(
        "./dl-models/2-inputs.v2/" + "all_sites" + "/" + now + "/"
    )
    checkpoint_path.mkdir(parents=True, exist_ok=True)

    main_train(X_train, y_train, checkpoint_path=checkpoint_path)


class PixelBasedKeras:
    """
    Fits a logistic regression model.
    """

    def __init__(self, model, logfile, **kwargs):

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename=logfile,
            level="DEBUG",
            format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S",  # %p',
            filemode="w",
        )

        self.logger.info("Starting processing by " + getpass.getuser())
        self.logger.info("Machine name " + socket.gethostname())
        # self.logger.debug('Memory usage '+str(np.round((psutil.Process(os.getpid()).memory_info()[0]/2.**30) / 512. * 100.,2))+ 'Gb')

        self.model = model
        self.kwargs = kwargs

        # self.regressor = self.REGRESSORS[method]
        self.regressor = tf.keras.models.load_model(model.parent)

    def fit(self, X_train, y_train=None):
        self.logger.debug("Train the regressor: %s", str(self.regressor))

        # self.gbm.fit(X_train, y_train)
        # X_emb = self.gbm.apply(X_train).reshape(X_train.shape[0], -1)
        # X_emb = self.bin.fit_transform(X_emb)
        # self.lr.fit(X_emb, y)
        self.logger.debug("Train the classifier: %s", str(self.regressor))
        self.regressor.fit(X_train, y_train)
        # dump(self.regressor, 'filename.joblib')

    def predict(self, X_test, y_test=None, with_tree=False):
        if with_tree:
            y_pred = self.predict(X_test)
        else:
            # X_emb = self.gbm.apply(X_test).reshape(X_test.shape[0], -1)
            # X_emb = self.bin.transform(X_emb)
            # preds = self.lr.predict(X_emb)
            y_pred = self.regressor.predict(X_test)
            print(
                "Mean Absolute Error:",
                metrics.mean_absolute_error(y_test, y_pred),
            )
            print(
                "Mean Squared Error:",
                metrics.mean_squared_error(y_test, y_pred),
            )
            print(
                "Root Mean Squared Error:",
                np.sqrt(metrics.mean_squared_error(y_test, y_pred)),
            )

        return y_pred

    def predict_xarray(self, X_xarray, var=None):
        df = X_xarray[var].to_dataframe()
        X_df_xarray_re = df.replace(to_replace=[np.nan, -np.Inf], value=-9999)

        y_pred = self.regressor.predict(X_df_xarray_re[var])
        X_df_xarray_re["y_pred"] = y_pred
        X_xarray_pred = X_df_xarray_re.to_xarray()
        # X_xarray_pred.values = (np.ma.MaskedArray(X_xarray_pred, mask=X_xarray[var[0]] != np.nan)).data
        # X_xarray_pred.values = np.ma.masked_array( X_xarray_pred, mask = X_xarray[var[0]] == -9999, fill_value=np.nan).filled()
        # X_xarray_pred['y_pred'].where(X_xarray_pred.coherence != -9999.0)
        #
        x_pred = X_xarray_pred["y_pred"].where(
            X_xarray_pred.coherence != -9999.0
        )
        return x_pred

    # , X_df_xarray_re
