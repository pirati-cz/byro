
Non python dependency
=====================

Package from repository in most common Linux distributions.

Fedora 22:
---------

```
sudo dnf install gcc python3 python3-pip git pandoc tesseract tesseract-langpack-ces \
texlive texlive-collection-langczechslovak texlive-collection-mathextra texlive-mathspec texlive-euenc \
texlive-xetex texlive-xetex-def texlive-xltxtra
```
(~ 198 M)


Ubuntu 14.04 LTS
----------------

```
sudo apt-get install gcc python3 python3-pip git pandoc tesseract-ocr tesseract-ocr-ces \
texlive texlive-lang-czechslovak texlive-xetex texlive-latex-extra
```
(~ 969 M)

Other dependency
----------------

* [jSignPdf][signHP], [download][signDownload]: in roadmap is automatic installation


Python dependency
=================

```bash
sudo pip3 install --upgrade pip  
sudo pip3 install wget dateutils markdown ConfigArgParse python-redmine python-docx
```


Install Byro itself
===================

```bash
cd <path-to-repo>
git clone https://github.com/pirati-cz/byro
cd byro
git checkout `git for-each-ref --sort='*authordate' --format='%(tag)' refs/tags`
python3 -m unittest discover
```

Path to repo is directory where repository is cloned. For example `/opt/`.

Last command launch unit tests. If all pass everything is ok.

For simple using, create alias: 

```
alias byro="$PWD/byro.py"
```

Update
------

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

Remove
------

```
unalias byro
rm -rf <path-to-repo>
```

[signHP]: http://sourceforge.net/projects/jsignpdf
[signDownload]: http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files