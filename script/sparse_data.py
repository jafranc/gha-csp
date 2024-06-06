import matplotlib.pyplot as plt
import numpy as np

from data import Data, Conversion


class Sparse_Data(Data):
    """ Class for handling from vtm time series to sparse data SPE11-CSP"""

    def __init__(self, version, units, suffix):
        super().__init__(version, suffix)

        self.converters = [('sec', 1), ('kg', 1), ('Pa', 1)]

        if 's' in units:
            self.converters[0] = ('sec', Conversion.SEC2SEC)
        elif 'h' in units:
            self.converters[0] = ('hour', Conversion.SEC2HOUR)
        elif 'd' in units:
            self.converters[0] = ('day', Conversion.SEC2DAY)
        elif 'y' in units:
            self.converters[0] = ('year', Conversion.SEC2YEAR)

        if 'kg' in units:
            self.converters[1] = ('kg', Conversion.KG2KG)
        elif 't' in units:
            self.converters[1] = ('t', Conversion.KG2T)
        elif 'g' in units:
            self.converters[1] = ('g', Conversion.KG2G)

        if 'Pa' in units:
            self.converters[2] = ('Pa', Conversion.PA2PA)
        elif 'bar' in units:
            self.converters[2] = ('bar', Conversion.PA2BAR)

        # geom in meters
        self.boxes = {'Whole': [(0.0, 0.0, -1.2), (2.8, .01, 0.0)]}
        self.PO1 = [1.5, -0.7]
        self.PO2 = [1.7, -0.1]
        self.schedule = np.arange(0, 5 * Conversion.SEC2DAY, 30000.)

        if self.version == 'b':
            self.boxes['Whole'] = [(item[0] * 3000, 1. / 0.01 * item[1], item[2] * 1000) for item in
                                   self.boxes['Whole']]
            self.PO1 = [self.PO1[0] * 3000, self.PO1[1] * 1000]
            self.PO2 = [self.PO2[0] * 3000, self.PO2[1] * 1000]
            self.schedule = np.arange(0., 1000 * Conversion.SEC2YEAR, 1000 / 200 * Conversion.SEC2YEAR)

        elif self.version == 'c':
            # self.schedule = np.asarray([5 * Conversion.SEC2YEAR, 25 * Conversion.SEC2YEAR, 50 * Conversion.SEC2YEAR,
            #                             100 * Conversion.SEC2YEAR,
            #                             250 * Conversion.SEC2YEAR, 500 * Conversion.SEC2YEAR, 750 * Conversion.SEC2YEAR,
            #                             1000 * Conversion.SEC2YEAR])
            self.PO1 = [4500, 2500, 655]
            self.PO2 = [5100, 2500, 1255]
        # origin
        Ox, Oy, Oz = self.boxes['Whole'][0]
        # full length
        Lx, Ly, Lz = self.boxes['Whole'][1]
        Lx -= Ox
        Ly -= Oy
        Lz -= Oz

        self.boxes['A'] = [(Ox + 1.1 / 2.8 * Lx, Oy, Oz), (Ox + Lx, Oy + Ly, Oz + 0.6 / 1.2 * Lz)]
        self.boxes['B'] = [(Ox, Oy, Oz + 0.6 / 1.2 * Lz), (Ox + 1.1 / 2.8 * Lx, Oy + Ly, Oz + Lz)]
        self.boxes['C'] = [(Ox + 1.1 / 2.8 * Lx, Oy, Oz + 0.1 / 1.2 * Lz),
                           (Ox + 2.6 / 2.8 * Lx, Oy + Ly, Oz + 0.5 / 1.2 * Lz)]

        # too distorded boxes, easier to hard code
        if self.version == 'c':
            self.boxes['Whole'] = [(0., 0., 0.), (8400., 5000., 1200.)]
            self.boxes['A'] = [(3300., 0., 0.), (8300., 5000., 750.)]
            self.boxes['B'] = [(100., 0., 750.), (3300., 5000., 1350.)]
            self.boxes['C'] = [(3300., 0., 250.), (7800., 5000., 550.)]

    def process(self, odir, idir):

        self._plot_(idir, odir)

    def _plot_(self, idir, odir):

        import pandas as pd
        df = pd.read_csv(idir + '/spe11' + self.version + '_time_series.csv')
        print(df.keys())
        fig, axs = plt.subplots(2, 2)
        (time_name, time_unit), (mass_name, mass_unit), (pressure_name, pressure_unit) = self.converters
        # pressures
        axs[0][0].plot(df['t[s]'].to_numpy() / time_unit, df['p1[Pa]'].to_numpy() / pressure_unit,
                       label=f'pressure 1 [{pressure_name}]')
        axs[0][0].plot(df['t[s]'].to_numpy() / time_unit, df['p2[Pa]'].to_numpy() / pressure_unit,
                       label=f'pressure 2 [{pressure_name}]')
        axs[0][0].legend()
        # box A
        axs[0][1].plot(df['t[s]'].to_numpy() / time_unit, df['mobA[kg]'].to_numpy() / mass_unit,
                       label=f'mobile CO2 [{mass_name}]')
        axs[0][1].plot(df['t[s]'].to_numpy() / time_unit, df['immA[kg]'].to_numpy() / mass_unit,
                       label=f'immobile CO2 [{mass_name}]')
        axs[0][1].plot(df['t[s]'].to_numpy() / time_unit, df['dissA[kg]'].to_numpy() / mass_unit,
                       label=f'dissolved CO2 [{mass_name}]')
        axs[0][1].plot(df['t[s]'].to_numpy() / time_unit, df['sealA[kg]'].to_numpy() / mass_unit,
                       label=f'seal CO2 [{mass_name}]')
        axs[0][1].legend()
        axs[0][1].set_title('boxA')
        # box B
        axs[1][0].plot(df['t[s]'].to_numpy() / time_unit, df['mobB[kg]'].to_numpy() / mass_unit,
                       label=f'mobile CO2 [{mass_name}]')
        axs[1][0].plot(df['t[s]'].to_numpy() / time_unit, df['immB[kg]'].to_numpy() / mass_unit,
                       label=f'immobile CO2 [{mass_name}]')
        axs[1][0].plot(df['t[s]'].to_numpy() / time_unit, df['dissB[kg]'].to_numpy() / mass_unit,
                       label=f'dissolved CO2 [{mass_name}]')
        axs[1][0].plot(df['t[s]'].to_numpy() / time_unit, df['sealB[kg]'].to_numpy() / mass_unit,
                       label=f'seal CO2 [{mass_name}]')
        axs[1][0].legend()
        axs[1][0].set_title('boxB')
        # boxC
        axs[1][1].plot(df['t[s]'].to_numpy() / time_unit, df['M_C[m]'].to_numpy(), label='M_C[m]')
        axs[1][1].legend()
        axs[1][1].set_title('boxC')

        fig.tight_layout()
        fig.savefig(f'{odir}/spe11{self.version}_timeseries-{self.suffix}.png', bbox_inches='tight')
