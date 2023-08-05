import tensorflow as tf


def build_mlp(dim, regress=False):
    model = tf.keras.layers.Sequential()
    model.add(tf.keras.layers.Dense(8, input_dim=dim, activation="relu"))
    model.add(tf.keras.layers.Dense(4, activation="relu"))

    if regress:
        model.add(tf.keras.layers.Dense(1, activation="linear"))

    return model


def build_cnn(width, height, depth, filters=(16, 32, 64), regress=False):
    shape = (height, width, depth)
    channel_dim = -1

    inputs = tf.keras.Input(shape=shape)
    for (i, f) in enumerate(filters):
        if i == 0:
            x = inputs

        x = tf.keras.layers.Conv2D(f, (3, 3), padding="same")(x)
        x = tf.keras.layers.Activation("relu")(x)
        x = tf.keras.layers.BatchNormalization(axis=channel_dim)(x)
        x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(x)

    # CNN
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(16)(x)
    x = tf.keras.layers.Activation("relu")(x)
    x = tf.keras.layers.BatchNormalization(axis=channel_dim)(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    # MLP
    x = tf.keras.layers.Dense(4)(x)
    x = tf.keras.layers.Activation("relu")(x)

    if regress:
        x = tf.keras.layers.Dense(1, activation="linear")(x)

    model = tf.keras.Model(inputs, x)

    return model
