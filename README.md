![GitHub Repo stars](https://img.shields.io:/github/stars/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub forks](https://img.shields.io:/github/forks/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub last commit](https://img.shields.io:/github/last-commit/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub](https://img.shields.io:/github/license/Tr4shL0rd/ytDownloader?style=for-the-badge)

# INSTALLATION

* [LINUX](README.md#linux)
* [MACOS](README.md#macOS)
* [WINDOWS](README.md#Windows)

# linux

### Debian-based Linux

``` debian-linux
sudo apt-get install python3.10
sudo apt-get install python-tk
pip install -r requirements.txt
```

### Arch-based Linux

``` arch-linux
sudo packman -S python3.10
sudo pacman -S tk
pip install -r requirements.txt
```

### Fedora-based Linux

``` fedora-linux
sudo dnf install python3.10
sudo dnf install python3-tkinter
pip install -r requirements.txt
```

### RHEL, CentOS, Oracle Linux

``` rhel centos oracle Linux
sudo yum install -y python3.10
sudo yum install -y tkinter tk-devel
pip install -r requirements.txt
```

# macOS

``` mac
brew install python3.10
brew install python-tk@3.10
pip install -r requirements.txt
```

# Windows

* install python from [python.org](https://www.python.org/downloads/)
* Tkinter Comes With python3.7 & Greater

``` windows
pip install -r requirements.txt
```

## BUILD

``` _
git clone https://github.com/Tr4shL0rd/ytDownloader.git
pip install -r requirements.txt
python guiSetup.py build
cd build/exe."PLATFORM"
./guiDownloader.exe
```

# TODO

## General

* add multiple files in one email
* [✓]Prettify song titles

## CLI

* --json
* stderr for errors
* grep-able output

## GUI

* [✓]add "Remember Me" check box in gui
* [✓]convert to executable
* [✓]add check box to toggle reading from file

# RESOURCES

* <https://www.flaticon.com/>
* <https://img.shields.io/>
