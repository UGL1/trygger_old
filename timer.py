from time import perf_counter_ns


class Timer:

    def __init__(self, duration: int):
        """        
        :param duration: int in milliseconds
        """
        self.duration = duration * 10 ** 6
        self.is_running = False
        self.last_time_reset = perf_counter_ns()

    def start(self, duration=None) -> None:
        """
        Starts the timer
        
        :param duration: int in milliseconds
        """
        self.last_time_reset = perf_counter_ns()
        self.is_running = True
        if duration:
            self.duration = duration * 10 ** 6

    def duration(self) -> float:
        """
        Returns timer's duration
        """
        return self.duration / 10 ** 6

    def stop(self) -> None:
        """
        Stops the timer
        """
        self.is_running = False

    def has_expired(self, delay=False) -> bool:
        """
        If delay is not set, returns True or False depending on current time.
        
        If set, returns the same and a duration (positive if late, negative if early).
       
        :param delay: bool
        """
        if not delay:
            return self.is_running and perf_counter_ns() - self.last_time_reset >= self.duration
        else:
            return self.is_running and perf_counter_ns() - self.last_time_reset >= self.duration, (
                    self.is_running and perf_counter_ns() - self.last_time_reset - self.duration) / 10 ** 6
