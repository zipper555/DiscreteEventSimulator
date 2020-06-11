from simstate import SimState
from systemstate import SystemState
from event import EventChain, CustomerArrival, SimulationTermination
from simresult import SimResult
from simparam import SimParam
from countercollection import CounterCollection
from rng import RNG, ExponentialRNS


class Simulation(object):

    def __init__(self, sim_param=SimParam(), no_seed=False):
        """
        Initialize the Simulation object.
        :param sim_param: is an optional SimParam object for parameter pre-configuration
        :param no_seed: is an optional parameter. If it is set to True, the RNG should be initialized without a
        a specific seed.
        """
        self.sim_param = sim_param
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        self.counter_collection = CounterCollection(self)
        if no_seed:
            self.rng = RNG(ExponentialRNS(1), ExponentialRNS(1./float(self.sim_param.RHO)))
        else:
            self.rng = RNG(ExponentialRNS(1, self.sim_param.SEED_IAT),
                           ExponentialRNS(1./float(self.sim_param.RHO), self.sim_param.SEED_ST))

    def reset(self):
        """
        Reset the Simulation object.
        """
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        self.counter_collection = CounterCollection(self)
        self.rng.iat_rns.set_parameters(1.)
        self.rng.st_rns.set_parameters(1./float(self.sim_param.RHO))

    def do_simulation(self):
        """
        Do one simulation run. Initialize simulation and create first and last event.
        After that, one after another event is processed.
        :return: SimResult object
        """
        # insert first and last event
        self.event_chain.insert(CustomerArrival(self, 0))
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sim_state.stop:

            # get next simevent from events
            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sim_state.now <= e.timestamp:
                    self.sim_state.now = e.timestamp
                    self.counter_collection.count_queue()
                    e.process()
                else:
                    print "NOW: " + str(self.sim_state.now) + ", EVENT TIMESTAMP: " + str(e.timestamp)
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print "Event chain is empty. Abort"
                self.sim_state.stop = True

        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result

    def do_simulation_n_limit(self, n, new_batch=False):
        """
        Call this function, if the simulation should stop after a given number of packets
        Do one simulation run. Initialize simulation and create first event.
        After that, one after another event is processed.
        :param n: number of customers, that are processed before the simulation stops
        :return: SimResult object
        """
        # insert first event only if no new batch has been started
        if not new_batch:
            self.event_chain.insert(CustomerArrival(self, 0))

        # start simulation (run)
        while not self.sim_state.stop:

            # get next simevent from events
            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sim_state.now <= e.timestamp:
                    self.sim_state.now = e.timestamp
                    self.counter_collection.count_queue()
                    e.process()

                    if self.sim_state.num_packets >= n:
                        self.sim_state.stop = True

                else:
                    print "NOW: " + str(self.sim_state.now) + ", EVENT TIMESTAMP: " + str(e.timestamp)
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print "Event chain is empty. Abort"
                self.sim_state.stop = True

        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result
