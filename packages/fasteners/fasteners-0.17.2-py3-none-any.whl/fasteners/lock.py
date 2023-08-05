# -*- coding: utf-8 -*-

# Copyright (C) 2014 Yahoo! Inc. All Rights Reserved.
# Copyright 2011 OpenStack Foundation.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections
import contextlib
import functools
import threading

from fasteners import _utils


def read_locked(*args, **kwargs):
    """Acquires & releases a read lock around call into decorated method.

    NOTE(harlowja): if no attribute name is provided then by default the
    attribute named '_lock' is looked for (this attribute is expected to be
    a :py:class:`.ReaderWriterLock`) in the instance object this decorator
    is attached to.
    """

    def decorator(f):
        attr_name = kwargs.get('lock', '_lock')

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            rw_lock = getattr(self, attr_name)
            with rw_lock.read_lock():
                return f(self, *args, **kwargs)

        return wrapper

    # This is needed to handle when the decorator has args or the decorator
    # doesn't have args, python is rather weird here...
    if kwargs or not args:
        return decorator
    else:
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator


def write_locked(*args, **kwargs):
    """Acquires & releases a write lock around call into decorated method.

    NOTE(harlowja): if no attribute name is provided then by default the
    attribute named '_lock' is looked for (this attribute is expected to be
    a :py:class:`.ReaderWriterLock` object) in the instance object this
    decorator is attached to.
    """

    def decorator(f):
        attr_name = kwargs.get('lock', '_lock')

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            rw_lock = getattr(self, attr_name)
            with rw_lock.write_lock():
                return f(self, *args, **kwargs)

        return wrapper

    # This is needed to handle when the decorator has args or the decorator
    # doesn't have args, python is rather weird here...
    if kwargs or not args:
        return decorator
    else:
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator


class ReaderWriterLock(object):
    """A reader/writer lock.

    This lock allows for simultaneous readers to exist but only one writer
    to exist for use-cases where it is useful to have such types of locks.

    Currently a reader can not escalate its read lock to a write lock and
    a writer can not acquire a read lock while it is waiting on the write
    lock.

    In the future these restrictions may be relaxed.

    This can be eventually removed if http://bugs.python.org/issue8800 ever
    gets accepted into the python standard threading library...
    """

    #: Writer owner type/string constant.
    WRITER = 'w'

    #: Reader owner type/string constant.
    READER = 'r'

    def __init__(self,
                 condition_cls=threading.Condition,
                 current_thread_functor=None):
        self._writer = None
        self._pending_writers = collections.deque()
        self._readers = {}
        self._cond = condition_cls()
        self._current_thread = threading.current_thread

    @property
    def has_pending_writers(self):
        """Returns if there are writers waiting to become the *one* writer."""
        return bool(self._pending_writers)

    def is_writer(self, check_pending=True):
        """Returns if the caller is the active writer or a pending writer."""
        me = self._current_thread()
        if self._writer == me:
            return True
        if check_pending:
            return me in self._pending_writers
        else:
            return False

    @property
    def owner(self):
        """Returns whether the lock is locked by a writer or reader."""
        if self._writer is not None:
            return self.WRITER
        if self._readers:
            return self.READER
        return None

    def is_reader(self):
        """Returns if the caller is one of the readers."""
        me = self._current_thread()
        return me in self._readers

    @contextlib.contextmanager
    def read_lock(self):
        """Context manager that grants a read lock.

        Will wait until no active or pending writers.

        Raises a ``RuntimeError`` if a pending writer tries to acquire
        a read lock.
        """
        me = self._current_thread()
        if me in self._pending_writers:
            raise RuntimeError("Writer %s can not acquire a read lock"
                               " while waiting for the write lock"
                               % me)
        with self._cond:
            while True:
                # No active writer, or we are the writer;
                # Also no pending writers;
                # we are good to become a reader.
                if self._writer is None or self._writer == me:
                    if me in self._readers:
                        # ok to get a lock if current thread already has one
                        self._readers[me] = self._readers[me] + 1
                        break
                    elif not self.has_pending_writers:
                        self._readers[me] = 1
                        break
                # An active or pending writer; guess we have to wait.
                self._cond.wait()
        try:
            yield self
        finally:
            # I am no longer a reader, remove *one* occurrence of myself.
            # If the current thread acquired two read locks, then it will
            # still have to remove that other read lock; this allows for
            # basic reentrancy to be possible.
            with self._cond:
                try:
                    me_instances = self._readers[me]
                    if me_instances > 1:
                        self._readers[me] = me_instances - 1
                    else:
                        self._readers.pop(me)
                except KeyError:
                    pass
                self._cond.notify_all()

    @contextlib.contextmanager
    def write_lock(self):
        """Context manager that grants a write lock.

        Will wait until no active readers. Blocks readers after acquiring.

        Guaranteed for locks to be processed in fair order (FIFO).

        Raises a ``RuntimeError`` if an active reader attempts to acquire
        a lock.
        """
        me = self._current_thread()
        i_am_writer = self.is_writer(check_pending=False)
        if self.is_reader() and not i_am_writer:
            raise RuntimeError("Reader %s to writer privilege"
                               " escalation not allowed" % me)
        if i_am_writer:
            # Already the writer; this allows for basic reentrancy.
            yield self
        else:
            with self._cond:
                self._pending_writers.append(me)
                while True:
                    # No readers, and no active writer, am I next??
                    if len(self._readers) == 0 and self._writer is None:
                        if self._pending_writers[0] == me:
                            self._writer = self._pending_writers.popleft()
                            break
                    self._cond.wait()
            try:
                yield self
            finally:
                with self._cond:
                    self._writer = None
                    self._cond.notify_all()


@contextlib.contextmanager
def try_lock(lock):
    """Attempts to acquire a lock, and auto releases if acquired (on exit)."""
    # NOTE(harlowja): the keyword argument for 'blocking' does not work
    # in py2.x and only is fixed in py3.x (this adjustment is documented
    # and/or debated in http://bugs.python.org/issue10789); so we'll just
    # stick to the format that works in both (oddly the keyword argument
    # works in py2.x but only with reentrant locks).
    was_locked = lock.acquire(False)
    try:
        yield was_locked
    finally:
        if was_locked:
            lock.release()


def locked(*args, **kwargs):
    """A locking **method** decorator.

    It will look for a provided attribute (typically a lock or a list
    of locks) on the first argument of the function decorated (typically this
    is the 'self' object) and before executing the decorated function it
    activates the given lock or list of locks as a context manager,
    automatically releasing that lock on exit.

    NOTE(harlowja): if no attribute name is provided then by default the
    attribute named '_lock' is looked for (this attribute is expected to be
    the lock/list of locks object/s) in the instance object this decorator
    is attached to.

    NOTE(harlowja): a custom logger (which will be used if lock release
    failures happen) can be provided by passing a logger instance for keyword
    argument ``logger``.
    """

    def decorator(f):
        attr_name = kwargs.get('lock', '_lock')
        logger = kwargs.get('logger')

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, (tuple, list)):
                with _utils.LockStack(logger=logger) as stack:
                    for i, lock in enumerate(attr_value):
                        if not stack.acquire_lock(lock):
                            raise threading.ThreadError("Unable to acquire"
                                                        " lock %s" % (i + 1))
                    return f(self, *args, **kwargs)
            else:
                lock = attr_value
                with lock:
                    return f(self, *args, **kwargs)

        return wrapper

    # This is needed to handle when the decorator has args or the decorator
    # doesn't have args, python is rather weird here...
    if kwargs or not args:
        return decorator
    else:
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator
