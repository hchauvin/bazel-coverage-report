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

import io
import re
import subprocess
import sys
import unittest

from report import report

class LcovParseException(Exception):
    pass

def parse_cov(lcov_lines, with_zero=False):
  """Parse code coverage data into coverage results per source node.
  Use lcov and linecount data to create a map of source nodes to
  corresponding total and tested line counts.
  Args:
    lcov_lines: Lines within the lcov file.
  Returns:
    List of strings with comma separated source node and coverage.
  """
  files = {}
  for line in lcov_lines:
    line = line.strip()

    # Set the current srcfile name for a new src file declaration.
    if line[:len('SF:')] == 'SF:':
      lines = {}
      functions = {}
      srcfile_name = line[len('SF:'):]

    if line[:len('DA:')] == 'DA:':
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
        "lines": lines,
      }

  if len(files) == 0:
    raise LcovParseException("no coverage info was found")

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

  def assertCoverage(self, lcov_path=None, lcov_lines=None, files=None, functions=None, lines=None):
    close_here = False
    if not lcov_lines:
      lcov_stream = open(lcov_path, 'r')
      lcov_lines = lcov_stream.readlines()
      close_here = True
    lcov = parse_cov(lcov_lines)
    if functions:
      actual_functions = {}
      for file in lcov:
        actual_functions.update(lcov[file]["functions"])
      self.assertDictEqual(functions, actual_functions)
    if lines:
      actual_lines = {}
      for file in lcov:
        actual_lines[file] = lcov[file]["lines"]
      self.assertDictEqual(lines, actual_lines)
    if files:
      actual_files = lcov.keys()
      self.assertSetEqual(set(files), set(actual_files))
    if close_here:
      lcov_stream.close()

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
    if sys.platform == "darwin":
      # Until issue in Bazel is resolved, see clang/BUILD
      return

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

    cov = self.coverage([
      "//clang:foo_test",
    ], ["--instrumentation_filter=//clang:foo"])
    self.assertCoverage(
      cov["//clang:foo_test"],
      functions = {
        "foo": 1,
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

  def test_golang(self):
    cov = self.coverage([
      "//go/bar:go_default_test",
    ], ["--instrumentation_filter=//go/bar"])
    with open(cov["//go/bar:go_default_test"], 'r') as cp:
      self.assertCoverage(
        lcov_lines = report.Coverprofile(cp).to_lcov(),
        lines = {
          "github.com/hchauvin/bazel-coverage-example/go/bar/bar.go": {
            '21': 1,
            '22': 1,
            '23': 1,
          },
        },
      )

    cov = self.coverage([
      "//go/foo:go_default_test",
    ], ["--instrumentation_filter=//go/foo"])
    with open(cov["//go/foo:go_default_test"], 'r') as cp:
      self.assertCoverage(
        lcov_lines = report.Coverprofile(cp).to_lcov(),
        lines = {
          "github.com/hchauvin/bazel-coverage-example/go/foo/foo.go": {
            '17': 1,
            '18': 1,
            '19': 1,
          },
        },
      )

    cov_transitive = self.coverage([
      "//go/bar:go_default_test",
    ], ["--instrumentation_filter=//go/bar,//go/foo"])
    with open(cov_transitive["//go/bar:go_default_test"], 'r') as cp:
      self.assertCoverage(
        lcov_lines = report.Coverprofile(cp).to_lcov(),
        lines = {
          "github.com/hchauvin/bazel-coverage-example/go/bar/bar.go": {
            '21': 1,
            '22': 1,
            '23': 1,
          },
          "github.com/hchauvin/bazel-coverage-example/go/foo/foo.go": {
            '17': 1,
            '18': 1,
            '19': 1,
          },
        },
      )

    cov_cumulative = self.coverage([
      "//go/...",
    ], ["--instrumentation_filter=//go/bar,//go/foo"])
    with open(cov_cumulative["//go/bar:go_default_test"], 'r') as cp:
      self.assertCoverage(
        lcov_lines = report.Coverprofile(cp).to_lcov(),
        lines = {
          "github.com/hchauvin/bazel-coverage-example/go/bar/bar.go": {
            '21': 1,
            '22': 1,
            '23': 1,
          },
          "github.com/hchauvin/bazel-coverage-example/go/foo/foo.go": {
            '17': 1,
            '18': 1,
            '19': 1,
          },
        },
      )
    with open(cov_cumulative["//go/foo:go_default_test"], 'r') as cp:
      self.assertCoverage(
        lcov_lines = report.Coverprofile(cp).to_lcov(),
        lines = {
          "github.com/hchauvin/bazel-coverage-example/go/foo/foo.go": {
            '17': 1,
            '18': 1,
            '19': 1,
          },
        },
      )


if __name__ == '__main__':
  unittest.main()