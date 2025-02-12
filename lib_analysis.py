
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from datetime import time
import math

# Identify the Start and Finish Times
# column_name = datetime column
def init_transformation(df, column_name, compare_algo="diff_compare"):    
    df[column_name] = pd.to_datetime(df[column_name], format='%m/%d/%Y %I:%M:%S %p')
    
    # Sort records
    df = df.sort_values(by=column_name)
    
    if compare_algo == "diff_compare":
        # Compute time difference
        df['TimeDiff'] = df[column_name].diff()
        
        # Convert TimeDiff to hours
        df['TimeDiffHours'] = df['TimeDiff'].dt.total_seconds() / 3600
        
        # Create StartDay
        df['StartDay'] = ((df['TimeDiffHours'] > 6) & (df['TimeDiffHours'] <= 15)).astype(int)
    elif compare_algo == "earliest_pt":
        df['Date'] = df[column_name].dt.date
        df['Time'] = df[column_name].dt.time
        df['Hour'] = df[column_name].dt.hour
        
        # Identify the first entry for each day within time range (4 AM - 5 PM)
        df['StartDay'] = 0
        first_valid_entries = df[(df['Hour'] >= 4) & (df['Hour'] < 17)].groupby('Date').head(1).index
        df.loc[first_valid_entries, 'StartDay'] = 1
    
    # Create Finish Day
    df['FinishDay'] = df['StartDay'].shift(-1).fillna(0).astype(int)
    
    # Extract date and time into separate columns
    df['Date'] = df[column_name].dt.date
    df['Time'] = df[column_name].dt.time
    
    return df

# Plot the given dataframe
def plot_start_end_activity(df, x_label="week"):
    # Plot
    df.loc[:, 'Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

    plt.figure(figsize=(8, 4))
    # colors = np.where(df['FinishDay'] == 1, 'r', np.where(df['StartDay'] == 1, 'b', 'gray'))  # Default to gray if neither is 1
    # scatter = plt.scatter(df['Date'], df['TimeFormatted'], color=colors, label="Values")
    
    # Plot gray points (background layer)
    mask_gray = (df['FinishDay'] != 1) & (df['StartDay'] != 1)
    df_gray = df.loc[mask_gray]  # Store filtered DataFrame for correct indexing
    scatter_gray = plt.scatter(df_gray['Date'], df_gray['Time'], 
                            color='gray', label="Other", alpha=0.5)

    # Plot StartDay (blue points)
    mask_blue = df['StartDay'] == 1
    df_blue = df.loc[mask_blue]  
    scatter_blue = plt.scatter(df_blue['Date'], df_blue['Time'], 
                            color='b', label="StartDay")

    # Plot FinishDay (red points) 
    mask_red = df['FinishDay'] == 1
    df_red = df.loc[mask_red]  
    scatter_red = plt.scatter(df_red['Date'], df_red['Time'], 
                            color='r', label="FinishDay")

    # Interactive hover
    cursor = mplcursors.cursor([scatter_gray, scatter_blue, scatter_red], hover=True)

    def update_annotation(sel):
        if sel.artist == scatter_gray:
            df_selected = df_gray
        elif sel.artist == scatter_blue:
            df_selected = df_blue
        elif sel.artist == scatter_red:
            df_selected = df_red
        else:
            return 

        # Fetch row from DataFrame
        row = df_selected.iloc[sel.index]
        
        sel.annotation.set_text(
            f"Date: {row['Date'].strftime('%Y-%m-%d')}\n"
            f"Time: {row['Time'].strftime('%I:%M %p')}"
        )

    cursor.connect("add", update_annotation)

    # Format x-axis
    if x_label == "month":
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    elif x_label == "week":
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())  # Places tick marks at the start of each week
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))  # Format as "Month Day, Year"

    # Format y-axis
    plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    plt.gca().yaxis.set_major_locator(mdates.HourLocator(interval=2))
    
    # # Add dotted lines at 10:56 AM and 11:58 PM
    # plt.axhline(pd.to_datetime("10:56:00", format="%H:%M:%S"), color='blue', linestyle='dotted', linewidth=1.2, label="10:56 AM")
    # plt.axhline(pd.to_datetime("23:58:00", format="%H:%M:%S"), color='red', linestyle='dotted', linewidth=1.2, label="11:58 PM")

    # Formatting
    plt.xlabel("Date")
    plt.ylabel("Time")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Finish Day', markerfacecolor='r', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Start Day', markerfacecolor='b', markersize=8),
    ]
    plt.legend(handles=legend_elements)
    
    # Show plot
    plt.show()

# Analyzing September 14 '24 to Feb 5 '25
# start_date and end_date in 'YYYY-MM-DD' format
def filter_by_date(df, start_date, end_date):
    # Ensure inputs in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter records
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Given a list of times, return the avg time
def get_avg_time(time_list, is_finish_time=False):
    time_minutes = []
    
    # Convert times to minutes since midnight
    for t in time_list:
        minutes = t.hour * 60 + t.minute
        # Handle crossing midnight (+24 hours) before 12pm
        if is_finish_time and  t.hour < 12:
            minutes += 24 * 60  
        time_minutes.append(minutes)
    
    # Compute average time in minutes
    avg_minutes = sum(time_minutes) / len(time_minutes)
    
    # Convert
    avg_minutes = avg_minutes % (24 * 60)  # Keep within a 24-hour range
    avg_time = time(int(avg_minutes // 60), int(avg_minutes % 60))
    
    return avg_time.strftime('%I:%M %p'), avg_minutes


# Compute the variance of a time list given avgerage minutes
# Set finish time to handle Finsih Day calculations
def calculate_variance(time_list, avg_minutes, is_finish_time=False):
    time_minutes = []

    for t in time_list:
        minutes = t.hour * 60 + t.minute
        # Handle crossing midnight (+24 hours) before 12pm
        if is_finish_time and t.hour < 12:
            minutes += 24 * 60  
        time_minutes.append(minutes)

    # Compute variance
    variance = sum((x - avg_minutes) ** 2 for x in time_minutes) / len(time_minutes)

    return variance

# Remove df times in windows that are extreme ie. Finish Day at 6 pm.
# The Pair is not removed
# Start Day exclusion window (5pm - 3am)
# Finish Day exclusion window (5am  - 5pm)
def filter_extraneous_times(df):
    df = df.copy()
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

    # Apply filtering conditions
    return df[
        (
            (df['StartDay'] == 1) & (df['FinishDay'] == 0) &
            ((df['Time'] > pd.to_datetime('03:00:00').time()) & 
             (df['Time'] < pd.to_datetime('17:00:00').time()))
        ) |
        (
            (df['StartDay'] == 0) & (df['FinishDay'] == 1) &
            ((df['Time'] < pd.to_datetime('05:00:00').time()) | 
             (df['Time'] > pd.to_datetime('17:00:00').time()))
        )
    ]

# Filter by date and valid days in a week. 
def filter_by_date_custom(df, start_date, end_date, valid_days=None):
    # Ensure datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Default to Monday-Friday
    if valid_days is None:
        valid_days = [0, 1, 2, 3, 4]  # Monday to Friday

    # Filter records based on date range and valid days
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Date'].dt.weekday.isin(valid_days))]

# Prints stats of the data frame related to StartDay and Finish Day Records
def print_stats(df,description=""):
    start_times = df.loc[(df['StartDay'] == 1) & (df['FinishDay'] == 0), 'Time'].tolist()
    start_day_avg_time, start_day_avg_min = get_avg_time(start_times, False)
    print(f"AVG Start Time {description} {start_day_avg_time}")

    finish_times = df.loc[(df['StartDay'] == 0) & (df['FinishDay'] == 1), 'Time'].tolist()
    finish_day_avg_time, finish_day_avg_min = get_avg_time(finish_times, True)
    print(f"AVG Finish Time {description} {finish_day_avg_time}")

    print(f"STDev of Start Time {description} {math.sqrt(calculate_variance(start_times, start_day_avg_min, False)):.2f}")
    print(f"STDev of Finish Time {description} {math.sqrt(calculate_variance(finish_times, finish_day_avg_min, True)) % 1440:.2f}")
    
# Given a list of data frames
# Update StartDay time to the earliest
# Update FinishDay to latest
def update_df_start_points(df_list):
    if not df_list:
        return pd.DataFrame()  # Return an empty DataFrame if the list is empty
    
    # Concatenate DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)

    # Sort by date and time
    combined_df = combined_df.sort_values(by=['Date', 'Time']).reset_index(drop=True)

    ### ---- StartDay Logic ---- ###
    mask_start_day = combined_df['StartDay'] == 1
    earliest_start_per_day = combined_df[mask_start_day].groupby('Date')['Time'].idxmin()
    
    # Reset StartDay values
    combined_df['StartDay'] = 0
    
    # Set StartDay = 1 only for earliest StartDay
    combined_df.loc[earliest_start_per_day, 'StartDay'] = 1
    
    ### ---- FinishDay Logic ---- ###
    # FinishDay window: 9 PM (21:00) and 4 AM (next day)
    combined_df['Hour_temp'] = combined_df['Day-Time'].dt.hour
    mask_finish_window = (combined_df['Hour_temp'] >= 21) | (combined_df['Hour_temp'] < 4)

    # Adjust logical date for finishes after midnight
    combined_df['LogicalDate'] = combined_df['Date']
    combined_df.loc[combined_df['Hour_temp'] < 4, 'LogicalDate'] = combined_df['LogicalDate'] - pd.Timedelta(days=1)
    combined_df.loc[combined_df['Hour_temp'] < 4, 'Hour_temp'] = combined_df['Hour_temp'] + 24

    # Identify the latest FinishDay
    mask_finish_day = combined_df['FinishDay'] == 1
    valid_finish_entries = combined_df[mask_finish_day & mask_finish_window]

    latest_finish_per_day = valid_finish_entries.groupby(valid_finish_entries['LogicalDate'].dt.date)['Day-Time'].idxmax()

    # Reset FinishDay values
    combined_df['FinishDay'] = 0

    # Set FinishDay = 1 for latest FinishDay
    combined_df.loc[latest_finish_per_day, 'FinishDay'] = 1

    return combined_df

