#!/bin/bash
for i in {1..25}; do
    echo
    echo "Day $i :"
    time AOC_QUIET=TRUE run_day$i --skip
done

echo ""
echo "25 Days:"
