# %% [markdown]
# ## Imports

# %%
import pandas as pd
import matplotlib.pyplot as plt
from enum import Enum

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


# %%
columns = [Column.TYPE.value, Column.TITLE.value,
           Column.RELEASE_YEAR.value, Column.DURATION.value]

# %%


class Types(Enum):
    TV_SHOW = 'TV Show'
    MOVIE = 'Movie'

# %% [markdown]
# # Load data from csv file


# %%
df = pd.read_csv('netflix_data.csv', usecols=columns)  # [:3500]

# %% [markdown]
# # Plot data

# %%
print("Contents in csv file:", df)

# %%
titles = df.title
# y = df.release_year
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
# clean df duration column
movies_df.duration = clean_durations(movies_df.duration)
tv_shows_df.duration = clean_durations(tv_shows_df.duration)

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
# # Plot

# %% [markdown]
# ### Plot tv shows mean duration per year

# %%
tv_shows_year_mean_df = tv_shows_year_mean_df.reset_index()
plt.bar(tv_shows_year_mean_df.release_year,
        tv_shows_year_mean_df.duration, label='TV Shows')
plt.show()

# %% [markdown]
# ### Plot tv shows count per year

# %%
tv_shows_year_count_df = tv_shows_year_count_df.reset_index()
plt.bar(tv_shows_year_count_df.release_year,
        tv_shows_year_count_df.duration, label='TV Shows')
plt.show()

# %% [markdown]
# ### Plot movies mean durations per year

# %%
movies_year_mean_df = movies_year_mean_df.reset_index()
plt.bar(movies_year_mean_df.release_year,
        movies_year_mean_df.duration, label='Movies')
plt.show()

# %% [markdown]
# ### Plot movies duration count per  year

# %%
movies_year_count_df = movies_year_count_df.reset_index()
plt.bar(movies_year_count_df.release_year,
        movies_year_count_df.duration, label='Movies')
plt.show()
