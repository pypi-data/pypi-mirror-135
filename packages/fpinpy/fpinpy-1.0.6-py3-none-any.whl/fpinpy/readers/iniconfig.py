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
from fpinpy.result import Result
import typing
import configparser
import logging
logger = logging.getLogger('IniConfigReader')

class IniConfigReader():
  def __init__(self, configFileName:str):
    self.config = self.readConfig(configFileName)

  def readConfig(self, configFileName:str) -> Result:
    try:
      parser = configparser.ConfigParser()
      parser.read(configFileName)
      return Result.of(parser)
    except Exception as e:
      return Result.failure(e)

  def getProperty(self, section:str, key:str) -> Result:
    try:
      return self.config.map(lambda parser: parser.get(section, key))
    except Exception as e:
      return Result.failure("Could not get value for section {} key {}".format(section, key))

  def readSection(self, section:str) -> Result: # Result<configparser>
    r = self.config.map(lambda parser: parser.get(section))

  def __str__(self):
    return "{}({})".format(__name__, self.config)
