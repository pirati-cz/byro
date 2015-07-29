
Non python dependency
=====================

Package from repository in most common Linux distributions (tested on Ubuntu and Fedora):

```
gcc python3 python3-pip git pandoc tesseract tesseract-langpack-ces
texlive texlive-collection-langczechslovak texlive-collection-mathextra texlive-mathspec texlive-euenc
texlive-xetex texlive-xetex-def texlive-xltxtra
```

(~ 198 M)

Other dependency:

* [jSignPdf][signHP], [download][signDownload]


Python dependency
=================

```
pip3 install --upgrade pip  
pip3 install wget dateutils markdown ConfigArgParse python-redmine python-docx
```


Install Byro itself
===================

```
cd <path-to-repo>
git clone https://github.com/pirati-cz/byro
cd byro
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

For newest version: 
```
cd <path-to-repo>
git pull
```

Or for newest stable release:

```
cd <path-to-repo>
git pull
```

Remove
------

```
unalias byro
rm -rf <path-to-repo>
```

[signHP]: http://sourceforge.net/projects/jsignpdf
[signDownload]: http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files