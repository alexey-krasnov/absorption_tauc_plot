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
    """Read data from csv files in the current directory, make Kubelka-Munk transformation
     if it needs, return DataFrame. Assign proper column names as 'Wavelength (nm)', 'Absorbance'."""
    column_names = ['Wavelength (nm)', 'Absorbance']
    # Data could be separated by comma or spase
    df = pd.read_csv(file, header=0, names=column_names, sep=r"\s+|,", engine='python')
    while True:
        answer = input("Is your data in the form of 'Wavelength (nm)', 'Absorbance'? Enter 1 if so or 0 if not: ")
        if answer == '0':
            # Make Kubelka-Munk transformation from reflectance to absorbance
            df['Absorbance'] = (1 - df['Absorbance']/100)**2 / (2 * df['Absorbance']/100)
            break
        elif answer not in ('0', '1'):
            print('Please, enter just 1 or 0')
            continue
        else:
            break
    return df


def ask_semiconductor_type(file_name: str) -> float:
    """Ask user about semiconductor type.
    n is an indicator that characterizes the process of optical absorption,
    and n is equal to 0.5 or 2 for indirect/direct allowed transitions."""
    while True:
        try:
            n = float(input(f"Enter 2 or 0.5 if {file_name.replace('.txt', '')} "
                        f"is a direct or indirect type semiconductor. \n"
                        f"Enter 0.5 if you do not have any information about semiconductor type: "))
            if n in {0.5, 2}:
                break
            else:
                print("Warning!!!The Tauc indicator should be only equal to 0.5 or 2.")
                continue
        except ValueError:
            print("The values should be only digits equal to 2 or 0.5")
    return n


def data_processing(df, n):
    """Read data from csv files in the current directory, making Tauc transformation, writing, and exporting data.
    Calculation of the corresponding energy values and Tauc transformation for direct/indirect allowed transition."""
    df['Energy (eV)'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy (eV)']) ** 2
    if n == 0.5:
        df['Indirect transition'] = (df['Absorbance'] * df['Energy (eV)']) ** n
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
    ax.set_ylim(auto=True)  # set y limits at 0
    ax.set_title(file_name.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('λ, nm')
    ax.set_ylabel('F(R), a.u.')
    ax.plot(df['Wavelength (nm)'], df['Absorbance'])
    plt.savefig(file_name.replace('txt', 'png'), dpi=300)


def tauc_generator(df, n):
    """Generator of pandas Series from processed Data Frame
    depending on type of semiconductor: direct or indirect """
    if n == 0.5:
        for col_name in ['Direct transition', 'Indirect transition']:
            yield df[col_name]
    else:
        yield df['Direct transition']


def linearization(x_axis, y_axis):
    """Make linearization of 'Direct transition'/'Indirect transition' plot vs energy"""
    #  Convert Pandas Series 'Energy (eV)'; 'Direct transition'/'Indirect transition' to NumPy arrays
    x_numpy = x_axis.to_numpy()
    y_numpy = y_axis.to_numpy()
    # Smooth y line
    y_smooth = savgol_filter(y_numpy, 51, 3)
    # Get the 1st differential of numpy arrays with smoothing of y functions
    dx = np.diff(x_numpy)
    dy = np.diff(y_smooth)
    # Select the global maximum point on the graph, smooth dy/dx plot
    max_index = np.argmax(savgol_filter(dy / dx, 101, 3))
    x_linear = x_numpy[max_index - 10: max_index + 10]
    y_linear = y_smooth[max_index - 10: max_index + 10]
    return x_linear, y_linear, max_index


def calc_linear_coeff(x_linear, y_linear) -> tuple:
    """Calculate a regression line and return its coefficients"""
    a, b, r_value, p_value, stderr = linregress(x_linear, y_linear)
    return a, b, r_value, p_value, stderr


def calc_band_gap(a, b, y_axis) -> float:
    """Calculate direct/indirect band gap value"""
    e_band_gap = round(-b / a, 2)
    print(f"{y_axis.name} band gap is: {e_band_gap}")
    return e_band_gap


def vizual_x(e_g, x_axis, max_index):
    """Return region of abscissa to plot a regression line"""
    visualization_x = np.linspace(e_g, x_axis[max_index - 60], 2)
    return visualization_x


def func(visualization_x, a, b):
    """Define and return a regression line function as 'y = a*x + b' """
    return a*visualization_x + b


def tauc_plot(x_axis, y_axis, file_name, e_g, a, b, visualization_x):
    """Plot Tauc figure for direct/indirect transition"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(auto=True)  # set x limits manually
    ax.set_ylim(ymin=0, auto=True)  # set y limits manually at 0
    ax.set_title(file.replace('.txt', ''))
    ax.title.set_size(15)
    ax.set_xlabel('hν, eV')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.4)) # Set major tick
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02)) # Set minor tick
    ax.set_ylabel(y_axis.name)
    ax.plot(x_axis, y_axis)
    ax.scatter(e_g, 0, marker='x', color='k', label=f"Band gap {e_g} eV")
    ax.plot(visualization_x, func(visualization_x, a, b), color='red')
    ax.legend()
    plt.savefig(file_name.replace('.txt', f'_{y_axis.name}.png'), dpi=300)


if __name__ == "__main__":
    # Exclude 'requirements.txt' file from processing
    txt_files = [f for f in glob.glob('*.txt') if not f == 'requirements.txt']
    # Check if you have already run the program and got the files.
    for file in txt_files:
        if fnmatch.fnmatch(file, '*_out.txt') or file.replace('.txt', '_out.txt') in txt_files:
            print(f"{file} is already processed or generated")
            continue
        print(f'Running for {file}...')
        # Read initial csv files from the current directory and make calculation
        initial_df = data_reading()
        # Get the type of semiconductor from user to determine Tauc indicator
        tauc_indicator = ask_semiconductor_type(file_name=file)
        print(tauc_indicator)
        processed_df = data_processing(df=initial_df, n=tauc_indicator)
        # Plot figures of the absorption spectra and Tauc transformation
        absorption_plot(df=processed_df, file_name=file)
        # Work with 'Direct/Indirect transition' series from DataFrame
        tauc_series = tauc_generator(df=processed_df, n=tauc_indicator)
        for tauc in tauc_series:
            x_linear, y_linear, max_index = linearization(x_axis=processed_df['Energy (eV)'], y_axis=tauc)
            a, b, r_value, p_value, stderr = calc_linear_coeff(x_linear, y_linear)
            e_g = calc_band_gap(a, b, y_axis=tauc)
            visualization_x = vizual_x(e_g, x_axis=processed_df['Energy (eV)'], max_index=max_index)
            tauc_plot(processed_df['Energy (eV)'], tauc, file, e_g, a, b, visualization_x)
    else:
        print("Processing of your absorption data is finished successfully!")
