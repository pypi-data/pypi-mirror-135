# @Author:  Felix Kramer
# @Date:   2021-06-03T11:02:57+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:    Felix Kramer
# @Last modified time: 2021-08-30T23:39:32+02:00
# @License: MIT
import numpy as np
from hailhydro.flow_init import flow


def initialize_flux_on_circuit(circuit):

    flux_landscape = flux(circuit)

    return flux_landscape


class flux(flow, object):

    def __init__(self, circuit):
        super(flux, self).__init__(circuit)

        # incidence correlation
        self.dict_in = {}
        self.dict_out = {}
        self.dict_edges = {}

        # incidence indices
        self.dict_node_out = {}
        self.dict_node_in = {}

        self.initialize()

    def initialize(self):

        diff = self.circuit.scales['diffusion']
        L = self.circuit.scales['length']
        self.ref_vars = diff/L
        self.N = len(self.circuit.list_graph_nodes)
        self.M = len(self.circuit.list_graph_edges)
        self.circuit.nodes['concentration'] = np.zeros(self.N)

        sinks = self.find_sinks(self.circuit.G)
        roots = self.find_roots(self.circuit.G)

        self.sinks = sinks
        self.roots = roots
        self.nodes_sinks = [self.circuit.G.nodes[n]['label'] for n in sinks]
        self.nodes_roots = [self.circuit.G.nodes[n]['label'] for n in roots]

        self.idx_eff = [i for i in range(self.N) if i not in self.nodes_sinks]

        for i, n in enumerate(self.circuit.list_graph_nodes):
            self.dict_in[n] = []
            self.dict_out[n] = []
            self.dict_node_out[n] = np.where(self.B[i, :] > 0)[0]
            self.dict_node_in[n] = np.where(self.B[i, :] < 0)[0]

        for j, e in enumerate(self.circuit.list_graph_edges):

            alpha = e[1]
            omega = e[0]
            if self.B[alpha, j] > 0.:

                self.dict_edges[e] = [alpha, omega]
                self.dict_in[omega].append(alpha)
                self.dict_out[alpha].append(omega)

            elif self.B[alpha, j] < 0.:

                self.dict_edges[e] = [omega, alpha]
                self.dict_in[alpha].append(omega)
                self.dict_out[omega].append(alpha)

            else:
                print('and I say...whats going on? I say heyayayayayaaaaa...')

    def calc_diff_flux(self, R_sq):

        A = np.pi*R_sq*self.ref_vars

        return A

    def calc_velocity_from_flowrate(self, Q, R_sq):

        V = np.divide(Q, R_sq*np.pi)

        return V

    def calc_peclet(self, V):

        PE = V/self.ref_vars

        return PE
