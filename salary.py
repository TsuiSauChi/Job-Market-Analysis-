from helper import glassdoor_api
from helper import file_to_json, json_to_file, volin_plot

import matplotlib.pyplot as plt
import time

search = "Software Developer"

data = []
page = 0

result = file_to_json(search)

if len(result) == 0:
    while True:
        print("Looping")
        response = glassdoor_api(page, search, 0).json()
        response = response["results"]
    
        if len(response) <= 0:
            break

        for i in response:
            data.append(i)

        page += 1 

    json_to_file(search, data)
    result = data

company_list = []
title_list = []
min_salary_list = []
max_salary_list = []
for i in result:
    if i["salary"]["type"]["salaryType"] == "Monthly":
        company_list.append(i["postedCompany"]["name"])
        title_list.append(i["title"])
        min_salary_list.append(i["salary"]["minimum"])
        max_salary_list.append(i["salary"]["maximum"])

volin_plot(min_salary_list,max_salary_list,search)

# Show the plot
plt.show()