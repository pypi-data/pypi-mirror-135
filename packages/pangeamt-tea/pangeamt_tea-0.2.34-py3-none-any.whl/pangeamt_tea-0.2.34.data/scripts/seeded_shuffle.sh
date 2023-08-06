#!/bin/bash
FILE=$1
SEED=$2
shuf --random-source=<(openssl enc -aes-256-ctr -pass pass:$SEED -nosalt </dev/zero 2>/dev/null) $FILE
