py_library(
    name = "report",
    srcs = glob(
        ["*.py"],
        exclude = ["main.py"],
    ),
    visibility = ["//visibility:public"],
)

py_binary(
    name = "bin",
    srcs = ["main.py"],
    main = "main.py",
    deps = ["//report"],
)
