RateLimiting
=======

[![Build Status](https://travis-ci.org/icecrime/RateLimiting.png)](https://travis-ci.org/icecrime/RateLimiting)

Simple Python module providing rate limiting.

Overview
-------------

This package provides the `ratelimiting` module, which ensures that an
operation will not be executed more than a given number of times on a given
period. This can prove useful when working with third parties APIs which
require for example a maximum of 10 requests per second.

Usage
-------------

Decorator flavor:

    >>> from ratelimiting import RateLimiting
    >>> @RateLimiting(max_calls=10, period=1.0)
    ... def do_something():
    ...     pass
    ...

Context manager flavor:

    >>> from ratelimiting import RateLimiting
    >>> rate_limiter = RateLimiting(max_calls=10, period=1.0)
    >>> for i in range(100):
    ...     with rate_limiter:
    ...         do_something()
    ...

Using with callback:

    >>> from ratelimiting import RateLimiting
    >>> import time
    >>> def limited(until):
    ...     duration = int(round(until - time.time()))
    ...     print('Rate limited, sleeping for %d seconds' % duration)
    ...
    >>> rate_limiter = RateLimiting(max_calls=2, period=3, callback=limited)
    >>> for i in range(3):
    ...     with rate_limiter:
    ...         print('Iteration', i)
    ...
    Iteration 0
    Iteration 1
    Rate limited, sleeping for 3 seconds
    Iteration 2

License
-------------

Copyright 2013 Arnaud Porterie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
