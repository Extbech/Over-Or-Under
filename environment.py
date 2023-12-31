from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.environments import utils
import numpy as np


class OverOrUnderEnv(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=1, name="action"
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=0, name="observation"
        )
        self._state = 0
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = 0
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.int32))

    def _step(self, action):
        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        # Make sure episodes don't go on forever.
        if action == 1:
            self._episode_ended = True
        elif action == 0:
            new_card = np.random.randint(1, 11)
            self._state += new_card
        else:
            raise ValueError("`action` should be 0 or 1.")

        if self._episode_ended or self._state >= 21:
            reward = self._state - 21 if self._state <= 21 else -21
            return ts.termination(np.array([self._state], dtype=np.int32), reward)
        else:
            return ts.transition(
                np.array([self._state], dtype=np.int32), reward=0.0, discount=1.0
            )


if __name__ == "__main__":
    get_new_card_action = np.array(0, dtype=np.int32)
    end_round_action = np.array(1, dtype=np.int32)

    environment = OverOrUnderEnv()
    time_step = environment.reset()
    print(time_step)
    cumulative_reward = time_step.reward

    for _ in range(3):
        time_step = environment.step(get_new_card_action)
        print(time_step)
        cumulative_reward += time_step.reward

    time_step = environment.step(end_round_action)
    print(time_step)
    cumulative_reward += time_step.reward
    print("Final Reward = ", cumulative_reward)
