load("@bazel_gazelle//:def.bzl", "gazelle")

gazelle(
    name = "gazelle",
    prefix = "github.com/hchauvin/bazel-coverage-example",
)

exports_files(["package.json"])

# The node_modules directory is created by `yarn install`
# WORKAROUND for https://github.com/bazelbuild/bazel/issues/374#issuecomment-296217940
filegroup(
    name = "node_modules",
    # Only include files needed for type-checking and runtime
    srcs = glob([
        "node_modules/**/*.js",
        "node_modules/**/*.d.ts",
        "node_modules/**/*.json"
    ]),
    visibility = ["//visibility:public"],
)