#!/bin/sh
STATS_FILE=$(mktemp)
python -m cProfile -o $STATS_FILE myclips batch $1
OUTPUT_FILE="profile-result.png"
python tools/gprof2dot.py -f pstats $STATS_FILE | dot -Tpng -o $OUTPUT_FILE
xdg-open $OUTPUT_FILE
#runsnake $STATS_FILE

rm $STATS_FILE