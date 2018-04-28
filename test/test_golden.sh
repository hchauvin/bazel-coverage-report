#!/bin/bash
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

set -eou pipefail

expect_equal() {
  local actual
  local actual_content
  local expected_content
  
  actual=$1
  actual_content=$(cat "${actual}")
  expected_content=$(cat "${2}")
  if [ "${actual_content}" != "${expected_content}" ]; then
    echo "==="
    echo "COVERAGE: ${actual}"
    echo "ACTUAL:"
    echo "${actual_content}"
    echo "---"
    echo "EXPECTED:"
    echo "${expected_content}"
    echo "==="
    return 1
  fi

  echo "PASSED ${actual}"
}

for i in $(cd test/golden; find . -type f); do
  expect_equal "bazel-testlogs/$i" "test/golden/$i"
done
