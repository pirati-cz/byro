
set boxwidth 0.6 relative
# set style data histograms
# set style histogram clustered
set style fill solid 1.0 border lt -2

set datafile separator ","


# set ytics 5000
set term png
set output 'aktivity.png'
set title customtitle
# set key autotitle columnhead
# set key outside bottom center
set key off
set xlabel customxlabel
set ylabel customylabel
set yrange [0:]

set term png size 850,340 #800 pixels by 400 pixels

plot filename using 2: xtic(1) with boxes, '' using 0:($2-1.5):(gprintf("%.0f %%",$3)) with labels
