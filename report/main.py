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

import argparse
import os
import shutil
import sys

from report import generator

def main(argv=None):
  if argv is None:
    argv = sys.argv

  parser = argparse.ArgumentParser(
    description='Bazel Coverage Report Generator')
  parser.add_argument("--dest_dir", type=str, default="/tmp/cov_report")
  parser.add_argument("--project_dir", type=str, default=os.getcwd())

  args = parser.parse_args()

  if os.path.exists(args.dest_dir):
    shutil.rmtree(args.dest_dir)
  os.makedirs(args.dest_dir)

  # TODO: deal gracefully with exceptions

  rg = generator.ReportGenerator(dest_dir = args.dest_dir, project_dir = args.project_dir)
  rg.copy_sources()
  rg.copy_cov()
  rg.genhtml()

  print("coverage report at %s" % rg.report_index_url())

  return 0

if __name__ == "__main__":
  sys.exit(main())