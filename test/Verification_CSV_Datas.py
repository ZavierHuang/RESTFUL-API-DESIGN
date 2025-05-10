import csv
import os


def calcualteTotalValidData(file_path):
    total = 0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)

        for row in rows:
            try:
                name = row[0]
                age = row[1]

                if len(name.strip()) > 0 and age.isdigit() and int(age) > 0:
                    total += 1
            except IndexError:
                continue

    return total

if __name__ == '__main__':
    ROOT = r'F:\GITHUB\FAST_API_Web_RESTFUL'
    file_path = os.path.join(ROOT, "data/backend_users.csv")
    print(calcualteTotalValidData(file_path))