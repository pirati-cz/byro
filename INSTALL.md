
Installation manual for Byro
============================

Non python dependency
---------------------

Package from repository in most common Linux distributions.

### Fedora 22

```bash
sudo dnf install gcc python3 python3-pip git tesseract tesseract-langpack-ces poppler-utils \
texlive texlive-collection-langczechslovak texlive-collection-mathextra texlive-mathspec texlive-euenc \
texlive-xetex texlive-xetex-def texlive-xltxtra \
pandoc libreoffice
```
(~ 200 MB)


### Ubuntu 14.04 LTS

```bash
sudo apt-get install gcc python3 python3-pip git pandoc libreoffice \
tesseract-ocr tesseract-ocr-ces poppler-utils \
texlive texlive-lang-czechslovak texlive-xetex texlive-latex-extra
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


Python dependency
-----------------

```bash
sudo pip3 install --upgrade pip  
sudo pip3 install wget dateutils markdown ConfigArgParse python-redmine python-docx pytesseract
```


Install Byro itself
-------------------

```bash
cd <path-to-repo>
git clone https://github.com/pirati-cz/byro
cd byro
git checkout `git for-each-ref --sort='*authordate' --format='%(tag)' refs/tags`
cp files/config-example.ini files/config.ini
python3 -m unittest discover
```

Path to repo is directory where repository is cloned. For example `/opt/`.

Last command launch unit tests. If all pass everything is ok.

For simple using, create alias: 

```bash
alias byro="$PWD/byro.py"
```

### Config file

Important parameters are in config file: `files/config.ini`

Args that start with '--' (eg. --config)
can also be set in a config file (files/config.ini or specified via -c) by
using .ini or .yaml-style syntax (eg. config=value). If an arg is specified in
more than one place, then command-line values override config file values
which override defaults.

### Tests

Classic unit tests:

```
python3 -m unittest discover
```

For more detail add `-v`.

### Update

For newest repository version: 

```bash
cd <path-to-repo>
git pull
```

Or for newest stable release:

```bash
cd <path-to-repo>
git pull
git checkout `git for-each-ref --sort='*authordate' --format='%(tag)' refs/tags`
```

### Remove

```
unalias byro
rm -rf <path-to-repo>
```

Using
-----

Everythink is in the help: `byro -h`


[signHP]: http://sourceforge.net/projects/jsignpdf
[signDownload]: http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files
[Python 3]: https://www.python.org
[XeLaTeX]: http://www.latex-project.org
[Pandoc]: http://pandoc.org
[Tesseract]: https://github.com/tesseract-ocr/tesseract

