from simparam import SimParam
from simulation import Simulation
import random


"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""

def task_1_7_1():
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_2():
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    sim = Simulation(sim_param)
    return do_simulation_study(sim)

def task_1_7_3():
    """
    Execute task 1.7.3.
    """
    # TODO Task 1.7.3: Your code goes here (if necessary)
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    init_simulation_time = 100000000
    for iter in range(1,5):
        sim.reset()
        sim_param.SIM_TIME = init_simulation_time * iter
        sim.sim_param.S = 2
        sim_param.MAX_DROPPED = 10000000
        sim_res = sim.do_simulation()
        print("pkdrp = {} and pktot = {}".format(sim_res.packets_dropped, sim_res.packets_total))
        block_pr = float (sim_res.packets_dropped/sim_res.packets_total)
        #Plot using sim_param.SIM_TIME and block_pr

def do_simulation_study(sim):
    """
    Implement according to task description.
    """
    # TODO Task 1.7.1: Your code goes here
    #Start with minimum queue length and iterate
    qlen = sim.sim_param.S_MIN
    success_count = 0 # Indicates if numbner of dropped packets is within the limit

    while True:
        for simulate_count in range (1,sim.sim_param.NO_OF_RUNS): #Fix up number of simulations
            sim.reset()
            sim.sim_param.S = qlen
            pktdrp = sim.do_simulation().packets_dropped
            #print("qlen = {} packets dropped = {}".format(qlen, pktdrp))
            if pktdrp < sim.sim_param.MAX_DROPPED:
                success_count += 1
        #print("qlen = {} success count = {}".format(qlen, success_count))      
        if (success_count >= 0.8 * sim.sim_param.NO_OF_RUNS):
            break
        else: 
            qlen += 1
    print("Returning {}".format(sim.sim_param.S))
    return sim.sim_param.S


if __name__ == '__main__':
    task_1_7_1()
    task_1_7_2()
    task_1_7_3()

