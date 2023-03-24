from time import perf_counter_ns


class Timer:

    def __init__(self, duration: int):
        self.duration = duration * 10 ** 6
        self.is_running = False
        self.last_time_reset = perf_counter_ns()

    def start(self, duration: int = 0) -> None:
        self.last_time_reset = perf_counter_ns()
        self.is_running = True
        if duration != 0:
            self.duration = duration * 10 ** 6

    def get_duration(self) -> float:
        return self.duration // 10 ** 6

    def set_duration(self, duration: float) -> None:
        self.duration = duration * 10 ** 6

    def stop(self) -> None:
        self.is_running = False

    def has_expired(self) -> bool:
        return not self.is_running or perf_counter_ns() - self.last_time_reset >= self.duration
