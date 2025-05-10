import csv
import os


def calcualteGroupAndAverage(file_path):
    dictionary = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)

        for row in rows:
            try:
                name = row[0]
                age = row[1]

                if len(name.strip()) > 0 and age.isdigit() and int(age) > 0:
                    first_character = name.strip()[0]
                    if first_character in dictionary:
                        dictionary[first_character].append(int(age))
                    else:
                        dictionary[first_character] = [int(age)]
            except IndexError:
                return {}

    sorted_dict = dict(sorted(dictionary.items()))

    resultDict = {}

    for key, valueList in sorted_dict.items():
        resultDict[key] = sum(valueList)/len(valueList)

    return resultDict

if __name__ == '__main__':
    ROOT = r'F:\GITHUB\FAST_API_Web_RESTFUL'
    file_path = os.path.join(ROOT, "data/backend_users.csv")
    print(calcualteGroupAndAverage(file_path))