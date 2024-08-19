import tensorflow as tf
import constants

@tf.function
def agent_learn(experiences, q, target_q, optimizer):
    with tf.GradientTape() as tape:
        states, actions, rewards, next_states, done_vals = experiences
        # Compute max Q^(s,a)
        max_qsa = tf.reduce_max(target_q(next_states), axis=-1)
        # Set y = R if episode terminates, otherwise set y = R + γ max Q^(s,a).
        y_targets = rewards + ((1 - done_vals) * (constants.GAMMA * max_qsa))
        # Get the q_values and reshape to match y_targets
        q_values = q(states)
        reshaped_actions = tf.stack([tf.cast(actions, tf.int32)], axis=-1)
        q_values = tf.gather_nd(q_values, reshaped_actions)
        # Compute the loss
        loss = tf.keras.losses.MSE(y_targets, q_values)
        # Get the gradients of the loss with respect to the weights.
        gradients = tape.gradient(loss, q.trainable_variables)
        # Update the weights of the q_network.
        optimizer.apply_gradients(zip(gradients, q.trainable_variables))
        # update the weights of target q_network
        for target_weights, q_net_weights in zip(target_q.weights, q.weights):
            target_weights.assign(constants.TAU * q_net_weights + (1.0 - constants.TAU) * target_weights)