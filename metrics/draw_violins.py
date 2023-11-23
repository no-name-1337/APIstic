import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.5)
# Load the data from your JSON file. Replace the file path with the location of your file.
file_path = '/Users/usi/git/2024MSR/2024MSR-scripts/allData-average.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Filter out null values from each dataset. This step ensures that the analysis does not include any missing or undefined values.
filtered_data = {key: [value for value in data[key] if value is not None and value < 50] for key in data.keys()}

# count how many were filtered out because of value < 110 in each dataset
for key in data.keys():
    print(key, len(data[key]) - len(filtered_data[key]))


# Combine all datasets into a single dataset for an overall comparison.
filtered_data['Combined'] = [value for dataset in filtered_data.values() for value in dataset if value is not None]

# Create a DataFrame for seaborn. This structure is suitable for creating violin plots using seaborn.
filtered_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in filtered_data.items() ]))

# Plotting the violin plots. This visualization will show the distribution of values for each dataset.
plt.figure(figsize=(12, 7))
sns.violinplot(data=filtered_df)

# Customizing the plot to enhance readability and aesthetics.
plt.title('Distributions of Average Secured Endpoints Across Datasets and Combined')  # Adding a title.
plt.ylabel('Average Secured Endpoints')  # Labeling the y-axis.
plt.xlabel('Datasets')  # Labeling the x-axis.
sns.despine(top=True, right=True)  # Removing the top x-axis and right y-axis for a cleaner look.
plt.grid(axis='y', linestyle='--')
plt.savefig('security_average.svg', format='svg')
plt.show()

