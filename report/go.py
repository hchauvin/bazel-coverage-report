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

# This is inspired by Golang package golang.org/x/tools/cover.

import re

class GoCoverprofileParseException(Exception):
    pass

_line_re = re.compile(
  r"^(.+):([0-9]+).([0-9]+),([0-9]+).([0-9]+) ([0-9]+) ([0-9]+)$")

class Coverprofile:
  def __init__(self, f):
    self._parse_coverprofile(f)

  def _parse_coverprofile(self, f):
    mode = None
    self.data = {}
    for line in f:
      line = line.strip()

      if not mode:
        p = "mode: "
        if line[:len(p)] != p:
          raise GoCoverprofileParseException("bad mode line: %s" % line)
        mode = line[len(p):]
        continue

      m = _line_re.match(line)
      if not m:
        raise GoCoverprofileParseException(
          "line %s doesn't match expected format: %s" % 
            (line, _line_re.pattern))
      fn = m.group(1)
      p = self.data.get(fn, None)
      if not p:
        p = {}
        self.data[fn] = p
      start_line = int(m.group(2))
      end_line = int(m.group(4))
      count = int(m.group(7))
      for lineno in range(start_line, end_line+1):
        p[lineno] = p.get(lineno, 0) + count

  def to_lcov(self):
    lines = []
    for file in self.data:
      lines.append("SF:%s" % file)
      for lineno in self.data[file]:
        lines.append("DA:%d,%d" % (lineno, self.data[file][lineno]))
      lines.append("end_of_record")
    return lines
