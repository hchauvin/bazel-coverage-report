#!/usr/bin/env python

# Copyright 2018 The Bazel Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Parts come from
# https://chromium.googlesource.com/chromium/src/tools/code_coverage/+/6396ef11b54bfd45543870f33cea3e801f41d036/process_coverage.py
#
# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import re
import subprocess
import unittest

class LcovParseException(Exception):
    pass

def parse_cov(lcov_path, with_lines=False, with_zero=False):
  """Parse code coverage data into coverage results per source node.
  Use lcov and linecount data to create a map of source nodes to
  corresponding total and tested line counts.
  Args:
    lcov_path: File path to lcov coverage data.
  Returns:
    List of strings with comma separated source node and coverage.
  """
  lcov_file = open(lcov_path, 'r')
  files = {}
  for line in lcov_file:
    line = line.strip()

    # Set the current srcfile name for a new src file declaration.
    if line[:len('SF:')] == 'SF:':
      lines = {}
      functions = {}
      srcfile_name = line[len('SF:'):]

    if with_lines and line[:len('DA:')] == 'DA:':
      line_info = line[len('DA:'):].split(',')
      if len(line_info) != 2:
        raise LcovParseException('DA: line format unexpected - %s' % line)
      (line_num, exec_count) = line_info
      exec_count = int(exec_count)
      if with_zero or exec_count > 0:
        lines[line_num] = exec_count

    if line[:len('FNDA:')] == 'FNDA:':
      line_info = line[len('FNDA:'):].split(',')
      if len(line_info) != 2:
        raise LcovParseException('DA: line format unexpected - %s' % line)
      (executed, function_name) = line_info
      executed = int(executed)
      if with_zero or executed > 0:
        functions[function_name] = executed
    
    # Update results for the current src file at record end.
    if line == 'end_of_record':
      files[srcfile_name] = {
        "functions": functions,
      }
      if with_lines:
        files[srcfile_name]["lines"] = lines

  lcov_file.close()
  return files

class CoverageTest(unittest.TestCase):
  def coverage(self, targets, options=[]):
    cmd = [
      "bazel", 
      "coverage", 
    ] + targets + options
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    infos = re.finditer(r"(//[^ ]+)[^\n]+\n +([^\n]+)", out)
    ans = {}
    for info in infos:
      target = info.group(1)
      ans[target] = info.group(2)
    return ans

  def assertCoverage(self, lcov_path, files=None, functions=None):
    lcov = parse_cov(lcov_path)
    if functions:
      actual_functions = {}
      for file in lcov:
        actual_functions.update(lcov[file]["functions"])
      self.assertDictEqual(functions, actual_functions)
    if files:
      actual_files = lcov.keys()
      self.assertSetEqual(set(files), set(actual_files))

  def test_java_examples(self):
    cov = self.coverage([
      "//jvm:java_ExampleATest", 
      "//jvm:java_ExampleBTest", 
      "//jvm:java_ExampleCTest",
    ], ["--instrumentation_filter=//jvm:java"])
    self.assertCoverage(cov["//jvm:java_ExampleATest"], functions = {
      "com/github/hchauvin/bazelcoverageexample/Foo::exampleA ()Ljava/lang/String;": 1,
    })
    self.assertCoverage(cov["//jvm:java_ExampleBTest"], functions = {
      "com/github/hchauvin/bazelcoverageexample/Foo::exampleB ()Ljava/lang/String;": 1,
    })
    self.assertCoverage(cov["//jvm:java_ExampleCTest"], functions = {
      "com/github/hchauvin/bazelcoverageexample/Foo::exampleA ()Ljava/lang/String;": 1,
      "com/github/hchauvin/bazelcoverageexample/Foo::exampleB ()Ljava/lang/String;": 1,
      "com/github/hchauvin/bazelcoverageexample/Foo::exampleC ()Ljava/util/List;": 1,
    })

  def test_java_examples_transitive(self):
    cov = self.coverage([
      "//jvm:java_Foo2ExampleATest",
    ], ["--instrumentation_filter=//jvm:java2"])
    self.assertCoverage(cov["//jvm:java_Foo2ExampleATest"], functions = {
      "com/github/hchauvin/bazelcoverageexample/Foo2::exampleA ()Ljava/lang/String;": 1,
    })

    cov_transitive = self.coverage([
      "//jvm:java_Foo2ExampleATest",
    ], ["--instrumentation_filter=//jvm"])
    self.assertCoverage(
      cov_transitive["//jvm:java_Foo2ExampleATest"],
      files = {
        "com/github/hchauvin/bazelcoverageexample/Foo.java",
        "com/github/hchauvin/bazelcoverageexample/Foo2.java",
      },
      functions = {
        "com/github/hchauvin/bazelcoverageexample/Foo::exampleA ()Ljava/lang/String;": 1,
        "com/github/hchauvin/bazelcoverageexample/Foo2::exampleA ()Ljava/lang/String;": 1,
      })

  def test_clang(self):
    # NOTE: File names are currently a mess for clang, and not really usable for coverage.
    cov = self.coverage([
      "//clang:bar_test",
    ], ["--instrumentation_filter=//clang:bar"])
    self.assertCoverage(
      cov["//clang:bar_test"],
      functions = {
        "bar": 1,
      },
    )

    cov_transitive = self.coverage([
      "//clang:bar_test",
    ], ["--instrumentation_filter=//clang:bar,//clang:foo"])
    self.assertCoverage(
      cov["//clang:bar_test"],
      functions = {
        "bar": 1,
        "foo": 1,
        "main": 1,
      },
    )


if __name__ == '__main__':
  unittest.main()