from conans import ConanFile, CMake, tools


class FlameshotConan(ConanFile):
    name = "flameshot"
    version = "0.8.5"
    license = "GNU GENERAL PUBLIC LICENSE"
    author = "Max Christy <tchristy001@outlook.com>"
    url = "https://github.com/flameshot-org/flameshot.git"
    description = "Powerful yet simple to use screenshot software"
    topics = ("screenshot", "screen clip", "Qt")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "qtsvg": [True, False],
        "openssl": [True, False]
    }
    default_options = {
        "shared": False,
        "qtsvg": True,
        "openssl": True
    }
    generators = "cmake"

    def export_sources(self):
        self.copy("*", excludes=["build*", "tmp*"])

    requires = [
        "qt/5.15.2@bincrafters/stable",
        "openssl/1.1.1h"
    ]

    build_requires = [
        "cmake/[3]",
        "catch2/[]"
    ]

    def configure(self):
        self.options["qt"].qtsvg = self.options.qtsvg
        self.options["qt"].qttools = True

    def build(self):
        cmake = CMake(self)
        cmake.configure(
            defs={
                "ENABLE_OPENSSL": self.options.openssl,
            }
        )
        cmake.build()

    def test(self):
        cmake = CMake(self)
        try:
            cmake.test()
        except ConanException:
            print("One or more unit tests failed")
            # pass  # allow the unit test to fail and not fail hard as we want the CI to continue and report the error
        else:
            print("All unit tests successful")

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.regex.libs = ["lib{{ name }}"]

    def imports(self):
        self.copy("*.dll", "", "bin")
        self.copy("*.dylib", "", "lib")
