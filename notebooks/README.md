Structure of the notebooks
Each notebook is prefixed with a number that indicates the order in which the notebooks need to be executed. Each notebook is designed to do a specific task. After processing the notebook, the updated state is optionally saved into a pickle file which is can be loaded in subsequent notebooks.

Notebook name|Description|
-------------|-------------|
0_DataCleanup|Performs data cleanup on the input donor dataset
11_County_Data|Loads the gps co-ordinates by county and state and saves them to a pickle file after cleaning. This data is needed for some bokeh plots in the web application.
21_FeatureEngineering_Appeal|The input dataset has an appeal column that is indicative of the specific fund-raiser campaign if the money was for a fund-raiser or the marketing campaign if it was a donation. We identify the transactions as fund-raiser or donation by a flag (is_service). For marketing campaigns, we also create a channel column that indicates the marketing channel.
30_DataVisualization|This notebook serves as an experimentation platform for trying out bokeh plots.
40_Data_preparation|Extract out summary data from the donation data which can be used by the web application.
41_ExtractEventData|The organization does not save the fund-raiser information. It is all just buried in the transactions. Here, I apply a heuristic method to identify the fund-raisers and then associate each transaction to the fund-raiser that it belongs to. The methodology identifies peaks in the data (by location and time) to identify the fund-raiser campaigns and then associates each transaction to the nearest peak.
42_ExtractDonor_Data|Create a donor dataset from the donations and events datasets. Then study repeat donors and overall growth.
61_TimeSeriesForChannel|Create a time-series of the donation amounts and predict future donations.
80_BokehPlots|Create two interactive visualizations using bokeh to see market growth potential and YTD comparison for donations with previous year.
