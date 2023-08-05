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
import abc
from fpinpy.meta.decorators import overrides
from fpinpy.meta import caller
from typing import Iterator, TypeVar, Generic, Callable
# Declare module-scoped type variables for generics
T = TypeVar('T')
U = TypeVar('U')

class SinglyLinkedList(abc.ABC, Generic[T]):
    """
    """

    @staticmethod
    def list(*args):
        if len(args) == 0:
            return SinglyLinkedList.nil()
        else:
            output = SinglyLinkedList.nil()
            for i in range(len(args)-1, -1, -1):
                output = Cons(args[i], output)
            return output 

    @staticmethod
    def nil():
        return Nil()

    @staticmethod
    def cons(head: T, tail):# Tail is Cons[T]
        return Cons(head, tail)

    @abc.abstractmethod
    def head(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def tail(self):# -> SinglyLinkedList[T]
        raise NotImplementedError

    @abc.abstractmethod
    def isEmpty(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def setHead():# -> SinglyLinkedList[T]
        raise NotImplementedError

#    @abc.abstractmethod
#    def length() -> int:
#        raise NotImplementedError

    @abc.abstractmethod
    def foldLeft(self, identity: U, function: Callable[[U, T], U]):
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

class Nil(SinglyLinkedList[T]):
    """Represents empty list.
    """
    def __new__(cls, *args, **kwargs):
        if caller() != "nil":
            raise RuntimeError(f"Prefer SinglyLinkedList.nil() for instantiatiation.  You used {caller()}.")
        return object.__new__(cls)

    @overrides(SinglyLinkedList)
    def head(self) -> T:
        raise RuntimeError("head called on empty list")

    @overrides(SinglyLinkedList)
    def tail(self) -> SinglyLinkedList[T]:
        raise RuntimeError("tail called on empty list")

    @overrides(SinglyLinkedList)
    def isEmpty(self) -> bool:
        return True

    @overrides(SinglyLinkedList)
    def setHead(self, element: T):# -> SinglyLinkedList[T]
        raise RuntimeError("setHead called on empty list.")

    @overrides(SinglyLinkedList)
    def foldLeft(self, identity: U, function: Callable[[U, T], U]):# TODO add out type
        return self
    
    @overrides(SinglyLinkedList)
    def __str__(self):
        return "[NIL]"
    
class Cons(SinglyLinkedList[T]):
    """Represents non-empty list.
    """
    def __new__(cls, *args, **kwargs):
        if caller() != "list":
            raise RuntimeError(f"Prefer SinglyLinkedList.cons() for instantiatiation.  You used {caller()}.")
        return object.__new__(cls)

    def __init__(self,
                 head: T,
                 tail: SinglyLinkedList[T]):
        self._head = head
        assert isinstance(tail, Cons) or isinstance(tail, Nil), f"Type was {type(tail)} but should have been Cons or Nil"
        self._tail = tail

    @overrides(SinglyLinkedList)
    def head(self) -> T:
        return self._head

    @overrides(SinglyLinkedList)
    def tail(self) -> SinglyLinkedList[T]:
        return self._tail
        
    @overrides(SinglyLinkedList)
    def isEmpty(self) -> bool:
        return False

    @overrides(SinglyLinkedList)
    def setHead(self, element: T):# -> SinglyLinkedList[T]
        return SinglyLinkedList.list(element, self.tail())

    @overrides(SinglyLinkedList)
    def foldLeft(self, identity: U, function: Callable[[U, T], U]) -> U:
        """ Implemented imperatively as technique to too many stack calls.
        """
        accumulator = identity
        tmpHead = self.head()
        tmpList = self.tail()
        while not tmpList.isEmpty():
            accumulator = function(accumulator, tmpHead)
            tmpHead = tmpList.head()
            tmpList = tmpList.tail()
        accumulator = function(accumulator, tmpHead)
        return accumulator
        #def _foldLeft(acc: U, lst: SinglyLinkedList[T]):
        #    if lst.isEmpty():
        #        return acc
        #    else:
        #        return _foldLeft(function(acc, lst.head()), lst.tail())
        #return _foldLeft(identity, self)

    @overrides(SinglyLinkedList)
    def __str__(self) -> str:
        accumulator = ""
        def toString(accumulator: str, aList: SinglyLinkedList) -> str:
            if aList.isEmpty():
                return accumulator
            else:
                accumulator = accumulator.__add__(str(aList.head())).__add__(", ")
                return toString(accumulator , aList.tail())
        return f"[{toString(accumulator, self)}NIL]"
