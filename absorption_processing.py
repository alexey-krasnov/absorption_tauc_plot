# -*- coding: UTF-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
import glob
import matplotlib.ticker as ticker
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress


def data_reading():
    """Read data from csv files in the current directory, checking id the txt file is proper."""
    global df
    df = pd.read_csv(i, sep=",")


def data_processing():
    """Read data from csv files in the current directory, making Tauc transformation, writing, and exporting data."""
    global df
    # Calculation of the corresponding energy values and Tauc transformation for direct/indirect allowed transition.
    df['Energy, eV'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy, eV']) ** 2
    df['Indirect transition'] = (df['Absorbance'] * df['Energy, eV']) ** 0.5
    # Export excel and/or txt files, comment-uncomment if necessary.
    # df.to_excel(i.replace('txt', 'xlsx'), 'Sheet1', index=False)
    df.to_csv(i.replace('.txt', '+.txt'), sep=',', index=False)


def absorption_plot():
    """Plot figures of the absorption spectra"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(250, 700)  # set x limits
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.set_ylim(auto=True)  # set y limits
    ax.set_title(i.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('λ, nm')
    ax.set_ylabel('F(R), a.u.')
    ax.plot(df['Wavelength (nm)'], df['Absorbance'])
    plt.savefig(i.replace('txt', 'png'), dpi=300)


def direct_plot():
    """Plot figure for direct transition"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(auto=True)  # set x limits manually
    ax.set_ylim(auto=True)  # set y limits manually
    ax.set_title(i.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('hν, eV')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.4)) # Set major tick
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02)) # Set minor tick
    ax.set_ylabel(r'(F(R)·hν)$^{2}$')
    ax.plot(df['Energy, eV'], df['Direct transition'])
    plt.savefig(i.replace('.txt', '_direct_Tauc.png'), dpi=300)


def indirect_plot():
    """Plot figure for indirect transition"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(auto=True)  # set x limits manually
    ax.set_ylim(auto=True)  # set y limits manually
    ax.set_title(i.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('hν, eV')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.4)) # Set major tick
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02)) # Set minor tick
    ax.set_ylabel(r'(F(R)·hν)$^{1/2}$')
    ax.plot(df['Energy, eV'], df['Indirect transition'])
    plt.savefig(i.replace('.txt', '_indirect_Tauc.png'), dpi=300)

def direct_band_gap():
    #  Convert Pandas Series 'Energy, eV' and 'Direct transition' to NumPy arrays
    x = df['Energy, eV'].to_numpy()
    y = df['Direct transition'].to_numpy()
    # Get the 1st differential with smoothing of y functions
    dx = np.diff(x, 1)
    dy = np.diff(savgol_filter(y, 51, 3), 1)
    # Select the global maximum point on the graph
    maxindex_dir = np.argmax(dy/dx)
    x_linear_dir = x[maxindex_dir - 10: maxindex_dir + 10]
    y_linear = y[maxindex_dir - 10: maxindex_dir + 10]
    a, b, r_value, p_value, stderr = linregress(x_linear_dir, y_linear)
    E_dir_band_gap = round(-b / a, 2)
    print(f"Direct band gap is : {E_dir_band_gap}")
    # visualization_x = np.linspace(E_dir_band_gap, x[maxindex_dir-60], 2)
    # plt.scatter(E_dir_band_gap, 0, marker='x', color='k', label="Bandgap = " + str(E_dir_band_gap) + "eV")
    # plt.plot(x, y)
    # plt.plot(visualization_x, color='red')
    # plt.xlabel("Energia")
    # plt.ylabel("$(alpha h nu)^2$")
    # plt.title("Tauc plot")
    # plt.legend()
    # plt.grid()
    # plt.show()


def indirect_band_gap():
    #  Convert Pandas Series 'Energy, eV' and 'Inirect transition' to NumPy arrays
    x = df['Energy, eV'].to_numpy()
    y = df['Indirect transition'].to_numpy()
    # Get the 1st differential with smoothing of y functions
    dx = np.diff(x, 1)
    dy = np.diff(savgol_filter(y, 51, 3), 1)
    # Select the global maximum point on the graph
    maxindex_dir = np.argmax(dy / dx)
    x_linear_dir = x[maxindex_dir - 10: maxindex_dir + 10]
    y_linear = y[maxindex_dir - 10: maxindex_dir + 10]
    a, b, r_value, p_value, stderr = linregress(x_linear_dir, y_linear)
    E_indir_band_gap = round(-b / a, 2)
    print(f"Indirect band gap is : {E_indir_band_gap}")


# Check if you have already run the program and got the files.
if not glob.glob('*+.txt'):
    for i in glob.glob('*.txt'):
        # Read initial csv files from the current directory and make calculation
        data_reading()
        # Check if the txt file is proper
        if 'Wavelength (nm)' not in df.columns.tolist():
            print(f"Check the file {i}. It should contain two columns Wavelength (nm) and Absorbance.")
            continue
        else:
            n = input(f"Enter 0 or 1 if {i.replace('.txt', '')} is a direct or indirect type semiconductor."
                      "Enter 1 if you do not have any information about type semiconductor. ")
            data_processing()
            # Plot figures of the absorption spectra
            absorption_plot()
            # Plot Tauc figures
            if int(n) == 0:
                direct_plot()  # Plot Tauc only for direct transition
                direct_band_gap()
            elif int(n) == 1:
                # Plot Tauc both for indirect/direct transitions
                direct_plot()
                direct_band_gap()
                indirect_plot()
                indirect_band_gap()
            else:
                print("Please enter 0 ir 1 for direct/indirect type semiconductor.")
else:
    print("You have already generated necessary files.")

print("Processing of your absorption data is finished successfully!")
