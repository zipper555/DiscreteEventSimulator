import heapq
import random

class EventChain(object):

    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time.
    Always the oldest event is removed.
    """

    def __init__(self):
        """
        Initialize variables and event chain
        """
        self.event_list = []

    def insert(self, e):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent

        """
        heapq.heappush(self.event_list, e)

    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (and priority) from queue
        :return: next event in event chain
        """
        return heapq.heappop(self.event_list)


class SimEvent(object):

    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for EventChain insertion is implemented by comparing first the timestamps and then the priorities
    """

    def __init__(self, sim, timestamp):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        """
        self.timestamp = timestamp
        self.priority = 0
        self.sim = sim

    def process(self):
        """
        General event processing routine. Should be implemented in subclass
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, priorities are compared.
        """
        if self.timestamp != other.timestamp:
            return self.timestamp < other.timestamp
        elif self.priority != other.priority:
            return self.priority < other.priority
        else:
            return self.priority < other.priority


class CustomerArrival(SimEvent):

    """
    Defines a new customer arrival event (new packet comes into the system)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new customer arrival event with given execution time.

        Priority of customer arrival event is set to 1 (second highest)
        """
        super(CustomerArrival, self).__init__(sim, timestamp)
        self.priority = 1

    def process(self):
        """
        Processing procedure of a customer arrival.

        First, the next customer arrival event is created
        Second, the process tries to add the packet to the server, then to the queue, if necessary.
        If packet is added to the server, a service completion event is generated.
        Each customer is counted either as accepted or as dropped.
        """
        ev = CustomerArrival(self.sim, self.sim.sim_state.now + self.sim.rng.get_iat())
        self.sim.event_chain.insert(ev)

        if self.sim.system_state.add_packet_to_server():
            # packet is added to server and served
            ev = ServiceCompletion(
                self.sim, self.sim.sim_state.now + self.sim.rng.get_st())
            self.sim.event_chain.insert(ev)
            self.sim.sim_state.packet_accepted()

        else:
            if self.sim.system_state.add_packet_to_queue():
                # packet is added to queue
                self.sim.sim_state.packet_accepted()
            else:
                self.sim.sim_state.packet_dropped()


class ServiceCompletion(SimEvent):

    """
    Defines a service completion event (highest priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new service completion event with given execution time.

        Priority of service completion event is set to 0 (highest).
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.priority = 0

    def process(self):
        """
        Processing procedure of a service completion.

        First, the server is set from busy to idle.
        Then, if the queue is not empty, the next packet is taken from the queue and served,
        hence a new service completion event is created and inserted in the event chain.
        """
        self.sim.system_state.complete_service()
        if self.sim.system_state.start_service():
            # trigger next packet
            ev = ServiceCompletion(
                self.sim, self.sim.sim_state.now + self.sim.rng.get_st())
            self.sim.event_chain.insert(ev)


class SimulationTermination(SimEvent):

    """
    Defines the end of a simulation. (least priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.

        Priority of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.priority = 2

    def process(self):
        """
        Simulation stop flag is set to true, so simulation is stopped after this event.
        """
        self.sim.sim_state.stop = True