import math
import numpy
import scipy
import scipy.stats

class Counter(object):

    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print "Name: " + str(self.name) + ", Mean: " + str(self.get_mean()) + ", Variance: " + str(self.get_var())
        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):
    
    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """
    
    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)
    
    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])
        
    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        if len(self.values) > 0:
            return numpy.mean(self.values)
        else:
            return 0

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        return numpy.var(self.values, ddof=1)

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        return numpy.std(self.values, ddof=1)

    def report_confidence_interval(self, alpha=0.05, print_report=True):
        """
        Report a confidence interval with given significance level.
        This is done by using the t-table provided by scipy.
        :param alpha: is the significance level (default: 5%)
        :param print_report: enables an output string
        """
        n = len(self.values)
        mean = self.get_mean()
        var = self.get_var()
        h = math.sqrt(var/n)*scipy.stats.t.ppf(1-alpha/2., n-1)

        if print_report:
            print "Counter: " + str(self.name) + "; number of samples: " + str(n) + "; mean: " + str(mean) + "; var: " + str(var) + "; confidence interval: [" + str(mean-h) + " ; " + str(mean+h) + "] (h/2: " + str(h) + ")"

        return h

    def is_in_confidence_interval(self, x, alpha=0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        h = self.report_confidence_interval(alpha, print_report=False)
        m = self.get_mean()

        print "Value: " + str(x) + ", mean: " + str(m) + ", confidence interval: " + str(h)

        return math.fabs(m-x) <= h

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000, print_report=True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is done with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        n = len(self.values)
        mean = self.get_mean()
        var = self.get_var()

        means = []
        for i in range(resample_size):
            samples = numpy.random.choice(self.values, len(self.values), replace=True)
            means.append(numpy.mean(samples))

        # Percentile confidence intervals (option 1)
        lower_index, upper_index = int(alpha / 2 * resample_size), int(resample_size * (1 - alpha / 2))
        lower, upper = numpy.sort(means)[lower_index], numpy.sort(means)[upper_index]

        # Empirical confidence intervals (option 2)
        devs = numpy.subtract(means, mean)
        lower, upper = mean - numpy.sort(devs)[upper_index], mean - numpy.sort(means)[lower_index]

        if print_report:
            print "Counter: " + str(self.name) + "; number of samples: " + str(n) + "; mean: " + str(mean) + "; var: " + str(var) + "; confidence interval: [" + str(lower) + " ; " + str(upper) + "] "

        return lower, upper

    def is_in_bootstrap_confidence_interval(self, x, resample_size=5000, alpha=0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return:
        """
        (lower, upper) = self.report_bootstrap_confidence_interval(alpha, resample_size, print_report=False)
        m = self.get_mean()

        print "Value: " + str(x) + ", mean: " + str(m) + ", confidence interval: [" + str(lower) + " ; " + str(upper) + "]"
        return upper > x > lower


class TimeDependentCounter(Counter):
    
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """
    
    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.sum_power_two = [] #second moment used for variance calculation
    
    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """
        dt = self.sim.sim_state.now - self.last_timestamp
        if dt < 0:
            print "Error in calculating time dependent statistics. Current time is smaller than last timestamp."
            raise ValueError
        self.sum_power_two.append(value * value * dt)
        self.values.append(value * dt)
        self.last_timestamp = self.sim.sim_state.now
        
    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        return float(sum(self.values)) / float((self.last_timestamp - self.first_timestamp))
        
    def get_var(self):
        """
        Return the variance of the TDC.
        """
        dt = self.last_timestamp - self.first_timestamp
        return float(sum(self.sum_power_two)) / float(dt) - self.get_mean() * self.get_mean()
        
    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        return numpy.sqrt(self.get_var())
    
    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        self.sum_power_two = []
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):

    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        self.x = TimeIndependentCounter()
        self.y = TimeIndependentCounter()
        self.xy = TimeIndependentCounter()
        self.reset()

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        self.x.reset()
        self.y.reset()
        self.xy.reset()

    def count(self, x, y):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        self.x.count(x)
        self.y.count(y)
        self.xy.count(x*y)

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.

        Simple calculation with numpy:
        cov = numpy.cov(self.x.values, self.y.values, ddof=0)[0, 1]
        """
        return self.xy.get_mean() - self.x.get_mean() * self.y.get_mean()

    def get_cor(self):
        """
        Calculate the correlation coefficient between the two internal arrays x and y.

        Simple calculation with numpy:
        cor = numpy.corrcoef(self.x.values, self.y.values, ddof=0)[0, 1]
        """
        return self.get_cov() / math.sqrt(self.x.get_var() * self.y.get_var())

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print "Name: " + self.name + "; covariance = " + str(self.get_cov()) + "; correlation = " + str(self.get_cor())


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):

    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        self.max_lag = max_lag
        self.cycle_len = max_lag + 1
        self.first_samples = []
        self.last_samples = []
        self.squared_sums = []
        self.reset()

    def reset(self):
        """
        Reset the counter to its original state.
        """
        TimeIndependentCounter.reset(self)
        self.first_samples = numpy.zeros(self.cycle_len)
        self.last_samples = numpy.zeros(self.cycle_len)
        self.squared_sums = numpy.zeros(self.cycle_len)

    def count(self, x):
        """
        Add new element x to counter.
        """
        TimeIndependentCounter.count(self, x)
        n = len(self.values) - 1
        if n < self.cycle_len:
            self.first_samples[n] = x
        self.last_samples[n % self.cycle_len] = x

        for i in range(min(self.max_lag, n) + 1):
            squared_sums_i = self.squared_sums[i]
            index = (n - i + self.cycle_len) % self.cycle_len
            last_sample_i = self.last_samples[index]
            self.squared_sums[i] = squared_sums_i + x*last_sample_i

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.

        Note, that you can simplify this function significantly using numpy.roll(self.x, lag) and correlate the
        resulting array with your initial array (self.x). However this method is more efficient for large size arrays.

        :return: auto covariance
        """
        if lag <= self.max_lag:
            sum_of_firsts = 0
            sum_of_lasts = 0
            for i in range(lag):
                sum_of_firsts += self.first_samples[i]
                sum_of_lasts += self.last_samples[(len(self.values) - 1 - i + self.max_lag + 1) % (self.max_lag + 1)]
            return (self.squared_sums[lag] - self.get_mean() * (2 * numpy.sum(self.values) - sum_of_firsts - sum_of_lasts)) /  (len(self.values) - lag) + self.get_mean() * self.get_mean()
        else:
            print "lag larger than max_lag, please correct!"
            return -1

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation coefficient
        """
        if lag <= self.max_lag:
            var = self.get_var()
            if var != 0:
                return self.get_auto_cov(lag) / var
            else:
                raise ValueError("not applicable, variance == 0!")
        else:
            print "lag larger than max_lag, please correct!"
            return -1

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        self.max_lag = max_lag
        self.cycle_len = max_lag + 1
        self.reset()

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print "Name: " + self.name
        for i in range(0, self.max_lag+1):
            print "Lag = " + str(i) + "; covariance = " + str(self.get_auto_cov(i)) + "; correlation = " + str(self.get_auto_cor(i))