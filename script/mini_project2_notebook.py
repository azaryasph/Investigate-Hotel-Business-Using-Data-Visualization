# %% [markdown]
# # Investigate Business Hotel using Data Visualization
# 
# |  |  |
# |:---:|:---:|
# | ![alt text](../images/hb_img_norm.jpg) | ![alt text](../images/hb_img_revert.jpg) |
# 
# **Project Overview**:<br>
# It is very important for a company always to analyze its business performance. On this occasion, we will delve deeper into business in the hospitality sector. Our focus is to find out how our customers behave in making hotel reservations, and its relationship to the rate of cancelation of hotel reservations. We will present the results of the insights we find in data visualization to make it easier to understand and more persuasive.
# 
# **Project Goals**:<br>
# 1. Find out how customers behave in making hotel reservations.
# 2. Find out the relationship between customer behavior in making hotel reservations and the rate of cancelation of hotel reservations.
# 3. Present the results of the insights we find in data visualization to make it easier to understand and more persuasive.
# 
# **Project Objective**:<br>
# 1. Data Preparation
# 2. Data Visualization
# 3. Insight and Conclusion

# %% [markdown]
# ## Data Preprocessing

# %% [markdown]
# ### Import Library

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# %% [markdown]
# ### Load Data and Preliminary Data Exploration

# %%
# Importing the hotel bookings data from a CSV file into a pandas DataFrame
df = pd.read_csv('../data/hotel_bookings_data.csv')

# Setting pandas option to display all columns of the DataFrame when it is printed
pd.set_option('display.max_columns', None)

# Print the shape of the DataFrame
print(df.shape)

# Displaying the first 2 rows of the DataFrame for a quick overview of the data
display(df.head(2))

# Displaying a concise summary of the DataFrame including the number of non-null entries in each column
display(df.info())

# %% [markdown]
# Dataframe info summary:
# - There's 4 columns containing missing values: `children`, `country`, `agent`, and `company`.
# - There's 2 columns containing datetime data type: `reservation_status_date` and `arrival_date_month`.

# %%
cats = df.select_dtypes('object')
nums = df.select_dtypes('number')

print('Statistical summary for categorical variables')
display(cats.describe())

print('Statistical summary for numerical variables')
display(nums.describe())

# Display all the value counts from the categorical columns
for col in cats.columns:
    print(f'Value counts for {col}')
    print(cats[col].value_counts())
    print('='*50)

# %% [markdown]
# Category data Statistical Summary:
# - `hotel`: There are 2 types of hotel, City Hotel and Resort Hotel.
# - `meal`: There are 5 types of meal, Breakfast are the most ordered meal.
# - `city`: There are 177 countries that make reservations, Kota Denpasar is the most city that made reservations.
# - `market_segment`: There are 8 types of market segment, Online TA (Travel Agent) is the most market segment.
# - `distribution_channel`: There are 5 types of distribution channel, TA/TO (Travel Agent/Tour Operator) is the most distribution channel.
# - `deposit_type`: There are 3 types of deposit type, No Deposit is the most deposit type.
# - `customer_type`: There are 4 types of customer type, Personal Travel is the most customer type.
# - `reservation_status`: There are 3 types of reservation status, Check-Out is the most reservation status.
# 
# Numerical data Statistical Summary:
# - `is_cancelled` & `is_repeated_guest`: The min value is 0 and the max value is 1, which means this column is a binary column.
# - `children` & `babies`: the max value of this column is 10, which is quite high and rare.
# 
# For the column that supposed to be a binary categorical will be changed to a binary data type for better analysis. For the column that has a negative value, we will remove the negative value because it is impossible for the price to be negative.

# %% [markdown]
# ### Handling Missing Values

# %%
# Copy the original dataframe to avoid modifying the original data
dfs = df.copy()

# Calculate the percentage of missing values in each column
missing = dfs.isnull().sum()*100 / len(dfs)

# Create a new DataFrame to store the column names and their corresponding missing values percentages
missing_data = pd.DataFrame({'column':df.columns,
                                   'missing_percentage %':missing.values})


# FIlter out the columns that have no missing values
missing_data = missing_data[missing_data['missing_percentage %'] > 0]

# Sort the DataFrame by the mising percentage in descending order
missing_data = missing_data.sort_values('missing_percentage %', ascending=False)

# Create a bar plot to visualize the missing data
plt.figure(figsize=(10,5))
ax = sns.barplot(x='missing_percentage %', y='column', data=missing_data, color='#E1341E')

# Annotate the bars with the missing percentage values
for p in ax.patches:
    ax.annotate('%.2f' % p.get_width() + '%', xy=(p.get_width(), p.get_y()+p.get_height()/2),
                xytext=(8,0), textcoords='offset points', ha='left', va='center', fontsize=10)

# Set the title and labels of the plot
plt.title('Percentage of values for each Features', fontsize=17, fontweight='bold')
sns.despine()
plt.ylabel('Column', fontsize=12, fontweight='bold')
plt.xlabel('Percentage', fontsize=12, fontweight='bold')
plt.xlim(0,100)
plt.show()

# %%
dfs[dfs.agent.notna()].sample(3)

# %% [markdown]
# As we have seen before that these 4 columns contain missing values,
# - For the `company` column will be dropped because it contains too many missing values (>90%)
# - `agent` and `children` column contain missing values seems reasonable, because it is possible that the customer doesn't use the agent to make a reservation, and is is possible that the customer doesn't have children. So, we will fill the missing values with 0.
# - For the `city` column will be filled/imputed with the 'unknown' value, because it is possible that the customer doesn't want to share their city information.

# %%
# impute missing values for the 'agent', 'children', and 'city' columns
dfs.fillna({'agent':0}, inplace=True)
dfs.fillna({'children':0}, inplace=True)
dfs.fillna({'city':'Unknown'}, inplace=True)

# drop company column as it has more than 90% missing values
dfs.drop(columns=['company'], inplace=True)

# %% [markdown]
# ### Replace values

# %% [markdown]
# change the data type of the `is_cancelled` and `is_repeated_guest` column to category data type.

# %%
# Define a dictionary to map cancellation status from numerical to categorical data
map_cancel = {
    0: 'not canceled',
    1: 'canceled'
}

# Apply the mapping to the 'is_canceled' column
dfs['is_canceled'] = dfs['is_canceled'].map(map_cancel)

# Define a dictionary to map guest repeat status from numerical to categorical data
map_repeat = {
    0: 'first time',
    1: 'repeat'
}

# Apply the mapping to the 'is_repeated_guest' column
dfs['is_repeated_guest'] = dfs['is_repeated_guest'].map(map_repeat)

# Replace the column with undefined values with 'other'
dfs['meal'] = dfs['meal'].replace('Undefined', 'Other')
dfs['market_segment'] = dfs['market_segment'].replace('Undefined', 'Other')
dfs['distribution_channel'] = dfs['distribution_channel'].replace('Undefined', 'Other')

# %% [markdown]
# ### Drop invalid data

# %%
dfs[(dfs['children']==0) & (dfs['adults'] == 0) & (dfs['babies'] == 0)].shape[0]

# %% [markdown]
# There's 180 data record that has 0 adults and children, this can be considered as an invalid data record. We will remove this data record.

# %%
# drop rows where both adults, children, and babies are 0
dfs_clean = dfs[~((dfs['children']==0) & (dfs['adults']==0) & (dfs['babies']==0))]

# %% [markdown]
# # Task 2 : Monthly Hotel Booking Analysis Based On Hotel Type

# %% [markdown]
# ### Create an aggregate table that shows the comparison of the number of hotel bookings each month based on hotel type

# %%
# Create a copy of the original dataframe to avoid modifying the original data
dfx = dfs.copy()

# Group the data by hotel, arrival year and arrival month, and count the number of bookings for each group
booking_counts = (
    dfx.groupby(['hotel', 'arrival_date_year', 'arrival_date_month'])
    ['hotel']
    .count()
    .rename("count_booking")
    .reset_index()
)

# Sort the booking counts dataframe by arrival month for easier analysis
booking_counts.sort_values(by='arrival_date_month')

# %% [markdown]
# The aggregate table not yet ordered based on the month order, so let's reorder the month order.

# %% [markdown]
# ### Order the data based on month

# %%
# Define the correct order of the months
months_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Convert the 'arrival_date_month' column to a categorical type with the defined order
# This allows for proper sorting and visualization in the correct month order
booking_counts['arrival_date_month'] = pd.Categorical(
    booking_counts['arrival_date_month'],
    categories=months_order,
    ordered=True
)

# Sort the dataframe first by year, then by month (in the correct order)
booking_counts = booking_counts.sort_values(
    ['arrival_date_year', 'arrival_date_month']
)

# Display sorted aggregated booking counts
booking_counts

# %% [markdown]
# ### Normalized the data

# %%
# Generate all posible combinations of hotel, year, and month
all_combinations = pd.MultiIndex.from_product([
    booking_counts['hotel'].unique(),
    booking_counts['arrival_date_year'].unique(),
    months_order
], names=['hotel', 'arrival_date_year', 'arrival_date_month']).to_frame(index=False)

# Merge with original booking counts, filling missing combinations with NaN
booking_counts_normalized = pd.merge(
    all_combinations,
    booking_counts,
    how='left',
    on=['hotel','arrival_date_year', 'arrival_date_month']
)

# Normalize the booking counts by dividing the 2018 counts by 3 to account for the incomplete year
divided_counts = booking_counts[
    (booking_counts['arrival_date_year'] == 2018)
][['hotel', 'arrival_date_month', 'count_booking']].copy()

divided_counts['count_booking'] /= 3
divided_counts.set_index(['hotel', 'arrival_date_month'], inplace=True)

# Fill missing booking counts for 2017 and 2019 with normalized 2018 counts
for year in [2017, 2019]:
    for month in months_order:
        for hotel in booking_counts['hotel'].unique():
            mask = (
                (booking_counts_normalized['hotel'] == hotel) &
                (booking_counts_normalized['arrival_date_year'] == year) &
                (booking_counts_normalized['arrival_date_month'] == month)
            )
            booking_counts_normalized.loc[mask, 'count_booking'] = booking_counts_normalized.loc[
                mask, 'count_booking'
            ].fillna(divided_counts.loc[(hotel, month), 'count_booking'])

# Display the final normalized booking counts dataframe
booking_counts_normalized

# %% [markdown]
# ### Aggregate SUM booking count based on hotel type and month

# %%
# Sum the booking counts for each hotel and month aross all years
booking_counts_sum = (
    booking_counts_normalized. groupby(['hotel', 'arrival_date_month'])
    ['count_booking']
    .sum()
    .reset_index()
)

# Convert the 'arrival_date_month' column to a categorical type with the defined order
booking_counts_sum['arrival_date_month'] = pd.Categorical(
    booking_counts_sum['arrival_date_month'],
    categories=months_order,
    ordered=True
)

# Sort the dataframe by month (in the correct order)
booking_counts_sum = booking_counts_sum.sort_values(['arrival_date_month'])

# Display the final aggregated booking counts across all years
booking_counts_sum

# %%
# Seperate the city_hotel data and resort_hotel data
city_hotel = booking_counts_sum.loc[booking_counts_sum.hotel=='City Hotel']
resort_hotel = booking_counts_sum.loc[booking_counts_sum.hotel=='Resort Hotel']

# plot the data with line plot from seaborn
plt.figure(figsize=(16,10))

# lineplot for city_hotel
sns.lineplot(
    x='arrival_date_month',
    y='count_booking',
    data=city_hotel,
    marker='o',
    label='city_hotel',
    linewidth=2.5
)

# lineplot for resort_hotel
sns.lineplot(
    x='arrival_date_month',
    y='count_booking',
    data=resort_hotel,
    marker='o',
    label='resort_hotel'
)

# barplot for city_hotel
city_bar = sns.barplot(
    x='arrival_date_month',
    y='count_booking',
    data=city_hotel,
    label='city_hotel',
    color='b',
    alpha=0.5
)

# barplot for resort_hotel
resort_bar = sns.barplot(
    x='arrival_date_month',
    y='count_booking',
    data=resort_hotel,
    label='resort_hotel',
    color='r',
    alpha=0.5
)

sns.despine()

plt.legend()
plt.title('Monthly Hotel Booking Based On Hotel Type', fontsize=20, fontweight='bold', y=1.1)
plt.xlabel('Month', fontsize=12, labelpad=10)
xticks_labels = [month[:3] for month in months_order]
plt.xticks(ticks=range(12), labels=xticks_labels, fontsize=12)
plt.ylabel('Booking Count', fontsize=12)

# Add number annotations
for p in city_bar.patches:
    city_bar.annotate(format(p.get_height(), '.1f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')

for p in resort_bar.patches:
    resort_bar.annotate(format(p.get_height(), '.1f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')

plt.show()

# %% [markdown]
# **Insight**:
# - The number of bookings in City Hotel is higher than Resort Hotel.
# - The number of bookings in City Hotel is increasing from April to July, and then decreasing from August to October, and then increasing again from November to December.
# - The number of bookings in Resort Hotel pattern is almost similiar to City Hotel, *But* the number of bookings is much lower than City Hotel.

# %% [markdown]
# ### Task 3 Impact Analysis Of Stay Duration On Hotel Bookings Cancellation Rates

# %% [markdown]
# ### Create a new column contains stay in duration

# %%
# Create a new column 'stay_in_duration' by adding the 'stays_in_weekend_nights' and 'stays_in_weekdays_nights' columns
dfx['stay_duration'] = dfx['stays_in_weekdays_nights'] + dfx['stays_in_weekend_nights']

# %% [markdown]
# ### Group the values from stay in duration column

# %%
dfx.stay_duration.value_counts()

# %%
sns.histplot(dfx['stay_duration'], bins=50)

# %% [markdown]
# because the `stay_in_duration` value distribution most of the values are concetrated in the range 0-10, so we want to have more granular bins in this range, and larger bins for the higher values.

# %%
# Define bins for categoriczation, ranging from 0 to 10, then 15, 20, and above
bins = list(range(0, 11)) + [15, 20, np.inf]

# Define labels for each bin, corresponding to the range defined in 'bins'
labels = ['0-1'] + [str(i) for i in range(2, 11)] + ['11-15', '16-20', '>20']

# Categorize 'stay_in_duration' into bins with corresponding labels, storing the result in a new column 'stay_duration_bins
dfx['stay_duration_bins'] = pd.cut(dfx['stay_duration'], bins, labels=labels)

# %% [markdown]
# ### Create an aggregate table that shows the ratio of the number of canceled hotel reservations to the duration of stay for each type of hotel

# %%
# Group the data by 'hotel', 'is_canceled', and 'stay_duration_bins', and count the number of bookings for each group
data_cancel = (
    dfx.groupby(['hotel', 'is_canceled', 'stay_duration_bins'], observed=True)['is_canceled']
    .count()
    .reset_index(name='count')
)

# Pivot the 'data_cancel' DataFrame to create a new DataFrame
# 'hotel' and 'stay_duration_bins' are set as index
# 'is_canceled' is set as columns
# 'count' is set as values
pivot_args = {
    'index': ['hotel', 'stay_duration_bins'],
    'columns': 'is_canceled',
    'values': 'count'
}
data_cancel_pivot = data_cancel.pivot(**pivot_args).reset_index()

# Rename the columns of 'data_cancel_pivot' for better readability
new_column_names = ['hotel', 'stay_duration_bins', 'canceled', 'not_canceled']
data_cancel_pivot.columns = new_column_names

# Calculate the cancelation rate
# It's the ratio of 'canceled' to the sum of 'not_canceled' and 'canceled'
total_stays = data_cancel_pivot['not_canceled'] + data_cancel_pivot['canceled']
data_cancel_pivot['cancellation_rate'] = data_cancel_pivot['canceled'] / total_stays

data_cancel_pivot

# %% [markdown]
# ### Plot the data

# %%
# Define the color palette for the stacked bar plot
colors = ['#5D5DEF', '#C22673']

# Create a stacked bar plot to visualize the cancelation rate beased on the duration of stay
plt.figure(figsize=(13, 9))


# Stacked barplot for city hotel
sns.barplot(
    x='stay_duration_bins',
    y='cancellation_rate',
    data=data_cancel_pivot[data_cancel_pivot['hotel'] == 'City Hotel'],
    color=colors[0],
    label='City Hotel',
    alpha=0.85
)

# Stacked barplot for resort hotel
sns.barplot(
    x='stay_duration_bins',
    y='cancellation_rate',
    data=data_cancel_pivot[data_cancel_pivot['hotel'] == 'Resort Hotel'],
    color=colors[1],
    label='Resort Hotel',
    alpha=0.85
)

sns.despine()

# plt.legend(title='Hotel Type', title_fontsize='13', fontsize='12', loc='upper right')
plt.legend(title='Hotel Type', title_fontsize='12', fontsize='12', prop={'size': 10}, loc=[0.85, 0.98])
avg_cancellation_rate = data_cancel_pivot.cancellation_rate.mean()
plt.axhline(avg_cancellation_rate, color='black', linestyle='--', label=f'Average Cancellation Rate: {avg_cancellation_rate:.2f}')
plt.title('Cancellation Rate Based On Stay Duration', fontsize=20, fontweight='bold', y=1.05)
plt.xlabel('Stay Duration', fontsize=12, labelpad=10)
plt.xticks(fontsize=11)
plt.ylabel('Cancellation Rate (%)', fontsize=12)


plt.show()

# %% [markdown]
# - City hotel cancellation rate by the stay duration is higher and more unstable (above average cancelation rate) than the Resort hotel from the stay duration 0-15.
# - The cancellation rate increases significantly for the City Hotel type when the stay duration is more than 10 days, while the Resort hotel only increase significantly when the stay duration in range 16 to >20 days.

# %% [markdown]
# ### Task 4 Impact Analysis Of Lead Time On Hotel Bookings Cancellation Rates

# %%
dfx.lead_time.value_counts().head(30)

# %%
sns.histplot(dfx['lead_time'], bins=50)

# %% [markdown]
# ### Group/Bin the values from lead time column

# %%
# Define categories for lead time based on the number of days
leadtime_category = [
    (dfx['lead_time'] <= 30),  # Less than or equal to 30 days
    (dfx['lead_time'] >= 31) & (dfx['lead_time'] <= 120),  # Between 31 and 120 days
    (dfx['lead_time'] >= 121) & (dfx['lead_time'] <= 210),  # Between 121 and 210 days
    (dfx['lead_time'] >= 211) & (dfx['lead_time'] <= 300),  # Between 211 and 300 days
    (dfx['lead_time'] >= 301) & (dfx['lead_time'] <= 365),  # Between 301 and 365 days
    (dfx['lead_time'] > 365)  # More than 365 days
]

# Define the corresponding group names for the lead time categories
leadtime_group = [
    '<1 Month', '1-3 Months', '4-6 Months',
    '7-9 Months', '10-12 Months', '>12 Months'
]

# Create a new column 'lead_time_group' in the DataFrame 'dfx'
# Assign the group names based on the lead time categories
dfx['lead_time_group'] = np.select(leadtime_category, leadtime_group)

# %% [markdown]
# ### Create an aggregate table that shows the ratio of the number of canceled hotel reservations to the lead time for each type of hotel

# %%
# Group the DataFrame 'dfx' by 'hotel', 'is_canceled', and 'lead_time_group'
# Count the number of cancellations for each group and reset the index
data_lt = dfx.groupby(['hotel', 'is_canceled', 'lead_time_group'])['is_canceled'].count().reset_index(name='count')

# Pivot the 'data_lt' DataFrame to create a new DataFrame
# 'hotel' and 'lead_time_group' are set as index
# 'is_canceled' is set as columns
# 'count' is set as values
data_lt_pivot = data_lt.pivot(index=['hotel', 'lead_time_group'], columns='is_canceled', values='count').reset_index()

# Rename the columns of 'data_lt_pivot' for better readability
new_col_names = ['hotel', 'lead_time_group', 'canceled', 'not_canceled']
data_lt_pivot.columns = new_col_names

# Calculate the cancelation rate
data_lt_pivot['cancellation_rate'] = data_lt_pivot['canceled'] / (data_lt_pivot['canceled'] + data_lt_pivot['not_canceled'])

data_lt_pivot

# %%
# Your existing code
plt.figure(figsize=(13, 9))

# Stacked barplot for City hotel
city_bar = sns.barplot(
    x='lead_time_group',
    y='cancellation_rate',
    data=data_lt_pivot[data_lt_pivot['hotel'] == 'City Hotel'],
    color=colors[0],
    label='City Hotel',
    order=leadtime_group,
    alpha=0.85
)

# Stacked barplot for Resort hotel
resort_bar = sns.barplot(
    x='lead_time_group',
    y='cancellation_rate',
    data=data_lt_pivot[data_lt_pivot['hotel'] == 'Resort Hotel'],
    color=colors[1],
    label='Resort Hotel',
    order=leadtime_group,
    alpha=0.85
)

# Line plot for City hotel
sns.lineplot(
    x='lead_time_group', 
    y='cancellation_rate',
    data=data_lt_pivot[data_lt_pivot['hotel'] == 'City Hotel'], 
    marker='o', 
    label='City Hotel', 
    linewidth=1.5,
    alpha=0.5
)

# Line plot for Resort hotel
sns.lineplot(
    x='lead_time_group',
    y='cancellation_rate',
    data=data_lt_pivot[data_lt_pivot['hotel'] == 'Resort Hotel'],
    marker='o',
    label='Resort Hotel',
    linewidth=1.5,
    alpha=0.5
)


sns.despine()

plt.legend(title='Hotel Type', title_fontsize='12', fontsize='12', prop={'size': 12}, loc=[0.04, 0.8])
plt.title('Cancellation Rate Based On Lead Time', fontsize=20, fontweight='bold', y=1.05)
plt.xlabel('Lead Time', fontsize=12, labelpad=10)
plt.xticks(fontsize=11)
plt.ylabel('Cancellation Rate (%)', fontsize=12)

# Annotations
for p in city_bar.patches:
    city_bar.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 10), 
                   textcoords = 'offset points')

for p in resort_bar.patches:
    resort_bar.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 10), 
                   textcoords = 'offset points')

plt.show()


