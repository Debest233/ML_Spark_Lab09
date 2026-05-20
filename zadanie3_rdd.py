import os
import sys
import csv
from pyspark.sql import SparkSession

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder.appName("RDD_Titanic").getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("ERROR")

print("\nRozpoczynam przetwarzanie RDD\n")

with open("titanic.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

rdd_text = sc.parallelize(lines)

header = lines[0]
rdd_data = rdd_text.filter(lambda line: line != header)

def parse_line(line):
    return next(csv.reader([line.strip()]))

rdd_parsed = rdd_data.map(parse_line)

total_passengers = rdd_parsed.count()
print(f"Całkowita liczba pasażerów (liczba wierszy): {total_passengers}")

rdd_survived = rdd_parsed.filter(lambda cols: cols[1] == '1')
survived_count = rdd_survived.count()
print(f"Liczba ocalałych pasażerów: {survived_count}")

def get_fare(cols):
    try:
        return float(cols[9])
    except ValueError:
        return 0.0

rdd_fares = rdd_parsed.map(get_fare)
total_fare = rdd_fares.reduce(lambda x, y: x + y)
print(f"Łączna suma zapłacona za bilety: {total_fare:.2f}\n")

spark.stop()