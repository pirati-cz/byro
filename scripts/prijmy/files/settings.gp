

# set style data histograms
set style histogram cluster gap 2
set style fill solid 1.0 border lt -1

refwidth= 0.3
pfactor = 1
mywidth = refwidth * (col_count + pfactor)/(1.0+pfactor)
set boxwidth mywidth absolute


set datafile separator ","

scalenum = 5000.0
subscale = 4.0

set ytics scalenum

set title customtitle
set key autotitle columnhead
set key bmargin
set xlabel customxlabel
set ylabel customylabel

# Retrieve statistical properties via dummy plot
plot for [COL=2:col_count:1] filename using COL: xtic(1) with histogram ls COL

max_y = GPVAL_DATA_Y_MAX
num_months = GPVAL_DATA_X_MAX+GPVAL_DATA_X_MIN + 1
print num_months

myrangey = ceil(subscale*max_y/scalenum)*(scalenum/subscale)

# define my values of margin in pixels
mylmargin = 150.0                    # includes ylegend and ytics
myrmargin = 20.0                     # simple margin
mybmargin = (col_count-1)*20 + 80.0  # includes title
mytmargin = 100.0                    # includes legend + xlegend and xtics

mywidth  = (num_months) * (850/12.0) + mylmargin + myrmargin 
myheight = 400/20000.0*myrangey + mytmargin + mybmargin 

set lmargin at screen mylmargin/mywidth
set rmargin at screen (mywidth-myrmargin)/mywidth
set tmargin at screen (myheight-mytmargin)/myheight
set bmargin at screen mybmargin/myheight

set term png size mywidth,myheight #800 pixels by 400 pixels
set output imagepath

set yrange [0:myrangey]
show margin
show boxwidth

load 'files/templates/YlOrRd.plt'

replot
