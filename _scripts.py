import pandas as pd
import matplotlib.pyplot as plt

# Set plot parameters
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# choose columns to plot
columns = ['type', 'title']

# Load data from csv file
df = pd.read_csv('netflix_data.csv', usecols=columns)

# Plot data
print("Contents in csv file:", df)
plt.plot(df.type, df.title)
plt.show()
