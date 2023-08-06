NAME=$1
CLUSTER=$2
STAGEDIR=$3
REGION=$4
SCRIPT=$5
PARQUET=$6

pyemr init $NAME $CLUSTER $STAGEDIR dev $REGION
poetry add cowsay==4.0 fire==0.4.0
pyemr test count_rows.py $SCRIPT $PARQUET $STAGEDIR
poetry pyemr build
pyemr submit count_rows.py $SCRIPT $PARQUET $STAGEDIR
pyemr export count_rows.py $SCRIPT $PARQUET $STAGEDIR
