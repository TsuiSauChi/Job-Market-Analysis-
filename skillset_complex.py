from helper import glassdoor_api
from helper import file_to_json, json_to_file, volin_plot
from db import db_init

import matplotlib.pyplot as plt
import numpy as np

import sqlite3

freq= 35
search = "Software Developer"
medium = 8000

data = []
page = 0

result = file_to_json(search)
conn, cursor = db_init()

for i in result:
    for j in i["skills"]:
        cursor.execute("INSERT OR IGNORE INTO skill (skill, freq, freq_threshold) VALUES (?, ?, ?)", (j["skill"], 1, 0.0))
        cursor.execute("UPDATE skill SET freq = freq + 1 WHERE skill = ?", (j["skill"],))
    if i["salary"]["maximum"] > medium:
        for j in i["skills"]:
            cursor.execute("UPDATE skill SET freq_threshold = freq_threshold + 1.0 WHERE skill = ?", (j["skill"],))

# Commit the changes to the database
conn.commit()

cursor.execute("SELECT * FROM skill WHERE freq>? ORDER BY freq DESC", (freq,))
rows = cursor.fetchall()

freq_list = []
for i in rows:
    freq_list.append(i[1])

# Step 1: Calculate Q1 and Q3
q1 = np.percentile(freq_list, 25)
q3 = np.percentile(freq_list, 75)
# Step 2: Calculate IQR
iqr = q3 - q1
# Step 3: Identify outliers
# Step 3: Identify outliers
upper_bound = q3 + 1.5 * iqr

cursor.execute("SELECT * FROM skill WHERE freq<? ORDER BY freq DESC", (upper_bound,))
rows = cursor.fetchall()

for i in rows:
    importance = round(i[2]/len(result), 2)
    print(i[2])
    cursor.execute("UPDATE skill SET importance = ? WHERE skill = ?", (importance, i[0]))

conn.commit()

cursor.execute("SELECT * FROM skill WHERE freq>? ORDER BY freq DESC", (freq,))
rows = cursor.fetchall()

categories = []
data = []
importance_threshold = []
for i in rows:
    print(i)
    categories.append(i[0])
    data.append(i[1])
    importance_threshold.append(i[3])

# You can choose any colormap from matplotlib, here we use 'viridis'
cmap = plt.get_cmap('YlOrRd')

# Normalize the frequencies to the range [0, 1] to be used with the colormap
normalized_frequencies = np.array(importance_threshold) / max(importance_threshold)

fig, ax = plt.subplots()
bars = plt.bar(categories, data, color=cmap(normalized_frequencies))
# Set the x-axis tick positions
ax.set_xticks(range(len(categories)))

# Set the x-axis tick labels and rotate them by 90 degrees
ax.set_xticklabels(categories, rotation=90)

# Create custom legend based on colors
legend_labels = ['Outliers (not included)', '25%', '50%', '75%', '100%']
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=cmap(0.0)),
                  plt.Rectangle((0, 0), 1, 1, color=cmap(0.25)),
                  plt.Rectangle((0, 0), 1, 1, color=cmap(0.5)),
                  plt.Rectangle((0, 0), 1, 1, color=cmap(0.75)),
                  plt.Rectangle((0, 0), 1, 1, color=cmap(1.0))]

# Add the custom legend to the plot
ax.legend(legend_handles, legend_labels, title='Skill Important Based on >$8000 Monthly Salary', loc='upper right')


# Add labels and title
ax.set_xlabel('Skill Set')
ax.set_ylabel('No of Company Looking for Skillset')
ax.set_title('Realtionship between Skillset popularity and importance')

# Show the plot
plt.tight_layout()
plt.show()