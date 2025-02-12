import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from datetime import datetime, time
import math
import json
from lib_analysis import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    ## Initliaze locaction dataframe
    # Load JSON data from file
    with open("loction_timeline_redacted.json", "r") as file:
        data = json.load(file)

    # Convert JSON to DataFrame
    df = pd.DataFrame(data, columns=["startTime", "endTime"])

    # Transform to long format (one column for Time)
    df = df.melt(value_name="Day-Time", var_name="Type")

    # Convert Time column to datetime format    
    df["Day-Time"] = pd.to_datetime(df["Day-Time"])

    # Format the datetime column to MM/DD/YYYY HH:MM:SS AM/PM
    df["Day-Time"] = df["Day-Time"].dt.strftime('%m/%d/%Y %I:%M:%S %p')

    df = init_transformation(df, "Day-Time", compare_algo="earliest_pt")

    # # Display the DataFrame
    # print(df)

    # Original Plot
    # plot_start_end_activity(df)

    # Filter extreme start/finish times
    df = filter_extraneous_times(df)

    # Filtred Plot 
    # plot_start_end_activity(df)
    
    # Analyze this Semester
    print("--- Location Stats ---")
    df = filter_by_date_custom(df, "2025-01-13", "2025-02-05")
    print_stats(df, " - Spring Semester:")
    print()
    plot_start_end_activity(df)
    
    # Analyze this Semester M/W/F
    df_M_W_F = filter_by_date_custom(df, "2025-01-13", "2025-02-05",[0,2,4])
    print_stats(df_M_W_F, " - Spring Semester (M/W/F Only):")
    print()
    # plot_start_end_activity(df_M_W_F)
    
    # Analyze this Semester T/Th
    df_T_TH = filter_by_date_custom(df, "2025-01-13", "2025-02-05",[1,3])
    print_stats(df_T_TH, " - Spring Semester (T/Th Only):")
    print()
    # plot_start_end_activity(df_T_TH)
    
    # Initialize search dataframe
    file_path = 'all_browser_search_redacted.xlsx'
    column_name = 'Day-Time'
    df_search = pd.read_excel(file_path, usecols=[0])
    df_search = init_transformation(df_search, column_name, compare_algo="diff_compare")
    # plot_start_end_activity(df_search, x_label="month")
    
    df_search = filter_extraneous_times(df_search)
    df_search = filter_by_date_custom(df_search, "2025-01-13", "2025-02-05")
    plot_start_end_activity(df_search)

    # Analyze this Semester - Search
    print("--- Search Stats ---")
    print_stats(df_search, " - Combined Spring Semester:")
    print()
    # plot_start_end_activity(df_combined)
    
    # Analyze this Semester M/W/F - Combined
    df_M_W_F = filter_by_date_custom(df_search, "2025-01-13", "2025-02-05",[0,2,4])
    print_stats(df_M_W_F, " - Combined Spring Semester (M/W/F Only):")
    print()
    # plot_start_end_activity(df_M_W_F)
    
    # Analyze this Semester T/Th - Combined
    df_T_TH = filter_by_date_custom(df_search, "2025-01-13", "2025-02-05",[1,3])
    print_stats(df_T_TH, " - Combined Spring Semester (T/Th Only):")
    print()
    # plot_start_end_activity(df_T_TH)
    
    # plot_start_end_activity(df_search)
    
    ## Combine search and location dataframes
    # Ensure correct format of df's
    df.loc[:, 'Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    df_search.loc[:, 'Time'] = pd.to_datetime(df_search['Time'], format='%H:%M:%S')
    
    df_combined = update_df_start_points([df, df_search]) 
    
    # Analyze this Semester - Combined
    print("--- Combined Stats ---")
    print_stats(df_combined, " - Combined Spring Semester:")
    print()
    plot_start_end_activity(df_combined)
    
    # Analyze this Semester M/W/F - Combined
    df_M_W_F = filter_by_date_custom(df_combined, "2025-01-13", "2025-02-05",[0,2,4])
    print_stats(df_M_W_F, " - Combined Spring Semester (M/W/F Only):")
    print()
    # plot_start_end_activity(df_M_W_F)
    
    # Analyze this Semester T/Th - Combined
    df_T_TH = filter_by_date_custom(df_combined, "2025-01-13", "2025-02-05",[1,3])
    print_stats(df_T_TH, " - Combined Spring Semester (T/Th Only):")
    print()
    # plot_start_end_activity(df_T_TH)
    
    # plot_start_end_activity(df_combined)                    # Grey points show previous start values
    
    
    
    
    
    # # Redact JSON Data
    # json_data = []
    # for i in range(len(df) - 1):
    #     json_data.append({
    #         "startTime": df["Day-Time"][i].isoformat(),
    #         "endTime": df["Day-Time"][i + 1].isoformat()
    #     })

    # # Save to JSON file
    # with open("data.json", "w") as file:
    #     json.dump(json_data, file, indent=2)