import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
file_path = 'Top 10 medal rankings(1896–2022)(combines NOCs).xlsx'
df = pd.read_excel(file_path)

# Extract necessary columns for plotting
countries = df['Countries']
gold = df['gold']
silver = df['silver']
bronze = df['bronze']
total = df['total']

# Create a line graph
plt.figure(figsize=(10, 6))

plt.plot(countries, gold, marker='o', label='Gold', linestyle='-', color='gold')
plt.plot(countries, silver, marker='s', label='Silver', linestyle='-', color='silver')
plt.plot(countries, bronze, marker='d', label='Bronze', linestyle='-', color='peru')
plt.plot(countries, total, marker='*', label='Total', linestyle='-', color='steelblue')

plt.title('Medal Rankings (1896–2022)')
plt.xlabel('Countries')
plt.ylabel('Number of Medals')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()
