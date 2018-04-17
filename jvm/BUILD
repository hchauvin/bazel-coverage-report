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

java_library(
    name = "java",
    srcs = glob(["src/main/java/**/Foo.java"]),
)

[java_test(
    name = "java_Example%sTest" % example,
    size = "small",
    srcs = ["src/test/java/com/github/hchauvin/bazelcoverageexample/Example%sTest.java" % example],
    test_class = "com.github.hchauvin.bazelcoverageexample.Example%sTest" % example,
    deps = [
        ":java",
    ],
) for example in [
    "A",
    "B",
    "C",
]]

java_library(
    name = "java2",
    srcs = glob(["src/main/java/**/Foo2.java"]),
    deps = [
        ":java",
    ],
)

java_test(
    name = "java_Foo2ExampleATest",
    size = "small",
    srcs = ["src/test/java/com/github/hchauvin/bazelcoverageexample/Foo2ExampleATest.java"],
    test_class = "com.github.hchauvin.bazelcoverageexample.Foo2ExampleATest",
    deps = [
        ":java2",
    ],
)
