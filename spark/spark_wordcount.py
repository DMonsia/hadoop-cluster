#!/usr/bin/python3
import sys

from pyspark.sql import SparkSession
from operator import add

if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    lines = spark.sparkContext.textFile(sys.argv[1])
    word_counts = (
        lines.flatMap(lambda line: line.split())
        .map(lambda word: (word, 1))
        .reduceByKey(add)
    )

    result = word_counts.collect()
    # with open(sys.argv[2], "w") as f:
    #     f.writelines([f"{word}\t{count}\n" for word, count in result])

    for (word, count) in result:
        print(word, count, sep="\t")
