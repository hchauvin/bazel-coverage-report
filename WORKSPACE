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

workspace(name = "hchauvin_bazel_coverage_example")

http_archive(
    name = "com_google_protobuf",
    sha256 = "f6600abeee3babfa18591961a0ff21e7db6a6d9ef82418a261ec4fee44ee6d44",
    strip_prefix = "protobuf-3.4.0",
    urls = ["https://github.com/google/protobuf/archive/v3.4.0.tar.gz"],
)

http_archive(
    name = "io_bazel_rules_go",
    sha256 = "f70c35a8c779bb92f7521ecb5a1c6604e9c3edd431e50b6376d7497abc8ad3c1",
    url = "https://github.com/bazelbuild/rules_go/releases/download/0.11.0/rules_go-0.11.0.tar.gz",
)

http_archive(
    name = "bazel_gazelle",
    sha256 = "92a3c59734dad2ef85dc731dbcb2bc23c4568cded79d4b87ebccd787eb89e8d0",
    url = "https://github.com/bazelbuild/bazel-gazelle/releases/download/0.11.0/bazel-gazelle-0.11.0.tar.gz",
)

load("@io_bazel_rules_go//go:def.bzl", "go_rules_dependencies", "go_register_toolchains")

go_rules_dependencies()

go_register_toolchains()

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

local_repository(
    name = "com_grail_rules_r",
    path = "../rules_r",
)

new_http_archive(
    name = "R_bitops",
    build_file = "R/cran/BUILD.bitops",
    sha256 = "9b731397b7166dd54941fb0d2eac6df60c7a483b2e790f7eb15b4d7b79c9d69c",
    strip_prefix = "bitops",
    urls = [
        "https://cloud.r-project.org/src/contrib/bitops_1.0-6.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/bitops/bitops_1.0-6.tar.gz",
    ],
)

new_http_archive(
    name = "R_crayon",
    build_file = "R/cran/BUILD.crayon",
    sha256 = "9a6b75d63c05fe64baf222f1921330ceb727924bcc5fc2753ff0528d42555e68",
    strip_prefix = "crayon",
    urls = [
        "https://cloud.r-project.org/src/contrib/crayon_1.3.2.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/crayon/crayon_1.3.2.tar.gz",
    ],
)

new_http_archive(
    name = "R_digest",
    build_file = "R/cran/BUILD.digest",
    sha256 = "a479463f120037ad8e88bb1387170842e635a1f07ce7e3575316efd6e14d9eab",
    strip_prefix = "digest",
    urls = [
        "https://cloud.r-project.org/src/contrib/digest_0.6.12.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/digest/digest_0.6.12.tar.gz",
    ],
)

new_http_archive(
    name = "R_magrittr",
    build_file = "R/cran/BUILD.magrittr",
    sha256 = "05c45943ada9443134caa0ab24db4a962b629f00b755ccf039a2a2a7b2c92ae8",
    strip_prefix = "magrittr",
    urls = [
        "https://cloud.r-project.org/src/contrib/magrittr_1.5.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/magrittr/magrittr_1.5.tar.gz",
    ],
)

new_http_archive(
    name = "R_praise",
    build_file = "R/cran/BUILD.praise",
    sha256 = "5c035e74fd05dfa59b03afe0d5f4c53fbf34144e175e90c53d09c6baedf5debd",
    strip_prefix = "praise",
    urls = [
        "https://cloud.r-project.org/src/contrib/praise_1.0.0.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/praise/praise_1.0.0.tar.gz",
    ],
)

new_http_archive(
    name = "R_R6",
    build_file = "R/cran/BUILD.R6",
    sha256 = "087756f471884c3b3ead80215a7cc5636a78b8a956e91675acfe2896426eae8f",
    strip_prefix = "R6",
    urls = [
        "https://cloud.r-project.org/src/contrib/R6_2.2.2.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/R6/R6_2.2.2.tar.gz",
    ],
)

new_http_archive(
    name = "R_RCurl",
    build_file = "R/cran/BUILD.RCurl",
    sha256 = "e72243251bbbec341bc5864305bb8cc23d311d19c5d0d9310afec7eb35aa2bfb",
    strip_prefix = "RCurl",
    urls = [
        "https://cloud.r-project.org/src/contrib/RCurl_1.95-4.8.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/RCurl/RCurl_1.95-4.8.tar.gz",
    ],
)

new_http_archive(
    name = "R_RProtoBuf",
    build_file = "R/cran/BUILD.RProtoBuf",
    sha256 = "35c4274af518c686db99f93b7372f8c1edd37ae00b3c4b024bf355bb0898de3a",
    strip_prefix = "RProtoBuf",
    urls = [
        "https://cloud.r-project.org/src/contrib/RProtoBuf_0.4.10.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/RProtoBuf/RProtoBuf_0.4.10.tar.gz",
    ],
)

new_http_archive(
    name = "R_Rcpp",
    build_file = "R/cran/BUILD.Rcpp",
    sha256 = "9f3eb1e6154f4d56b52ab550a22e522e9999c7998388fdc235e48af5e8c6deaf",
    strip_prefix = "Rcpp",
    urls = [
        "https://cloud.r-project.org/src/contrib/Rcpp_0.12.12.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/Rcpp/Rcpp_0.12.12.tar.gz",
    ],
)

new_http_archive(
    name = "R_testthat",
    build_file = "R/cran/BUILD.testthat",
    sha256 = "0ef7df0ace1fddf821d329f9d9a5d42296085350ae0d94af62c45bd203c8415e",
    strip_prefix = "testthat",
    urls = [
        "https://cloud.r-project.org/src/contrib/testthat_1.0.2.tar.gz",
        "https://cloud.r-project.org/src/contrib/Archive/testthat/testthat_1.0.2.tar.gz",
    ],
)

new_http_archive(
    name = "R_Rgraphviz",
    build_file = "R/cran/BUILD.Rgraphviz",
    sha256 = "1bfb8ac90df797365cf883813505f3b63a01061f515c009924c424e59cf436f9",
    strip_prefix = "Rgraphviz",
    urls = [
        "https://bioconductor.org/packages/release/bioc/src/contrib/Rgraphviz_2.22.0.tar.gz",
    ],
)

new_http_archive(
    name = "R_graph",
    build_file = "R/cran/BUILD.graph",
    sha256 = "c12a519e9984ca2e134a8bef75aac63be59a33691e2206d025e10b88ae944a95",
    strip_prefix = "graph",
    urls = [
        "https://bioconductor.org/packages/release/bioc/src/contrib/graph_1.56.0.tar.gz",
    ],
)

new_http_archive(
    name = "R_BiocGenerics",
    build_file = "R/cran/BUILD.BiocGenerics",
    sha256 = "517d31c47d7d807170031e116af3ffeba57baca3980ef4d85b37c2ec3bdc9d0f",
    strip_prefix = "BiocGenerics",
    urls = [
        "https://bioconductor.org/packages/release/bioc/src/contrib/BiocGenerics_0.24.0.tar.gz",
    ],
)

load("@com_grail_rules_r//R:covr.bzl", "covr_dependencies")

new_local_repository(
    name = "R_covr",
    build_file = "../rules_r/R/cran/BUILD.covr",
    path = "../covr",
)

covr_dependencies(cran_path = "../rules_r/R/cran")
