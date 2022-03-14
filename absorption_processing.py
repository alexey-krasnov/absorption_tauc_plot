# -*- coding: UTF-8 -*-
"""Process UV-Vis absorption spectra, make Tauc transformation for direct/indirect allowed transition,
extract band gap values for corresponding transition type, and plot figures"""


import fnmatch
import glob
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
from matplotlib import ticker
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import linregress


def data_reading():
    """Read data from csv files in the current directory, return DataFrame.
    Assign proper column names as 'Wavelength (nm)', 'Absorbance'."""
    column_names = ['Wavelength (nm)', 'Absorbance']
    df = pd.read_csv(file, header=0, names=column_names, sep=",")
    return df


def ask_semiconductor_type(file_name: str) -> float:
    """Ask user about semiconductor type. n is an indicator that characterizes the process of optical absorption
    and is equal to 1/2 and 2 for indirect allowed and direct allowed transitions, respectively."""
    try:
        n = float(input(f"Enter 2 or 0.5 if {file_name.replace('.txt', '')} "
                        f"is a direct or indirect type semiconductor. \n"
                        f"Enter 0.5 if you do not have any information about type semiconductor: "))
    except ValueError:
        print("The values should be only digits, e.g. 2 or 0.5")
    return n


def data_processing(df, n=2.0):
    """Read data from csv files in the current directory, making Tauc transformation, writing, and exporting data.
    Calculation of the corresponding energy values and Tauc transformation for direct/indirect allowed transition."""
    df['Energy, eV'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy, eV']) ** 2
    if n == 0.5:
        df['Indirect transition'] = (df['Absorbance'] * df['Energy, eV']) ** 0.5
    # Export excel and/or txt files, comment-uncomment if necessary.
    # df.to_excel(i.replace('txt', 'xlsx'), 'Sheet1', index=False)
    df.to_csv(file.replace('.txt', '_out.txt'), sep=',', index=False)
    return df


def absorption_plot(df, file_name):
    """Plot figures of the absorption spectra"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(250, 700)  # set x limits
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.set_ylim(auto=True)  # set y limits
    ax.set_title(file_name.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('λ, nm')
    ax.set_ylabel('F(R), a.u.')
    ax.plot(df['Wavelength (nm)'], df['Absorbance'])
    plt.savefig(file_name.replace('txt', 'png'), dpi=300)


def tauc_gen(df):
    for tauc in ['Direct transition', 'Indirect transition']:
        yield df[tauc]


def tauc_plot(x_axis, y_axis, n, file_name):
    """Plot Tauc figure for direct/indirect transition"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(auto=True)  # set x limits manually
    ax.set_ylim(auto=True)  # set y limits manually
    ax.set_title(file.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('hν, eV')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.4)) # Set major tick
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02)) # Set minor tick
    ax.set_ylabel(rf'(F(R)·hν)$^{n}$')
    ax.plot(x_axis, y_axis)
    plt.savefig(file_name.replace('.txt', f'_{y_axis.name}.png'), dpi=300)


def get_band_gap(x_axis, y_axis) -> float:
    """Calculate direct band gap value"""
    #  Convert Pandas Series 'Energy, eV', 'Direct transition' or 'Indirect transition' to NumPy arrays
    x_numpy = x_axis.to_numpy()
    y_numpy = y_axis.to_numpy()
    # Get the 1st differential with smoothing of y functions
    dx = np.diff(x_numpy, 1)
    dy = np.diff(savgol_filter(y_numpy, 51, 3), 1)
    # Select the global maximum point on the graph
    maxindex = np.argmax(dy / dx)
    x_linear = x_numpy[maxindex - 10: maxindex + 10]
    y_linear = y_numpy[maxindex - 10: maxindex + 10]
    a, b, r_value, p_value, stderr = linregress(x_linear, y_linear)
    e_band_gap = round(-b / a, 2)
    print(f"{y_axis.name} band gap is: {e_band_gap}")
    return e_band_gap


if __name__ == "__main__":
    # Check if you have already run the program and got the files.
    txt_files = glob.glob('[!requirements]*.txt')
    for file in txt_files:
        if fnmatch.fnmatch(file, '*_out.txt') or file.replace('.txt', '_out.txt') in txt_files:
            print(f"{file} is already processed or generated")
            continue
        print(f'Running for {file}')
        # Read initial csv files from the current directory and make calculation
        initial_df = data_reading()
        tauc_indicator = ask_semiconductor_type(file_name=file)
        processed_df = data_processing(df=initial_df, n=tauc_indicator)
        # Plot figures of the absorption spectra and Tauc transformation
        absorption_plot(df=processed_df, file_name=file)
        # Work with 'Direct/Indirect transition' series from df
        tauc_series = tauc_gen(df=processed_df)
        for tauc in tauc_series:
            tauc_plot(x_axis=processed_df['Energy, eV'], y_axis=tauc, n=tauc_indicator, file_name=file)
            # Get Eg
            e_g = get_band_gap(x_axis=processed_df['Energy, eV'], y_axis=tauc)
    print("Processing of your absorption data is finished successfully!")
