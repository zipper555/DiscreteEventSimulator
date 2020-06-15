from simstate import SimState
from systemstate import SystemState
from event import EventChain, CustomerArrival, SimulationTermination
from simresult import SimResult
from simparam import SimParam
from countercollection import CounterCollection
from rng import RNG, ExponentialRNS, UniformRNS
from random import Random
import math
import numpy
from matplotlib import pyplot
from simulation import Simulation

"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""


def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    # TODO Task 3.2.1: Your code goes here
    exp_rns = ExponentialRNS(mean=1, the_seed=0)
    uni_rns = UniformRNS(low=2, high=3, the_seed=0)
    exp_list = []
    uni_list = []
    for i in range(100000):
        x = exp_rns.next()
        y = uni_rns.next()
        exp_list.append(x)
        uni_list.append(y)
    weights1 = numpy.full(len(exp_list), 1.0 / float(len(exp_list)))
    weights2 = numpy.full(len(uni_list), 1.0 / float(len(uni_list)))
    pyplot.hist(exp_list, bins=10, weights=weights1, histtype='bar')
    pyplot.xlabel("Exponential")
    pyplot.show()
    pyplot.hist(uni_list, bins=10, weights=weights2, histtype='bar')
    pyplot.xlabel("Uniform")
    pyplot.show()

    pass


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    sim = Simulation()
    sim.sim_param.SEED_IAT = 0
    sim.sim_param.SEED_ST = 1
    sim.sim_param.S = 5

    sim.sim_param.SIM_TIME = 100000
    print("100s Simulation:")
    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sys_util = sim.do_simulation().system_utilization
        print("p = {} System Utilization = {}".format(rho, sys_util))

    sim.sim_param.SIM_TIME = 1000000
    print("\n1000s Simulation:")
    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sys_util = sim.do_simulation().system_utilization
        print("p = {} System Utilization = {}".format(rho, sys_util))

    pass


if __name__ == '__main__':
    task_3_2_1()
    task_3_2_2()