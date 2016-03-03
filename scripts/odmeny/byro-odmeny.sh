#! /bin/bash
# Ze souboru odměny vytvoří soubor
#
# Autoři:
# - Jakub Michálek

# Prerequisites:
# Install: sudo pip3 install csvtomd - not used any more
# sudo apt-get install gnuplot
# sudo apt-get install gawk
# sudo apt-get install python3-pip
#
# use as
# 1) odmeny.sh -n -u 3 -t 2015-08
#    create new report for user number 3 for the period 2015-08
# 2) fill in manual variables
# 3) odmeny.sh -f -u 3 -t 2015-08
#    calculate missing sums in the report
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
export LC_NUMERIC=en_US.utf-8 # sorting numbers with decimal *point*
username="jmi"
output="README.md"
gh="https://github.com/pirati-cz/KlubPraha/blob/master/odmeny"

scriptDir() {
  local SOURCE="${BASH_SOURCE[0]}"
  local DIR=""

while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
echo "$DIR"
}

baseDir="$( scriptDir )"
helpfile="$baseDir/files/README.md"
source "$baseDir/files/library.sh"


readPayrol "$baseDir/files/payroll.csv"

################################################
#                                              #
#   PARSING THE COMMAND LINE ARGUMENTS         #
#                                              #
################################################

while [[ $# > 0 ]]
do
key="$1"

case $key in
    -u|--user)
    user_id="$2"
    shift # past argument
    ;;
    -p|--password)
    pass="$2"
    shift # past argument
    ;;
    -t|--time)
    obdobi="$2"
    shift # past argument
    ;;
    -wd|--workingdays)
    pracdny="$2"
    shift # past argument
    ;;
    -a|--accounting)
    accounting="YES"
    shift # past argument
    ;;
    --all)
    ALL="YES"
    shift # past argument
    ;;
    -h|--help)
    HELP="YES"
    shift # past argument
    ;;
    -n|--new)
    NEW=YES
    ;;
    -f|--finish)
    FINISH=YES
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done



if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 $1
fi


################################################
#                                              #
#      MAIN EXECUTION OF THE PROGRAM           #
#                                              #
################################################

startInfo

checkPrerequisites

if [ "$ALL" == "YES" ] && [ "$NEW" == "YES" ]; then
  echo "You have requested to create reports for all users."
  askPassword
  createUserFiles
  exit 0
fi

if [ "$NEW" == "YES" ]; then
  echo "You have requested to create user file."
  createUserFile
fi

# instructions for full update of all but manu

if [ "$ALL" == "YES" ] && [ "$FINISH" == "YES" ]; then
  echo -e "You have requested to update reports for all users.\n"
  updateUserFiles
  exit 0
fi

if [ "$FINISH" == "YES" ] && [ -n "$user_id" ]; then
  echo "You have requested to update the report for user number "$user_id"."
  uname=$( translit "${users[$user_id]}")
  rok=$( awk -F '-' '{ print $1 }' <<< "$obdobi" );
  mesic=$( awk -F '-' '{ print $2 }' <<< "$obdobi" );
  path="output/$rok/$mesic/$uname/$output"
  updateUserFile $path
fi

if [ "$HELP" == "YES" ]; then
  cat $helpfile
fi

if [ "$accounting" == "YES" ]; then
  echo "You have requested to show the accounting information of all reports in the output directory."
  showAccounting
  exit 0
fi
