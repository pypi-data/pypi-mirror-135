# pyspark-df-cleaner
Making life easier. This package is used for cleaning Pyspark dataframes. The module will be extended in the future.

It currently consists of three main features:
- Removing leading zeros from column -> e.g. Turns "0000F45" into "F45"
- Casting int/long column to date -> e.g. Turns int/long column into Pyspark DateType()
- keep_alphanumeric_string -> e.g. Turns "444-555-666" into "444555666"

Should you have any suggestions for additional features, just let me know.
