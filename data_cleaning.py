from pyspark.sql import SparkSession

# Inizializza una sessione Spark
spark = SparkSession.builder \
    .appName("Game of Life Data Cleaning") \
    .getOrCreate()

def clean_data(data):
    # Crea un DataFrame PySpark dai dati
    df = spark.createDataFrame(data)
    # Pulizia dei dati: riempie i valori mancanti con 0
    cleaned_df = df.na.fill(0)
    return cleaned_df.toPandas()  # Converte nuovamente in Pandas DataFrame
