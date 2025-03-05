import pandas as pd

df = pd.read_csv('salaries_by_college_major.csv',header=0,delimiter=',')

#peek at the top 5 rows of our dataframe.
print(df.head())

#see the number of rows and columns
print(df.shape)

#access the column names directly
print(df.columns)

# look for NaN (Not A Number) values in our dataframe. NAN values are blank cells or cells that contain strings instead of numbers.
print(df.isna())

#the last couple of rows in the dataframe:
print(df.tail())

#Delete the Last Row
clean_df = df.dropna()
print(clean_df.tail())

#access a particular column from a data frame we can use the square bracket notation
print(clean_df['Starting Median Salary'])


# find the highest starting salary we can simply chain the .max() method.
print(clean_df['Starting Median Salary'].max())

#the .idxmax() method will give us index for the row with the largest value.
print(clean_df['Starting Median Salary'].idxmax())

#To see the name of the major that corresponds to that particular row, we can use the .loc (location) property.
print(clean_df['Undergraduate Major'].loc[43])
print(clean_df['Undergraduate Major'][43])


# Challenge
#
#
# Now that we've found the major with the highest starting salary, can you write the code to find the following:
#
print(clean_df['Mid-Career Median Salary'].max())
# What college major has the highest mid-career salary? How much do graduates with this major earn? (Mid-career is defined as having 10+ years of experience).
#
print(clean_df['Mid-Career Median Salary'].idxmax())
print(clean_df['Undergraduate Major'][8])
# Which college major has the lowest starting salary and how much do graduates earn after university?
#
print(clean_df['Starting Median Salary'].idxmin())
print(clean_df['Undergraduate Major'][49])
# Which college major has the lowest mid-career salary and how much can people expect to earn with this degree?
print(clean_df['Mid-Career Median Salary'].idxmin())
print(clean_df['Undergraduate Major'][18])
print(clean_df['Mid-Career Median Salary'].min())

#calculate the difference between the earnings of the 10th and 90th percentile
print(clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary'])
print(clean_df['Mid-Career 90th Percentile Salary'].subtract(clean_df['Mid-Career 10th Percentile Salary']))

#The output of this computation will be another Pandas dataframe column. We can add this to our existing dataframe with the .insert() method:
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
clean_df.insert(1, 'Spread', spread_col)
print(clean_df.head())

#the smallest spread, we can use the .sort_values() method.
low_risk = clean_df.sort_values('Spread')
print(low_risk[['Undergraduate Major', 'Spread']].head())


# Challenge
# 
#
# Using the .sort_values() method, can you find the degrees with the highest potential? Find the top 5 degrees with the highest values in the 90th percentile.
#
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
print(highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head())
# Also, find the degrees with the greatest spread in salaries. Which majors have the largest difference between high and low earners after graduation.
highest_spread = clean_df.sort_values('Spread', ascending=False)
print(highest_spread[['Undergraduate Major', 'Spread']].head())

print(clean_df.groupby('Group').count())
clean_df.groupby('Group')['Mid-Career Median Salary'].mean()
#clean_df/['Mid-Career Median Salary'].mean()#.groupby('Group')
print(clean_df.groupby('Group')['Mid-Career Median Salary'].mean())

pd.options.display.float_format = '{:,.2f}'.format()