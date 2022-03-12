<h1 align="center">Welcome to Absorption_Tauc_processing 👋</h1>
<p>
  <a href="https://twitter.com/AlekseiKrasnov4" target="_blank">
    <img alt="Twitter: AlekseiKrasnov4" src="https://img.shields.io/twitter/follow/AlekseiKrasnov4.svg?style=social" />
  </a>
</p>

> Plot absorption spectra and make Tauc transformation for direct/indirect allowed transition based on UV-Vis absorption data

## Usage
`absorption_processing` should be used within a directory containing your raw csv (.txt) files. These files should have the following format:
```python
"Wavelength nm." "Abs."
X1 Y1
X2 Y2
 .  .
 .  .
 .  .
```
where Xi and Yi are the recorded wavelengths and absorption coefficients (Kubelka-Munk function), respectively. 
Within the directory containing csv (.txt) files files, run:
```sh
absorption_processing.py
```
The program asks to specify the semiconductor type. Enter 0 for direct; 1 for indirect or if you do not have any information about type semiconductor. The program creates txt file with data in 5 columns: Wavelength (nm), Absorbance,  Energy, eV, Direct transition, Indirect transition, for further plotting of the figures. The corresponding figures of the absorption spectra, Tauc plot for direct/indirect transition for each sample are also generated. 


## Author

👤 **Aleksei Krasnov**

* Website: https://www.researchgate.net/profile/Aleksei-Krasnov
* Twitter: [@AlekseiKrasnov4](https://twitter.com/AlekseiKrasnov4)
* Github: [@alexey-krasnov](https://github.com/alexey-krasnov)
* LinkedIn: [@aleksei-krasnov-b53b2ab6](https://linkedin.com/in/aleksei-krasnov-b53b2ab6)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/alexey-krasnov/Absorption_Tauc_plot/issues). 
