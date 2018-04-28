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

java_binary(
    name = "java_format",
    main_class = "com.google.googlejavaformat.java.Main",
    runtime_deps = ["@google_java_format"],
)

load("@format_py_deps//:requirements.bzl", "requirement")

py_binary(
    name = "pylint_bin",
    srcs = ["pylint_bin.py"],
    deps = [
        requirement("pylint"),
        requirement("enum34"),
        requirement("lazy-object-proxy"),
        requirement("wrapt"),
    ],
)
