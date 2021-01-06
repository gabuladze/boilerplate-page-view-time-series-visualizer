import calendar
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')

# Clean data
df = df[
    (df['value'] <= df['value'].quantile(0.975))
    & (df['value'] >= df['value'].quantile(0.025))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5), dpi=200)
    
    ax.plot(df, color='#DB4243')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_bar['month_i'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month', 'month_i']).mean()
    df_bar.sort_values(by='month_i', inplace=True)
    df_bar = df_bar.reset_index()
    df_bar = df_bar.drop(['month_i'], axis=1)
    df_bar = df_bar.pivot('year', 'month', 'value')
    df_bar.columns = [calendar.month_name[i+1] for i in range(12)]

    # Draw bar plot
    ax = df_bar.plot.bar(figsize=(8, 7), xlabel='Years', ylabel='Average Page Views')
    # ax.legend([calendar.month_name[i+1] for i in range(12)], title='Months')
    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    # df_box.reset_index(inplace=True)
    # df_box['year'] = [d.year for d in df_box.date]
    

    df_box['year'] = df_box.index.year
    df_box['month'] = [d.strftime('%b') for d in df_box.index]
    df_box['month_i'] = df_box.index.month
    df_box.sort_values(by='month_i', inplace=True)
    df_box.reset_index(inplace=True)
    df_box = df_box.drop(['month_i'], axis=1)

    # Draw box plots (using Seaborn)
    # print(df_box.head())
    fig, ax = plt.subplots(1,2, figsize=(15,5), dpi=200)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1])
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
