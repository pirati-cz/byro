
Installation manual for Byro
============================


Non python dependency
---------------------

Package from repository in most common Linux distributions.

### Fedora 28

```bash
sudo dnf install gcc python3 python3-pip git tesseract tesseract-langpack-ces poppler-utils \
texlive texlive-collection-langczechslovak texlive-collection-mathextra texlive-mathspec texlive-euenc \
texlive-xetex texlive-xetex-def texlive-xltxtra texlive-tcolorbox texlive-datetime2-czech\
pandoc libreoffice gnuplot
```
(~ 212 MB download, ~ 514 MB installed)


### Ubuntu 14.04 LTS

```bash
sudo apt-get install gcc python3 python3-pip git pandoc libreoffice \
tesseract-ocr tesseract-ocr-ces poppler-utils \
texlive texlive-lang-czechslovak texlive-xetex texlive-latex-extra gnuplot
```
(~ 1 GB)

### Other OS and other distribution

App is writen in [Python 3][] and using multiplatform technology
([XeLaTeX][], [Pandoc][], [Tesseract][]).
It should be possible to port to other os and other distribution.
Feel free to send pull request with manual for other OS.

### Other dependency

Other dependency that are not present in repository:

* [jSignPdf][signHP], [download][signDownload]: in roadmap is automatic installation


Install
-------

Once you have all OS dependencies installed, you can run following command:

```bash
sudo pip3 install git+https://github.com/pirati-cz/byro
```

Then just run `byro`!

### Reinstall

```bash
sudo pip3 uninstall byro
sudo pip3 install git+https://github.com/pirati-cz/byro
```

### Config file

Important parameters are in config file: `byro/resource/config.ini`.
After first run is created `$HOME/.byro.ini`.

Generaly args that start with '--' (eg. --config)
can also be set in a config file (files/config.ini or specified via -c) by
using .ini or .yaml-style syntax (eg. config=value). If an arg is specified in
more than one place, then command-line values override config file values
which override defaults.

### Tests

Unit tests run:

```
python3 -m unittest
```

For more details add `-v`.

### Update

Update already installed instance:

```bash
pip3 install --upgrade byro
```

### Remove

Remove from os:

```
pip3 uninstall byro
[rm ~/.byro.ini]
```


Using
-----

Everythink is in the help: `byro -h`


Creating distribution packages
-------------------------------

### RPM

```
./setup.py bdist_rpm
```


[signHP]: http://sourceforge.net/projects/jsignpdf
[signDownload]: http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files
[Python 3]: https://www.python.org
[XeLaTeX]: http://www.latex-project.org
[Pandoc]: http://pandoc.org
[Tesseract]: https://github.com/tesseract-ocr/tesseract
