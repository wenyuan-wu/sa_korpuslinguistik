#!/bin/bash

for year in 2020 2021
do
    find data/$year -type f | xargs wc
done
