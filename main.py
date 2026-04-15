# -- Import -------------------------------------------------------------------

from cvs import DictReader

# -- Functions ----------------------------------------------------------------

with open("wpk.csv", newline="", encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["Text"])
        print("—" * 50)
