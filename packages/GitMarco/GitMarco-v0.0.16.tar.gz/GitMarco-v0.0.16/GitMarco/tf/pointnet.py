import os
from datetime import date
import tensorflow as tf
import numpy as np


class OrthogonalRegularizer(tf.keras.regularizers.Regularizer):
    def __init__(self, num_features, l2reg=0.001):
        self.num_features = num_features
        self.l2reg = l2reg
        # self.eye = tf.eye(num_features)

    def __call__(self, x):
        x = tf.reshape(x, (-1, self.num_features, self.num_features))
        xxt = tf.tensordot(x, x, axes=(2, 2))
        xxt = tf.reshape(xxt, (-1, self.num_features, self.num_features))
        return tf.reduce_sum(self.l2reg * tf.square(xxt - tf.eye(self.num_features)))

    def get_config(self):
        return {
            'num_features': self.num_features,
            'l2reg': self.l2reg,
            # 'eye': self.eye

        }


def dense_bn(x, filters):
    x = tf.keras.layers.Dense(filters)(x)
    x = tf.keras.layers.BatchNormalization(momentum=0.0)(x)
    return tf.keras.layers.Activation("relu")(x)


def t_network(inputs,
              num_features,
              orto_reg: bool = True):
    # Initalise bias as the indentity matrix
    bias = tf.keras.initializers.Constant(np.eye(num_features).flatten())
    if orto_reg:
        reg = OrthogonalRegularizer(num_features)
    else:
        reg = None

    x = conv_bn(inputs, 32)
    x = conv_bn(x, 64)
    x = conv_bn(x, 512)
    x = tf.keras.layers.GlobalMaxPooling1D()(x)
    x = dense_bn(x, 256)
    x = dense_bn(x, 128)
    x = tf.keras.layers.Dense(
        num_features * num_features,
        kernel_initializer="zeros",
        bias_initializer=bias,
        activity_regularizer=reg,
    )(x)
    feat_t = tf.keras.layers.Reshape((num_features, num_features))(x)
    # Apply affine transformation to input features
    return tf.keras.layers.Dot(axes=(2, 1))([inputs, feat_t])


def conv_bn(x, filters):
    x = tf.keras.layers.Conv1D(filters, kernel_size=1, padding="valid")(x)
    x = tf.keras.layers.BatchNormalization(momentum=0.0)(x)
    return tf.keras.layers.Activation("relu")(x)


def exp_dim(global_feature, num_points):
    return tf.tile(global_feature, [1, num_points, 1])


class Pointnet(object):
    def __init__(self,
                 n_points: int = 1024,
                 setup: str = 'seg',  # class - seg - both
                 input_setup: str = 'grid',  # grid - both
                 n_fields: int = 1,
                 n_scalars: int = 1,
                 n_features: int = 1,
                 grid_size: int = 3,
                 orto_reg: bool = True,
                 encoding_size: int = 1024,
                 feature_transform: bool = True,
                 dropout_rate: float = 0.3,
                 out_class_activation: str = 'relu',
                 out_reg_activation: str = 'sigmoid',
                 class_neurons: tuple = (512, 256),
                 seg_kernels: tuple = (512, 256, 128, 128),
                 ):

        self.n_points = n_points
        self.setup = setup
        self.input_setup = input_setup
        self.n_fields = n_fields
        self.n_scalars = n_scalars
        self.n_features = n_features
        self.grid_size = grid_size
        self.orto_reg = orto_reg
        self.encoding_size = encoding_size
        self.feature_transform = feature_transform
        self.dropout_rate = dropout_rate
        self.out_class_activation = out_class_activation
        self.out_reg_activation = out_reg_activation
        self.class_neurons = class_neurons
        self.seg_kernels = seg_kernels

    def create_model(self):
        inputs = tf.keras.Input(shape=(self.n_points, self.grid_size))

        if self.input_setup == 'both':
            inputs_2 = tf.keras.Input(shape=[self.n_features, ])
        else:
            inputs_2 = None

        x = t_network(inputs, self.grid_size, orto_reg=self.orto_reg)
        x = conv_bn(x, 64)
        x = conv_bn(x, 64)
        if self.feature_transform:
            x = t_network(x, 64, orto_reg=self.orto_reg)
        feat_1 = x
        x = conv_bn(x, 64)
        x = conv_bn(x, 128)
        x = conv_bn(x, self.encoding_size)
        y = tf.keras.layers.GlobalMaxPooling1D()(x)

        if self.input_setup == 'both':
            y = tf.keras.layers.concatenate([inputs_2, y])

        if self.setup == 'seg':
            if self.input_setup == 'both':
                x = tf.keras.layers.Reshape((1, self.encoding_size + self.n_features))(y)
            else:
                x = tf.keras.layers.Reshape((1, self.encoding_size))(y)

            x = tf.keras.layers.Lambda(exp_dim, arguments={'num_points': self.n_points})(x)

            # point_net_seg
            x = tf.keras.layers.concatenate([feat_1, x])
            x = conv_bn(x, self.seg_kernels[0])
            x = conv_bn(x, self.seg_kernels[1])
            x = conv_bn(x, self.seg_kernels[2])
            x = conv_bn(x, self.seg_kernels[3])
            outputs = tf.keras.layers.Dense(self.n_fields,
                                            name="output_fields",
                                            activation=self.out_reg_activation)(x)

            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2], outputs=outputs, name="PointNet")

        elif self.setup == 'class':
            x = dense_bn(y, self.class_neurons[0])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)
            x = dense_bn(x, self.class_neurons[1])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)

            outputs = tf.keras.layers.Dense(self.n_scalars,
                                            activation=self.out_class_activation,
                                            name='output_scalars')(x)
            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2], outputs=outputs, name="PointNet")

        elif self.setup == 'both':
            if self.input_setup == 'both':
                x = tf.keras.layers.Reshape((1, self.encoding_size +self.n_features))(y)
            else:
                x = tf.keras.layers.Reshape((1, self.encoding_size))(y)
            x = tf.keras.layers.Lambda(exp_dim, arguments={'num_points': self.n_points})(x)

            # point_net_seg
            x = tf.keras.layers.concatenate([feat_1, x])
            x = conv_bn(x, self.seg_kernels[0])
            x = conv_bn(x, self.seg_kernels[1])
            x = conv_bn(x, self.seg_kernels[2])
            x = conv_bn(x, self.seg_kernels[3])
            outputs_seg = tf.keras.layers.Dense(self.n_fields,
                                                name="output_fields",
                                                activation=self.out_reg_activation)(x)
            x = dense_bn(y, self.class_neurons[0])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)
            x = dense_bn(x, self.class_neurons[1])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)

            outputs_class = tf.keras.layers.Dense(self.n_scalars,
                                                  activation=self.out_class_activation,
                                                  name='output_scalars')(x)
            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=[outputs_seg, outputs_class], name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2],
                                            outputs=[outputs_seg, outputs_class],
                                            name="PointNet")

        return self.model

    def model_2_image(self, path: str = ''):
        tf.keras.utils.plot_model(self.model, os.path.join(os.getcwd(),
                                                           path, 'PointNet' +
                                                           date.today().strftime("_%d_%m_%Y") +
                                                           '.png'),
                                  show_shapes=True,
                                  show_dtype=True,
                                  show_layer_names=True,
                                  rankdir="TB",
                                  expand_nested=True,
                                  dpi=96,
                                  layer_range=None,
                                  )
