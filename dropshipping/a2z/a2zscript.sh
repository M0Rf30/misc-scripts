#!/bin/sh
SUPPLIER=a2zworld
EXT="csv"
OUTPUT="$SUPPLIER-elaborato"

if [ -f $OUTPUT.$EXT ]; then
	rm $OUTPUT.$EXT
fi

INPUT=$(ls *.csv)

sed -e 's/^/1|/' $INPUT > $OUTPUT.$EXT
scp $OUTPUT.$EXT root@79.39.253.225:/srv/http/admin033tqfqsd/import/
