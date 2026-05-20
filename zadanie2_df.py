from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg

# Inicjalizacja sesji Spark
spark = SparkSession.builder \
    .appName("DataFrameKaggle") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Wczytanie danych z Kaggle do DataFrame
csv_path = "Titanic.csv"
df = spark.read.csv(csv_path, header=True, inferSchema=True)

print("\nSchemat DataFrame")
df.printSchema()

print("\nPodgląd wczytanych danych")
df.show(5)

print("\nSelekcja kolumn (Klasa, Wiek, Opłata)")
df.select("Pclass", "Age", "Fare").show(5)

print("\nFiltrowanie: Pasażerowie starsi niż 30 lat")
df.filter(col("Age") > 30).show(5)

print("\nGrupowanie: Średnia opłata i suma ocalałych w zależności od klasy")
df_grouped = df.groupBy("Pclass").agg(
    avg("Fare").alias("srednia_oplata"),
    spark_sum("Survived").alias("suma_ocalalych")
)
df_grouped.show()

# Zapis przetworzonego DataFrame do pliku CSV
output_path = "output_kaggle.csv"
df_grouped.toPandas().to_csv(output_path, index=False)
print(f"\n2. Zapisano przetworzone dane do pliku: {output_path}")

# Zatrzymanie sesji
spark.stop()