for f in *.aux
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

