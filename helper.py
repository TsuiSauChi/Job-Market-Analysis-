import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def volin_plot(min_salaries, max_salaries, title):
    # Combine the minimum and maximum salaries into a single array
    salary_data = np.vstack((min_salaries, max_salaries)).T
    df = pd.DataFrame(salary_data, columns=['Min Salary', 'Max Salary'])

    # Set up the plot
    plt.figure(figsize=(10, 6))

    # Create a violin plot
    ax = sns.violinplot(data=df, inner='quart', orient='h')
    sns.boxplot(data=df, width=0.2, boxprops=dict(alpha=0.9), orient='h')

    # Add labels and title
    plt.xlabel('Salary Range')
    plt.ylabel('Categories')
    plt.title('Minimum to Maximum Salary Ranges for ' + title)

    # Annotate median values
    for tick, median in zip(ax.get_yticks(), df.median().values):
        ax.text(median, tick, f'{median:.2f}', ha='right', va='center', fontweight='bold', color='white')

    # Create the legend for data point counts
    handles, labels = [], []
    for i, (category, count) in enumerate(zip(df.columns, df.count().values)):
        handles.append(plt.Rectangle((0, 0), 0, 0, fill=False, edgecolor='none'))
        labels.append(f'{category} (n={count})')

    # Add the legend to the plot
    ax.legend(handles, labels, loc='lower right')

    # Show the plot
    plt.show()

def json_to_file(filename, data):
    # Step 1: Convert data to a JSON string
    json_data = json.dumps(data, indent=4)  # The 'indent' argument adds indentation for better readability

    # Step 2: Open a file in write mode
    filename_with_hyphen = filename.replace(" ", "-")
    filename_with_hyphen = filename_with_hyphen + ".json"

    with open(filename_with_hyphen, 'w') as file:
        # Step 3 and Step 4: Write JSON string to the file
        file.write(json_data)

    # File is automatically closed when the 'with' block is exited
    print(f"Data has been written to '{filename_with_hyphen}'.")

def file_to_json(search):
    filename_with_hyphen = search.replace(" ", "-")
    file_path = filename_with_hyphen + ".json" 
    # Step 1: Open the JSON file
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            # Step 2 and Step 3: Load JSON data into a Python data structure
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it as an empty file
        with open(file_path, "w") as file:
            print("File created as an empty file.")
            return []

def glassdoor_api(page, search, flag):

    if flag:
        return requests.post(
            url="https://api.mycareersfuture.gov.sg/v2/search?limit=100&page=" + str(page),
            json = {
                "positionLevels": ["Fresh/entry level"],
                "search": search
            })
    else:
        return requests.post(
            url="https://api.mycareersfuture.gov.sg/v2/search?limit=100&page=" + str(page),
            json = {
                "search": search
            })