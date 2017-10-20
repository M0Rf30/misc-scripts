#!/bin/sh
SUPPLIER=pannomagico
EXT="csv"
OUTPUT="$SUPPLIER-elaborato"

if [ -f $OUTPUT.$EXT ]; then
	rm $OUTPUT.$EXT
fi

INPUT=$(ls *.csv)

dos2unix $INPUT
sed -e 's/\xA7/\x7C/g' $INPUT > $OUTPUT.$EXT
sed -e 's/^/3|/' $INPUT > $OUTPUT.$EXT
scp $OUTPUT.$EXT root@79.39.253.225:/srv/http/admin033tqfqsd/import/