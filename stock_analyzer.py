import numpy as np
# from pandas import Series
import matplotlib.pyplot as plt
import csv
import os

# ======================================================================================================================
#   Constants
# ======================================================================================================================
WORKING_DIRECTORY_PATH = os.getcwd()
STOCKS_DIRECTORY = 'downloads'
RESULTS_DIRECTORY = 'results'
STOCKS_DIRECTORY_PATH = os.path.join(WORKING_DIRECTORY_PATH, STOCKS_DIRECTORY)
RESULTS_DIRECTORY_PATH = os.path.join(WORKING_DIRECTORY_PATH, RESULTS_DIRECTORY)
PRICE_INCREASE_THRESHOLD = 0.1  # [%]

# ======================================================================================================================
#   Extract stock data
# ======================================================================================================================
stock_file_list = os.listdir(STOCKS_DIRECTORY_PATH)
plt.ioff()  # call .ion for interactive mode
fig = plt.figure(num='Stock Analyzer')
ax = plt.axes()
fig.add_axes(ax)

for stock_file in stock_file_list:
    # Read csv
    stock_file_path = os.path.join(STOCKS_DIRECTORY_PATH, stock_file)
    with open(stock_file_path, 'r') as f:
        reader = csv.reader(f)
        data = np.asarray(list(reader))

    # Delete row containing string null
    null_str = 'null'
    i_row = 0
    print('>> ' + stock_file)
    while i_row < data.shape[0]:
        if null_str in data[i_row]:
            data = np.delete(data, i_row, axis=0)
        else:
            i_row += 1

    # Calculate percentage increase from close to next open
    open_price = data[1:, 1].astype(np.float)
    close_price = data[1:, 4].astype(np.float)
    close_to_open_increase = open_price[1:] - close_price[:-1]
    close_to_open_percentage_increase = close_to_open_increase / close_price[:-1]
    i_sufficient_price_increase = np.argwhere(close_to_open_percentage_increase > PRICE_INCREASE_THRESHOLD).squeeze()
    sufficient_price_increase_data = data[i_sufficient_price_increase+2]

    if len(sufficient_price_increase_data) > 0:
        # Create stock image and csv in results directory
        result_csv_path = os.path.join(RESULTS_DIRECTORY_PATH, stock_file)

        if len(sufficient_price_increase_data.shape) > 1:
            np.savetxt(
                result_csv_path,
                np.concatenate(([data[0]], sufficient_price_increase_data)),
                delimiter=',',
                fmt='%s'
            )
        else:
            np.savetxt(
                result_csv_path,
                np.concatenate((data[0], sufficient_price_increase_data)),
                delimiter=',',
                fmt='%s'
            )

        # Plot data stock price open, close, diff, and sufficient price increase days
        ax.clear()
        ax.plot(open_price)
        ax.plot(close_price)
        ax.plot(close_to_open_increase)
        t = np.arange(len(open_price))
        ax.plot(t[i_sufficient_price_increase+1], open_price[i_sufficient_price_increase+1], 'o')

        ax.set_title('Stock: ' + str(stock_file))
        ax.set_xlabel('Time [days]')
        ax.set_ylabel('Price [SEK]')
        ax.legend((
            'Open',
            'Close',
            'Close to open increase',
            str(PRICE_INCREASE_THRESHOLD*100) + '% increase'
        ))
        result_fig_path = os.path.join(RESULTS_DIRECTORY_PATH, stock_file[:-3] + 'png')
        fig.savefig(result_fig_path)
print('Done!')
