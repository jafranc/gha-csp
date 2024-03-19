import numpy as np
from data import Data, Conversion


class Dense_Data(Data):
    """ Class for handling from vtm time series to dense data SPE11-CSP """

    def __init__(self, version, suffix):

        super().__init__(version, suffix)
        self.phydims = (2.8, 1., 1.2)
        self.dims = (280, 1, 120)
        self.offset = [0., 0., -1.2]
        self.filename_converter, self.filename_marker = (Conversion.SEC2HOUR, 'h')

        if version[0] == 'b':
            self.phydims = (2.8 * 3000, 1., 1.2 * 1000)
            self.dims = (840, 1, 120)
            self.offset = [0., 0., -1200.]
            #
            self.schedule = np.arange(0., 1000 * Conversion.SEC2YEAR, 50 * Conversion.SEC2TENTHOFYEAR)
            self.filename_converter, self.filename_marker = (Conversion.SEC2YEAR, 'y')
        elif version[0] == 'c':
            self.phydims = (2.8 * 3000, 5000., 1.2 * 1000 + 150)
            self.dims = (168, 100, 120)
            self.offset = [0., 0., 0.]
            #
            self.schedule = list(np.arange(0, 50 * Conversion.SEC2YEAR, 5 * Conversion.SEC2YEAR))
            self.schedule.extend([75 * Conversion.SEC2YEAR, 100 * Conversion.SEC2YEAR])
            self.schedule.extend(
                np.arange(100 * Conversion.SEC2YEAR, 500 * Conversion.SEC2YEAR, 50 * Conversion.SEC2YEAR))
            self.schedule.extend(
                np.arange(500 * Conversion.SEC2YEAR, 1000 * Conversion.SEC2YEAR, 100 * Conversion.SEC2YEAR))
            self.filename_converter, self.filename_marker = (Conversion.SEC2YEAR, 'y')

        Nx, Ny, Nz = self.dims
        Lx, Ly, Lz = self.phydims
        self.x, self.y, self.z = np.meshgrid(np.linspace(Lx / 2 / Nx, (2 * Nx - 1) * Lx / 2 / Nx, Nx) + self.offset[0],
                                             np.linspace(Ly / 2 / Ny, (2 * Ny - 1) * Ly / 2 / Ny, Ny) + self.offset[1],
                                             np.linspace(Lz / 2 / Nz, (2 * Nz - 1) * Lz / 2 / Nz, Nz) + self.offset[2],
                                             indexing='xy')

    def process(self, odir, idir):

        # import multiprocessing as mp
        baseFileName = f'spe11{self.version}_dense'
        import matplotlib.pyplot as plt
        fig = {'satg': plt.figure(figsize=(18, 6)),
               'mCO2': plt.figure(figsize=(18, 6))}

        if 'temp' in self.name_indirection.values():
            fig['temp'] = plt.figure(figsize=(18, 6))

        csv_keys_translation = {'x': '# #x[m]', 'y': ' y[m]',
                                'z': ' z[m]',
                                'satg': ' gas saturation[-]',
                                'mCO2': ' mass fraction of CO2 in liquid[-]',
                                'temp': ' temperature[C]'}

        for itime, time in enumerate(self.schedule[:9]):
            import pandas as pd
            print(time)
            fname = idir + '/spatial_map_' + "{time:2}".format(
                time=time / self.filename_converter) + self.filename_marker + '.csv'
            data = pd.read_csv(fname)
            data = data.drop(0)  # miss write from numpy
            # as for out regular grid size it is faster just to dump the values
            fn = lambda k: data[csv_keys_translation[k]]
            self._plot_((itime, time), fig, fn, self.dims)

        for key, _ in fig.items():
            fig[key].savefig(f'{odir}/{baseFileName}_{key}-{self.suffix}.png', bbox_inches='tight')
    def _plot_(self, ttime, figdict, fn, dims):
        """ To check good rendition of plots - extract of B.Flemish code"""
        nx, ny, nz = dims
        Lx, Ly, Lz = self.phydims
        itime, time = ttime

        xgrid, zgrid = np.meshgrid(np.linspace(0 + self.offset[0], Lx + self.offset[0], nx + 1),
                                   np.linspace(0 + self.offset[1], Lz + self.offset[1], nz + 1), indexing='xy')

        for key, fig in figdict.items():
                ax = fig.add_subplot(3, 3, itime + 1)
                im = ax.pcolormesh(xgrid, zgrid,
                                   np.reshape(fn(key).to_numpy(), (nx, nz)).transpose(),
                                   shading='flat',
                                   cmap='coolwarm')
                ax.axis([self.x.min(), self.x.max(), self.z.min(), self.z.max()])
                ax.axis('scaled')
                fig.tight_layout()
                fig.colorbar(im, orientation='horizontal')
                ax.set_title(
                    '{:s} at t = {:1.0f} {:s}'.format(key, time / self.filename_converter, self.filename_marker))
