from cx_Freeze import setup, Executable

includeFiles = ["assets/", "config.json"]
target = Executable(
    script="guiDownloader.py",
    icon="assets/icon/icon.ico", 
)

setup(
    name        = "guiYTDownloader",
    options     = {"build_exe": {"include_files": includeFiles}},
    version     = "0.1",
    description = "A GUI for youtube-dl",
    executables = [Executable(script="guiDownloader.py", icon="assets/icon/icon.ico")]
    )