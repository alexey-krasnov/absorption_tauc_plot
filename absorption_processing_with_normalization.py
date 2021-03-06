import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
import glob
import matplotlib.ticker as ticker


def data_processing():
    """Read data from csv files in the current directory, making Tauc transformation, writing, and exporting data."""
    global df
    df = pd.read_csv(i, sep=",")
    # Calculation of the corresponding energy values and Tauc transformation for direct/indirect allowed transition.
    norm_coeff = float(input(f"Enter the normalized coefficient for {i.replace('.txt', '')}: "))
    df['Absorbance'] = df['Absorbance'] * norm_coeff # Make normalization of Absorption
    df['Energy, eV'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy, eV']) ** 2
    df['Indirect transition'] = (df['Absorbance'] * df['Energy, eV']) ** 0.5
    # Export excel and/or txt files, comment-uncomment if necessary.
    # df.to_excel(i.replace('txt', 'xlsx'), 'Sheet1', index=False)
    df.to_csv(i.replace('.txt', '+.txt'), sep=',', index=False)

def absorbtion_plot():
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


# Check if you have already run the program and got the files.
if not glob.glob('*+.txt'):
    for i in glob.glob('*.txt'):
        # Read initial csv files from the current director
        data_processing()
        # Plot figures of the absorption spectra
        absorbtion_plot()
        # Plot Tauc figures
        n = input(f"Enter 0 or 1 if {i.replace('.txt', '')} is a direct or indirect type semiconductor."
                  "Enter 1 if you do not have any information about type semiconductor. ")
        if int(n) == 0:
            direct_plot()  # Plot Tauc only for direct transition
        elif int(n) == 1:
            direct_plot()  # Plot Tauc both for indirect/direct transitions
            indirect_plot()
        else:
            print("Please enter 0 ir 1 for direct/indirect type semiconductor.")
else:
    print("You have already generated necessary files.")

print("Processing of your absorption data is finished successfully!")
