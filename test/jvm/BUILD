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

load("@io_bazel_rules_kotlin//kotlin:kotlin.bzl", "kt_jvm_library", "kt_jvm_test")

kt_jvm_library(
    name = "kt",
    srcs = glob(["src/main/kotlin/**/FooKotlin.kt"]),
)

kt_jvm_test(
    name = "kt_ExampleATest",
    size = "small",
    srcs = ["src/test/kotlin/com/github/hchauvin/bazelcoverageexample/ExampleAKotlinTest.kt"],
    test_class = "com.github.hchauvin.bazelcoverageexample.ExampleAKotlinTest",
    deps = [
        ":kt",
        "@junit",
    ],
)

kt_jvm_library(
    name = "kt2",
    srcs = glob(["src/main/kotlin/**/Foo2Kotlin.kt"]),
    deps = [
        ":kt",
    ],
)

kt_jvm_test(
    name = "kt_Foo2ExampleATest",
    size = "small",
    srcs = ["src/test/kotlin/com/github/hchauvin/bazelcoverageexample/Foo2ExampleAKotlinTest.kt"],
    test_class = "com.github.hchauvin.bazelcoverageexample.Foo2ExampleAKotlinTest",
    deps = [
        ":kt2",
        "@junit",
    ],
)
