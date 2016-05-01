#! /bin/bash

DIR="/home/saikiran/Documents/Projects/FinalYearProject/bbc/business"
DIR2="/home/saikiran/Documents/Projects/FinalYearProject/"

i=100

while [ $i -le 510 ]
	do
	# echo $i
	cat "$DIR/$i.txt" >> "$DIR2/testdatabusiness.txt"
	echo "$DIR/00$i.txt"
	(( i++ ))
	done
