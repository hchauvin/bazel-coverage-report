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
"""Interacts with Bazel's directory layout."""

import os

_bazel = {}


def runfiles():
  """Returns the runfiles manifest entries.

  Returns: A dictionary of runfiles to their real absolute paths.
  """
  if not _bazel.has_key("runfiles"):
    _bazel["_runfiles"] = {}
    with open(os.path.join(os.getenv("RUNFILES_MANIFEST_FILE")), 'r') as f:
      for l in f:
        tokens = l.strip().split(' ')
        if len(tokens) == 2:
          _bazel["_runfiles"][tokens[0]] = tokens[1]
  return _bazel["_runfiles"]


def runfile(relative_path):
  """Returns the real absolute path of a runfile relative path.

  The runfiles manifest is used."""
  return runfiles()[relative_path]
