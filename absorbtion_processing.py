import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
import glob
import matplotlib.ticker as ticker


def abs_plot():
    """Plot figure of the absorption spectra"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert isinstance(ax, axes.Axes)
    ax.set_xlim(250, 700)  # set x limits manually
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.set_ylim(auto=True)  # set y limits manually

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
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02))
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
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.02))
    ax.set_ylabel(r'(F(R)·hν)$^{1/2}$')
    # ax.set_ylabel(r'(F(R)·$h\nu)^{1/2}$)')
    ax.plot(df['Energy, eV'], df['Indirect transition'])
    plt.savefig(i.replace('.txt', '_indirect_Tauc.png'), dpi=300)


# Read initial csv files from the current directory
for i in glob.glob('*.txt'):
    df = pd.read_csv(i, sep=",")

    # Calculation of the corresponding energy and Tauc transformation for direct/indirect allowed transition
    df['Energy, eV'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy, eV'])**2
    df['Indirect transition'] = (df['Absorbance'] * df['Energy, eV'])**0.5
    # Check if you have already run the program for the files
    if i in glob.glob('*+.txt'):
        print("You have already generated necessary files")
        continue
    else:
        # Export Excel and txt files
        # df.to_excel(i.replace('txt', 'xlsx'), 'Sheet1', index=False)
        df.to_csv(i.replace('.txt', '+.txt'), sep=',', index=False)
        # Plot absorption figures
        abs_plot()
        # Plot Tauc plot figures
        n = input(f"Enter 0 or 1 if {i.replace('.txt', '')} is a direct or indirect type semiconductor. "
                  "Enter 1 if you do not have any information. ")
        if int(n) == 0:
            direct_plot()
        elif int(n) == 1:
            direct_plot()
            indirect_plot()

print("Processing of your absorption data is finished!")
