import subprocess as sp
import sys
from pathlib import Path
from shutil import copytree, make_archive, rmtree, copyfile

from platform_utils import deduce_platform_dirname_from_pip_platform

if len(sys.argv) != 2:
    print("Usage: package.py addon_source_directory")
    exit(1)

source_addon_dir_name = sys.argv[1]

# NOTE: if "--no-deps" is used when executing pip you should supply dependencies of dependencies explicitly
# unless they already ship with Blender
dependencies = {
    "scipy==1.9.1": {
        # NOTE: Sadly you have to find these names by yourself for each package for now
        "platforms": [
            "macosx_10_9_x86_64",
            "macosx_12_0_universal2",  # MacOS X ARM64
            "win_amd64",
            "manylinux2014_x86_64",
            "manylinux2014_aarch64",
        ]
    }
}

parent_dir = Path(__file__).parent

source_addon_dir = parent_dir / source_addon_dir_name
source_platform_utils_path = parent_dir / "platform_utils.py"

package_dir = parent_dir / "package"
package_addon_dir = package_dir / source_addon_dir_name
package_addon_lib_root_dir = package_addon_dir / "lib"
package_platform_utils_path = package_addon_dir / "platform_utils.py"


rmtree(package_dir, ignore_errors=True)
copytree(source_addon_dir, package_addon_dir)
copyfile(source_platform_utils_path, package_platform_utils_path)

# TODO: allow building separate package for each platform
for dep_name, dep_info in dependencies.items():
    for pip_platform in dep_info["platforms"]:
        platform_dirname = deduce_platform_dirname_from_pip_platform(pip_platform)
        target_dir = (package_addon_lib_root_dir / platform_dirname).as_posix()
        args = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--only-binary",
            ":all:",
            "--target",
            target_dir,
            "--platform",
            pip_platform,
            "--no-deps",
            "--python-version",
            "310", # TODO: support multiple Python versions
            dep_name,
        ]
        print(f"Executing: {' '.join(args)}")
        sp.run(args)

make_archive(
    source_addon_dir_name,
    "zip",
    root_dir=package_dir,
    base_dir=source_addon_dir_name,
    verbose=True,
)
