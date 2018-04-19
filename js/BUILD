load("@build_bazel_rules_nodejs//:defs.bzl", "jasmine_node_test")
load("@build_bazel_rules_typescript//:defs.bzl", "ts_library")

# This is like a "js_library", but there are no actions to run on JS files so a
# filegroup is semantically equivalent.
ts_library(
    name = "foo",
    srcs = ["foo.ts"],
)

ts_library(
    name = "bar",
    srcs = ["bar.ts"],
    deps = [
        ":foo",
    ]
)

jasmine_node_test(
    name = "foo_test",
    srcs = ["foo_test.js"],
    node_modules = "@js_deps//:node_modules",
    deps = [
        ":foo",
    ],
)

jasmine_node_test(
    name = "bar_test",
    srcs = ["bar_test.js"],
    node_modules = "@js_deps//:node_modules",
    deps = [
        ":bar",
    ],
)
