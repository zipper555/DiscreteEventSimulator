from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation
from matplotlib import pyplot

"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    autocorrelation_test_counter = TimeIndependentAutocorrelationCounter("test sequence", max_lag=1)

    print "First test series:"

    # Test first series:
    for _ in range(5000):
        autocorrelation_test_counter.count(1)
        autocorrelation_test_counter.count(-1)

    print "Mean = " + str(autocorrelation_test_counter.get_mean())
    print "Var = " + str(autocorrelation_test_counter.get_var())
    autocorrelation_test_counter.report()

    print "____________________________________________"
    print "Second test series:"
    autocorrelation_test_counter.reset()
    autocorrelation_test_counter.set_max_lag(2)

    # Test second series
    for _ in range(5000):
        autocorrelation_test_counter.count(1)
        autocorrelation_test_counter.count(1)
        autocorrelation_test_counter.count(-1)

    # print results
    print "Mean = " + str(autocorrelation_test_counter.get_mean())
    print "Var = " + str(autocorrelation_test_counter.get_var())

    autocorrelation_test_counter.report()


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    sim = Simulation()
    sim.sim_param.SIM_TIME = 10000000
    sim.sim_param.S = 10000
    for rho in [.01, .5, .8, .95]:
        sim.sim_param.RHO = rho
        sim.reset()
        print "_____________________________________________________"
        print "NEW RUN with rho=" + str(sim.sim_param.RHO)
        print "_____________________________________________________\n"
        sim.do_simulation()
        sim.counter_collection.report()


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    sim = Simulation()
    sim.sim_param.SIM_TIME = 10000000
    sim.sim_param.S = 10000
    plot_id = 1
    for rho in [.01, .5, .8, .95]:
        sim.sim_param.RHO = rho
        sim.reset()
        print "NEW RUN with rho=" + str(sim.sim_param.RHO)
        sim.do_simulation()

        iat = sim.counter_collection.cnt_iat_st.x.values
        service_time = sim.counter_collection.cnt_iat_st.y.values
        system_time = sim.counter_collection.cnt_iat_syst.y.values

        # Plot iat vs. service time
        pyplot.subplot("42%d" % plot_id)
        plot_id += 1
        pyplot.title(r"$\rho$=" + str(rho))

        pyplot.xlabel("inter-arrival time")
        pyplot.ylabel("service time")
        pyplot.scatter(iat, service_time, marker="+", color="red")

        # Plot service time vs. system time
        pyplot.subplot("42%d" % plot_id)
        plot_id += 1
        pyplot.title(r"$\rho$=" + str(rho))

        pyplot.xlabel("inter-arrival time")
        pyplot.ylabel("service time")
        pyplot.scatter(service_time, system_time, marker="+")

    pyplot.show()


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the blocking probability is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.DES and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    sim = Simulation()

    sim.sim_param.S = 10000

    n = 100
    for rho in [.01, .5, .8, .95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation_n_limit(n)

        lag = []
        cor = []

        for i in range(20):
            c = sim.counter_collection.acnt_wt.get_auto_cor(i+1)
            lag.append(i+1)
            cor.append(c)

        pyplot.subplot(121)
        pyplot.plot(lag, cor, "-o", label="rho = " + str(rho))

    pyplot.subplot(121)
    pyplot.xlabel("lag")
    pyplot.ylabel("autocorrelation")
    pyplot.legend(loc='upper right')
    pyplot.title("N=" + str(n))

    n = 10000
    for rho in [.01, .5, .8, .95]:
        sim.sim_param.RHO = rho
        sim.sim_param.SEED_IAT = 5
        sim.sim_param.SEED_ST = 0
        sim.reset()
        sim.do_simulation_n_limit(n)

        lag = []
        cor = []

        for i in range(20):
            c = sim.counter_collection.acnt_wt.get_auto_cor(i+1)
            lag.append(i+1)
            cor.append(c)

        pyplot.subplot(122)
        pyplot.plot(lag, cor, "-o", label="rho = " + str(rho))

    pyplot.subplot(122)
    pyplot.xlabel("lag")
    pyplot.ylabel("autocorrelation")
    pyplot.legend(loc='upper right')
    pyplot.title("N=" + str(n))
    pyplot.show()



if __name__ == '__main__':
    # task_4_2_1()
    # task_4_3_1()
    # task_4_3_2()
    task_4_3_2()