#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <heroku-directory>"
    exit
fi
rsync -avzr --exclude '.git' --exclude 'env' ../* $1/
