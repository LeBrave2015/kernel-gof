"""
Module for testing goftest module.
"""

__author__ = 'wittawat'

import numpy as np
import matplotlib.pyplot as plt
import kgof.data as data
import kgof.density as density
import kgof.util as util
import kgof.kernel as kernel
import kgof.goftest as gof
import kgof.glo as glo
import scipy.stats as stats

import unittest


class TestFSSD(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        """
        Nothing special. Just test basic things.
        """
        seed = 12
        # sample
        n = 100
        alpha = 0.01
        for d in [1, 4]:
            mean = np.zeros(d)
            variance = 1
            isonorm = density.IsotropicNormal(mean, variance)

            # only one dimension of the mean is shifted
            #draw_mean = mean + np.hstack((1, np.zeros(d-1)))
            draw_mean = mean +0
            draw_variance = variance + 1
            X = util.randn(n, d, seed=seed)*np.sqrt(draw_variance) + draw_mean
            dat = data.Data(X)

            # Test
            for J in [1, 3]:
                sig2 = util.meddistance(X, subsample=1000)**2
                k = kernel.KGauss(sig2)

                # random test locations
                V = util.fit_gaussian_draw(X, J, seed=seed+1)
                null_sim = gof.FSSDH0SimCovObs(n_simulate=200, seed=3)
                fssd = gof.FSSD(isonorm, k, V, null_sim=null_sim, alpha=alpha)

                tresult = fssd.perform_test(dat, return_simulated_stats=True)

                # assertions
                self.assertGreaterEqual(tresult['pvalue'], 0)
                self.assertLessEqual(tresult['pvalue'], 1)

    def test_ustat_h1_mean_variance(self):
        seed = 20
        # sample
        n = 200
        alpha = 0.01
        for d in [1, 4]:
            mean = np.zeros(d)
            variance = 1
            isonorm = density.IsotropicNormal(mean, variance)

            draw_mean = mean + 2
            draw_variance = variance + 1
            X = util.randn(n, d, seed=seed)*np.sqrt(draw_variance) + draw_mean
            dat = data.Data(X)

            # Test
            for J in [1, 3]:
                sig2 = util.meddistance(X, subsample=1000)**2
                k = kernel.KGauss(sig2)

                # random test locations
                V = util.fit_gaussian_draw(X, J, seed=seed+1)

                null_sim = gof.FSSDH0SimCovObs(n_simulate=200, seed=3)
                fssd = gof.FSSD(isonorm, k, V, null_sim=null_sim, alpha=alpha)
                fea_tensor = fssd.feature_tensor(X)

                u_mean, u_variance = gof.FSSD.ustat_h1_mean_variance(fea_tensor)

                # assertions
                self.assertGreaterEqual(u_variance, 0)
                # should reject H0
                self.assertGreaterEqual(u_mean, 0)

    def tearDown(self):
        pass


if __name__ == '__main__':
   unittest.main()

