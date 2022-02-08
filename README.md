<!-- Project Shields -->
![GitHub contributors](https://img.shields.io:/github/contributors/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub forks](https://img.shields.io:/github/forks/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io:/github/stars/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub last commit](https://img.shields.io:/github/last-commit/Tr4shL0rd/ytDownloader?style=for-the-badge)
![GitHub](https://img.shields.io:/github/license/Tr4shL0rd/ytDownloader?style=for-the-badge)

# CONTENTS

-   [Description](#DESCRIPTION)
-   [Installation](#INSTALLATION)
-   [Build](#BUILD)
-   [Todo](#DOING)
-   [Known Bugs](#BUGS)
-   [Built With](#BUIlT-WITH)
-   [Acknowledgements](#ACKNOWLEDGEMENTS)
-   [License](#LICENSE)



# DESCRIPTION

**ytDownloader** is a Command-line / graphical user interface application based on [youtube-dl](https://github.com/ytdl-org/youtube-dl). The application is written in python3.10 and allows the user to downloads a youtube video from a url and then it automatically converts it into a audio file and sends that file to your email address.

**Please be aware that since this program uses gmail to send the files, you need to toggle *["Less secure app access"](https://support.google.com/accounts/answer/6010255?hl=en)* on in your gmail account settings.** *I am looking for an alternative to gmail for this project.*

# INSTALLATION

-   [LINUX](README.md#linux)
-   [MACOS](README.md#macOS)
-   [WINDOWS](README.md#Windows)

# linux

### Debian-based Linux

```debian-linux
sudo apt-get install python3.10
sudo apt-get install python-tk
pip install -r requirements.txt
```

### Arch-based Linux

```arch-linux
sudo packman -S python3.10
sudo pacman -S tk
pip install -r requirements.txt
```

### Fedora-based Linux

```fedora-linux
sudo dnf install python3.10
sudo dnf install python3-tkinter
pip install -r requirements.txt
```

### RHEL, CentOS, Oracle Linux

```rhel centos oracle Linux
sudo yum install -y python3.10
sudo yum install -y tkinter tk-devel
pip install -r requirements.txt
```

# macOS

```mac
brew install python3.10
brew install python-tk@3.10
pip install -r requirements.txt
```

# Windows

-   install python from [python.org](https://www.python.org/downloads/)
-   Tkinter Comes With python3.7 & Greater

```windows
pip install -r requirements.txt
```

## BUILD

```_
git clone https://github.com/Tr4shL0rd/ytDownloader.git
pip install -r requirements.txt
python guiSetup.py build
cd build/exe."PLATFORM"
./guiDownloader.exe
```

# DOING

-   add multiple files in one email

# NEED TO HAVE

## CLI

-   --json

# NICE TO HAVE

## cli

-   stderr for errors

## gui

-   progress bar in GUI
-   all entries and button stays in the same place no matter if the url entry box is there or not
-   Icon for windows taskbar

## General

-   Google Drive for file sharing
-   SMS API For Google Drive Link
-   Add gif that shows how to use GUI and CLI 
-.  Add option to choose which audio format to convert to

# DONE

## Cli

### Args

-   [✓] --ignore
-   [✓] --no-download
-   [✓] --version
-   [✓] --no-color
-   [✓] --quite

## Gui

-   [✓] add "Remember Me" check box in gui
-   [✓] add "Load From File" check box in gui
-   [✓] convert to executable
-   [✓] add check box to toggle reading from file

## General

-   [✓] Prettify song titles





# BUGS

* sometimes youtube-dl throws an http error code 403 when downloading a video. url get downloaded when trying to download the video again. **[Cause: unknown]**
* When clicking the **Remeber Me** button in the gui application, the program writes to the config file when toggling the checkbox ON and OFF **[Cause: seems to be some weird logic in the if statement]**

# BUILT WITH

-   [tkinter](https://docs.python.org/3/library/tkinter.html)
-   [YouTube-dl](https://github.com/ytdl-org/youtube-dl)
-   [Youtube Video Search](https://github.com/alexmercerind/youtube-search-python)
-   [Rich](https://github.com/Textualize/rich)

# ACKNOWLEDGEMENTS

-   [flaticon.com](https://www.flaticon.com/)
-   [img.shields.io](https://img.shields.io/)
-   [GeeksForGeeks.org](https://www.geeksforgeeks.org/)
-   [README.md template](https://github.com/othneildrew/Best-README-Template)

# LICENSE

Distributed under the MIT License. See `LICENSE.txt` for more information.
