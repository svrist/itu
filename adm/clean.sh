
endings="aux toc dvi log out blg bbl"
for e in $endings
do
  for f in `find -name "*.$e"`
  do
    echo "Cleaing $f"
    rm $f
  done
done
exit

for f in `find -name "*.aux"`
do
  rm $f
done

if [ -f project.toc ]
then
 rm *.toc
fi

if [ -f project.dvi ]
then
  rm project.dvi
fi

if [ -f project.log ]
then
rm *.log

fi
if [ -f project.out ]
then
rm *.out
fi

if [ -f project.blg ]; then
  rm *.blg
fi

if [ -f project.bbl ]; then
  rm *.bbl
fi
