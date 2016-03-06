#downloadedVariables=(cityhours homehours otherhours)
#calculatedAfterDownload=(partyhours totalhours percentage refundmoney citymoney fixedmoney workloadmoney overtimemoney)

#manualVariables=(tasksmoney sanctions)
varmoney="0"

# Link to tasks
tasksInCsv='https://redmine.pirati.cz/projects/kspraha/time_entries/report.csv?columns=month&criteria[]=issue&f[]=spent_on&f[]=user_id&f[]=&op[spent_on]=><&op[user_id]==&utf8=✓&'"$filter"
tasksInHtml="https://redmine.pirati.cz/projects/kspraha/time_entries/report?f[]=spent_on&f[]=user_id&op[user_id]==&f[]=&columns=month&criteria[]=issue&$filter"

# Link to activities
activitiesInCsv="https://redmine.pirati.cz/projects/kspraha/time_entries/report.csv?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"
activitiesInHtml="https://redmine.pirati.cz/projects/kspraha/time_entries/report?columns=month&criteria[]=activity&f[]=spent_on&f[]=user_id&f[]=&$filter"

# there are two modes of calculation: after download and after manual completion

downloadVariables() {
  # CITYHOURS

  linktocsv='https://redmine.pirati.cz/projects/praha/time_entries/report.csv?c[]=project&c[]=spent_on&c[]=user&c[]=activity&c[]=issue&c[]=comments&c[]=hours&columns=month&criteria[]=project&criteria[]=&f[]=spent_on&f[]=user_id&'$filter

  linktohtml="https://redmine.pirati.cz/projects/praha/time_entries?f[]=spent_on&f[]=user_id&f[]=&$filter"

  query "cityhours"

}

calculateAfterDownload() {
# partyhours=$( bc <<< "$homehours + $otherhours" );
  totalhours=$( bc <<< "$cityhours" );
  thisdaynorm="${daynorms[$user_id]}";
  norm=$( bc <<< "$pracdny * $thisdaynorm * 1.00" );
  percentage=$( bc <<< "100 * $totalhours/$norm" );
  agreedwage="${sallaries[$user_id]}";
# refundmoney=$( bc <<< "450 * $cityhours/ 1" );
  fixedmoney=$( bc <<< "$agreedwage" )

  citymoney=$( bc <<< "$fixedmoney + $varmoney" )
  totalmoney=$( bc <<< "$citymoney" )

  fillIn "totalhours"
  fillIn "percentage"
  fillIn "norm"
  fillIn "fixedmoney"
  fillIn "varmoney"
  fillIn "totalmoney"
  fillIn "citymoney"
}

calculateAfterManual() {
  return 0;
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

  echo "$obdobi,$datum,Praha,$person,$fixedmoney,měsíční plat zaměstnance,$gh/$rok/$mesic/$uname/$output"
  echo "$obdobi,$datum,Praha,$person,$varmoney,mimořádná odměna,$gh/$rok/$mesic/$uname/$output"

}
