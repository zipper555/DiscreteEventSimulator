from finitequeue import FiniteQueue
from packet import Packet


class SystemState(object):
    
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the queue (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        """
        self.buffer = FiniteQueue(sim)
        self.server_busy = False
        self.served_packet = None
        self.sim = sim
        self.last_arrival = 0

    def add_packet_to_server(self):
        """
        Try to add a packet to the server unit.
        :return: True if server is not busy and packet has been added successfully.
        """
        if self.server_busy:
            return False
        else:
            self.server_busy = True
            self.served_packet = Packet(self.sim, self.sim.sim_state.now - self.last_arrival)
            self.last_arrival = self.sim.sim_state.now
            self.served_packet.start_service()
            return True

    def add_packet_to_queue(self):
        """
        Try to add a packet to the buffer.
        :return: True if buffer/queue is not full and packet has been added successfully.
        """
        if self.buffer.add(Packet(self.sim, self.sim.sim_state.now - self.last_arrival)):
            self.last_arrival = self.sim.sim_state.now
            return True
        else:
            self.last_arrival = self.sim.sim_state.now
            return False

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        self.server_busy = False
        p = self.served_packet
        p.complete_service()
        self.sim.counter_collection.count_packet(p)
        self.served_packet = None
        return p

    def start_service(self):
        """
        If the buffer is not empty, take the next packet from there and serve it.
        :return: True if buffer is not empty and a stored packet is being served.
        """
        if self.buffer.is_empty():
            return False
        else:
            self.served_packet = self.buffer.remove()
            self.served_packet.start_service()
            self.server_busy = True
            return True

    def get_queue_length(self):
        """
        Return the current buffer content.
        :return: Fill status of the buffer
        """
        return self.buffer.get_queue_length()
