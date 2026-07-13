from pathlib import Path
import tarfile
import os.path

import FastQCompressor.Config as Config
import FastQCompressor.FastQ as FastQ


class FolderCompressor:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = Config.Config(config_path)

    def compress(self, folder_path: str):
        folder_extension = self.config.print(["FolderCompressor", "folderextension"])
        file_compressor = FastQ.FileCompressor(self.config_path)
        folder = Path(folder_path)
        for root, _, files in folder.walk():
            for file in files:
                filepath = f"{root}/{file}"
                file_compressor.compress(filepath)
        _make_tarfile(folder.name + folder_extension, folder)


def _make_tarfile(output_filename, source_dir):
    basename = os.path.basename(source_dir)
    assert isinstance(basename, str)
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=basename)
