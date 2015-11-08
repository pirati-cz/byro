#! /bin/bash
# Ze souboru odměny vytvoří soubor
#
# Autoři:
# - Jakub Michálek

# Prerequisites:
# Install: sudo pip3 install csvtomd
# sudo apt-get install gnuplot

sourcefile="https://raw.githubusercontent.com/pirati-cz/KlubPraha/master/odmeny/odmeny.csv"
data="data.csv"
pivotdata="pivotdata.csv"
template="files/templates/README.md"
output="output/README.md"

pivotTable() {
  awk -F\, '
NR>1 {
    if(!($1 in indicators)) { indicator[++types] = $1 }; indicators[$1]++
    if(!($2 in countries)) { country[++num] = $2 }; countries[$2]++
    map[$1,$2] = $3
}
END {
    printf "%s," ,"Měsíc";
    for(ind=1; ind<=types; ind++) {
        printf "%s%s", sep, indicator[ind];
        sep = ","
    }
    print "";
    for(coun=1; coun<=num; coun++) {
        printf "%s", country[coun]
        for(val=1; val<=types; val++) {
            printf "%s%s", sep, map[indicator[val], country[coun]];
        }
        print ""
    }
}' $1
}

transposeTable() {
  awk -F\, '
{
    for (i=1; i<=NF; i++)  {
        a[NR,i] = $i
    }
}
NF>p { p = NF }
END {
    for(j=1; j<=p; j++) {
        str=a[1,j]
        for(i=2; i<=NR; i++){
            str=str","a[i,j];
        }
        print str
    }
}' $1
}

# Month,Date,Payer,PayerId,Payee,PayeeId,Amount,Claim,Source

printImage() {
# $1 je nadpis tabulky

translit="$( iconv -f utf-8 -t ascii//translit <<< $1)"
dirname="${translit// /-}"
pathname=output/$dirname
mkdir -p output/$dirname



title="$1"

mkdir -p "output"

awk -F ',' -v mycolname="$1" 'BEGIN {OFS=","} { if (tolower($6) == mycolname || NR == 1)  print $1","$4","$5}' tmp.csv > $pathname/$data

# export table to markdown

pivotTable $pathname/$data > $pathname/pivot.csv # generate pivot table in csv
transposeTable $pathname/pivot.csv > $pathname/$data
rm $pathname/pivot.csv

# table="`csvtomd $pathname/$pivotdata`" # convert it to markdown

# add currency (Kč) and alignment (---:)
# table="`echo "$table" | sed -re 's/(\s[0-9]+\s)(\s\s)/\1Kč/g' -e 's/(\|\s*\-+)\-/\1:/g'`"

# insert it into template
#<"$template" awk -v table="$table" '
#    {gsub(/^TMPTABLE$/, table); print}
#' > "$output"



#IFS=","
#header=$(head -n 1 $data)
#labels=( echo "$header" | cut -d ',' -f1 )

customxlabel="Měsíc"
customylabel="Výše příjmů (Kč)"


#customxlabel=$( awk -F ','  'BEGIN {OFS=","} { if (NR == 1)  print $1}' $pathname/$data )
#customylabel=$( awk -F ','  'BEGIN {OFS=","} { if (NR == 1)  print $3}' $pathname/$data )

# number of columns
col_count=$(awk -F"," "{print NF;exit}" $pathname/$data )

gnuplot  -e "filename='$pathname/$data'" -e "imagepath='$pathname/graf.png'" -e "customtitle='$title'" -e "customxlabel='$customxlabel'" -e "customylabel='$customylabel'" -e "col_count='$col_count'" "files/settings.gp" #&> /dev/null

}

incometypes=("paušální odměna" "náhrada výdělku" "pevná část odměny z mandátní smlouvy" "proměnlivá část odměny z mandátní smlouvy" "plat zaměstnance")

wget "$sourcefile" -O tmp.csv;

for var in "${incometypes[@]}"
do
	printImage "$var"
done

cp files/templates/sunshine.jpg output/sunshine.jpg
cp $template $output

rm tmp.csv
