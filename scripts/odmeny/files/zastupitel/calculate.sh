#downloadedVariables=(cityhours homehours otherhours)
#calculatedAfterDownload=(partyhours totalhours percentage refundmoney citymoney fixedmoney workloadmoney overtimemoney)
manualVariables=(tasksmoney sanctions)
rewardmoney="5486"

# Link to tasks
tasksInCsv='https://redmine.pirati.cz/projects/kspraha/time_entries/report.csv?columns=month&criteria[]=issue&f[]=spent_on&f[]=user_id&f[]=&op[spent_on]=><&op[user_id]==&utf8=✓&'"$filter"
tasksInHtml="https://redmine.pirati.cz/projects/kspraha/time_entries/report?f[]=spent_on&f[]=user_id&op[user_id]==&f[]=&columns=month&criteria[]=issue&$filter"

# Link to activities
activitiesInCsv="https://redmine.pirati.cz/projects/kspraha/time_entries/report.csv?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"
activitiesInHtml="https://redmine.pirati.cz/projects/kspraha/time_entries/report?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"

# there are two modes of calculation: after download and after manual completion

downloadVariables() {
  # CITYHOURS

  linktocsv='https://redmine.pirati.cz/projects/praha/time_entries/report.csv?c[]=project&c[]=spent_on&c[]=user&c[]=activity&c[]=issue&c[]=comments&c[]=hours&columns=month&criteria[]=project&criteria[]=&f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=*&'$filter

  linktohtml="https://redmine.pirati.cz/projects/praha/time_entries?f[]=spent_on&f[]=user_id&f[]=cf_16&f[]=&op[cf_16]=*&$filter"

  query "cityhours"

  # HOMEHOURS

  linktocsv=$( homeHoursLink ${homeprojects[$user_id]} 'csv')
  linktohtml=$( homeHoursLink ${homeprojects[$user_id]} 'html')
  query "homehours"

  # OTHERHOURS - in all projects except KS Praha

  linktocsv=$( otherHoursLink ${homeprojects[$user_id]} 'csv')
  linktohtml=$( otherHoursLink ${homeprojects[$user_id]} 'html')
  query "otherhours"

}

calculateAfterDownload() {
  partyhours=$( bc <<< "$homehours + $otherhours" );
  totalhours=$( bc <<< "$partyhours + $cityhours" );
  thisdaynorm="${daynorms[$user_id]}";
  norm=$( bc <<< "$pracdny * $thisdaynorm * 1.00" );
  percentage=$( bc <<< "100 * $totalhours/$norm" );
  agreedwage="${sallaries[$user_id]}";
  refundmoney=$( bc <<< "450 * $cityhours/ 1" );
  citymoney=$( bc <<< "$refundmoney + $rewardmoney" )
  if (( $(echo "$partyhours >= $norm" | bc -l) ))
    then
    fixedmoney=$agreedwage;
    overtimehours=$( bc <<< "$partyhours - $norm" )
    overtimemoney=$( bc <<< "$overtimehours * $agreedwage/ $norm" )
  else
    fixedmoney=$( bc <<< "$partyhours * $agreedwage/$norm" );
    overtimemoney="0"
  fi
  if (( $(echo "$percentage >= 100 " | bc -l) ))
  then
    workloadmoney=1000
  else
    workloadmoney=$( bc <<< "$percentage^2 / 10" );
  fi

  fillIn "partyhours"
  fillIn "totalhours"
  fillIn "percentage"
  fillIn "norm"
  fillIn "fixedmoney"
  fillIn "overtimemoney"
  fillIn "workloadmoney"
  fillIn "rewardmoney"
  fillIn "refundmoney"
  fillIn "citymoney"
}

calculateAfterManual() {
  finalVariables=(workloadmoney overtimemoney tasksmoney sanctions fixedmoney citymoney)

  for var in "${finalVariables[@]}"
  do
  	readVariable "$var"
  done

  varmoney=$( bc <<< "$workloadmoney + $overtimemoney + $tasksmoney - $sanctions")
  partymoney=$( bc <<< "$fixedmoney + $varmoney" )
  totalmoney=$( bc <<< "$partymoney + $citymoney" )

  calculatedAfterManual=(varmoney partymoney totalmoney)

  for var in "${calculatedAfterManual[@]}"
  do
  	fillIn "$var"
  done

}

printAccountingForJob() {
  accountedVariables=(refundmoney varmoney fixedmoney)

  for var in "${accountedVariables[@]}"
  do
    readVariable "$var" &> /dev/null
  done

  datum=$( date +%F );
  rok=$( awk -F '-' '{ print $1 }' <<< "$obdobi" );
  mesic=$( awk -F '-' '{ print $2 }' <<< "$obdobi" );
  uname=$( translit "${users[$user_id]}")

  echo "$obdobi,$datum,Praha,$person,$refundmoney,náhrada výdělku,$gh/$rok/$mesic/$uname/$output"
  echo "$obdobi,$datum,Pirati,$person,$fixedmoney,pevná část odměny z mandátní smlouvy,$gh/$rok/$mesic/$uname/$output"
  echo "$obdobi,$datum,Pirati,$person,$varmoney,proměnlivá část odměny z mandátní smlouvy,$gh/$rok/$mesic/$uname/$output"

  printf "\nImportant notice: The reward money from the city is not accounted for and is calculated every month. \n"

}
