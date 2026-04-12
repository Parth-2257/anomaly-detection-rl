# Core environment logic

from env.tasks import load_all_tasks
from env.grader import grade


class Environment:
    def __init__(self, difficulty="easy"):
        self.tasks = load_all_tasks(difficulty)
        self.current_index = 0
        self.current_task = None

        self.total_reward = 0
        self.steps_done = 0
        self.total_steps = len(self.tasks)

    def reset(self):
        self.current_index = 0
        self.total_reward = 0
        self.steps_done = 0

        self.current_task = self.tasks[self.current_index]
        return self.current_task["input"]

    def step(self, action):
        truth = self.current_task

        reward = grade(action, truth)

        self.total_reward += reward
        self.steps_done += 1

        self.current_index += 1
        done = self.current_index >= len(self.tasks)

        if not done:
            self.current_task = self.tasks[self.current_index]
            next_state = self.current_task["input"]
        else:
            next_state = None

        info = {
            "truth": truth,
            "reward": reward,
            "total_reward": self.total_reward,
            "steps_done": self.steps_done,
            "total_steps": self.total_steps
        }

        return next_state, reward, done, info

    def get_state(self):
        return {
            "current_index": self.current_index,
            "steps_done": self.steps_done,
            "total_reward": self.total_reward
        }


