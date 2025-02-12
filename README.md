# A Bespoke Framework for Inferring Sleep Patterns  

## Overview  

This project presents a framework for inferring sleep patterns based on online activity data. By analyzing data from Google Takeout location history and Microsoft Edge browsing history, the study demonstrates how aggregating multiple data sources improves the accuracy of sleep inference. The framework is designed as a proof of concept and encourages further research into using online behavioral data for health monitoring.  

## Features  

- Aggregates multiple online activity data sources  
- Extracts sleep and wake-up times from browsing and location data  
- Implements data filtering techniques to improve accuracy  
- Evaluates results based on consistency and alignment with ground truth  

## Data Sources  

- **Google Takeout (Location History)**: Provides timestamps of physical movements  
- **Microsoft Edge Search History**: Tracks online activity timestamps  

## Methodology  

1. **Data Collection**: Extracts timestamps from online activity logs  
2. **Data Processing**: Filters records within the study period (January 13 - February 5, 2025)  
3. **Sleep Pattern Identification**:  
   - Uses a time difference method (6-15 hour gap) to infer sleep intervals  
   - Applies an earliest/latest time threshold for location data  
4. **Data Cleaning**: Removes outliers and non-sensical records  
5. **Analysis**: Compares different datasets to evaluate accuracy  

## Results  

- Combining data sources improves sleep inference accuracy  
- Start times have a 1-hour 9-minute lead time, while finish times have a 52-minute lag  
- Search history provides better estimates for sleep end times  
- Data sparsity can impact accuracy; more sources enhance reliability  

## Ethical Considerations  

- Only the author’s data was analyzed with full consent  
- No mental health analysis was conducted beyond sleep inference  
- Sensitive data was anonymized before processing  

## Future Work  

- Incorporating additional data sources (e.g., mobile phone activity)  
- Refining sleep detection algorithms with machine learning  
- Expanding study scope to multiple participants

## Paper
For more details, refer to the full paper:  
[**A Bespoke Framework for Inferring Sleep Patterns**](https://github.com/gladstone-9/cs6501-bespoke-framework/blob/main/sleep_inference_Gabriel_Gladstone.pdf)  