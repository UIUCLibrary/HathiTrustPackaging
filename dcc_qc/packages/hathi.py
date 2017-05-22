from dcc_qc.packages.abs_package import AbsPackage, PackageItem
from dcc_qc import packages
import typing
import os


class HathiPackage(AbsPackage):
    @property
    def items(self) -> typing.Generator[PackageItem, None, None]:
        for i in self._items:
            yield i

    def load(self):
        def get_package_paths(path) -> typing.Tuple[str, str]:
            found_access = []
            found_preservation = []

            for root, dirs, files in os.walk(path):
                for dir_ in dirs:
                    if dir_ == "preservation":
                        found_preservation.append(os.path.join(root, dir_))
                    elif dir_ == "access":
                        found_access.append(os.path.join(root, dir_))

            if len(found_access) == 1 and len(found_preservation) == 1:
                return found_access[0], found_preservation[0]

            if len(found_access) > 1 or len(found_preservation) > 1:
                raise Exception("Error: Found multiple access or preservation folders in {}".format(path))

            if len(found_access) == 0 or len(found_preservation) == 0:
                raise packages.PackagePartMissing("Error: Missing access and/or preservation folders in {}".format(path))
            raise packages.PackageError("Error: Unable to find access and preservation folders in {}".format(path))

        def create_pairs(access_path, preservation_path) -> typing.Generator[typing.Tuple[str, str], None, None]:
            access_folders = sorted(os.listdir(access_path))
            preservation_folders = sorted(os.listdir(preservation_path))

            assert len(access_folders) == len(preservation_folders)
            for pair in zip(access_folders, preservation_folders):
                assert pair[0] == pair[1]
                yield os.path.join(access_path, pair[0]), os.path.join(preservation_path, pair[1])

        access_path, preservation_path = get_package_paths(self.root_path)
        assert access_path.replace("access", "") == preservation_path.replace("preservation", "")

        for access, preservation in create_pairs(access_path, preservation_path):
            self._items.append(
                PackageItem(
                    root=self.root_path,
                    directories={
                        "access": access,
                        "preservation": preservation
                    }
                )
            )