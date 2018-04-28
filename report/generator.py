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
"""Coverage report generator."""

import fnmatch
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree

from report import bazel
from report import normalize


def _source_files_ignore(directory, children, patterns):
  """'ignore' lambda for shutil.copytree."""
  res = []
  for child in children:
    if os.path.isdir(os.path.join(directory, child)):
      # TODO: do not hardcode gh-pages
      if child.startswith('bazel-') or child in ['.git', 'gh-pages']:
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


def _get_workspace_name(wspace_file):
  for line in wspace_file:
    m = _wspace_name_re.match(line)
    if m:
      return m.group(1)
  return None


def _get_go_importmap(project_dir, workspace_name):
  if not os.path.exists(os.path.join(project_dir, "WORKSPACE")):
    raise Exception(
        "project_dir '%s' does not contain a WORKSPACE file" % project_dir)

  query_str = subprocess.check_output(
      [
          'bazel',
          'query',
          'kind(_gazelle_runner, //:*)',
          '--output=xml',
      ],
      cwd=project_dir)

  query = xml.etree.ElementTree.fromstring(query_str)
  gazelle_prefixes = query.findall('./rule/string[@name="prefix"]')
  if len(gazelle_prefixes) == 0:
    raise Exception("no gazelle rule in root BUILD file")
  if len(gazelle_prefixes) > 1:
    raise Exception("multiple gazelle rules in root BUILD file")
  workspace_prefix = gazelle_prefixes[0].get('value')

  return {
      workspace_prefix: workspace_name,
  }


_java_paths_re = re.compile(r"^.+/src/[^/]+/(java|kotlin)$")


def _find_java_paths(path):
  java_paths = []
  for root, dirnames, _ in os.walk(path):
    for dirname in dirnames:
      cur_path = os.path.join(root, dirname)
      if _java_paths_re.match(cur_path):
        java_paths.append(cur_path)
  return java_paths


_DEFAULT_SOURCE_FILE_PATTERNS = ["*.R", "*.c", "*.go", "*.java", "*.kt", "*.ts"]


class ReportGenerator(object):
  """Coverage report generator."""

  def __init__(  # pylint: disable=too-many-arguments
      self,
      dest_dir,
      project_dir,
      workspace_name=None,
      testlogs_dir=None,
      go_importmap=None,
      source_file_patterns=None):
    """Creates a coverage report generator.

    Args:
      dest_dir: Destination directory where to put the report.
      project_dir: Root of project directory (containing a WORKSPACE file).
      workspace_name: Name of the workspace.  If not given, it is guessed
        from the `workspace(name = "...")` rule of the WORKSPACE file or the
        basename of the project directory, in this order.
      testlogs_dir: Directory where the coverage data is located.
        Defaults to `<project_dir>/bazel-testlogs`.
      go_importmap: Map of go prefixes (e.g., `github.com/orga/project`) to
        relative directories with the execroot (e.g., `com_github_orga_project`).
        Defaults to one mapping for the current WORKSPACE, derived from the
        `//:gazelle` target.
      source_file_patterns: globs of source files to copy.
    """
    # TODO: instead of using source_file_patterns, we should rely on
    # "*.instrumented_files" generated files (they contain a list of
    # instrumented files, and there is one such file per test target).
    if not dest_dir:
      raise Exception("dest_dir is required")

    if not project_dir:
      raise Exception("project_dir is required")

    self.dest_dir = dest_dir
    self.project_dir = project_dir
    self.testlogs_dir = testlogs_dir
    self.workspace_name = workspace_name
    self.go_importmap = go_importmap
    self.source_file_patterns = source_file_patterns

    if not self.workspace_name:
      with open(os.path.join(self.project_dir, 'WORKSPACE'), 'r') as wspace:
        self.workspace_name = _get_workspace_name(wspace)
      if not self.workspace_name:
        self.workspace_name = os.path.basename(self.project_dir)

    if not self.testlogs_dir:
      self.testlogs_dir = os.readlink(
          os.path.join(self.project_dir, "bazel-testlogs"))

    if not self.go_importmap:
      self.go_importmap = _get_go_importmap(self.project_dir,
                                            self.workspace_name)

    if not self.source_file_patterns:
      self.source_file_patterns = _DEFAULT_SOURCE_FILE_PATTERNS

    self.coverage_files = []

  def _create_normalizer(self):
    return normalize.SourceFilenameNormalizer(
        go_importmap=self.go_importmap,
        java_paths=_find_java_paths(self.dest_dir),
        workspace_name=self.workspace_name,
        dest_dir=self.dest_dir,
    )

  def copy_sources(self):
    """Copies relevant sources to the output directory."""
    shutil.copytree(
        self.project_dir,
        os.path.join(self.dest_dir, self.workspace_name),
        ignore=lambda dir, children: _source_files_ignore(
            dir,
            children,
            patterns=self.source_file_patterns))

  def copy_cov(self):
    """Copies coverage data files to the output directory."""
    normalizer = self._create_normalizer()
    for root, _, files in os.walk(self.testlogs_dir):
      for f in files:
        path = os.path.join(root, f)
        if os.path.isfile(path) and f.endswith('coverage.dat'):
          with open(path, 'r') as f_cov:
            normalized = normalizer.normalize_coverage_dat(f_cov.readlines())
          if len(normalized) > 0:
            dest_root = os.path.join(self.dest_dir,
                                     os.path.relpath(
                                         root, start=self.testlogs_dir))
            if not os.path.exists(dest_root):
              os.makedirs(dest_root)
            dest_path = os.path.join(dest_root, f)
            self.coverage_files.append(dest_path)
            with open(dest_path, 'w') as f_cov_dest:
              f_cov_dest.write('\n'.join(normalized))

  def genhtml(self):
    """Generates the report."""
    subprocess.check_call(
        [
            bazel.runfile("lcov/bin/genhtml"), '-o', '.', '--ignore-errors',
            'source', '--'
        ] + self.coverage_files,
        cwd=self.dest_dir)

  def report_index_url(self):
    """Returns the URL of the HTML index of the index."""
    return "file://%s/index.html" % self.dest_dir
