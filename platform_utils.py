import platform
import site
from pathlib import Path

WINDOWS = "win"
LINUX = "linux"
MACOSX = "macosx"

ARM64 = "arm64"
X86_64 = "x86_64"


platform_map = {
    ("Darwin", "x86_64"): (MACOSX, X86_64),
    ("Darwin", "arm64"): (MACOSX, ARM64),
    ("Linux", "x86_64"): (LINUX, X86_64),
    ("Linux", "aarch64"): (LINUX, ARM64),
    ("Windows", "x86_64"): (WINDOWS, X86_64),
}


def get_platform_dirname():
    return "_".join(platform_map[(platform.system(), platform.machine())])  # type: ignore


def setup_site_packages(lib_root_dir: Path):
    """Setup site-package directories (in order to import 3rd-party packages)"""
    platform_lib_dir = lib_root_dir / get_platform_dirname()
    any_lib_dir = lib_root_dir / "any"

    if platform_lib_dir.exists():
        site.addsitedir(platform_lib_dir.as_posix())
    else:
        print(f"Warning: {platform_lib_dir} does not exist")

    if any_lib_dir.exists():
        site.addsitedir(any_lib_dir.as_posix())
    else:
        print(f"Warning: {any_lib_dir} does not exist")


def deduce_platform_dirname_from_pip_platform(pip_platform: str):
    """Deduce a valid directory name representing a platform (OS and Architecture) from pip platform argument"""
    pip_platform = pip_platform.lower()
    if "linux" in pip_platform:
        os = LINUX
    elif "macosx" in pip_platform:
        os = MACOSX
    elif "win" in pip_platform:
        os = WINDOWS
    else:
        raise RuntimeError(
            f"Failed to deduce system from pip platform {pip_platform!r}"
        )

    if "x86_64" in pip_platform:
        machine = X86_64
    elif "amd64" in pip_platform:
        machine = X86_64
    elif "universal2" in pip_platform:
        machine = ARM64
    elif "aarch64" in pip_platform:
        machine = ARM64
    else:
        raise RuntimeError(
            f"Failed to deduce architecture from pip platform {pip_platform!r}"
        )

    return f"{os}_{machine}"
