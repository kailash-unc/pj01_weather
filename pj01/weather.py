"""PJ00!

Kailash Muthu
9/14/2020
UNC Chapel Hill
COMP110 - Prof. Kris Jordan

PJ01 - Weather Stats

The following project analyzes .CSV formatted weather data and performs operations given a column for analysis.

Data is resourced from NOAA's National Center for Environemental Information

Dataset consists of weather information from:
    May-10-2020 to May-16-2020 of Raleigh Airport, NC US
    Jan-01-2020 to Jan-31-2020 of Newark Liberty International Airport, NJ US

Start by using the following command to run through py module:
    python -m projects.pj01.weather [FILE] [COLUMN] [OPERATION]
Available operations are:
    list, min, max, avg, chart


HAVE AN EPIC DAY 
-----------------------------
( ͡° ͜ʖ ͡°)                 ಠ_ಠ 
-----------------------------

"""


from typing import List, Dict
from csv import DictReader
import sys


__author__ = "730411609"


SUMMARY_OF_DAY = "SOD  "


def main() -> None:
    """Main method that initiates a read of console arguments and performs operations based on args."""
    args: Dict[str, str] = read_args()
    check_args_validity(args["file"], args["column"], args["operation"])
    data: List[float] = list_op(args["file"], args["column"])
    
    if(args["operation"] == "list"):
        print(data)
    elif(args["operation"] == "min"):
        print(min(data))
    elif(args["operation"] == "max"):
        print(max(data))
    elif(args["operation"] == "avg"):
        print(sum(data) / len(data))
    elif(args["operation"] == "chart"):
        chart_op(args["file"], args["column"], data)


def read_args() -> Dict[str, str]:
    """Check for valid CLI arguments nd return them in a dictionary."""
    if len(sys.argv) != 4:
        print("Usage: python -m projects.pj01.weather [FILE] [COLUMN] [OPERATION]")
        exit()
    return {
        "file": sys.argv[1],
        "column": sys.argv[2],
        "operation": sys.argv[3]
    }


def check_args_validity(file: str, column: str, operation: str) -> None:
    """Checks for argument validity."""
    file_handle = open(file, "r", encoding="utf8")
    csv_reader = DictReader(file_handle)
    condition: bool = False
    
    for row in csv_reader:
        for _column in row:
            if _column == column:
                condition = True
    
    condition_two: bool = False

    operation_vals: List[str] = ["list", "min", "max", "avg", "chart"]

    for op in operation_vals:
        if op == operation:
            condition_two = True

    if condition is not True and condition_two is not True:
        print("Invalid column and operation: " + column + " & " + operation)
        exit()
    elif condition is not True:
        print("Invalid column: " + column)
        exit()
    elif condition_two is not True:
        print("Invalid operation: " + operation)
        exit()


def list_op(file: str, column: str) -> List[float]:
    """Returns data for desired column."""
    file_handle = open(file, "r", encoding="utf8")
    csv_reader = DictReader(file_handle)
    values: List[float] = []
    for data_row in csv_reader:
        if data_row["REPORT_TYPE"] == SUMMARY_OF_DAY:
            try:
                values.append(float(data_row[column]))
            except ValueError:
                ...
    file_handle.close()
    return values


def dates_op(file: str, column: str) -> List[str]:
    """Returns data for desired column."""
    file_handle = open(file, "r", encoding="utf8")
    csv_reader = DictReader(file_handle)
    holder: List[str] = []
    for row in csv_reader:
        if row["REPORT_TYPE"] == SUMMARY_OF_DAY:
            holder.append(row["DATE"])
    file_handle.close()
    fixedDateFormat: List[str] = []
    if(len(holder) < 30):
        for date in holder:
            date_holder: str = ""
            for char in date:
                if(char == "T"):
                    break
                date_holder += char
            fixedDateFormat.append(date_holder)
    elif(len(holder) > 30):    # When dates are greater than 30 days (more than a month)
        for date in holder:    # new format that shows only the month and date
            date_holder: str = ""
            for char in range(5, 10):
                date_holder += date[char]
            fixedDateFormat.append(date_holder)
    else:
        fixedDateFormat = holder
    return fixedDateFormat


def chart_op(file: str, column: str, data: List[float]) -> None:
    """Creates a chart of weather specific data."""
    import matplotlib.pyplot as plt
    values: List[float] = data
    dates: List[str] = dates_op(file, column)
    plt.title(column + " Over Time")
    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.show()


if __name__ == "__main__":
    main()
