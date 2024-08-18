import tensorflow as tf
import constants

def DeepQNetwork():
    q_network = tf.keras.Sequential([
        tf.keras.layers.Conv2D(128, (4,4), input_shape=(constants.STATE_SIZE), activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])

    opt = tf.keras.optimizers.Adam(learning_rate=constants.ALPHA)
    q_network.compile(loss="mse", optimizer=opt)
    
    return q_network