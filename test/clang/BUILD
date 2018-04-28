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

licenses(["notice"])  # Apache 2.0

# Until https://github.com/bazelbuild/bazel/commit/d6f706d334046601df9d0a58b993b705e9e371a0:
# - Coverage does not work on Mac OSX.
# - We must explicitly use --coverage.

cc_library(
    name = "foo",
    srcs = ["foo.c"],
    hdrs = ["foo.h"],
    linkopts = ["--coverage"],
)

cc_test(
    name = "foo_test",
    size = "small",
    srcs = ["foo_test.c"],
    linkopts = ["--coverage"],
    deps = [":foo"],
)

cc_library(
    name = "bar",
    srcs = ["bar.c"],
    hdrs = ["bar.h"],
    linkopts = ["--coverage"],
    deps = [":foo"],
)

cc_test(
    name = "bar_test",
    size = "small",
    srcs = ["bar_test.c"],
    linkopts = ["--coverage"],
    deps = [":bar"],
)
