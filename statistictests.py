import numpy
from scipy import stats

class ChiSquare(object):

    def __init__(self, emp_x, emp_n, name="default"):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param name: name for better distinction of tests
        """
        self.name = name
        # TODO Task 6.1.1: Your code goes here
        self.bins = emp_x
        self.values = emp_n
        pass

    def test_distribution(self, alpha, mean, var):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance of test
        :param mean: mean value of the gaussian distribution
        :param var: variance of the gaussian distribution
        """
        # TODO Task 6.1.1: Your code goes here
        chi2 = 0
        exp_temp = 0
        obs_temp = 0
        sigma = numpy.sqrt(var)
        n = len(self.bins) - 1
        exp_val1 = numpy.random.normal(mean, sigma, 100)
        exp_val, _ = numpy.histogram(exp_val1, bins=self.bins)

        for obs, exp in zip(self.values, exp_val):
            if exp < 5 or exp_temp>0:
                exp_temp += exp
                obs_temp += obs
                if exp_temp < 5:
                    continue
                else:
                    exp_fin = exp_temp
                    obs_fin = obs
                    exp_temp = 0
                    obs_temp = 0
            else:
                exp_fin = exp
                obs_fin = obs
            chi2 += numpy.square(float(obs_fin - exp_fin))/ float(exp_fin)
        
        chi2_table = stats.chi2.ppf(alpha, n)
        #chi2, chi2_table = stats.chisquare(self.values, f_exp=exp_val)
        #print "chi2: " + str(chi2) + "chi2_table: " + str(chi2_table)
        return chi2, chi2_table
        
        pass