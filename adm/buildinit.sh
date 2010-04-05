#!/bin/sh
ac=`ps | grep Acro | awk '{ print $1 }'`

if [ ! "x${ac}" = "x" ];
then
  kill $ac;
fi

dobuild(){
  base=
  echo "Clean"
  sh clean.sh
  for f in $@; do
    base=$f
    echo "Pdflatext $base"
    pdflatex $base.tex  |grep -B2 -A3 -P "^\s*!"
    echo "BibTex $base"
    bibtex $base | egrep -i -A3 -B3 "warning|error"
    echo "PdfLatex $base"
    pdflatex $base.tex > /dev/null
    echo "PdfLatex $base"
    pdflatex $base.tex > /dev/null
    echo "PdfLatex $base" 
    pdflatex $base.tex | grep -v "use images/" |grep -Pv "-error\d+"| egrep -i -A3 -B3 "warning|error" | grep -v "PNG copy"
    echo "Acrobat $base"
    AcroRd32 /n /s /A "page=1&zoom=100,0,0&navpanes=0=OpenActions" "$base.pdf" &
  done
  echo "Backup"
  sh clean.sh
  bash backup.sh
  echo "Done"
}
