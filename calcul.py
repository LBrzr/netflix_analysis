# %%
# Loading the required liabries.

from enum import Enum
import plotly as py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from pyspark.sql import SparkSession, DataFrameReader

import warnings
warnings.filterwarnings("ignore")

py.offline.init_notebook_mode(connected=True)


# %%
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Netflix") \
    .getOrCreate()

# %%
CSV_DATA_PATH = './data/netflix_data.csv'

# %%
# df=pd.read_csv("./netflix_titles.csv")
df_reader = spark.read
global_df = df_reader.csv(CSV_DATA_PATH, header=True,
                          inferSchema=True).toPandas()
global_df

# %%
global_df.info()

# %%
# Missing data
df = global_df.copy(deep=True)

for i in df.columns:
    null_rate = df[i].isna().sum() / len(df) * 100
    if null_rate > 0:
        print("{} null rate: {}%".format(i, round(null_rate, 2)))

# %% [markdown]
# Data Cleaning

# %%
df = df[['type', 'title', 'director', 'cast', 'country',
         'release_year', 'rating', 'duration', 'listed_in']]

df.isnull()

df.isnull().sum()

pd.options.mode.chained_assignment = None

df.fillna({'director': 'Unavailable'}, inplace=True)

df.fillna({'cast': 'Unavailable'}, inplace=True)

df.fillna({'country': 'Unavailable'}, inplace=True)

df.fillna({'rating': 'Unavailable'}, inplace=True)

df.dtypes

# %% [markdown]
# Ratio Film / Series

# %%
plt.figure(figsize=(14, 7))
labels = ['TV Show', 'Movie']
print(df['type'].value_counts().sort_values())
plt.pie(df['type'].value_counts().sort_values()[-2:], labels=labels, explode=[0.1, 0.1],
        autopct='%1.2f%%', colors=['lightblue', 'royalblue'], startangle=90)
plt.title('Type of Netflix Content')
plt.axis('equal')

plt.savefig("./chart_images/pie.png")
# plt.show()

# %% [markdown]
# Les pays qui produisent le plus de films / series

# %%
country_count = df['country'].value_counts().head(10)
fig = px.bar(y=country_count.values,
             x=country_count.index,
             color=country_count.index,
             text=country_count.values,
             title='Top 10 des pays qui produisent des Film')

fig.write_image("./chart_images/top_10.png")

fig

# %% [markdown]
# La courbe des sorties des films sur Netflix

# %%
release_year_count = df.release_year.value_counts()
print(release_year_count)
# release_year_count=spark.createDataFrame(release_year_count).toPandas()
# release_year_count=release_year_count.copy(deep=True)

plt.figure(figsize=(10, 9))
# sns.set()
# sns.lineplot(data=release_year_count)
plt.plot(release_year_count[0], release_year_count[1])
plt.title('Date de sortie Film et series sur Netflix ')
plt.xlim(1940, 2021)
plt.xlabel('Année de Sortie')
plt.ylabel('Nombre total de film sortie')
# plt.show()
# sns.plt.show()

# %% [markdown]
# Courbe de différents type de films

# %% [markdown]
#

# %%
plt.figure(figsize=(20, 5))
plt.style.use('seaborn-whitegrid')
ax = sns.countplot(x='rating', data=df)
plt.xlabel('Catégorie')
plt.ylabel('Nombre de film')
plt.xticks(rotation=45)
for p in ax.patches:
    ax.annotate(int(p.get_height()), (p.get_x()+0.25,
                p.get_height()+1), va='bottom', color='black')

plt.savefig("./chart_images/cat.png")

# %% [markdown]
# Les Tops genre sur Netflix

# %%
plt.figure(figsize=(15, 5))
sns.barplot(x=df["listed_in"].value_counts().head(10).index,
            y=df["listed_in"].value_counts().head(10).values, palette="pink")
plt.xticks(rotation=60)
plt.title("Top10 Genre de Film", fontweight="bold")
plt.savefig("./chart_images/top_10_cat.png")
# plt.show()

# %% [markdown]
# # Set plot parameters

# %%
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# %% [markdown]
# # choose columns to plot

# %%


class Column(Enum):
    TYPE = 'type'
    TITLE = 'title'
    DIRECTOR = 'director'
    CAST = 'cast'
    COUNTRY = 'country'
    DATE_ADDED = 'date_added'
    RELEASE_YEAR = 'release_year'
    RATING = 'rating'
    DURATION = 'duration'
    LISTED_IN = 'listed_in'
    DESCRIPTION = 'description'


columns = [Column.TYPE.value, Column.TITLE.value,
           Column.RELEASE_YEAR.value, Column.DURATION.value]


class Types(Enum):
    TV_SHOW = 'TV Show'
    MOVIE = 'Movie'

# %% [markdown]
# # reset data set


# %%
df = global_df.copy(deep=True)

# %% [markdown]
# # Plot data

# %%
print("Contents in csv file:", df)

# %%
titles = df.title
durations = df.duration

# %% [markdown]
# ## cleaning data

# %% [markdown]
# types

# %%
movies_df = df[df.type == Types.MOVIE.value]
tv_shows_df = df[df.type == Types.TV_SHOW.value]

# %% [markdown]
# durations

# %%


def clean_durations(durations: list) -> list:
    cleaned_durations = []

    for duration in durations:
        try:
            duration = int(duration.split(' ')[0])
        except:
            duration = 0
        cleaned_durations.append(duration)

    return cleaned_durations


# %%
movies_df.duration = clean_durations(movies_df.duration)
tv_shows_df.duration = clean_durations(tv_shows_df.duration)

# %%
print(tv_shows_df.duration.head(10))

# %%


def clean_years(years: list) -> list:
    cleaned_years = []

    for year in years:
        try:
            # print(year)
            year = year if year is int else int(year.split(', ')[-1])
        except:
            print(year)
            # year = 'Unknown'
            year = float('nan')
        cleaned_years.append(year)

    return cleaned_years


# %%
clean_years(movies_df.release_year)
movies_df.release_year = clean_years(movies_df.release_year)
tv_shows_df.release_year = clean_years(tv_shows_df.release_year)

# %%
tv_shows_year_mean_df = tv_shows_df.drop(
    [Column.TYPE.value, Column.TITLE.value], axis=1).copy(deep=True)
tv_shows_year_mean_df.set_index([Column.RELEASE_YEAR.value], inplace=True)
tv_shows_year_mean_df = tv_shows_year_mean_df.groupby(
    by=Column.RELEASE_YEAR.value).mean()

tv_shows_year_count_df = tv_shows_df.drop(
    [Column.TYPE.value, Column.TITLE.value], axis=1).copy(deep=True)
tv_shows_year_count_df = tv_shows_year_count_df.groupby(
    by=Column.RELEASE_YEAR.value).count()

movies_year_mean_df = movies_df.drop(
    [Column.TYPE.value, Column.TITLE.value], axis=1).copy(deep=True)
movies_year_mean_df.set_index([Column.RELEASE_YEAR.value], inplace=True)
movies_year_mean_df = movies_year_mean_df.groupby(
    by=Column.RELEASE_YEAR.value).mean()

movies_year_count_df = movies_df.drop(
    [Column.TYPE.value, Column.TITLE.value], axis=1).copy(deep=True)
movies_year_count_df = movies_year_count_df.groupby(
    by=Column.RELEASE_YEAR.value).count()

print('done')

# %% [markdown]
# ### Plot tv shows mean duration per year

# %%
tv_shows_year_mean_df = tv_shows_year_mean_df.reset_index()
plt.bar(tv_shows_year_mean_df[Column.RELEASE_YEAR.value],
        tv_shows_year_mean_df[Column.DURATION.value], label='TV Shows')
plt.xlabel('Années')
plt.ylabel('Nombre de saisons')
plt.title("Nombre moyen de saisons des séries", fontweight="bold")
plt.savefig("./chart_images/tv_show_mean_duration.png")
# plt.show()

# %% [markdown]
# ### Plot movies mean durations per year

# %%
movies_year_mean_df = movies_year_mean_df.reset_index()
plt.bar(movies_year_mean_df.release_year,
        movies_year_mean_df.duration, label='Movies')
plt.xlabel('Années')
plt.ylabel('Durées moyennes')
plt.title('Durées moyennes des films', fontweight="bold")
plt.savefig("./chart_images/movie_mean_duration.png")
# plt.show()

# %% [markdown]
# ### Plot movies duration count per  year

# %%
movies_year_count_df = movies_year_count_df.reset_index()
plt.bar(movies_year_count_df.release_year,
        movies_year_count_df.duration, label='Movies')
plt.xlabel('Années')
plt.ylabel('Nombre')
plt.title('Nombre de films par an', fontweight="bold")
plt.savefig("./chart_images/movie_count.png")
# plt.show()
