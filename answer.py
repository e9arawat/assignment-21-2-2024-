""" 
CRR
"""

import os
import csv
import datetime


def get_data():
    """
    return thr data
    """
    filepath = os.path.abspath("HB_NORTH_CRR.csv")
    with open(filepath, "r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        data = list(csv_reader)
    return data


def create_file(final_data):
    """
    creates a csv file
    """
    with open("recent_data.csv", "w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["iso", "refdate", "fordate", "sequence", "node", "shape", "price"]
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in final_data:
            csv_writer.writerow(row)


def answer():
    """
    CRR
    """

    data = get_data()

    sorted_data = sorted(data, key=lambda x: x["fordate"])
    index = 0
    final_data = []

    while index < len(sorted_data):
        current_fordate = sorted_data[index]["fordate"]
        current_month = datetime.datetime.strptime(current_fordate, "%Y-%m-%d").month
        month_data = []
        for d in sorted_data[index:]:
            if (
                datetime.datetime.strptime(d["fordate"], "%Y-%m-%d").month
                != current_month
            ):
                break
            month_data.append(d)
            index += 1

        unique_pair = {}
        for d in month_data:
            shape = d["shape"]
            unique_pair[shape] = unique_pair.get(shape,[])+[d]
            
        for item in unique_pair:
            unique_pair[item] = sorted(
                unique_pair[item], key=lambda x: x["sequence"], reverse=True
            )
            final_data.append(unique_pair[item][-1])

    create_file(final_data)


if __name__ == "__main__":
    answer()
