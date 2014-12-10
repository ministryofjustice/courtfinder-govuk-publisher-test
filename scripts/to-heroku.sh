#!/bin/bash

rsync -avzr --exclude '.git' --exclude 'env' ../* $1/
