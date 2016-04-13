#! /bin/bash

DIR="/home/saikiran/Desktop/FYproject/bbc/business"
DIR2="/home/saikiran/Desktop/FYproject"

i=10

while [ $i -le 50 ]
	do
	# echo $i
	cat "$DIR/0$i.txt" >> "$DIR2/testcorpus.txt"
	(( i++ ))
	done
