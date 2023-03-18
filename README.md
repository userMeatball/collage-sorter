#CONTOUR APPROXIMATION
#turn imperfect contours to more basic

##App flow
###automatic scanner
add img or directory source
loop through files in directory or single img
grayscale img
blur img
threshold img
bitwise_not img
get contours
loop contours
crop img to contour boundary size
create directory with source image as 'AA1-src-img' to keep top
save cropped

##report gui
open dir
show dir tree on side
src img small thumbnail at top of tree
show imgs in main view
arrow or click to scroll through
manual button
boundingreact around src img
save boundingreact

##dir tree
each src img gets a dir
cycling through img updates tree
when no more imgs in dir skip to next dir