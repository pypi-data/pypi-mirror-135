#!/usr/bin/env python3
#
# Copyright 2022 Jonathan L. Komar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import sys
import logging
from typing import Callable
logger = logging.getLogger('Result')

class Result():
  """Carrier monad of a value, result, and error message
  """

  @classmethod
  def of(cls, value, errorMsg="default empty value message"):
    """Factory method.

    """
    logger.debug("Result.of({}, errorMsg=\"{}\")".format(value, errorMsg))
    if value is None:
      return Result.failure(errorMsg)
    try:
      return cls(value)
    except Exception as e:
      return Result.failure(e)

  @classmethod
  def success(cls, value):
    logger.debug("Result.success({}) called.".format(repr(value)))
    return Result(value)

  @classmethod
  def failure(cls, errorMsg="default error message"):
    logger.debug("Result.failure({}) called.".format(errorMsg))
    return Result(errorMsg, failed=True)

  @classmethod
  def empty(cls):
    return Result.success(None)
  #empty = Result.empty()

  def __init__(self, value, failed=False):
    self.value = value
    self.failed = failed
    logger.debug("Result.__init__({}, failed={})".format(repr(value), failed))

  def get(self):
    if self.isFailure() is True:
      return AttributeError("Cannot call get on failure: {}".format(self.value))
    return self.value

  def successValue(self):
    return self.get()

  def isFailure(self):
    if self.failed == True:
      return True
    else:
      return False

  def map(self, f):
    """ f: A -> B
    returns M<B>
    Because the function f passed in returns a B not in a computational context (monad),
    we must explicitly wrap its output, because the map function must return
    a value within a computational context (monad).
    """
    if self.isFailure() is True:
      logger.debug("map detected failure, returning {}".format(repr(self)))
      return self
    try:
      # java: return Result.success((f.apply(successValue()))
      logger.debug("map({}) called.".format(f))
      r = Result.success(f(self.successValue()))
      logger.debug("map succeeded, returning {} of type({})".format(r, repr(r)))
      return r
    except Exception as e:
      logger.debug("map() caught exception. returning failure: {}".format(repr(e)))
      #e = sys.exc_info()[0]
      return Result.failure("{}::{}".format(repr(e),sys.exc_info()[0]))

  def bind(self, f):
    """ f: A -> M<B> 
    returns M<B>
    Because the function f returns a value within a computational context already,
    we could handle function application separate from map, but instead we run
    it through map so that it gets doubly wrapped M<M<B>>. We then unwrap it with
    getOrElse using a default value of Result.empty.
    """
    if self.isFailure() == True:
      logger.debug("bind/flatMap detected failure, returning {}".format(repr(self)))
      return self
    try:
      # Java: return map(f).getOrElse(Option::none)
      logger.debug("flatMap/bind succeeded, detected isFailure() == False")
      step1 = self.map(f) # yields Result<Result<A>>
      logger.debug("flatMap/bind self.map yielded value {} of type {}.".format(repr(step1.get()), type(step1.get())))
      r = step1.getOrElse(Result.empty()) # unwraps outer Result yields Result<A>
      logger.debug("flatMap returning {} of type {}".format(r, type(r)))
      return r
    except Exception as e:
      logger.debug("flatMap/bind failed, returning {} of type {}".format(e, type(e)))
      return Result.failure("{}::{}".format(repr(e), sys.exc_info()[0]))

  def flatMap(self, f):
    return self.bind(f)

  def getOrElse(self, defaultValue):
    if self.isFailure() == True:
      if callable(defaultValue):
        return defaultValue()
      return defaultValue
    else:
      return self.successValue()

  def getOrException(self):
    logger.debug("Result.getOrException called: isFailure: {}".format(self.isFailure()))
    if self.isFailure() == True:
      raise Exception(self.value) 
    return self.get()

  def orElse(self, defaultValue):
    """Defined ad-hoc but could be designed in terms of map and get_or_else
    """
    logger.debug("orElse called with {}".format(defaultValue))
    if self.isFailure() is True:
      if callable(defaultValue):
        evaluated = defaultValue()
        assert isinstance(evaluated, Result), ("defaultValue must be a function from None -> Result<A> or a Result<A>. It is a {}".format(str(type(evaluated))))
        logger.debug("orElse returning default: {}".format(evaluated))
        return evaluated
      assert isinstance(defaultValue, Result), ("defaultValue must be a function from None -> Result<A> or a Result<A>. It is a {}".format(str(type(defaultValue))))
      logger.debug("orElse returning default: {}".format(defaultValue))
      return defaultValue
    logger.debug("orElse returning unmodified input: {}".format(self))
    return self

  def forEach(self, effect:Callable):
    if self.isFailure() == True:
      pass
    effect(self.value)

  def forEachOrFail(self, effect:Callable):
    if self.isFailure() == True:
      return Result.success(self)
    effect(self.value)

  def __or__(self, f):
    """Override the or operator symbol (|) to call bind/flat_map.
       answer = Result.of('1') | int | neg | str
    """
    return self.bind(f)

  def __str__(self):
    return 'Result({}, failed={})'.format(str(self.value), str(self.failed))

  def __repr__(self):
    return "{}(value={}, failed={})".format(type(self).__name__, repr(self.value), self.failed)

  def __eq__(self, o):
    return isinstance(o, type(self)) and o.value == self.value

  
  
