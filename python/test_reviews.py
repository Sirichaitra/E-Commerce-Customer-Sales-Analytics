import pandas as pd

reviews = pd.read_csv("../cleaned_data/reviews.csv")

print("Total rows:", len(reviews))
print("Unique review_id:", reviews["review_id"].nunique())
print("Duplicate review_id:", reviews["review_id"].duplicated().sum())