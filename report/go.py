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
"""Temporary bridge to `rules_go` coverage representation.

Currently, `rules_go` reports in coverprofile, not in LCOV format."""

# This is inspired by Golang package golang.org/x/tools/cover.

import re


class GoCoverprofileParseException(Exception):
  """Raised when the parsing of a coverprofile fails."""
  pass


_line_re = re.compile(
    r"^(.+):([0-9]+).([0-9]+),([0-9]+).([0-9]+) ([0-9]+) ([0-9]+)$")


class Coverprofile(object):  # pylint: disable=too-few-public-methods
  """Represents a coverprofile coverage report."""

  def __init__(self, f):
    """Parses a Go coverprofile.

    Args:
      f: An array of coverprofile lines.
    """
    self._parse_coverprofile(f)

  def _parse_coverprofile(self, f):
    mode = None
    self.data = {}
    for line in f:
      line = line.strip()

      if not mode:
        pattern = "mode: "
        if line[:len(pattern)] != pattern:
          raise GoCoverprofileParseException("bad mode line: %s" % line)
        mode = line[len(pattern):]
        continue

      m = _line_re.match(line)
      if not m:
        raise GoCoverprofileParseException(
            "line %s doesn't match expected format: %s" % (line,
                                                           _line_re.pattern))
      filename = m.group(1)
      filename_data = self.data.get(filename, None)
      if not filename_data:
        filename_data = {}
        self.data[filename] = filename_data
      start_line = int(m.group(2))
      end_line = int(m.group(4))
      count = int(m.group(7))
      for lineno in range(start_line, end_line + 1):
        filename_data[lineno] = filename_data.get(lineno, 0) + count

  def to_lcov(self):
    """Converts the coverprofile to the LCOV format.

    Returns: An array of lines in LCOV format.
    """
    lines = []
    for f in self.data:
      lines.append("SF:%s" % f)
      for lineno in self.data[f]:
        lines.append("DA:%d,%d" % (lineno, self.data[f][lineno]))
      lines.append("end_of_record")
    return lines
