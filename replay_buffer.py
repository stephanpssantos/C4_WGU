import random
import numpy as np
import tensorflow as tf
from collections import deque, namedtuple
import constants

class ReplayBuffer:
    def __init__(self, buffer_size, mini_batch_size):
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.memory_buffer = deque(maxlen=buffer_size)
        self.temp_buffer = deque(maxlen=1000)
        self.mini_batch_size = mini_batch_size
        
    def append(self, prev_observation, prev_action, reward, observation, termination):
        self.temp_buffer.append(self.experience(prev_observation, prev_action, reward, observation, termination))

    def commit(self, reward):
        for i, exp_tuple in enumerate(reversed(self.temp_buffer)):
            updated_tuple = exp_tuple._replace(reward=reward)
            self.temp_buffer[i] = updated_tuple
            reward *= constants.GAMMA

        self.memory_buffer += self.temp_buffer
        self.temp_buffer.clear()

    def check_update_conditions(self):
        if len(self.memory_buffer) > self.mini_batch_size:
            return True
        else:
            return False
        
    def get_experiences(self):
        experiences = random.sample(self.memory_buffer, k=self.mini_batch_size)

        states = tf.convert_to_tensor(
            np.array([e.state for e in experiences if e is not None]), dtype=tf.float32
        )
        actions = tf.convert_to_tensor(
            np.array([e.action for e in experiences if e is not None]), dtype=tf.float32
        )
        rewards = tf.convert_to_tensor(
            np.array([e.reward for e in experiences if e is not None]), dtype=tf.float32
        )
        next_states = tf.convert_to_tensor(
            np.array([e.next_state for e in experiences if e is not None]), dtype=tf.float32
        )
        done_vals = tf.convert_to_tensor(
            np.array([e.done for e in experiences if e is not None]).astype(np.uint8),
            dtype=tf.float32,
        )

        return (states, actions, rewards, next_states, done_vals)