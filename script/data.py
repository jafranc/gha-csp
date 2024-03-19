from abc import ABCMeta, abstractmethod

import numpy as np
import logging


class Conversion:
    # sched in sec
    SEC2SEC = 1
    SEC2MIN = 60
    SEC2HOUR = 60 * SEC2MIN
    SEC2DAY = 24 * 60 * SEC2MIN
    SEC2YEAR = 3.1536E7
    SEC2TENTHOFYEAR = 3.1536E6

    KG2KG = 1
    KG2G = 1e-3
    KG2T = 1e3

    PA2PA = 1
    PA2BAR = 1e5

    CO2MOL2KG = 44.01e-3

    K2C = 273.15


class Data(metaclass=ABCMeta):
    def __init__(self, version, suffix):
        self.version = version[0]
        self.suffix = suffix[0]
        self.seal_facies_tag = "reservoir1"
        self.data_sets = {}

        logging.basicConfig(filename='spe11-pt.log', encoding='utf-8', level=logging.INFO)
        logging.info('Init')

        # default is a
        # self.schedule = np.arange(0, 5 * Conversion.SEC2DAY, 0.5 * Conversion.SEC2DAY)
        self.schedule = np.asarray([ time * Conversion.SEC2HOUR for time in [0,20,40,60,80,100] ])
        # for GEOS
        self.name_indirection = {'pressure': 'pres',
                                 'phaseVolumeFraction_0': 'satg',
                                 'phaseVolumeFraction_1': 'satw',
                                 'fluid_phaseCompFraction_2': 'mCO2',
                                 'fluid_phaseCompFraction_1': 'mH2O',
                                 'fluid_phaseDensity_0': 'rG',
                                 'fluid_phaseDensity_1': 'rL',
                                 'rockPorosity_porosity': 'poro',
                                 'elementVolume': 'vol',
                                 'phaseMobility_0': 'krg',
                                 'phaseMobility_1': 'krw'}

        # for everyone
        if version[0] in ['b', 'c']:
            # as described
            self.name_indirection['temperature'] = 'temp'

    # def _process_solubility_(self, path):
    #     import pandas as pd
    #     df = pd.read_csv(path)
    #     logging.info(f'Importing solubility {path}')
    #     p = df['pressure [Pa]'].to_numpy()
    #     T = np.arange(283, 345.5, 2.5)
    #     # note that solubility there is in molCo2/kgBrine
    #     S = df.to_numpy()[:, 1:].transpose()
    #     # convert to kgCO2/kgBrine
    #     S = S * Conversion.CO2MOL2KG
    #     p, T = np.meshgrid(p, T)
    #     return self._get_lambda_2_((p.flatten(), T.flatten()), S.flatten())

    @abstractmethod
    def process(self, odir, idir):
        """ god function to trigger processing """