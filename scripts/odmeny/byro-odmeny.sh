#! /bin/bash
# Ze souboru odměny vytvoří soubor
#
# Autoři:
# - Jakub Michálek

# Prerequisites:
# Install: sudo pip3 install csvtomd
# sudo apt-get install gnuplot
#
# use as
# 1) odmeny.sh -n -u 3 -t 2015-08
#    create new report for user number 3 for the period 2015-08
# 2) fill in manual variables
# 3) odmeny.sh -f -u 3 -t 2015-08
#    calculate missing sums in the report

username="jmi"
rewardmoney="5486"
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
template="$baseDir/files/template.md"
helpfile="$baseDir/files/README.md"

users=( [4]="Jakub Michálek"
        [3]="Ondřej Profant"
        [16]="Adam Zábranský"
        [17]="Mikuláš Ferjenčík" )

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

translit() {
  # $1 username
  vysl="$( iconv -f utf-8 -t us-ascii//TRANSLIT <<< $1 )"
  awk '{ x=$0;print tolower(gensub(/ /,"-",x)) }' <<< "$vysl"
}

readParameters() {

printf "\n"

if [ -z "$1" ]; then
  input="$output"
else
  input="$1"
fi

if [ -z "$obdobi" ]; then
  obdobi=$(awk -F ":[ ]+" '/období/ {print $2}' "$input")
fi

if [ -z "$obdobi" ]; then
  >&2 echo "Cannot read parameters: No valid time interval"
  >&2 echo "Please use with flag -t 2015-08"
  exit 1
fi

if [ -z "$pracdny" ]; then
  pracdny=$(awk -F ":[ ]+" '/počet pracovních dnů/ {print $2}' "$input")
fi

if [ -z "$pracdny" ]; then
  >&2 echo "Cannot read parameters: No number of working days in month"
  >&2 echo "Please use with flag -wd 21"
  exit 1
fi

if [ -z "$user_id" ]; then
  user_id=$(awk -F ":[ ]+" '/^user_id/ {print $2}' "$input")
fi

zastupitel="${users[$user_id]}"

if [ -z "$zastupitel" ]; then
  >&2 echo "Cannot read parameters: Unknown number of user"
  >&2 echo "Please use with flag -u 3 or --all"
  exit 1
fi

echo "The file of user $zastupitel in time $obdobi has been read"
}

lastDay() {
 mesic=${1:5}
 mesic=${mesic/0/}
 mesic=` (echo "$mesic+0" | bc )`
 days=(31 29 31 30 31 30 31 31 30 31 30 31)
 echo ${days[$mesic-1]}
}



findPattern() {
# $1="TMPCITYHOURS"

awk -F '|' -v TMP=$1 '
  function restricttosafe(string,safe) {
    safe = string
    gsub(/[^[:alnum:]_]/,"",safe)
    return safe
    }
$2 ~ TMP {print restricttosafe($1); exit}' $template

}

resetVariable() {
# $1="TMPCITYHOURS"

pattern="$(findPattern $1)"

awk -F '|' -v pattern="$pattern" -v TMP=$1 '
  function restrictsafe(pat,safe) {
    safe = pat
    gsub(/[^[:alnum:]_]/,"",safe)
    return safe
  }
  restrictsafe($1) == pattern { print $1"| "TMP; next;}
  {print $0}' $output > tmp && mv tmp $output
}

readVariable() {
# $1="cityhours"

placeholder="TMP`echo $1 | awk '{print toupper($0)}'`"

pattern="$(findPattern $placeholder)"

# 2) find the line which starts with the same character as pattern and read the value
value=$( awk -F '|' -v pat="$pattern" '
function restrictsafe(pat,safe) {
  safe = pat
  gsub(/[^[:alnum:]_]/,"",safe)
  return safe
}
restrictsafe($1) == pat { r = $2;
gsub(/[^[:digit:].]/,"",r)
print r; exit;}' $output )
declare -g $1="$value"

echo "The variable $1 was read to have value $value"
}

query() {
#1 link to csv
#2 link to html
#3 quantity
wget --user="$username" --password="$pass" --quiet "$1" -O table.csv;
hours=`awk -F, 'NR == 2 { print $3 }' table.csv;`
if [ "$hours" == "0" ] ; then hours="0.00"
fi
declare -g $3="$hours"
#echo $3":"${!3}

hours="[$hours][linkto$3]"
placeholder="TMP`echo $3 | awk '{print toupper($0)}'`"

resetVariable $placeholder

<$output awk -v hours=$hours -v placeholder=$placeholder '
    {gsub(placeholder, hours); print}
' > tmp && mv tmp $output

echo "[linkto$3]: $2" >> $output
rm table.csv
}

fillIn() {
#1 varname

placeholder="TMP`echo $1 | awk '{print toupper($0)}'`"
resetVariable $placeholder

awk -v hours="${!1}" -v placeholder="$placeholder" '
    {gsub(placeholder, hours); print > "tmp" }' $output
mv tmp $output
echo "The variable $1 was written with the value ${!1}"
}

askPassword() {
  if [ -z "$pass" ]; then
    echo -n "Password for user $username in redmine:"
    read -s pass
    echo -n "
"
  fi
}

downloadVariables() {

startdate=$obdobi"-01"
enddate=$obdobi"-`lastDay $obdobi`"
filter="op[spent_on]=><&op[user_id]==&utf8=✓&v[spent_on][]="$startdate"&v[spent_on][]="$enddate"&v[user_id][]="$user_id

# TASKS

tasklink="https://redmine.pirati.cz/projects/praha/time_entries/report.csv?c[]=project&c[]=spent_on&c[]=user&c[]=activity&c[]=issue&c[]=comments&c[]=hours&columns=month&criteria[]=issue&criteria[]=&f[]=spent_on&f[]=user_id&f[]=hours&f[]=&op[hours]=>=&v[hours][]=3&$filter"

tasklink2="https://redmine.pirati.cz/projects/praha/time_entries/report?f[]=spent_on&f[]=user_id&op[user_id]==&f[]=cf_16&op[cf_16]=!*&f[]=&columns=month&criteria[]=issue&$filter"

wget --user="$username" --password="$pass" --quiet "$tasklink" -O tasks.csv;

sed -re 's/[#:]/,/g' -e '1 s/Úkol/Fronta,Číslo, Úkol/g' -e '$ d' "tasks.csv" > tmp && mv tmp tasks.csv

awk -F ','  '{ if ( NR != 1) print "[#"$2"](https://redmine.pirati.cz/issues/"$2"),"$3","$1","$5; else print $2","$3","$1","$5}' tasks.csv > tmp && mv tmp tasks.csv

table="`csvtomd tasks.csv`" # convert it to markdown
table="`echo "$table" | sed -re 's/(\|\s*\-+)\-\s*$/\1:/g'`"

<$template awk -v table="$table" '
    {gsub(/^TMPTASKS$/, table); print}
' >> $output

echo "[tasklist]: $tasklink2" >> $output

# CITYHOURS

linktocsv="https://redmine.pirati.cz/projects/praha/time_entries/report.csv?c[]=project&c[]=spent_on&c[]=user&c[]=activity&c[]=issue&c[]=comments&c[]=hours&columns=month&criteria[]=project&criteria[]=&f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=*&$filter"

linktohtml="https://redmine.pirati.cz/projects/praha/time_entries?f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=*&$filter"

query $linktocsv $linktohtml "cityhours"

# HOMEHOURS

linktocsv="https://redmine.pirati.cz/projects/praha/time_entries/report.csv?columns=month&criteria[]=project&f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=!*&$filter"

linktohtml="https://redmine.pirati.cz/projects/praha/time_entries?f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=!*&$filter"

query $linktocsv $linktohtml "homehours"

# OTHERHOURS

linktocsv="https://redmine.pirati.cz/time_entries/report.csv?columns=month&criteria[]=user&f[]=spent_on&f[]=cf_16&f[]=project_id&f[]=&op[cf_16]==&op[project_id]=!&v[cf_16][]=strana&v[project_id][]=15&$filter"

linktohtml="https://redmine.pirati.cz/time_entries/report?f[]=spent_on&f[]=cf_16&op[cf_16]=%3D&v[cf_16][]=strana&f[]=project_id&op[project_id]=!&v[project_id][]=15&f[]=&columns=month&criteria[]=user&$filter"

query $linktocsv $linktohtml "otherhours"

# TYPE SPENT TIME

linktocsv="https://redmine.pirati.cz/projects/praha/time_entries/report.csv?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"

linktohtml="https://redmine.pirati.cz/projects/praha/time_entries/report?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"

graphActivities "$linktocsv"
echo "[activitylist]: $linktohtml" >> $output
}

graphActivities() {
  # $1 = link to csv
  wget --user="$username" --password="$pass"  --quiet "$1" -O aktivity.csv;

  title="Počet hodin strávených v měsíci na jednotlivých typech aktivit"
  customxlabel="Typ aktivity"
  customylabel="Počet hodin"

  filename="aktivity.csv"

  total="$( awk -F',' '$1 == "Celkem" { print $2 }' $filename )"
  head -n -1 "$filename" > tmp && mv tmp "$filename" # remove last line
  tail -n +2 "$filename" > tmp && mv tmp "$filename" # remove first line
  sort -r --field-separator=',' -n --key=2 $filename > tmp && mv tmp "$filename"
  # sort by 2nd column in numeric way
  head -5 "$filename" > tmp && mv tmp "$filename" # take top 5 activites
  awk -F',' -v total="$total" '{procento = 100 * $2 / total; printf "%s,%.2f,%.0f\n", $1,$2,procento}' "$filename" > tmp && mv tmp "$filename"

  # print first 7 activities
  gnuplot -e "filename='$filename'" -e "customtitle='$title'" -e "customxlabel='$customxlabel'" -e "customylabel='$customylabel'" "files/settings.gp"  &> /dev/null
}

calculateVariables() {
# PARTYHOURS
partyhours=$( bc <<< "$homehours + $otherhours" );
fillIn "partyhours"

# TOTALHOURS
totalhours=$( bc <<< "$partyhours + $cityhours" );
fillIn "totalhours"

# PERCENTAGE
norm=$( bc <<< "$pracdny * 6 * 1.00" );
percentage=$( bc <<< "100 * $totalhours/$norm" );
fillIn "percentage"
fillIn "norm"

# REFUNDMONEY
refundmoney=$( bc <<< "450 * $cityhours/ 1" );
fillIn "refundmoney"

# CITYMONEY
citymoney=$( bc <<< "$refundmoney + $rewardmoney" )
fillIn "citymoney"

# FIXEDMONEY
if (( $(echo "$partyhours >= $norm" | bc -l) ))
  then
  fixedmoney=8500;
  overtimehours=$( bc <<< "$partyhours - $norm" )
  overtimemoney=$( bc <<< "$overtimehours * 8500/ $norm" )
else
  fixedmoney=$( bc <<< "$partyhours * 8500/$norm" );
  overtimemoney="0"
fi


fillIn "fixedmoney"
fillIn "overtimemoney"

# WORKLOADMONEY
if (( $(echo "$percentage >= 100 " | bc -l) ))
then
  workloadmoney=1000
else
  workloadmoney=$( bc <<< "$percentage^2 / 10" );
fi

fillIn "workloadmoney"
fillIn "rewardmoney"
}

download=(cityhours homehours otherhours)
calcAfterDownload=(partyhours totalhours percentage refundmoney citymoney fixedmoney workloadmoney overtimemoney)
manual=(tasksmoney sanctions)
calcAfterManual=(varmoney partymoney totalmoney)

calculateFinals() {

finalVariables=(workloadmoney overtimemoney tasksmoney sanctions fixedmoney citymoney)

for var in "${finalVariables[@]}"
do
	readVariable "$var"
done

varmoney=$( bc <<< "$workloadmoney + $overtimemoney + $tasksmoney - $sanctions")
partymoney=$( bc <<< "$fixedmoney + $varmoney" )
totalmoney=$( bc <<< "$partymoney + $citymoney" )

for var in "${calcAfterManual[@]}"
do
	fillIn "$var"
done
}

moveFilesThere() {
  uname=$( translit "${users[$user_id]}")
  rok=$( awk -F '-' '{ print $1 }' <<< "$obdobi" );
  mesic=$( awk -F '-' '{ print $2 }' <<< "$obdobi" );
  dirname="output/$rok/$mesic/$uname"
  mkdir -p "$dirname"
  local=false
  if [ -e "$dirname/$output" ]; then
    saveManualVariables
    load=true
  fi
  mv $output $dirname/$output
  mv aktivity.png $dirname/aktivity.png
  if [ "$load" = true ]; then
    loadManualVariables
  fi
  rm tasks.csv aktivity.csv
  echo "Files were moved to directory $dirname"
}

createUserFile() {
askPassword
readParameters

echo "---
zastupitel:           $zastupitel
období:               $obdobi
počet pracovních dnů: $pracdny
user_id:              $user_id
---" > $output

echo "The file $output was filled with user $zastupitel in period $obdobi"

downloadVariables
calculateVariables
moveFilesThere
}

saveManualVariables() {
# at this moment we know $dirname

local currentdir=$( pwd )

cd $dirname

manual=(tasksmoney sanctions)

for var in "${manual[@]}"
do
	readVariable "$var"
done

cd $currentdir
}

loadManualVariables() {

  local currentdir=$( pwd )
  cd $dirname

  manual=(tasksmoney sanctions)

  local loadCondition=true
  for var in "${manual[@]}"
  do
    if [ -n "${!var}" ] && [ "${!var:0:3}" != "TMP" ]; then
      fillIn "$var"
      echo "Variable $var loaded with value ${!var}"
    else
      loadCondition=false
    fi
  done

  if [ "$loadCondtion" = true ] ; then
    updateUserFile $output
  fi
  cd $currentdir

}

createUserFiles() {
  for i in "${!users[@]}"
  do
    user_id=$i
    createUserFile
  done
}

updateUserFiles() {

find output/ -name "$output" -type f | while read line; do updateUserFile "$line"; done
}

updateUserFile() {
# $1 = path to file README.md
# will be called from the general function --all and also individualy
# from parameters
  unsetUserVariables
  readParameters "$1"

  local dirpath=$( dirname "$1" )
  local currentdir=$( pwd )

  cd $dirpath

  calculateFinals

  cd $currentdir

  printf "\n"
}

showAccounting() {
  find output/ -name "$output" -type f | while read line; do printAccountingLine "$line"; done
}

unsetUserVariables() {
  obdobi=""
  user_id=""
  zastupitel=""
  pracdny=""
}

printAccountingLine() {
# $1 = path to file README.md
# will be called from the general function --all and also individualy
# from parameters

    unsetUserVariables

    readParameters "$1"&> /dev/null

    local dirpath=$( dirname "$1" )
    local currentdir=$( pwd )

    cd $dirpath

    accountedVariables=(refundmoney varmoney fixedmoney)

    for var in "${accountedVariables[@]}"
    do
    	readVariable "$var" &> /dev/null
    done

    datum=$( date +%F );
    rok=$( awk -F '-' '{ print $1 }' <<< "$obdobi" );
    mesic=$( awk -F '-' '{ print $2 }' <<< "$obdobi" );
    uname=$( translit "${users[$user_id]}")

    echo "$obdobi,$datum,Praha,$zastupitel,$refundmoney,náhrada výdělku,$gh/$rok/$mesic/$uname/$output"
    echo "$obdobi,$datum,Pirati,$zastupitel,$fixedmoney,pevná část odměny z mandátní smlouvy,$gh/$rok/$mesic/$uname/$output"
    echo "$obdobi,$datum,Pirati,$zastupitel,$varmoney,proměnlivá část odměny z mandátní smlouvy,$gh/$rok/$mesic/$uname/$output"

    cd $currentdir
}


if [ "$ALL" == "YES" ] && [ "$NEW" == "YES" ]; then
  echo "You have requested to create reports for all users."
  askPassword
  createUserFiles
  exit 0
fi

if [ "$NEW" == "YES" ]; then
  createUserFile
fi

# instructions for full update of all but manu

if [ "$ALL" == "YES" ] && [ "$FINISH" == "YES" ]; then
  echo "You have requested to update reports for all users."
  updateUserFiles
  exit 0
fi

if [ "$FINISH" == "YES" ] && [ -n "$user_id" ]; then
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
  showAccounting
  exit 0
fi
