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

    def produce_milk(self, cow_id, lemon=False):
        cow = self.get_cow(cow_id)
        if cow:
            # คำนวณโอกาส BSOD
            if cow["color"] == "brown":  # วัวสีน้ำตาลไม่เกิด BSOD
                chance = 1 * cow["age_years"]  # 1% ต่อปี
                if random.uniform(0, 100) < chance:
                    cow["color"] = "blue"
                    cow["bsod"] = True
            elif (
                cow["color"] == "white" and not lemon
            ):  # วัวสีขาวเกิดและไม่ได้กินน้ำมะนาว BSOD ได้
                chance = 0.5 * cow["age_months"]  # 0.5% ต่อเดือน
                if random.uniform(0, 100) < chance:
                    cow["color"] = "blue"
                    cow["bsod"] = True

            # ถ้าไม่เกิด BSOD ให้รีดนม
            if not cow["bsod"]:
                if cow["color"] == "white":
                    if lemon:
                        cow["milk_sour"] += 1  # นมเปรี้ยว
                    else:
                        cow["milk_plain"] += 1  # นมจืด
                elif cow["color"] == "brown":
                    cow["milk_choco"] += 1  # นมช็อกโกแลต
                cow["milk_produced"] += 1  # จำนวนขวดนมที่ผลิตทั้งหมด
            return cow
        return None

    def reset_bsod(self, cow_id):
        cow = self.get_cow(cow_id)
        if cow and cow["bsod"]:
            cow["bsod"] = False
        return cow

    def save_cows(self):
        with open(self.csv_file, mode="w", newline="") as file:
            fieldnames = [
                "id",
                "color",
                "age_years",
                "age_months",
                "milk_produced",
                "bsod",
                "milk_plain",
                "milk_sour",
                "milk_choco",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for cow in self.cows.values():
                writer.writerow(cow)
