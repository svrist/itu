#!/bin/sh
ac=`ps | grep Acro | awk '{ print $1 }'`

if [ ! "x${ac}" = "x" ];
then
  kill $ac;
fi
echo "Clean"
sh clean.sh
echo "Pdflatext"
pdflatex project.tex  |grep -B2 -A3 -P "^\s*!"
echo "BibTex"
bibtex project | egrep -i -A3 -B3 "warning|error"
echo "PdfLatex"
pdflatex project.tex > /dev/null
echo "PdfLatex" 
pdflatex project.tex | grep -v "use images/" |grep -Pv "-error\d+"| egrep -i -A3 -B3 "warning|error" | grep -v "PNG copy"
echo "Acrobat"
AcroRd32 project.pdf &
echo "Done"
