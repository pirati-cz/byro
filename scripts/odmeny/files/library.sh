color='\033[0;31m'
nocolor='\033[0m' # No Color
record=""
redmine='https://redmine.pirati.cz'

declare -A projectnumbers
declare -A projectname

projectnumbers["kspraha"]="44"
projectnumbers["praha"]="15"
projectname["kspraha"]="krajské sdružení Praha"
projectname["praha"]="klub zastupitelů hl. m. Prahy"

################################################
#                                              #
#             BIG LIST OF FUNCTIONS            #
#                                              #
################################################

startInfo() {
  printf "\n${color}byro odmeny${nocolor}\n-------------\n \n"
}

checkPrerequisites() {

  # check if the required packages are installed, if not, install it

packages=('gnuplot' 'gawk' 'python3-pip')

echo -e "\n${color}Installation${nocolor}
The packages necessary packages may be installed..."
sudo apt-get install "${packages[@]}"
sudo pip3 install csvtomd
echo -e "\n"
}

readPayrol() {

  # for given csv file with payrol creates array structure with values
  # e.g.  use as: readPayrol baseDir/files/payroll.csv
  # now we can reference the information as such:
  # echo ${users[3]}", "${occupations[3]}

  while IFS=, read -r rmid name occupation homeproject dayhours thistemplate sallary contract
  do
    if [ "$rmid" != "Redmine" ]; then
      users[$rmid]=$name;
      occupations[$rmid]=$occupation;
      daynorms[$rmid]=$dayhours;
      homeprojects[$rmid]=$homeproject;
      templates[$rmid]=$thistemplate;
      sallaries[$rmid]=$sallary;
      contracts[$rmid]="$contract";
    fi
  done < $1

}

translit() {

  # convert a string with diacritics and spaces to an ASCII hyphenated string
  # use as translit $1 "$username"

  vysl="$( iconv -f utf-8 -t us-ascii//TRANSLIT <<< $1 )"
  awk '{ x=$0;print tolower(gensub(/ /,"-",x)) }' <<< "$vysl"
}

lastDay() {

  #return

  mesic=${1:5}
  mesic=${mesic/0/}
  mesic=$( bc <<< "$mesic+0" )
  days=(31 29 31 30 31 30 31 31 30 31 30 31)
  echo ${days[$mesic-1]}
}

findPattern() {

  # in the file $template find the pattern before the VARKEYWORD
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
  # in the file $output revert the line with variable to the line in $template
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

  # read the variable with the given name from $output and save it as global var
  # $1="cityhours"

  placeholder="TMP"$( awk '{print toupper($0)}' <<< $1 )

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

fillIn() {
  # write the variable with the given name to the file $output
  # $1=varname, $2=link (optional)

  placeholder="TMP"$(awk '{print toupper($0)}' <<< $1)
  resetVariable $placeholder

  if [ -n "$2" ]; then
    hours="[${!1}][$2]"
  else
    hours="${!1}"
  fi

  awk -v hours="$hours" -v placeholder="$placeholder" '
      {gsub(placeholder, hours); print > "tmp" }' $output
  mv tmp $output
  echo "The variable $1 was written with the value ${!1}"
}

query() {

  # download variable and fill it in with a link
  # requires $1=varname, $linktohtml $linktocsv, $update, $output

  downloadVariable "$linktocsv" "$1"
  fillIn "$1" "linkto$1"

  if [ -z "$update" ]; then
    echo "[linkto$1]: $linktohtml" >> $output
  fi
}

setFilter() {
  startdate=$obdobi"-01"
  enddate=$obdobi"-"$(lastDay $obdobi)
  filter="op[spent_on]=><&op[user_id]==&utf8=✓&v[spent_on][]="$startdate"&v[spent_on][]="$enddate"&v[user_id][]="$user_id
}

askPassword() {
  if [ -z "$pass" ]; then
    echo -n "Password for user $username in redmine:"
    read -s pass
    echo -en "\n"
  fi
}

downloadVariable() {

  # download the quantity, fill it into global variable
  #1 link to csv
  #2 quantity
  wget --user="$username" --password="$pass" --quiet "$1" -O table.csv;
  hours=$(awk -F, 'NR == 2 { print $3 }' table.csv)
  if [ "$hours" == "0" ] ; then
    hours="0.00"
  fi
  declare -g $2="$hours"
  rm table.csv
}

getParameters() {

  # returns the basic parameters from a file if not defined

  if [ -z "$1" ]; then
    input="$output" # read from basic file at the moment
  else
    input="$1"      # or the given file
  fi

  if [ -z "$obdobi" ]; then
    obdobi=$(awk -F ":[ ]+" '/období/ {print $2}' "$input")
  fi

  if [ -z "$obdobi" ]; then
    >&2 echo "Cannot read parameters: No valid time interval"
    >&2 echo "Please use with flag -t 2015-08"
    return 1
  fi

  if [ -z "$pracdny" ]; then
    pracdny=$(awk -F ":[ ]+" '/počet pracovních dnů/ {print $2}' "$input")
  fi

  if [ -z "$pracdny" ]; then
    >&2 echo "Cannot read parameters: No number of working days in month"
    >&2 echo "Please use with flag -wd 21"
    return 1
  fi

  if [ -z "$user_id" ]; then
    user_id=$(awk -F ":[ ]+" '/^user_id/ {print $2}' "$input")
  fi

  person="${users[$user_id]}"

  if [ -z "$person" ]; then
    >&2 echo "Cannot read parameters: Unknown number of user"
    >&2 echo "Please use with flag -u 3 or --all"
    return 1
  fi

  template="$baseDir/files/"$( translit "${templates[$user_id]}")"/template.md"

}

downloadTasks() {

  # downloads the list of tasks given in $tasksInCsv and prints it to template

  echo "Downloading list of tasks"
  wget --user="$username" --password="$pass" --quiet "$tasksInCsv" -O tasks.csv;

  echo "Printing the list of tasks"

  awk -F',' '{if ( $0 ~ /^#/ ) {print "Úkol "$1": nezveřejněný úkol,"$2","$3}
  else print}' tasks.csv > tmp && mv tmp tasks.csv
  # 2) change # and : to the official delimiter ","
  sed -re 's/[#:]/,/g' -e '1 s/Úkol/Fronta,Číslo, Název úkolu/g' tasks.csv > tmp && mv tmp tasks.csv
  # 3) remove the first and the last line
  head -n -1 tasks.csv > tmp && mv tmp tasks.csv # remove last line
  #tail -n +2 tasks.csv > tmp && mv tmp tasks.csv # remove first line
  # 4) filter only tasks with at least 3 hours in a month

  awk -F',' 'NR==1 {print $2","$3","$5; next;}
  $4 >= 3.0 {print $2","$3","$5}' "tasks.csv" > tmp && mv tmp tasks.csv
  # 5) save header and delete it from file
  tail -n +2 tasks.csv > body.csv
  head -n 1 tasks.csv > tmp && mv tmp tasks.csv
  # 6) sort it in the right direction
  sort -t ',' -k 3,3rn body.csv > tmp && mv tmp body.csv # we shall use this later when printing links
  # 7) join files
  awk -F',' '{print "[#"$1"][task"$1"],"$2",["$3"][time"$1"]"}' body.csv >> tasks.csv
  # cat tasks.csv # test file
  csvtomd tasks.csv > tasks.md
  # 8) change the alignment of the last column
  sed -re 's/(\|\s*\-+)\-$/\1:/g' tasks.md > tmp && mv tmp tasks.md
  tasks=$(cat tasks.md)
  rm tasks.md tasks.csv

  <$template awk -v table="$tasks" '
      {gsub(/^TMPTASKS$/, table); print}
  ' >> $output

  echo "[tasklist]: $tasksInHtml" >> $output

  awk -F ',' -v "filter=$filter" ' { print "[task"$1"]: https://redmine.pirati.cz/issues/"$1
  print "[time"$1"]:https://redmine.pirati.cz/issues/"$1"/time_entries?f[]=spent_on&f[]=user_id&f[]=&op[spent_on]=><&op[user_id]==&"filter  }' body.csv >> $output
  rm body.csv

  # TYPE SPENT TIME

  graphActivities "$activitiesInCsv"

  echo -e "[activitylist]: $activitiesInHtml\n" >> $output

  contract="${contracts[$user_id]}"
  if [ -n "$contract" ]; then
    echo -e "[smlouva]: $contract" >> $output
  fi

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

  sort -t ',' -k 2,2rn $filename > tmp && mv tmp $filename
  # sort by 2nd column in numeric way
  head -5 "$filename" > tmp && mv tmp "$filename" # take top 5 activites
  awk -F',' -v total="$total" '{procento = 100 * $2 / total; printf "%s,%.2f,%.0f\n", $1,$2,procento}' "$filename" > tmp && mv tmp "$filename"

  # print first 7 activities
  gnuplot -e "filename='$filename'" -e "customtitle='$title'" -e "customxlabel='$customxlabel'" -e "customylabel='$customylabel'" "files/settings.gp"  &> /dev/null
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
  rm aktivity.csv
  echo "Files were moved to directory $dirname"
}

createUserFile() {

  # create new user file and fill it with downloaded and calculated vars

  askPassword

  getParameters
  printf "\nCreating file for user $color$person$nocolor\n"
  setFilter

  myfunctions="$baseDir/files/"$( translit "${templates[$user_id]}")"/calculate.sh"
  source $myfunctions

  # create the basic
  echo "---
osoba:                $person
období:               $obdobi
počet pracovních dnů: $pracdny
user_id:              $user_id
---" > $output

  downloadTasks # also copies the template for the first time

  echo "The file $output was filled with user $person in period $obdobi"

  downloadVariables
  calculateAfterDownload
  moveFilesThere
}

saveManualVariables() {

  # saves the value of manual variables to global vars
  # at this moment we know $dirname

  local currentdir=$( pwd )

  cd $dirname

  for var in "${manualVariables[@]}"
  do
  	readVariable "$var"
  done

  cd $currentdir
}

loadManualVariables() {

  # updates user files with the loaded manually filled vars

  local currentdir=$( pwd )
  cd $dirname

  local loadCondition=true
  for var in "${manualVariables[@]}"
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

  # creates a user file for all $users

  for i in "${!users[@]}"
  do
    user_id=$i
    createUserFile
  done

  createUserList
}

createUserList() {
  rok=$( awk -F '-' '{ print $1 }' <<< "$obdobi" );
  mesic=$( awk -F '-' '{ print $2 }' <<< "$obdobi" );
  path="output/$rok/$mesic/README.md"
  local mylongdate=$(date --date "$obdobi-01" '+%B %Y' )
  echo "---
období: $obdobi
---

Česká pirátská strana  
krajské sdružení Praha  

Výkazy odměňování za $mylongdate
=======================================

" > $path

  while IFS=, read -r rmid name occupation homeproject dayhours thistemplate sallary contract
  do
    if [ "$name" == "jméno a příjmení" ]; then
      echo "$name,$occupation,$homeproject,$thistemplate" > tmp.csv
    else
      persontranslit=$(translit "$name")
      local num=${projectnumbers[$homeproject]}
      local pname=${projectname[$homeproject]}
      local contractfield=""
      if [ -n "$contract" ]; then
        contractfield="[$thistemplate][c$rmid]";
        echo "[c$rmid]: $contract" >> contracts.md
      fi
      echo '['"$name][u$rmid],$occupation,[$pname][p$num],$contractfield" >> tmp.csv
      echo "[u$rmid]: $persontranslit/" >> users.md
      local used[$num]=true
    fi
  done < files/payroll.csv

  csvtomd tmp.csv >> $path
  printf "\n" >> $path
  # echo all projects that have been used
  for i in "${!used[@]}"
  do
    echo "[p$i]: $redmine/project/$i" >> $path
  done
  printf "\n" >> $path
  cat users.md >> $path
  printf "\n" >> $path
  cat contracts.md >> $path
  rm tmp.csv users.md contracts.md
}

updateUserFiles() {

  # update all user files
  find output/ -name "$output" -type f | while read line; do updateUserFile "$line"; done
}

updateUserFile() {

  # update user file after filling in sanctions etc.

  # $1 = path to file README.md
  # will be called from the general function --all and also individualy
  # from parameters

  printf "Updating file $color$1$nocolor.\n"
  unsetUserVariables
  getParameters "$1"
  if [ -z "$person" ]; then
    echo -e "This file does not describe a report of a user, skipping.\n"
    return 1
  fi
  setFilter

  myfunctions="$baseDir/files/"$( translit "${templates[$user_id]}")"/calculate.sh"
  source $myfunctions

  local dirpath=$( dirname "$1" )
  local currentdir=$( pwd )

  cd $dirpath

  calculateAfterManual

  cd $currentdir

  printf "\n"
}



showAccounting() {

  # print accounting information for all files in directory structure

  find output/ -name "$output" -type f | while read line; do printAccountingLine "$line"; done
}

unsetUserVariables() {
  obdobi=""
  user_id=""
  person=""
  pracdny=""
}

printAccountingLine() {

  # prints accounting information to standard output

  # $1 = path to file README.md
  # will be called from the general function --all and also individualy
  # from parameters

    unsetUserVariables

    getParameters "$1"&> /dev/null

    local dirpath=$( dirname "$1" )
    local currentdir=$( pwd )

    myfunctions="$baseDir/files/"$( translit "${templates[$user_id]}")"/calculate.sh"
    source $myfunctions

    cd $dirpath

    printAccountingForJob

    cd $currentdir
}

prependArray() {
  # prepends all fields of $myarray with $1

  for i in "${!myarray[@]}"
  do
    myarray[$i]="$1${myarray[$i]}"
  done
}

concatArray() {
  local IFS='&'
  
  echo "${myarray[*]}"
}


homeHoursLink() {

  # returns the link to homehours project
  # $1 = name of the project
  # $2 = format of the project (csv or html)
  # use as: homeHoursLink 'praha' 'csv'

  case $2 in
  csv)  path="$1/time_entries/report.csv?columns=month&criteria[]=project&";;
  html) path="$1/time_entries?";;
  esac

  myarray=('spent_on' 'user_id' '' 'subproject_id')
  prependArray 'f[]='
  echo "$redmine/projects/$path"$(concatArray)'&op[subproject_id]=!*&'"$filter"
}

otherHoursLink() {

  # returns the link to homehours project
  # $1 = name of the project
  # $2 = format of the project (csv or html)
  # use as: homeHoursLink 'praha' 'csv'
  case $2 in
  csv)  path="time_entries/report.csv?";;
  html) path="time_entries?";;
  esac

  myarray=('spent_on' 'user_id' 'cf_16' 'project_id' '')
  prependArray 'f[]='
  local f=$(concatArray)
  local num="${projectnumbers[$1]}"
  myarray=('op[cf_16]==' 'op[project_id]=!' 'v[cf_16][]=strana' "v[project_id][]=$num")
  local a=$(concatArray)

  local b='columns=month&criteria[]=user'

  echo "$redmine/$path&$b&$f&$a&$filter"
}
