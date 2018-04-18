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

import fnmatch
import os
import re
import shutil
import subprocess

from report import normalize

def _source_files_ignore(dir, children, patterns):
  res = []
  for child in children:
    if os.path.isdir(os.path.join(dir, child)):
      if child.startswith('bazel-') or child in ['.git']:
        res.append(child)
    else:
      m = False
      for pat in patterns:
        if fnmatch.fnmatch(child, pat):
          m = True
          break
      if not m:
        res.append(child)
  return res

_wspace_name_re = re.compile(r"workspace\s*\(\s*name\s*=\s*\"([^\"]+)\"\s*\)")

def get_workspace_name(wspace_file):
  for line in wspace_file:
    m = _wspace_name_re.match(line)
    if m:
      return m.group(1)
  return None

class ReportGenerator:
  def __init__(
    self,
    dest_dir,
    project_dir,
    workspace_name = None,
    testlogs_dir = None,
    source_file_patterns = ["*.R", "*.c"]
  ):
    if not dest_dir:
      raise Exception("dest_dir is required")

    if not project_dir:
      raise Exception("project_dir is required")

    self.dest_dir = dest_dir
    self.project_dir = project_dir
    self.testlogs_dir = testlogs_dir
    self.workspace_name = workspace_name
    self.source_file_patterns = source_file_patterns

    if not self.workspace_name:
      with open(os.path.join(self.project_dir, 'WORKSPACE'), 'r') as wspace:
        self.workspace_name = get_workspace_name(wspace)
      if not self.workspace_name:
        self.workspace_name = os.path.basename(self.project_dir)

    if not self.testlogs_dir:
      self.testlogs_dir = os.readlink(
        os.path.join(self.project_dir, "bazel-testlogs"))

    self.coverage_files = []
    self.normalizer = normalize.SourceFilenameNormalizer()

  def copy_sources(self):
    shutil.copytree(
      self.project_dir, 
      os.path.join(self.dest_dir, self.workspace_name),
      ignore = lambda dir, children: _source_files_ignore(
        dir, 
        children, 
        patterns = self.source_file_patterns))

  def copy_cov(self):
    for root, _, files in os.walk(self.testlogs_dir):
      for f in files:
        path = os.path.join(root, f)
        if os.path.isfile(path) and f.endswith('coverage.dat'):
          with open(path, 'r') as f_cov:
            normalized = self.normalizer.normalize_coverage_dat(
              f_cov.readlines())
          if len(normalized) > 0:
            dest_root = os.path.join(
              self.dest_dir, 
              os.path.relpath(root, start=self.testlogs_dir))
            if not os.path.exists(dest_root):
              os.makedirs(dest_root)
            dest_path = os.path.join(dest_root, f)
            self.coverage_files.append(dest_path)
            with open(dest_path, 'w') as f_cov_dest:
              f_cov_dest.write('\n'.join(normalized))

  def genhtml(self):
    subprocess.check_call(
      ['genhtml', '-o', '.', '--ignore-errors', 'source', '--'] + 
        self.coverage_files,
      cwd=self.dest_dir)

  def report_index_url(self):
    return "file://%s/index.html" % self.dest_dir