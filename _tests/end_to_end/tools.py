from functools import partial
from kivy.clock import Clock


def without_schedule_seconds(function):
        def inner(*args, **kwargs):
                function(*args[:-1], **kwargs)

        return inner

def simulate(function):
        def simulate_inner(simulator, params):
                simulator.start(function, params or {})
        return simulate_inner


def execution_step(function):
        def execution_step_inner(self, *args, **kwargs):
                self.execution_queue.append((function, args, kwargs))

        return execution_step_inner
