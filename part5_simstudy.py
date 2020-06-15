from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot

"""
This file should be used to keep all necessary code that is used for the simulation section in part 5
of the programming assignment. It contains tasks 5.2.1, 5.2.2, 5.2.3 and 5.2.4.
"""


def task_5_2_1():
    """
    Run task 5.2.1. Make multiple runs until the blocking probability distribution reaches
    a significance level alpha. Simulation is performed for 100s and 1000s and for alpha = 10% and 5%.
    """
    sim = Simulation()

    # set parameters
    sim.sim_param.RHO = .9
    sim.reset()
    sim.sim_param.EPSILON = .0015
    sim.sim_param.S = 4

    # simulate
    results = []
    for sim_time in [100, 1000]:
        sim.sim_param.SIM_TIME = sim_time * 1000
        for alpha in [.1, .05]:
            sim.sim_param.ALPHA = alpha
            counter = TimeIndependentCounter("Blocking Probability")
            counter.reset()
            tmp = 1.0
            while len(counter.values) < 5 or tmp > sim.sim_param.EPSILON:
                sim.reset()
                sim_result = sim.do_simulation()
                bp = sim_result.blocking_probability
                counter.count(bp)
                tmp = counter.report_confidence_interval(alpha=sim.sim_param.ALPHA, print_report=False)
            results.append(len(counter.values))
            counter.report_confidence_interval(alpha=sim.sim_param.ALPHA, print_report=True)

    # print and return results
    print "SIM TIME:  100s; ALPHA: 10%; NUMBER OF RUNS: " + str(results[0]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]*100)
    print "SIM TIME:  100s; ALPHA:  5%; NUMBER OF RUNS: " + str(results[1]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]*100)
    print "SIM TIME: 1000s; ALPHA: 10%; NUMBER OF RUNS:  " + str(results[2]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]*1000)
    print "SIM TIME: 1000s; ALPHA:  5%; NUMBER OF RUNS:  " + str(results[3]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]*1000)
    return results


def task_5_2_2():
    """
    Run simulation in batches. Start the simulation with running until a customer count of n=100 or (n=1000) and
    continue to increase the number of customers by dn=n.
    Count the blocking probability for the batch and calculate the significance interval width of all values, that have
    been counted until now.
    Do this until the desired confidence level is reached and print out the simulation time as well as the number of
    batches.
    """
    sim = Simulation()

    # set parameters
    sim.sim_param.RHO = .9
    sim.sim_param.EPSILON = .0015
    sim.sim_param.S = 4

    results = []

    for batch_packets in [100, 1000]:
        for alpha in [.1, .05]:
            dn = batch_packets
            n = dn
            sim.sim_param.ALPHA = alpha
            counter = TimeIndependentCounter("Blocking Probability")
            counter.reset()
            confid_level_reached = False
            sim.reset()

            # execute simulation
            while not confid_level_reached:
                r = sim.do_simulation_n_limit(dn, new_batch=(n != dn))
                counter.count(r.blocking_probability)
                if len(counter.values) > 5 and counter.report_confidence_interval(sim.sim_param.ALPHA,
                                                                                  print_report=False) < sim.sim_param.EPSILON:
                    confid_level_reached = True
                else:
                    n += dn
                    sim.counter_collection.reset()
                    sim.sim_state.num_blocked_packets = 0
                    sim.sim_state.num_packets = 0
                    sim.sim_state.stop = False

            counter.report_confidence_interval(sim.sim_param.ALPHA, print_report=True)
            print "Number of batches (n=" + str(dn) + " for blocking probability confidence): " + str(n / dn) + \
                  "; simulation time: " + str(int(sim.sim_state.now / 1000)) + "s."

            results.append(sim.sim_state.now)

    # print and return results
    print "BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]/1000)
    print "BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]/1000)
    print "BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]/1000)
    print "BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]/1000)

    return results


def task_5_2_4():
    """
    Plot confidence interval as described in the task description given below.
    Use an M/M/1 system and perform multiple runs simulation. Make your study for system offered traffic 0.5 and 0.9.
    Use confidence levels of 0.9 and 0.95. Use 100 s and 1000 s as simulation time. Calculate the confidence interval
    for the system throughput of 30 runs. Repeat this 100 times.
    """
    sim = Simulation()
    sim.sim_param.S = 10000

    for sys_util in [.5, .9]:
        sim.sim_param.RHO = sys_util
        sim.reset()
        for alpha in [.1, .05]:
            sim.sim_param.ALPHA = alpha
            for time in [100, 1000]:
                sim.sim_param.SIM_TIME = time * 1000

                sys_util_counter = TimeIndependentCounter("su")
                mean_counter = TimeIndependentCounter("mc")
                y_min = []
                y_max = []
                x = []

                pyplot.hold(True)

                for run in range(100):
                    sys_util_counter.reset()
                    for _ in range(30):
                        sim.reset()
                        sim_result = sim.do_simulation()
                        su = sim_result.system_utilization
                        sys_util_counter.count(su)
                    h = sys_util_counter.report_confidence_interval(alpha=sim.sim_param.ALPHA, print_report=False)
                    m = sys_util_counter.get_mean()
                    mean_counter.count(m)
                    y_min.append(m - h)
                    y_max.append(m + h)
                    x.append(run + 1)

                mean_calc = sim.sim_param.RHO
                mean_real = mean_counter.get_mean()
                total = len(x)
                good = 0
                good_real = 0
                for i in range(len(x)):
                    if y_min[i] <= mean_calc <= y_max[i]:
                        good += 1
                    if y_min[i] <= mean_real <= y_max[i]:
                        good_real += 1
                print str(good) + "/" + str(total) + " cover theoretical mean, " + str(good_real) + "/" + str(
                    total) + " cover sample mean."

                if alpha == .1:
                    if time == 100:
                        pyplot.subplot(221)
                    else:
                        pyplot.subplot(223)
                else:
                    if time == 100:
                        pyplot.subplot(222)
                    else:
                        pyplot.subplot(224)
                plot_confidence(sim, x, y_min, y_max, mean_counter.get_mean(), sim.sim_param.RHO, "system utilization")

        pyplot.hold(False)
        pyplot.show()


def plot_confidence(sim, x, y_min, y_max, calc_mean, act_mean, ylabel):
    """
    Plot confidence levels in batches. Inputs are given as follows:
    :param sim: simulation, the measurement object belongs to.
    :param x: defines the batch ids (should be an array).
    :param y_min: defines the corresponding lower bound of the confidence interval.
    :param y_max: defines the corresponding upper bound of the confidence interval.
    :param calc_mean: is the mean calculated from the samples.
    :param act_mean: is the analytic mean (calculated from the simulation parameters).
    :param ylabel: is the y-label of the plot
    :return:
    """
    pyplot.vlines(x, y_min, y_max, colors='b', linestyles='solid')
    pyplot.hlines(act_mean, 0, x[len(x) - 1], colors='g', linestyles='-.', label='rho')
    pyplot.hlines(calc_mean, 0, x[len(x) - 1], colors='r', linestyles='-.', label='sample mean')
    pyplot.xlabel("sample id")
    pyplot.ylabel(ylabel)
    pyplot.ylim([sim.sim_param.RHO - .1, sim.sim_param.RHO + .1])
    pyplot.xlim([0, 100])
    pyplot.title(
        "SIM_TIME = " + str(sim.sim_param.SIM_TIME / 1000) + "s, ALPHA = " + str(100 * sim.sim_param.ALPHA) +
        "%, RHO = " + str(sim.sim_param.RHO))
    pyplot.legend(loc='lower right')


if __name__ == '__main__':
    task_5_2_1()
    # task_5_2_2()
    # task_5_2_4()