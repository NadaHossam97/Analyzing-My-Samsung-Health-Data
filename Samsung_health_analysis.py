# Load necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# Load the dataframes
activity_day_summary = pd.read_excel('./activity_day_summary.xlsx')
pedometer_day_summary = pd.read_excel('./pedometer_day_summary.xlsx')
step_count = pd.read_excel('./step_count.xlsx')
step_daily = pd.read_excel('./step_daily.xlsx')
calories_burned_details= pd.read_excel('./calories_burned_details.xlsx')

#index for datasets
datasets = {
        "Activity Day Summary": activity_day_summary,
        "Pedometer Day Summary": pedometer_day_summary,
        "Step Count": step_count,
        "Step Daily": step_daily,
        "Calories Burned Details": calories_burned_details
    }
##Data Cleaning
"""
# Loop through each DataFrame and print its info
for name, df in datasets.items():
    print(f"\nDataFrame: {name}")
    print(df.info())
# Loop through each DataFrame and calculate missing values percentage for columns with missing data
for name, df in datasets.items():
    print(f"\nMissing Data Summary for DataFrame: {name}")
    
    # Calculate missing values percentage for each column
    missing_percentage = df.isnull().mean() * 100
    
    # Filter only columns with missing data
    missing_percentage = missing_percentage[missing_percentage > 0]
    
    # Convert to a DataFrame for a cleaner table format
    missing_summary = pd.DataFrame({
        'Column': missing_percentage.index,
        'Missing_Percent': missing_percentage.values
    }).sort_values(by="Missing_Percent", ascending=False)
    
    # Print the table
    print(missing_summary.to_string(index=False))

# Loop through each DataFrame, check for duplicates, and output the results
for name, df in datasets.items():
    duplicates = df[df.duplicated(keep=False)]  # Keep all occurrences of duplicates
    
    # Count of duplicates
    duplicate_count = duplicates.shape[0]
    
    # Print the results
    print(f"\nDataFrame: {name}")
    print(f"Total duplicate rows: {duplicate_count}")
    
    if duplicate_count > 0:
        print(f"Duplicate entries:\n{duplicates}")
        # Optionally, save duplicates to separate CSV files
        duplicates.to_csv(f"./{name}_duplicates.csv", index=False)
"""
# Drop columns with missing data for each DataFrame
for name, df in datasets.items():
    # Drop columns with any missing values
    datasets[name] = df.dropna(axis=1)
    # Print the updated DataFrame info to confirm the columns have been dropped
    print(f"\nUpdated DataFrame after dropping columns with missing data: {name}")
    print(datasets[name].info())

"""
##Descreptive stats
#Calculate and print descriptive statistics for all datasets
for name, df in datasets.items():
    # Get descriptive statistics
    descriptive_stats = df.describe()
    print(f"\nDescriptive Statistics for {name}:\n")
    print(descriptive_stats)
    # Create histograms for each numeric variable in the dataset, excluding date and time columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    plt.figure(figsize=(15, 10))  # Create a new figure for each dataset
    df[numeric_cols].hist(bins=15, figsize=(15, 10), edgecolor='black')
    plt.suptitle(f'Histograms for {name}', fontsize=16)  # Set the super title for the figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust the layout to make room for the title
    plt.show()  # Show the plot

##Correlation analysis
#Heat-Map For pedometer_day_summary
# Set up the figure size for plots
plt.figure(figsize=(12, 10))

numeric_df = pedometer_day_summary.select_dtypes(include=['float64', 'int64'])
# Compute correlation matrix
correlation_matrix = numeric_df.corr()
    
# Plot the heatmap for each dataset
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
plt.title(f'Correlation Matrix for pedometer_day_summary')
plt.show()
"""
# Convert the 'date' column to datetime format (if not already)
pedometer_day_summary['update_time'] = pd.to_datetime(pedometer_day_summary['update_time'], format='%m/%d/%Y %I:%M:%S %p')
# Extract day of the week, month, year
pedometer_day_summary['day_of_week'] = pedometer_day_summary['update_time'].dt.day_name()
pedometer_day_summary['month'] = pedometer_day_summary['update_time'].dt.month
pedometer_day_summary['year'] = pedometer_day_summary['update_time'].dt.year

"""

print(pedometer_day_summary[['update_time', 'day_of_week', 'month', 'year']].head())
"""

# Set the date as the index
pedometer_day_summary.set_index('update_time', inplace=True)

# Resample to a weekly or monthly average
weekly_summary = pedometer_day_summary.resample('W').mean(numeric_only=True)

# Plot the trends for weekly average steps, run steps, and walk steps
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot the step_count and walk_step_count on the primary y-axis
ax1.plot(weekly_summary['walk_step_count'], label='Weekly Average Walk Step Count', color='g')
ax1.set_xlabel('Week')
ax1.set_ylabel('Average Walk Step Count', color='g')
ax1.tick_params(axis='y', labelcolor='g')

# Create a second y-axis to plot run_step_count with a different scale
ax2 = ax1.twinx()
ax2.plot(weekly_summary['run_step_count'], label='Weekly Average Run Step Count', color='r')
ax2.set_ylabel('Average Run Step Count', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Title and legend
plt.title('Weekly Trends of Step Counts')
fig.tight_layout() 
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9)) 

"""
# Display the plot
plt.show()

"""
"""
# Define activity levels based on step count or other criteria
def activity_level(steps):
    if steps < 1000:
        return 'Sedentary'
    elif 1000 <= steps < 5000:
        return 'Lightly Active'
    elif 5000 <= steps < 10000:
        return 'Active'
    else:
        return 'Very Active'

pedometer_day_summary['activity_level'] = pedometer_day_summary['step_count'].apply(activity_level)

# Plot the distribution of activity levels
sns.countplot(data=pedometer_day_summary, x='activity_level')
plt.title('Distribution of Activity Levels')
plt.show()

"""

day_of_week_summary = pedometer_day_summary.groupby('day_of_week')['walk_step_count'].mean()

# Step 3: Sort the days for better readability
day_of_week_summary = day_of_week_summary.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Step 4: Plot the average walk steps by day of the week
plt.figure(figsize=(10, 6))
day_of_week_summary.plot(kind='bar', color='green')
plt.title('Average Walk Steps by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Walk Steps')
plt.tight_layout()
plt.show()


# Filter data from February 1, 2023, to February 29, 2024
filtered_data = pedometer_day_summary[(pedometer_day_summary.index >= '2023-02-01') & 
                                      (pedometer_day_summary.index <= '2024-02-29')]

# Resample the data to get the monthly average walk steps
monthly_summary = filtered_data['walk_step_count'].resample('M').mean()

monthly_summary.index = monthly_summary.index.strftime('%B %Y')


plt.figure(figsize=(10, 6))
monthly_summary.plot(kind='bar', color='skyblue')
plt.title('Average Monthly Walk Steps from February 2023 to February 2024')
plt.xlabel('Month')
plt.ylabel('Average Walk Steps')

plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()