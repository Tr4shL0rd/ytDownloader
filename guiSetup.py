from click import option
from cx_Freeze import setup, Executable

includeFiles = ["assets/", "config.json"]

setup(
    name = "guiYTDownloader",
    version = "0.1",
    description = "A GUI for youtube-dl",
    options={"build_exe": {"include_files": includeFiles}},
    executables = [Executable("guiDownloader.py")]
    )