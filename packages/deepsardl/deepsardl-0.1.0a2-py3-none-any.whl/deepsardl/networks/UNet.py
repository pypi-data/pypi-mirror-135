#%%
from typing import List

import os

import tensorflow as tf

log_level = True
print("Logging: ", log_level)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


#%%


class UNet:
    """
    UNet Class Model
    """

    def __init__(
        self,
        input_height: int = 512,
        input_width: int = 512,
        input_features: int = 9,
        num_inputs: int = 12,
        filter_size: int = 12,
        depth: int = 4,
        output_features: int = 8,
        num_outputs: int = 6,
        logging: bool = log_level,
        branch_inputs: bool = False,
        num_branch_inputs: int = 1,
        branch_input_height: int = 512,
        branch_input_width: int = 512,
        branch_input_features: int = 1,
        problem_type: str = "Regression",
    ):

        self.input_height = input_height
        self.input_width = input_width
        self.num_inputs = num_inputs
        self.input_features = input_features

        self.input_size = (
            input_height,
            input_width,
            num_inputs * input_features,
        )
        self.filter_size = filter_size
        self.kernel_size = 3
        self.depth = depth

        self.branch_inputs = branch_inputs
        self.num_branch_inputs = num_branch_inputs
        self.branch_input_height = branch_input_height
        self.branch_input_width = branch_input_width
        self.branch_input_features = branch_input_features

        self.logging = logging

        self.num_outputs = num_outputs
        self.output_features = output_features

        self.output_size = num_outputs * output_features

        self.problem_type = problem_type

    def input_layer(self):
        x = tf.keras.Input(self.input_size)
        return x

    def single_conv_2d(self, input_layer, n_filters):
        x = tf.keras.layers.Conv2D(
            filters=n_filters,
            padding="same",
            kernel_size=(self.kernel_size, self.kernel_size),
            activation="sigmoid",
        )(input_layer)
        return x

    def final_conv_2d(self, input_layer, n_filters):
        if self.problem_type == "Classification":
            outputs = tf.keras.layers.Conv2D(
                filters=n_filters,
                padding="same",
                kernel_size=(self.kernel_size, self.kernel_size),
                activation="sigmoid",
            )(input_layer)

            # tf.keras.layers.Conv2D(self.output_nums, (1, 1),
            # activation='softmax', name="out")(deconv)
        elif self.problem_type == "Regression":
            outputs = tf.keras.layers.Conv2D(
                filters=n_filters,
                padding="same",
                kernel_size=(self.kernel_size, self.kernel_size),
                activation="linear",
            )(input_layer)

            # tf.keras.layers.Conv2D(self.output_nums, (1, 1),
            # activation='linear', name="out")(deconv)

        return outputs

    def double_conv_2d(self, input_layer, n_filters):
        x = tf.keras.layers.Conv2D(
            filters=n_filters,
            kernel_size=(self.kernel_size, self.kernel_size),
            padding="same",
            kernel_initializer="he_normal",
        )(input_layer)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)
        x = tf.keras.layers.Conv2D(
            filters=n_filters,
            kernel_size=(self.kernel_size, self.kernel_size),
            padding="same",
            kernel_initializer="he_normal",
        )(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)
        return x

    def deconv_2d(self, input_layer, n_filters, stride=2):
        x = tf.keras.layers.Conv2DTranspose(
            filters=n_filters,
            kernel_size=(self.kernel_size, self.kernel_size),
            strides=(stride, stride),
            padding="same",
        )(input_layer)
        return x

    def pool_and_drop(self, input_layer, dropout_rate=0.1, pool=2):
        x = tf.keras.layers.MaxPooling2D(pool_size=(pool, pool))(input_layer)
        x = tf.keras.layers.Dropout(rate=dropout_rate)(x)
        return x

    def generate_input_layers(self):
        inputs = []
        for _ in range(self.num_inputs):
            inputs.append(
                tf.keras.Input(
                    (self.input_height, self.input_width, self.input_features)
                )
            )
        x = tf.keras.layers.concatenate(inputs)
        return inputs, x

    def generate_branch_input_layers(self):
        side_inputs = []
        for _ in range(self.num_branch_inputs):
            side_inputs.append(
                tf.keras.Input(
                    (
                        self.branch_input_height,
                        self.branch_input_width,
                        self.branch_input_features,
                    )
                )
            )
        y = tf.keras.layers.concatenate(side_inputs)
        return side_inputs, y

    def build_model(self):
        # Initialize the Input
        input_layer, concat_layer = self.generate_input_layers()
        if self.branch_inputs is True:
            side_inputs, y_concat_layer = self.generate_branch_input_layers()

        # conv2d_layers: SizedIterable = []
        # pool_layers: SizedIterable = []
        conv2d_layers: List[int] = []
        pool_layers: List[int] = []
        for i in range(self.depth):
            if len(conv2d_layers) == 0:

                # Side Branch
                if self.branch_inputs is True:
                    x = self.double_conv_2d(concat_layer, self.filter_size // 2)
                    y = self.double_conv_2d(
                        y_concat_layer, self.filter_size // 2
                    )

                    x_model = tf.keras.Model(inputs=input_layer, outputs=x)
                    y_model = tf.keras.Model(inputs=side_inputs, outputs=y)
                    x = tf.keras.layers.concatenate(
                        [x_model.output, y_model.output]
                    )
                else:
                    # No side branches
                    x = self.double_conv_2d(concat_layer, self.filter_size)

                conv2d_layers.append(x)
            else:
                x = self.double_conv_2d(
                    pool_layers[-1], self.filter_size * (2 ** i)
                )
                conv2d_layers.append(x)

            x = self.pool_and_drop(conv2d_layers[-1])
            pool_layers.append(x)

        mid = self.double_conv_2d(
            pool_layers[-1], self.filter_size * (2 ** self.depth)
        )

        deconv_layers: List[int] = []
        for i in range(self.depth - 1, -1, -1):
            if len(deconv_layers) == 0:
                x = self.deconv_2d(mid, self.filter_size * (2 ** i))
                deconv_layers.append(x)
                x = tf.keras.layers.concatenate(
                    [conv2d_layers[i], deconv_layers[-1]]
                )
                x = self.double_conv_2d(x, self.filter_size * (2 ** i))
                conv2d_layers.append(x)

            else:
                x = self.deconv_2d(
                    conv2d_layers[-1], self.filter_size * (2 ** i)
                )
                deconv_layers.append(x)
                x = tf.keras.layers.concatenate(
                    [conv2d_layers[i], deconv_layers[-1]]
                )
                x = self.double_conv_2d(x, self.filter_size * (2 ** i))

                conv2d_layers.append(x)

        # final_layer = self.single_conv_2d(conv2d_layers[-1],
        # self.num_outputs * self.output_features)
        final_layer = self.final_conv_2d(
            conv2d_layers[-1], self.num_outputs * self.output_features
        )
        output_layer = []
        for i in range(self.num_outputs):
            output_layer.append(
                tf.keras.layers.Dense(self.output_features)(final_layer)
            )

        if self.branch_inputs is True:
            model = tf.keras.Model(
                inputs=[input_layer, side_inputs], outputs=output_layer
            )

        else:
            model = tf.keras.Model(inputs=[input_layer], outputs=output_layer)

        tf.keras.utils.plot_model(model, to_file="model.png", show_shapes=True)

        if self.logging:
            print(model.summary())
