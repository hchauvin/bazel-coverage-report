# `bazel-coverage-report`

**Unmaintained: Please look at forks instead!**

[![Build Status](https://travis-ci.org/hchauvin/bazel-coverage-report.svg?branch=master)](https://travis-ci.org/hchauvin/bazel-coverage-report)

`bazel-coverage-report` is a multi-language coverage report generator for
[Bazel](https://bazel.build).  It is based on [genhtml](https://github.com/linux-test-project/lcov.git).

See the [example report](https://hchauvin.github.io/bazel-coverage-report/index.html) generated
for the `//test/...` targets.

Bug reports and feature requests are welcome.

## Usage

In your WORKSPACE:
```python
git_repository(
    name = "hchauvin_bazel_coverage_report",
    remote = "https://github.com/hchauvin/bazel-coverage-report.git",
    commit = "{HEAD}",
)
load("@hchauvin_bazel_coverage_report//report:defs.bzl", "bazel_coverage_report_repositories")
bazel_coverage_report_repositories()  # lcov, ...
```

Then:

1. Generate coverage data with `bazel coverage //your/targets/... --instrumentation_filter=<...>`
2. Build the coverage report generator: `bazel build @hchauvin_bazel_coverage_report//report:bin`
3. Generate the report: `bazel-bin/external/hchauvin_bazel_coverage_report/report/bin --dest_dir=<dest dir>`

## Supported languages

- C, C++
- Golang
- Javascript, Typescript
- Java, Kotlin
- R

See [`./WORKSPACE`](./WORKSPACE) for the version of the rules that are supported.  Some of
these versions are pending Push Requests.
