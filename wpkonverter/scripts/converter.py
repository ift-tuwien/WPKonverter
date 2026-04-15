# -- Import -------------------------------------------------------------------

from csv import DictReader

# -- Functions ----------------------------------------------------------------


def main():
    with open("wpk.csv", newline="", encoding="utf8") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            print(row["Text"])
            print("—" * 50)
