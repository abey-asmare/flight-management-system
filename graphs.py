import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


import flet as ft
from flet.matplotlib_chart import MatplotlibChart

matplotlib.use("svg")



df = pd.read_csv('assets/charts/flight_charts.csv')
df_upd_del = pd.read_csv('assets/charts/flight_charts_upd_del.csv')
df['createdAt'] = pd.to_datetime(df['createdAt'], format='%d/%m/%Y')
df['fliedAt'] = pd.to_datetime(df['fliedAt'], format='%d/%m/%Y')
df_upd_del['updatedAt'] = pd.to_datetime(df_upd_del['updatedAt'], format='%d/%m/%Y')
df_upd_del['updatedDate'] = pd.to_datetime(df_upd_del['updatedDate'], format='%d/%m/%Y')
# Count the values in the "crud" column
crud_counts = df['crud'].value_counts()
df_filtered = df[df['crud'] == 'create']

def draw_crud():

    fig, ax = plt.subplots()
    # Create a pie chart
    ax.pie(crud_counts, labels=crud_counts.index, autopct='%1.1f%%')
    ax.set_title('Number of successful, Cancelled and recovered flights')
    ax.legend(title="Flight", loc='upper right')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)

def draw_flight_type():
    fig, ax = plt.subplots()
    # Count the number of local and international flights
    local_flights = df_filtered[df_filtered['flightType'] == 'local'].shape[0]
    international_flights = df_filtered[df_filtered['flightType'] == 'international'].shape[0]
    # Data for the pie chart
    labels = ['Local', 'International']
    sizes = [local_flights, international_flights]
    colors = ['#EF553B', '#636EFA']  # Colors for each section

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax.legend(title="Flight type", loc='upper right')

    # Add a title
    ax.set_title('Distribution of Flights')
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)

def draw_number_of_flights_by_destination():
    # Create a new dataframe with the 'to' column and its count
    df_to_counts = df['to'].value_counts().reset_index(name='count').rename(columns={'index': 'to'})

    fig, ax = plt.subplots()  # Create figure and axes
    ax.bar(df_to_counts['to'], df_to_counts['count'], color='#636EFA')  # Create the bar chart
    ax.set_xlabel('Destination')  # Set the x-axis label
    ax.set_ylabel('Number of Flights')  # Set the y-axis label
    ax.set_title('Number of Flights by Destination')  # Set the title
    ax.set_xticklabels(df_to_counts['to'], rotation=45)  # Rotate x-axis labels by 45 degrees
    fig.tight_layout()  # Adjust layout to prevent clipping of labels
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)


def successful_flights_till_now():
    fig, ax = plt.subplots()  # Set the figure size
    df_by_created_date = df_filtered['createdAt'].value_counts().reset_index(name='number_of_flights').rename(columns={'index': 'createdAt'})

    ax.plot(df_by_created_date['createdAt'], df_by_created_date['number_of_flights'], marker='o')  # Plot the data

    ax.set_xlabel('Created Date')  # Set the x-axis label
    ax.set_ylabel('Number of Flights')  # Set the y-axis label
    ax.set_title('Number of Flights by Created Date')  # Set the title

    plt.xticks(rotation=45)

    ax.grid(True)
    plt.tight_layout()
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)


def draw_reasons_for_delayal():
    reason_counts = df_upd_del['reason'].value_counts().reset_index(name='count').rename(columns={'index': 'reason'})

    fig, ax = plt.subplots()

    colors = ['#9EDAE5', '#1F77B4']
    ax.pie(reason_counts['count'], labels=reason_counts['reason'], autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title('Reasons for Flight delayal')
    ax.legend(title="Reasons for flight delayal", loc='upper right')

    ax.axis('equal')
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)

def draw_delayal_filter_by_state():
    merged_df = pd.merge(df, df_upd_del, on='flightId', how='inner', indicator=True)
    merged_df = merged_df[merged_df['crud'].isin(['update', 'delete'])]
    df_to_counts = merged_df['to'].value_counts().reset_index(name='count').rename(columns={'index': 'to'})
    df_to_counts['reason'] = merged_df['reason']
    df_to_counts['reason'] = df_to_counts['reason'].fillna("Natural Disasters")
    df_to_counts_sorted = df_to_counts.sort_values(by='count', ascending=False)

    # Create a color map based on the number of unique reasons
    unique_reasons = df_to_counts_sorted['reason'].unique()
    color_map = plt.cm.get_cmap('tab20', len(unique_reasons))  # Choose a colormap

    # Assign a color index to each reason
    color_dict = {reason: color_map(i) for i, reason in enumerate(unique_reasons)}

    # Create a figure and axis object
    fig, ax = plt.subplots()  # Set the figure size

    # Plot the bars with colors based on reason
    bars = ax.bar(df_to_counts_sorted['to'], df_to_counts_sorted['count'],
                  color=[color_dict[reason] for reason in df_to_counts_sorted['reason']])

    # Set labels and title
    ax.set_xlabel('Destination')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Bar chart showing the number of cancelled flights vs destination')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Show the bar chart
    plt.tight_layout()
    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)

def draw_flights_per_day():
    # Create a new dataframe with the 'createdAt' column and its count
    df_created_date = df_filtered['createdAt'].value_counts().reset_index(name='count').rename(columns={'index': 'createdAt'})

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df_created_date['createdAt'], df_created_date['count'], color='#636EFA')

    # Set labels and title
    ax.set_xlabel('Date of Creation')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Number of Flights by Date of Creation')

    # Rotate x-axis labels by 45 degrees for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()

    matplotlib.pyplot.close()

    return MatplotlibChart(fig, expand=True)

def draw_flights_per_month():
    # Create a new dataframe with the 'month' column and its count
    df_month = df_filtered['createdAt'].dt.month.value_counts().reset_index(name='count').rename(columns={'index': 'month'})

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df_month['month'], df_month['count'], color='#636EFA')

    # Set labels and title
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Number of Flights by Month')

    # Rotate x-axis labels by 45 degrees for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    matplotlib.pyplot.close()
    return MatplotlibChart(fig, expand=True)

def draw_flights_per_year():
    # Create a new dataframe with the 'year' column and its count
    df_year = df_filtered['createdAt'].dt.year.value_counts().reset_index(name='count').rename(columns={'index': 'year'})
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df_year['year'], df_year['count'], color='#636EFA')

    # Set labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Number of Flights by Year')

    # Rotate x-axis labels by 45 degrees for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    matplotlib.pyplot.close()
    return MatplotlibChart(fig, expand=True)



def draw(page: ft.Page, refresh_page):
    def handle_back(e):
         # Close Matplotlib figures after adding them to the grid
      matplotlib.pyplot.close()
      refresh_page()
    page.controls.clear()
    back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=handle_back)
    page.add(
        back_button
    )
    crud_chart = draw_crud()
    flight_type_chart = draw_flight_type()

    grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=500,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        padding=20
    )
    grid.controls.append(draw_crud())
    grid.controls.append(draw_flight_type())
    grid.controls.append(draw_reasons_for_delayal())
    grid.controls.append(draw_number_of_flights_by_destination())
    grid.controls.append(successful_flights_till_now())
    grid.controls.append(draw_delayal_filter_by_state())
    grid.controls.append(draw_flights_per_day())
    grid.controls.append(draw_flights_per_month())
    grid.controls.append(draw_flights_per_year())
    page.add(grid)
    page.update()
