# Running the DB Load from Spark
docker exec -it urbanmobility-spark-master-1 /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.jars.ivy=/tmp/.ivy2 \
  --packages org.postgresql:postgresql:42.7.7 \
  /jobs/load_bikes_postgres.py