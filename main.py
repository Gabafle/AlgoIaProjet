# This is a sample Python script.
from coverage.annotate import os
import pandas as pd
import matplotlib.pyplot as plt
from pre_processing_services.dataCollector import DataCollector

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(
        ROOT_DIR,
        "data_sample",
        "input",
        "Data",
        "Workload.xlsx"
    )
    collector = DataCollector()
    data = collector.collect(file_path)
    print(data)

    x= data.get("time").values
    y= data.get("input_rates").values
    plt.plot(x,y)
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
