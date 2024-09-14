import csv
import random


class CowModel:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.cows = self.load_cows()

    def load_cows(self):
        cows = {}
        with open(self.csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cows[row["id"]] = {
                    "id": row["id"],
                    "color": row["color"],
                    "age_years": int(row["age_years"]),
                    "age_months": int(row["age_months"]),
                    "milk_produced": int(row["milk_produced"]),
                    "bsod": row["bsod"] == "True",
                    "milk_plain": int(row["milk_plain"]),
                    "milk_sour": int(row["milk_sour"]),
                    "milk_choco": int(row["milk_choco"]),
                }
        return cows

    def get_cow(self, cow_id):
        return self.cows.get(cow_id, None)
