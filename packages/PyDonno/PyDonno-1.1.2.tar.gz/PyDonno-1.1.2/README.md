# PyDonno

This is a single PyPI package to install all my packages.

## Install requirements (only needed on Linux)

```sh
sudo apt install ffmpeg libsm6 libxext6 nasm python3-tk wget firefox-esr -y
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz # for yt2mp4
sudo tar xvzf geckodriver-v0.30.0-linux64.tar.gz -C /usr/bin/
chmod +x /usr/bin/geckodriver
rm geckodriver-v0.30.0-linux64.tar.gz
```

## To use

Just install the package.

### From PyPI

```sh
python3 -m pip install PyDonno
```

### From GitHub

```sh
python3 -m pip install git+https://github.com/donno2048/PyDonno
```
