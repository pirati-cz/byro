#! /bin/bash
# Sází dopis z markdownové šablony
#
# Autoři:
# - Jakub Michálek
# - Ondřej Profant

# Global variables
packages="texlive texlive-wallpaper texlive-smartref texlive-smartref"
pandocExe="";
template="";
DIR="";

###############################
# Help
###############################
function help() {
  echo "Usage:";
  echo -e "\t$0 [-t templatePath] [-p pandocBin] [files]";
  echo -e "\t-t\tpath to LaTeX template file";
  echo -e "\t-p\tpath to pandoc binary otherwise use cabal or system version";
  echo -e "\t-h\tthis help text";
  echo "Required packages:";
  echo -e "\t${packages} pandoc";
  echo "Authors: ";
  echo -e "\tJakub Michálek";
  echo -e "\tOndřej Profant";
  exit 0;
}

function checkTeX() {
  if xelatex --version > /dev/null; then
    :
  else
    echo "Cannot locate XeLaTeX binary";
    echo "Required packes: ${packages}";
    exit 0;
  fi;
}

###############################
# Locate pandoc executable file
#
# Cabal is way to install
# latest version of pandoc
###############################
function locatePandoc() {
  if [ -n "$pandocExe" ]; then
    :
  elif "$HOME/.cabal/bin/pandoc" -v > /dev/null; then
    pandocExe="$HOME/.cabal/bin/pandoc";
  elif pandoc -v > /dev/null; then
    pandocExe="pandoc";
  else
    echo "Cannot locate pandoc binary";
    exit 1;
  fi;
}

###############################
# Locate script directory
#
# Documentation:
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
###############################
function locateScriptDir() {
  SOURCE="${BASH_SOURCE[0]}"
  while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  done
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
}

##############################
# Prepare symlink
# to templates etc.
##############################
function prepareSymlink() {
  cleanUpSymlink;

  locateScriptDir;

  ln -s "$DIR/../files/" files;
}

function cleanUpSymlink() {
  rm -f files;
}

##############################
# Markdown to pdf
# via pandoc
##############################
function md2pdf() {
  # we extract the form from the yaml front matter
  form="files/forms/"$(awk -F ":[ ]+" '/sablona/ {print $2}' < "$1")"/main.tex";
  if [ -s "$form" ]; then
    template=$form;
  fi;
  $pandocExe \
    --template=${template} \
    --latex-engine=xelatex \
    -o "$2" \
    "$1";
}

###############################
# Markdown to pdf multiple files
###############################
function md2pdfMulti() {
  if [ "$#" -eq 0 ]; then
    md2pdf main.md main.pdf
  elif [ "$#" -gt 1 ]; then
    for i in "$@"; do
	echo "Zpracovávám $i";
	md2pdf "${i}" "${i%md}pdf";
    done;
  else
    md2pdf "${i}" "${i%md}pdf"
  fi;
}


###############################
# Parse command line's arguments
###############################
function parseCmdArgs() {
 while [ "$#" -gt 0 ]; do
   case "$1" in
    -h | --help )
      help;
    ;;
    -t )
      template="$2";
      shift 2;
    ;;
    -p )
      pandocExe="$2";
      shift 2;
    ;;
    -* )
      echo "Unknown parameter: $1";
      exit 1;
    ;;
    * )
      break;
    ;;
  esac;
 done;
}

parseCmdArgs "$@";

checkTeX;

locatePandoc;

if [ -z "$template" ]; then
  prepareSymlink;
  template="files/forms/dopis/main.tex";
fi;

md2pdfMulti "$@";

cleanUpSymlink;
