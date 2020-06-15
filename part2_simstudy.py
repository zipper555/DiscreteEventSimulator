from simparam import SimParam
from simulation import Simulation
import random
import numpy
from matplotlib import pyplot

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""

def task_2_7_1():
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want).
    """
    # TODO Task 2.7.1: Your code goes here
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    
    do_simulation_study(sim)
    pass

def task_2_7_2():
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    # TODO Task 2.7.2: Your code goes here or in the function above
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    sim.sim_param.SIM_TIME = 1000000
    
    do_simulation_study(sim)
    pass


def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """
    # TODO Task 2.7.1: Your code goes here
    sim_time = sim.sim_param.SIM_TIME
    for qlengths in [5, 6, 7]:
        avg_qlen = []
        avg_wt = []
        for simulation_iter in range(1, sim.sim_param.NO_OF_RUNS):
            sim.reset()
            sim.sim_param.SIM_TIME = sim_time
            sim.sim_param.S = qlengths
            sim.do_simulation()
            wtavg = sim.counter_collection.cnt_wt.get_mean()
            qlavg = sim.counter_collection.cnt_ql.get_mean()
            avg_wt.append(wtavg)
            avg_qlen.append(qlavg)
            print("Trial {} complete - mean wt and ql = {}, {}".format(simulation_iter, wtavg, qlavg))
            sim.counter_collection.report()
        #Plot histograms
        histogram1, bins1 = numpy.histogram(avg_qlen, bins = 7)
        histogram2, bins2 = numpy.histogram(avg_wt, bins = 7)
        weights1 = numpy.full(len(avg_qlen), 1.0 / float(len(avg_qlen)))
        weights2 = numpy.full(len(avg_wt), 1.0 / float(len(avg_wt)))
        
        if qlengths == 5:  
            rwidth = 0.40
            position = 'left'
        elif qlengths == 6:
            rwidth = 0.33
            position = 'mid'
        else:
            rwidth = 0.2
            position = 'right'
       
        pyplot.subplot(211)
        pyplot.legend(loc='upper right')
        pyplot.hist(avg_qlen, bins1, alpha=0.5, label='Qlen for S='+str(sim.sim_param.S), rwidth=rwidth, weights=weights1, histtype='bar', align=position)
        #pyplot.xlabel('Queue Length')
        #pyplot.show()
        pyplot.subplot(212)
        pyplot.legend(loc='upper right')
        pyplot.hist(avg_wt, bins2, alpha=0.5, label='WT for S='+str(sim.sim_param.S), rwidth=rwidth, weights=weights2, histtype='bar', align=position)
        #pyplot.xlabel('Waiting Time')
    pyplot.show()
        
    # TODO Task 2.7.2: Your code goes here
    pass


if __name__ == '__main__':
    task_2_7_1()
    task_2_7_2()
