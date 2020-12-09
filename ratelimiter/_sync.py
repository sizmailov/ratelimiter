# -*- coding: utf-8 -*-

import time
import functools
import threading


class RateLimiter(object):

    """Provides rate limiting for an operation with a configurable number of
    requests for a time period.
    """

    def __init__(self, max_calls, period=1.0, callback=None):
        """Initialize a RateLimiter object which enforces as much as max_calls
        operations on period (eventually floating) number of seconds.
        """
        if period <= 0:
            raise ValueError('Rate limiting period should be > 0')
        if max_calls <= 0:
            raise ValueError('Rate limiting number of calls should be > 0')

        self.calls = []

        self.period = period
        self.max_calls = max_calls
        self.callback = callback
        self._lock = threading.Lock()
        self._alock = None

        # Lock to protect creation of self._alock
        self._init_lock = threading.Lock()

    def __call__(self, f):
        """The __call__ function allows the RateLimiter object to be used as a
        regular function decorator.
        """
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                return f(*args, **kwargs)
        return wrapped

    def __enter__(self):
        with self._lock:
            # We want to ensure that no more than max_calls were run in the allowed
            # period. For this, we store the last timestamps of each call and run
            # the rate verification upon each __enter__ call.

            now = time.time()
            self.calls = [
                t
                for t in self.calls
                if t + self.period >= now
            ]

            if len(self.calls) >= self.max_calls:
                until = self.calls[0] + self.period
                if self.callback:
                    t = threading.Thread(target=self.callback, args=(until,))
                    t.daemon = True
                    t.start()
                sleeptime = until - now
                if sleeptime > 0:
                    time.sleep(sleeptime)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._lock:
            # Store the last operation timestamp.
            self.calls.append(time.time())