import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
df = pd.read_excel(file_path)

# Extracting necessary columns for plotting
years = df['year']
countries = df.columns[1:]  # Extract country names from columns (excluding 'year')

# Create a line graph for each country with markers
plt.figure(figsize=(15, 8))  # Increase figure size

for country in countries:
    plt.plot(years, df[country], marker='o', label=country, linestyle='-')

plt.title('Medals According to Years for Top 10 Countries (1896-2020)')
plt.xlabel('Year')
plt.ylabel('Number of Medals')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Set x-axis ticks to display only the actual years present in the dataset
plt.xticks(years, rotation=45)
plt.tight_layout()

plt.show()
