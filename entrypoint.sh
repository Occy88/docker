#!/bin/bash
command=$(echo $@ | envsubst)
echo '================= POSTGRES CONFIG ================'
echo $POSTGRES_HOST:$POSTGRES_PORT
/usr/bin/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

echo "Running command:"
echo "$command"
exec $command