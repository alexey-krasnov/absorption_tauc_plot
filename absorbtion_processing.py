import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
import glob

# Read input data file from the current directory
for i in glob.glob('*.txt'):
    df = pd.read_csv(i, sep=",")
    df['Energy, eV'] = 1240 / df['Wavelength (nm)']
    df['Direct transition'] = (df['Absorbance'] * df['Energy, eV'])**2
    df['Indirect transition '] = (df['Absorbance'] * df['Energy, eV'])**0.5
    print(df)
    df.to_excel(i.replace('txt', 'xlsx'), 'Sheet1', index=False)
    df.to_csv(i.replace('.txt', '+.txt'), sep=',', index=False)

    # Plot figures
    plt.plot(df['Wavelength (nm)'], df['Absorbance'])
    plt.ylim(0)  # set y limits manually
    plt.xlim((250,  700))  # set x limits manually
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    plt.savefig(i.replace('txt', 'png'), dpi=600)

print("Processing of your absorbtion data is finished!")


    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # assert isinstance(ax, axes.Axes)
    # ax.set_xlim(250, 700)# set x limits manually
    # ax.set_ylim(0)# set y limits manually
    # ax.set_title(i.replace('txt', ''))
    # ax.title.set_size(15)
    # ax.set_xlabel('λ, nm')
    # ax.set_ylabel('F(R), a.u.')
    # ax.plot(df['Wavelength (nm)'], df['Absorbance'])
