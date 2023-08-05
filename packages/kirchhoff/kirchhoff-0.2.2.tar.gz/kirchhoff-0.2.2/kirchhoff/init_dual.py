# @Author:  Felix Kramer
# @Date:   2021-05-23T15:58:07+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:    Felix Kramer
# @Last modified time: 2021-11-07T15:47:40+01:00
# @License: MIT

import networkx as nx
import numpy as np
import kirchhoff.init_crystal
from scipy.spatial import Voronoi
import kirchhoff.init_crystal  as init_crystal


def init_dual_minsurf_graphs(dual_type, num_periods):

    """
    Initialize a dual spatially embedded multilayer graph, with internal graphs based on
     the network skeletons of triply-periodic minimal surfaces.

    Args:
        dual_type (string): The type of dual skeleton (simple, diamond, laves, catenation).
        num_periods (int): Repetition number of the lattice's unit cell.

    Returns:
        networkx_dual: A dual networkx object.

    """

    plexus_mode = {
        'simple': networkx_dual_simple,
        'diamond':networkx_dual_diamond,
        'laves':networkx_dual_laves,
    }

    if  dual_type in plexus_mode:
        dual_graph = plexus_mode[dual_type](num_periods)

    else:
        print('Warning: Invalid graph mode, choose default')
        dual_graph = plexus_mode['default'](num_periods)

    return dual_graph

def init_dual_catenation(dual_type, num_periods):

    """
    Initialize a dual spatially embedded multilayer graph, with internal graphs based on
    simple catenated network skeletons.

    Args:
        dual_type (string): The type of dual skeleton (simple, diamond, laves, catenation).
        num_periods (int): Repetition number of the lattice's unit cell.

    Returns:
        networkx_dual: A dual networkx object.

    """
    plexus_mode={
        'catenation':networkx_dual_catenation,
        'crossMesh':networkx_dual_crossMesh,
    }

    if  dual_type in plexus_mode:
        dual_graph = plexus_mode[dual_type](num_periods)
    else:
        print('Warning: Invalid graph mode, choose default')
        dual_graph = plexus_mode['default'](num_periods)

    return dual_graph

class networkx_dual(init_crystal.networkx_crystal, object):

    """
    A base class for spatial, dual circuits.

    Attributes
    ----------
        layer (list): List of the graphs contained in the multilayer network.
        lattice_constant (float): Scale for the spacing between the networks.
        translation_length (float): Scale for the translation difference between the multiple networks.

    """
    def __init__(self):

        """
        A constructor for multilayer circuit objects, setting default values
         for the interal graph objects and geometry
        """

        super(networkx_dual, self).__init__()
        self.layer = [nx.Graph(), nx.Graph()]
        self.lattice_constant = 1
        self.translation_length = 1

    def periodic_cell_structure_offset(self, cell, num_periods, offset):

        """
        Repeat the unit cell with translational offset to create a graph.

        Args:
            cell (nx.Graph): unit cell in networkx graph format.
            num_periods (int): Repetition number for the unit cells.
            offset (ndarray): A translational offset for the lattice.

        Returns:
            nx.Graph: A simple, periodic Graph.

        """

        L = nx.Graph()
        periods = range(num_periods)
        for i in periods:
            for j in periods:
                for k in periods:
                    if (i+j+k) %2 == 0:
                        v = self.translation_length*np.array([i, j, k])
                        TD = self.lattice_translation(offset+v, cell)
                        L.add_nodes_from(TD.nodes(data=True))

        return L

    def prune_leaves(self, G, H, adj):

        """
        Remove non-affiliated edges in dual graphs.

        Args:
            G(nx.Graph): A networkx graph.
            H (nx.Graph): A networkx graph.
            adj (list): A list of affiliated edge pairs of the two graphs.

        Returns:
            list: A list of networkx graphs.

        """

        K = [G, H]
        for i in range(2):

            adj_x = np.array(adj)[:, i]
            list_e = list(K[i].edges())
            for e in list_e:
                if np.any( np.array(adj_x) == K[i].edges[e]['label']):
                    continue
                else:
                    K[i].remove_edge(*e)

            list_n = list(K[i].nodes())
            for n in list_n:
                if not K[i].degree(n) > 0:
                    K[i].remove_node(n)

        return K[0], K[1]

    def relabel_networkx(self, G1, G2, adj):

        """
        Relabel affiliations and graph attributes.

        Args:
            G(nx.Graph): A networkx graph.
            H (nx.Graph): A networkx graph.
            adj (list): A list of affiliated edge pairs of the two graphs.

        Returns:
            list: A list of networkx graphs.

        """
        K = [G1, G2]
        aff = [{}, {}]
        e_adj = []
        e_adj_idx = []
        P = [nx.Graph(), nx.Graph()]
        dict_P = [[{}, {}, {}], [{}, {}, {}]]

        for i in range(2):

            for idx_n, n in enumerate(K[i].nodes()):
                opt = {
                'pos': K[i].nodes[n]['pos'],
                'label': K[i].nodes[n]['label']
                }
                P[i].add_node(idx_n, **opt)
                dict_P[i][0].update({n: idx_n})
                aff[i][idx_n] = []

            for idx_e, e in enumerate(K[i].edges()):
                opt = {
                'slope': [K[i].nodes[e[0]]['pos'], K[i].nodes[e[1]]['pos']],
                'label': K[i].edges[e]['label']
                }
                v, u = dict_P[i][0][e[0]], dict_P[i][0][e[1]]

                P[i].add_edge(v, u, **opt)

            for j, e in enumerate(P[i].edges()):
                dict_P[i][1].update({P[i].edges[e]['label']:j})
                dict_P[i][2].update({P[i].edges[e]['label']:e})

        for a in adj:

            e = [dict_P[0][1][a[0]], dict_P[1][1][a[1]]]
            E = [dict_P[0][2][a[0]], dict_P[1][2][a[1]]]
            e_adj.append([e[0], e[1]])
            e_adj_idx.append([E[0], E[1]])

            for i in range(2):
                n0 = E[i][0]
                n1 = E[i][1]
                aff[i][n0].append(a[-(i+1)])
                aff[i][n1].append(a[-(i+1)])

        for i in range(2):

            for key in aff[i].keys():
                aff[i][key] = list(set(aff[i][key]))
                aux = []
                for l in aff[i][key]:
                    aux.append(dict_P[-(i+1)][1][l])
                aff[i][key] = aux

        self.e_adj = e_adj
        self.e_adj_idx = e_adj_idx
        self.n_adj = [aff[0], aff[1]]

        return P

    def set_graph_adjacency(self, G, H):

        """
        Relabel affiliations and graph attributes.

        Args:
            G (nx.Graph): The inner networkx graph.
            H (nx.Graph): The outer networkx graph.

        Returns:
            list:  A list of affiliated edge pairs of the two graphs.

        """
        adj = []

        for i, e in enumerate(G.edges()):
            a = np.add(G.edges[e]['slope'][0], G.edges[e]['slope'][1])
            for j, f in enumerate(H.edges()):
                b = np.add(H.edges[f]['slope'][0], H.edges[f]['slope'][1])
                c = np.subtract(a, b)
                if np.dot(c, c) == 14.:
                    adj.append([G.edges[e]['label'], H.edges[f]['label']])

        return adj

class networkx_dual_simple(networkx_dual, object):
    """
    A class for spatial, dual cubic circuits.

    Attributes
    ----------

        layer (list): List of the mutlilayered circuits.
        lattice_constant (float): Scale for the spacing between the networks.
        translation_length (float): Scale for the translation difference between the multiple networks.

    """
    def __init__(self, num_periods):

        """
        A constructor for multilayer circuit simple objects, setting default
         values for the interal graph objects and geometry
        """

        super(networkx_dual_simple, self).__init__()
        self.lattice_constant = 1
        self.translation_length = 1
        self.dual_simple(num_periods)

    def dual_simple(self, num_periods):

        """
        Set internal networks structure, dual cubic.

        Args:
            num_periods (int): A networkx graph.

        """

        # create primary point cloud with lattice structure
        # creating voronoi cells, with defined ridge structure
        ic = init_crystal.networkx_simple(1)
        unit_cell = ic.simple_unit_cell()
        self.periodic_cell_structure(unit_cell,num_periods)
        points = [self.G.nodes[n]['pos'] for i, n in enumerate(self.G.nodes())]
        V = Voronoi(points)

        # construct caged networks from given point clouds, with corresponding
         # adjacency list of edges
        G1, G2=self.init_graph_nuclei(V)

        adj = self.set_graph_adjacency(V, G1, G2)

        # cut off redundant (non-connected or neigborless) points/edges
        G1, G2 = self.prune_leaves(G1, G2, adj)

        # relabeling network nodes/edges & adjacency-list
        P = self.relabel_networkx(G1, G2, adj)

        self.layer = [P[0], P[1]]

    def init_graph_nuclei(self, V):

        """
        Generate points for a cubic lattice and its dual via Voronois
         tesselation and return dual graph representations.

        Args:
            Voronoi (scipy.spatial.Voronoi): A Tesselation object.

        Return:
            nx.Graph: Inner networkx graph.
            nx.Graph: Outer networkx graph.

        """
        H = nx.Graph()
        G = nx.Graph()
        list_p = np.array(list(V.points))
        list_v = np.array(list(V.vertices))

        counter_n = 0
        for j, v in enumerate(list_v):
            H.add_node(j, pos=v, label=counter_n)
            counter_n += 1

        counter_n = 0
        for j,p in enumerate(list_p):
            G.add_node(j, pos=p, label=counter_n)
            counter_n+=1

        counter_e = 0
        for i, n in enumerate(list_p[:-1]):
            for j, m in enumerate(list_p[(i+1):]):
                dist = np.linalg.norm(n-m)
                if dist == self.lattice_constant:
                    G.add_edge(i, (i+1)+j, slope=(n, m), label=counter_e)
                    counter_e += 1

        return G, H

    def set_graph_adjacency(self, V, G, H):

        """
        Return the affiliation list of two dual cubic lattices.

        Args:
            Voronoi (scipy.spatial.Voronoi): A Voronoi-Tesselation object.
            G (nx.Graph): The inner networkx graph.
            H (nx.Graph): The outer networkx graph.

        Return:
            list: The edge affiliation list of the dual cubic lattice.

        """
        rv_aux = []
        rp_aux = []
        adj = []

        list_p = np.array(list(V.points))
        for rv, rp in zip(V.ridge_vertices, V.ridge_points):
            if np.any(np.array(rv) == -1):
                continue
            else:
                rv_aux.append(rv)
                rp_aux.append(rp)

        counter_e = 0

        for i, rv in enumerate(rv_aux):
            E1 = (rp_aux[i][0], rp_aux[i][1])
            for j, v in enumerate(rv):
                e1 = rv[-1+j]
                e2 = rv[-1+(j+1)]
                E2 = (e1, e2)

                if not H.has_edge(*E2):
                    options = {
                    'slope': (V.vertices[e1], V.vertices[e2]),
                    'label': counter_e
                    }
                    H.add_edge(*E2, **options)
                    counter_e += 1
                if G.has_edge(*E1):
                    adj.append([G.edges[E1]['label'], H.edges[E2]['label']])

        return adj

class networkx_dual_diamond(networkx_dual, object):

    """
    A class for spatial, dual diamond circuits.

    Attributes
    ----------

        layer (list): List of the mutlilayered circuits.
        lattice_constant (float): Scale for the spacing between the networks.
        translation_length (float): Scale for the translation difference between the multiple networks.

    """
    def __init__(self, num_periods):

        """
        A constructor for multilayer circuit diamond objects, setting default values
         for the interal graph objects and geometry
        """

        super(networkx_dual_diamond, self).__init__()
        self.lattice_constant = np.sqrt(3.)/2.
        self.translation_length = 1
        self.dual_diamond(num_periods)

    def dual_diamond(self, num_periods):

        """
        Set internal networks structure, dual diamond.

        Args:
            num_periods (int): Repetition number of the unit cells.

        """

        # create primary point cloud with lattice structure
        adj = []
        adj_idx = []
        aff = [{}, {}]

        ic = init_crystal.networkx_diamond(1)
        unit_cell = ic.diamond_unit_cell()

        pg = [0, 0, 0]
        G_aux = self.periodic_cell_structure_offset(unit_cell, num_periods, pg)

        hg = [1, 0, 0]
        H_aux = self.periodic_cell_structure_offset(unit_cell, num_periods, hg)

        G1, G2 = self.init_graph_nuclei(G_aux, H_aux)

        adj = self.set_graph_adjacency(G1, G2)

        # cut off redundant (non-connected or neigborless) points/edges
        G1, G2=self.prune_leaves(G1, G2, adj)

        # relabeling network nodes/edges & adjacency-list
        P = self.relabel_networkx(G1, G2, adj)

        self.layer = [P[0], P[1]]

    def init_graph_nuclei(self, G_aux, H_aux):
        """
        Generate points for a diamond lattice and its dual via copy+translation
         and return dual graph representations.

        Args:
            G_aux (nx.Graph): Inner networkx graph.
            H_aux (nx.Graph): Outer networkx graph.

        Returns:
            nx.Graph: Inner networkx graph.
            nx.Graph: Outer networkx graph.

        """

        G = self.init_graph(G_aux)
        H = self.init_graph(H_aux)

        return G, H

    def init_graph(self, G_aux):

        """
        Generate points for a diamond lattice return dual graph representations.

        Args:
            G_aux (nx.Graph): A networkx graph.

        Returns:
            nx.Graph: A networkx graph.

        """

        G = nx.Graph()
        points_G = [G_aux.nodes[n]['pos'] for i, n in enumerate(G_aux.nodes())]
        counter_e = 0
        counter_n = 0

        for i, n in enumerate(G_aux.nodes()):
            G.add_node(i, pos=G_aux.nodes[n]['pos'], label=counter_n )
            counter_n += 1

        for i, n in enumerate(points_G[:-1]):
            for j, m in enumerate(points_G[(i+1):]):

                dist = np.linalg.norm(np.subtract(n, m))
                if dist == self.lattice_constant:
                    G.add_edge(i, (i+1)+j, slope=(n, m), label=counter_e)
                    counter_e += 1

        return G

class networkx_dual_laves(networkx_dual, object):

    """
    A class for spatial, dual Laves circuits.

    Attributes
    ----------

        layer (list): List of the mutlilayered circuits.
        lattice_constant (float): Scale for the spacing between the networks.

    """
    def __init__(self, num_periods):

        """
        A constructor for multilayer circuit laves objects, setting default values
         for the interal graph objects and geometry
        """

        super(networkx_dual_laves, self).__init__()
        self.lattice_constant = 2.
        self.dual_laves(num_periods)

    # test new minimal surface graph_sets

    def dual_laves(self, num_periods):

        """
        Set internal networks structure, dual diamond.

        Args:
            num_periods (int): A networkx graph.

        """

        G_aux = self.laves_graph(num_periods, 'R',[0., 0., 0.])
        H_aux = self.laves_graph(num_periods, 'L',[3., 2., 0.])

        G1, G2 = self.init_graph_nuclei(G_aux, H_aux)

        adj = self.set_graph_adjacency(G1, G2)

        # cut off redundant (non-connected or neigborless) points/edges
        G1, G2 = self.prune_leaves(G1, G2, adj)

        # relabeling network nodes/edges & adjacency-list
        P = self.relabel_networkx(G1, G2, adj)

        self.layer = [P[0], P[1]]

    def laves_graph(self, num_periods, chirality, offset):

        """
        Generate points for a Laves lattice and its dual via mirroring + translation
         and return dual graph representations.

        Args:
            num_periods (int): Repetition number of the unit cells..
            chirality (string): Chirality identifier for the current lattice generator.
            offset (ndarray): A translation vector.


        Returns:
            nx.Graph: A networkx graph

        """

        counter = 0
        L = nx.Graph()
        periods = range(num_periods)

        fundamental_points = [[0, 0, 0], [1 ,1 ,0], [1 ,2, 1], [0, 3, 1],
         [2, 2, 2], [3, 3, 2], [3, 0, 3], [2, 1, 3]]
        if chirality == 'R':

            for l, fp in enumerate(fundamental_points):
                for i in periods:
                    for j in periods:
                        for k in periods:

                            pos_n=np.add(np.add(fp,[4.*i, 4.*j, 4.*k]), offset)
                            L.add_node(tuple(pos_n), pos=pos_n)
        if chirality == 'L':
            for l, fp in enumerate(fundamental_points):
                for i in periods:
                    for j in periods:
                        for k in periods:

                            pos_n=np.add(np.add(np.multiply(fp, [-1., 1., 1.]),
                             [4.*i, 4.*j, 4.*k]), offset)
                            L.add_node(tuple(pos_n), pos=pos_n)

        return L

    def init_graph_nuclei(self, G_aux, H_aux):

        """
        Generate points for a Laves lattice and its dual via mirroring +
         translation and return dual graph representations.

        Args:
            G_aux (nx.Graph): Inner networkx graph.
            H_aux (nx.Graph): Outer networkx graph.

        Returns:
            nx.Graph: A networkx graph

        """

        G = self.init_graph(G_aux)
        H = self.init_graph(H_aux)

        return G, H

    def init_graph(self, G_aux):

        """
        Built labeled, attributed graphs from raw point sets.

        Args:
            G_aux (nx.Graph): Inner networkx graph holding unlabeled data.

        Returns:
            nx.Graph: A networkx graph

        """

        list_nodes = list(G_aux.nodes())
        points_G = [G_aux.nodes[n]['pos'] for i, n in enumerate(G_aux.nodes())]

        G = nx.Graph()
        counter_e = 0
        counter_n = 0
        for i, n in enumerate(G_aux.nodes()) :
            G.add_node(n, pos=G_aux.nodes[n]['pos'], label=counter_n)
            counter_n += 1

        for i, n in enumerate(list_nodes[:-1]):
            for j, m in enumerate(list_nodes[(i+1):]):

                v = np.subtract(n, m)
                dist = np.dot(v, v)

                if dist == self.lattice_constant:
                    options = {
                    'slope': (G_aux.nodes[n]['pos'], G_aux.nodes[m]['pos']),
                    'label': counter_e
                    }
                    G.add_edge(n, m, **options)
                    counter_e += 1

        return G

class networkx_dual_catenation(networkx_dual, object):

    """
    A class for spatial, dual Laves circuits.

    Attributes
    ----------

        layer (list): List of the mutlilayered circuits.
        lattice_constant (float): Scale for the spacing between the networks.

    """
    def __init__(self, num_periods):

        """
        A constructor for multilayer circuit catenation objects, setting default values
         for the interal graph objects and geometry
        """

        super(networkx_dual_catenation, self).__init__()
        self.lattice_constant = 1
        self.translation_length = 1
        self.dual_ladder(num_periods)

    def dual_ladder(self, num_periods):

        """
        Set internal networkx structure, dual ladder.

        Args:
            num_periods (int): Repetition number of the unit tile.

        """

        np1 = [num_periods, 1]
        np2 = [num_periods+1, 1]

        N = [np1, np2]
        ic = init_crystal.networkx_square
        G1, G2 = [nx.Graph(ic(i).G) for i in N]

        theta = np.pi/2.
        rot_mat = np.array(((1, 0, 0), (0, np.cos(theta), -np.sin(theta)),
               (0, np.sin(theta), np.cos(theta)) ))

        for n in G1.nodes():
            p = np.array(G1.nodes[n]['pos'])
            p1 = np.dot(rot_mat, p)
            p2 = np.add([0.5, 0.5, -0.5], p1 )

            G1.nodes[n]['pos'] = self.lattice_constant*p2


        self.layer = [G1,G2]

class networkx_dual_crossMesh(networkx_dual, object):

    """
    A class for spatial, dual Laves circuits.

    Attributes
    ----------

        layer (list): List of the mutlilayered circuits.
        lattice_constant (float): Scale for the spacing between the networks.

    """
    def __init__(self, num_periods):

        """
        A constructor for multilayer circuit catenation objects, setting default values
         for the interal graph objects and geometry
        """

        super(networkx_dual_crossMesh, self).__init__()
        self.lattice_constant = 1
        self.translation_length = 1
        self.dual_crossMesh(num_periods)

    def dual_crossMesh(self, num_periods):

        """
        Set internal networkx structure, dual crossed_mesh.

        Args:
            num_periods (int): Repetition number of the unit tile.

        """
        num_periods1X, num_periods1Y, num_periods2X, num_periods2Y =num_periods

        np1 = [num_periods1X, num_periods1Y]
        np2 = [num_periods2X, num_periods2Y]

        N = [np1, np2]
        ic = init_crystal.networkx_square
        G1, G2 = [nx.Graph(ic(i).G) for i in N]

        theta = np.pi/2.
        rot_mat = np.array(((1, 0, 0), (0, np.cos(theta), -np.sin(theta)),
               (0, np.sin(theta), np.cos(theta)) ))

        for n in G1.nodes():
            p = np.array(G1.nodes[n]['pos'])
            p1 = np.dot(rot_mat, p)
            p2 = np.add([0.5, 0.5, -0.5], p1 )

            G1.nodes[n]['pos'] = self.lattice_constant*p2

        self.layer = [G1,G2]
