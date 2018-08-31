#!/bin/bash

BGCOLOR="#152F56"

# Yellow - Artist
ARTISTCOLOR="#f2ac08"

# Green - Character
CHARACTERCOLOR="#00a000"

# Purple - Copyright
COPYRIGHTCOLOR="#d0d0d0"

# Orange - Species
SPECIESCOLOR="#ed5d1f"

# White - Any other tag
GENERALCOLOR="#b4c7d9"

COUNTCOLOR="#a0a0a0"

COMMAND="convert -font Verdana-Bold -background \"$BGCOLOR\" -pointsize 72 pango:'<span foreground=\""

if [ $# -lt 3 ]
then
	echo Only $# arguments supplied
	echo Provide a tag name, tag type and a result count
	exit 1
fi

COLOR="$2COLOR"

eval COLOR=\$$COLOR

COMMAND+=$COLOR
COMMAND+="\">? + - "
COMMAND+=$1
COMMAND+="</span><span foreground=\""
COMMAND+=$COUNTCOLOR
COMMAND+="\"> "
COMMAND+=$3

COMMAND+="</span>' tag.png"

echo $COMMAND
eval $COMMAND
