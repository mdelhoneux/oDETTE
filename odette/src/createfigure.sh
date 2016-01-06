#!/bin/bash 
nohup pdflatex figure
nohup convert -density 150 figure.pdf -quality 90 figure.png
#nohup google-chrome figure.png
mv figure.png ./Figures
rm figure*
nohup google-chrome ./Figures/figure.png
