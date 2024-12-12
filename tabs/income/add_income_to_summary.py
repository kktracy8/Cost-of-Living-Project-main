from database.database import DB

def add_income(df, occupations, location):
    db = DB()
    income_data = db.read_income(location, occupations).sum()
    df['Income'] = income_data.values[0]
    return df

# Adding calculation to pull city comparisons for income (user input)
def calc_est_income(income, occupation1, location):
    db = DB()
    df = db.read_income_comparison()

    # Added back current city for Summary tab
    df_filtered = df[(df.src_city == location) & (df.dest_occ_title.isin(list(occupation1)))].copy()

    # Add income input column
    df_filtered['Income Input'] = income

    # Calculate custom income based on difference of relative occupation means
    df_filtered['Avg Income Dif'] = (
                (df_filtered['dest_a_mean'] - df_filtered['src_a_mean']) / df_filtered['src_a_mean'])
    df_filtered['Income Estimate'] = df_filtered['Avg Income Dif'].apply(lambda x: (1 + x) * income)
    df_filtered['Income Input'] = df_filtered['Avg Income Dif'].apply(lambda x: (x - x) + income)

    # Select columns to view in the dash table
    df_filtered = df_filtered[
        ['src_city', 'dest_city', 'src_a_mean', 'dest_a_mean', 'a_mean_dif', 'Income Estimate',
         'Avg Income Dif', 'Income Input']].copy()

    # Aggregate results for selected occupations
    df_grouped = (df_filtered.groupby('dest_city')
                  .agg(Total_Mean_Current=('src_a_mean', 'sum'),
                       Total_Mean_Dest=('dest_a_mean', 'sum'),
                       Avg_Income_Dif=('Avg Income Dif', 'mean'),
                       Income_Input=('Income Input', 'mean'),
                       Total_Estimated_Income=('Income Estimate', 'sum'), )).reset_index()

    # Test adding new income calculation on grouped data table
    df_grouped['Total_Est_Income2'] = (df_grouped['Income_Input'] *
                                       (1 + ((df_grouped['Total_Mean_Dest'] -
                                              df_grouped['Total_Mean_Current']) /
                                             df_grouped['Total_Mean_Current'])))

    # Select final subset of columns needed for dash table
    df_grouped = df_grouped.rename(
        columns={'dest_city': 'Comparison City', 'Avg_Income_Dif': 'Avg. Income Difference (%)',
                 'Total_Est_Income2': 'Estimated Household Income'})
    df_grouped = df_grouped[
        ['Comparison City', 'Avg. Income Difference (%)', 'Estimated Household Income']].copy()

    # Column formatting
    df_grouped['Avg. Income Difference (%)'] = df_grouped['Avg. Income Difference (%)'].map('{:.2%}'.format)
    # df_grouped['Estimated Household Income'] = df_grouped['Estimated Household Income'].map('${:,.0f}'.format)

    # Map cities to state short - to align with Summary tab
    # Add City abbrev - for joining with other datasets
    states = {'Los Angeles, CA': 'California',
              'Dallas, TX': 'Texas',
              'Denver, CO': 'Colorado',
              'Las Vegas, NV': 'Nevada',
              'New York City, NY': 'New York',
              'Boston, MA': 'Massachusetts',
              'Chicago, IL': 'Illinois'}

    # Add state mapping to income tables
    df_grouped['state'] = df_grouped['Comparison City'].map(states)

    # Sort by state
    df_grouped = df_grouped.sort_values(by=['state'])

    #rename to match summary tab
    df_grouped = df_grouped.rename(columns={'state': 'Item', 'Estimated Household Income': 'Adjusted Income'})

    # Select columns for summary tab
    df_grouped = df_grouped[['Item', 'Adjusted Income']].copy().reset_index()

    # transpose
    df = df_grouped.T
    df = df.reset_index(names='Item')
    df.columns = df.iloc[1]
    df = df[['Item', 'California', 'Colorado', 'Illinois', 'Massachusetts', 'Nevada', 'New York', 'Texas']].copy()
    df['Item'] = 'Adjusted Income'
    df = df.iloc[2:]

    return df