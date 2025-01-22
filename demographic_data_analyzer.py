import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    races_series = df[~df.duplicated(subset=['race'])]['race']

    race_counts = []

    for race in races_series:
      n_race_max = df[df['race'] == race].count().max()
      race_counts.append(n_race_max)

    race_count = pd.Series(race_counts, index=races_series)

    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean()

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df[df['education'] == 'Bachelors'].count().max() / df.count().max())*100

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_ed_df = df[(df['education-num'] >= 13) & (df['education'] != 'Prof-school')]
    higher_education = higher_ed_df.shape[0]

    lower_ed_df = df[~df.isin(higher_ed_df)].dropna()
    lower_education = lower_ed_df['education'].notna().sum()

    # percentage with salary >50K
    he_fifty = higher_ed_df[higher_ed_df['salary'] == '>50K'].shape[0]
    higher_education_rich = (he_fifty / higher_education) * 100

    le_fifty = lower_ed_df[lower_ed_df['salary'] == '>50K'].shape[0]
    lower_education_rich = (le_fifty / lower_education) * 100

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_worker_df = df[df['hours-per-week'] == min_work_hours]
    num_min_workers = min_worker_df.shape[0]
    min_work_fifty = min_worker_df[min_worker_df['salary'] == '>50K'].shape[0]
    rich_percentage = (min_work_fifty / num_min_workers) * 100

    # What country has the highest percentage of people that earn >50K?
    countries_series = df[~df.duplicated(subset=['native-country'])]['native-country']
    countries_ave_salary = {}
    cols = ['country', 'ave_salary']

    for i, country in enumerate(countries_series):
      country_df = df[df['native-country'] == country]
      citizens = country_df.shape[0]
      rich_citizens = country_df[country_df['salary'] == '>50K'].shape[0]
      countries_ave_salary[i] = [country, ((rich_citizens / citizens) * 100)]
      
    country_rich_percentage = pd.DataFrame.from_dict(countries_ave_salary, orient='index', columns=cols).sort_values(by='ave_salary', axis=0, ascending=False, ignore_index=True)

    highest_earning_country = country_rich_percentage.iloc[0]['country']
    highest_earning_country_percentage = country_rich_percentage.iloc[0]['ave_salary']
    
    # Identify the most popular occupation for those who earn >50K in India.
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    india_rich_jobs = india_rich.drop_duplicates(subset=['occupation'])['occupation']

    job_popularity = []

    for job in india_rich_jobs:
      job_count = india_rich['occupation'].str.count(job).sum()
      job_popularity.append([job, job_count])

    job_count_df = pd.DataFrame(job_popularity, columns=['job', 'count']).sort_values(['count'], ascending=False)
    top_IN_occupation = job_count_df[job_count_df['count'] == job_count_df['count'].max()].iloc[0]['job']

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
