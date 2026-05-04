import pickle
import networkx as nx
from datetime import datetime
import numpy as np
import igraph as ig


def save_graph(graph, filename):
    with open(filename, "wb") as f:
        pickle.dump(graph, f)
    print(f"Graph saved as {filename}")

def load_graph(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    print(f"Graph loaded from {filename}")
    return graph


def graph_summary(G):
    """Provide a comprehensive summary of a NetworkX graph."""

    # Basic Information
    print(f'Number of Nodes: {G.number_of_nodes()}')
    print(f'Number of Edges: {G.number_of_edges()}')
    G.graph['num_nodes'] = G.number_of_nodes()
    G.graph['num_edges'] = G.number_of_edges()

    # Degree Distribution
    degrees = [degree for node, degree in G.degree()]
    print(f'Average Degree: {sum(degrees)/len(degrees):.2f}')
    print(f'Maximum Degree: {max(degrees)}')
    print(f'Minimum Degree: {min(degrees)}')
    G.graph['max_degree'] = max(degrees)
    G.graph['min_degree'] = min(degrees)
    G.graph['avg_degree'] = sum(degrees)/len(degrees)

    # Degree (Weighted) Distribution
    w_degrees = [degree for node, degree in G.degree(weight = "weight")]
    print(f'Average Weighted Degree: {sum(w_degrees)/len(w_degrees):.2f}')
    print(f'Maximum Weighted Degree: {max(w_degrees)}')
    print(f'Minimum Weighted Degree: {min(w_degrees)}')
    G.graph['max_w_degree'] = max(w_degrees)
    G.graph['min_w_degree'] = min(w_degrees)
    G.graph['avg_w_degree'] = sum(w_degrees)/len(w_degrees)

    # Compute the maximum in-degree and out-degree
    # in_degrees = dict(G.in_degree())
    # out_degrees = dict(G.out_degree())
    # max_in_degree = max(in_degrees.values())
    # max_out_degree = max(out_degrees.values())
    # print(f"Max in-degree: {max_in_degree}")
    # print(f"Max out-degree: {max_out_degree}")
    # G.graph['max_in_degree'] = max_in_degree
    # G.graph['max_out_degree'] = max_out_degree

    # Compute the maximum in-degree and out-degree
    # w_in_degrees = dict(G.in_degree(weight = "weight"))
    # w_out_degrees = dict(G.out_degree(weight = "weight"))
    # max_w_in_degree = max(w_in_degrees.values())
    # max_w_out_degree = max(w_out_degrees.values())
    # print(f"Max Weighted in-degree: {max_w_in_degree}")
    # print(f"Max Weighted out-degree: {max_w_out_degree}")
    # G.graph['max_w_in_degree'] = max_w_in_degree
    # G.graph['max_w_out_degree'] = max_w_out_degree

    # Edge Weights
    total_weight = sum([data['weight'] for _, _, data in G.edges(data=True)])
    print(f'Total Edge Weight: {total_weight}')
    G.graph['weights_sum'] = total_weight

    if G.is_directed():
        # Strongly and weakly connected components for directed graphs
        print(f'Number of Strongly Connected Components: {nx.number_strongly_connected_components(G)}')
        print(f'Number of Weakly Connected Components: {nx.number_weakly_connected_components(G)}')

        # Average shortest path over the largest strongly connected component
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        subgraph = G.subgraph(largest_scc)
        print(f'Size of the LSCC: {len(subgraph)}')
        if len(subgraph) > 1:
            avg_shortest_path = nx.average_shortest_path_length(subgraph)
            print(f'Average Shortest Path (largest SCC): {avg_shortest_path:.2f}')
    else:
        # Connected components for undirected graphs
        print(f'Number of Connected Components: {nx.number_connected_components(G)}')

        # Average shortest path over the largest connected component
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        if len(subgraph) > 1:
            avg_shortest_path = nx.average_shortest_path_length(subgraph)
            print(f'Average Shortest Path (largest CC): {avg_shortest_path:.2f}')

    G.graph['avg_shortest_path'] = avg_shortest_path

    # Graph Density
    density = nx.density(G)
    print(f'Density: {density:.2f}')
    G.graph['density'] = density

    # Diameter
    if not G.is_directed():
        if nx.is_connected(G):
            diameter = nx.diameter(G, weight = "weight")
            print(f'Diameter: {diameter}')
            G.graph['diameter'] = diameter
        else:
            print('Diameter: Undefined (Graph is not connected)')
    else:
        if nx.is_strongly_connected(G):
            diameter = nx.diameter(G, weight = "weight")
            print(f'Diameter: {diameter}')
            G.graph['diameter'] = diameter
        else:
            if len(subgraph) > 1:
                diameter = nx.diameter(subgraph, weight = "weight")
                print(f'Diameter on largest SCC (Graph is not strongly connected): {diameter}')
                G.graph['diameter'] = diameter


    # Average Clustering Coefficient
    clustering_coef = nx.average_clustering(G)
    print(f'Average Clustering Coefficient: {clustering_coef:.2f}')
    G.graph['avg_clustering_coef'] = clustering_coef

def calculate_node_graph_measures(G):
    # Calculate clustering coefficient
    clustering_coeffs = nx.clustering(G, weight='weight')
    nx.set_node_attributes(G, clustering_coeffs, "w_clustering_coefficient")
    clustering_coeffs = nx.clustering(G)
    nx.set_node_attributes(G, clustering_coeffs, "clustering_coefficient")
    
    # Calculate betweenness centrality
    betweenness = nx.betweenness_centrality(G, weight='weight')
    nx.set_node_attributes(G, betweenness, "w_betweenness_centrality")
    betweenness = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, betweenness, "betweenness_centrality")
    
    # Calculate hub score (HITS algorithm)
    # hubs, authorities = nx.hits(G, max_iter=1000)
    # nx.set_node_attributes(G, hubs, "hub_score")
    
    # Calculate weighted degree
    weighted_degree = dict(G.degree(weight='weight')) 
    nx.set_node_attributes(G, weighted_degree, "w_degree")
    degrees = nx.degree_centrality(G)
    nx.set_node_attributes(G, degrees, "degree")

    # Calculate closeness centrality
    closeness = nx.closeness_centrality(G, distance='weight',)
    nx.set_node_attributes(G, closeness, "w_closeness_centrality")
    closeness = nx.closeness_centrality(G)
    nx.set_node_attributes(G, closeness, "closeness_centrality")
    
    # Calculate eigenvector centrality
    eigenvector = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
    nx.set_node_attributes(G, eigenvector, "w_eigenvector_centrality")
    eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
    nx.set_node_attributes(G, eigenvector, "eigenvector_centrality")

    # Calculate eccentricity 
    eccentricity = nx.eccentricity(G, weight= 'weight')
    nx.set_node_attributes(G, eccentricity, "w_eccentricity")
    eccentricity = nx.eccentricity(G)
    nx.set_node_attributes(G, eccentricity, "eccentricity")

    # Calculate load centrality
    load_centrality = nx.load_centrality(G,weight='weight')
    nx.set_node_attributes(G, load_centrality, 'w_load_centrality')
    load_centrality = nx.load_centrality(G)
    nx.set_node_attributes(G, load_centrality, 'load_centrality')

    # Calcualte harmonic centrality
    harmonic_centrality = nx.harmonic_centrality(G)
    nx.set_node_attributes(G, harmonic_centrality, 'harmonic_centrality')

    # Calcualte percolation centrality
    percolation_centrality = nx.percolation_centrality(G, weight= 'weight')
    nx.set_node_attributes(G, percolation_centrality, 'w_percolation_centrality')
    percolation_centrality = nx.percolation_centrality(G)
    nx.set_node_attributes(G, percolation_centrality, 'percolation_centrality')
    

    # # Calcualte katz centrality - doesn't converge even with eigenvalue 
    # katz_centrality = nx.katz_centrality(G, alpha=0.5, beta=1.5,  weight= 'weight')
    # nx.set_node_attributes(G, katz_centrality, "katz_centrality")

    # Convert NetworkX graph to igraph, preserving node names and edge attributes
    # G_igraph = ig.Graph.TupleList(
    #     G.edges(data=True),
    #     directed=False,
    #     edge_attrs=['weight', 'type'],
    #     vertex_name_attr='name'
    # )
    # print(G_igraph.edges)
    # # Calculate diversity for each node, handling NaN values
    # diversity_scores = G_igraph.diversity(weights='weight')
    # diversity_scores = [0 if np.isnan(score) else score for score in diversity_scores]
    
    # # Map diversity scores back to the NetworkX graph
    # diversity_dict = {G_igraph.vs[idx]["name"]: score for idx, score in enumerate(diversity_scores)}
    # nx.set_node_attributes(G, diversity_dict, "diversity")

    print("Network measures calculated and stored as node attributes.")

def calculate_node_msg_metrics(G):
    # Initialize dictionaries to store metrics
    metrics = {
        "messages_sent": {},
        "messages_received": {},
        "avg_convo_length": {},
        "avg_response_time": {},
        "lifespan": {}
    }
    
    # Initialize earliest and latest message dates for lifespan calculation
    earliest_dates = {}
    latest_dates = {}

    for node in G.nodes():
        sent_count = 0
        received_count = 0
        convo_lengths = []
        response_times = []

        for neighbor in G.neighbors(node):
            for unit in G[node][neighbor]["units"]:
                convo_lengths.append(len(unit))
                
                for i, message in enumerate(unit):
                    timestamp, sender, receiver, content = message
                    
                    # Update sent and received counts
                    if sender == node:
                        sent_count += 1
                        # Track the earliest and latest message dates for the node
                        if node not in earliest_dates or timestamp < earliest_dates[node]:
                            earliest_dates[node] = timestamp
                        if node not in latest_dates or timestamp > latest_dates[node]:
                            latest_dates[node] = timestamp

                        # Calculate response time if there’s a following message from the receiver
                        if i + 1 < len(unit) and unit[i + 1][1] == receiver:
                            response_time = (unit[i + 1][0] - timestamp).total_seconds()
                            response_times.append(response_time)
                    elif receiver == node:
                        received_count += 1
                        # Track earliest and latest message dates for received messages
                        if node not in earliest_dates or timestamp < earliest_dates[node]:
                            earliest_dates[node] = timestamp
                        if node not in latest_dates or timestamp > latest_dates[node]:
                            latest_dates[node] = timestamp

        # Store metrics for each node
        metrics["messages_sent"][node] = sent_count
        metrics["messages_received"][node] = received_count
        metrics["avg_convo_length"][node] = np.mean(convo_lengths) if convo_lengths else 0
        metrics["avg_response_time"][node] = np.mean(response_times) if response_times else 0
        
        # Calculate lifespan for the node
        if node in earliest_dates and node in latest_dates:
            metrics["lifespan"][node] = (latest_dates[node] - earliest_dates[node]).total_seconds()
        else:
            metrics["lifespan"][node] = 0  # No messages for the node

    # Add calculated metrics to node attributes in the graph
    nx.set_node_attributes(G, metrics["messages_sent"], "messages_sent")
    nx.set_node_attributes(G, metrics["messages_received"], "messages_received")
    nx.set_node_attributes(G, metrics["avg_convo_length"], "avg_convo_length")
    nx.set_node_attributes(G, metrics["avg_response_time"], "avg_response_time")
    nx.set_node_attributes(G, metrics["lifespan"], "lifespan")

    print("Node metrics calculated and added as node attributes.")


def triplet_hub_score_calc(G, communities):
    scores = []

    for com in communities:
        if len(com) > 2:
            subgraph = nx.subgraph(G, com)
            max_degree = max(dict(nx.degree(subgraph)).values())
            scores.append(max_degree / (2 * (len(com) - 1)))  # degree of the node with max degree / max possible degree
        else:
            scores.append(0)
        # For communities with 2 or less members, you might want to handle this differently, e.g., append 0 or skip

    # Filter out None values and calculate mean
    valid_scores = [score for score in scores if score is not None]
    # print(valid_scores)
    return np.mean(valid_scores)


def clean_graph_for_graphml(G):
    # Make a copy of the original graph
    G_copy = G.copy()

    for attr, value in list(G_copy.graph.items()):
        if isinstance(value, dict):
            print(f"Removing attribute: {attr}")
            del G_copy.graph[attr]  # Remove the attribute if it is a dictionary

    # Iterate over edges and remove list attributes
    for u, v, data in G_copy.edges(data=True):
        for attr, value in list(data.items()):  # Use list to avoid runtime dictionary change error
            if isinstance(value, list):
                del data[attr]  # Delete the attribute if it is a list

    return G_copy


def assign_communities(G, *algorithm_names):
    for algorithm_name in algorithm_names:
        # Retrieve communities from the graph for the current algorithm
        communities = G.graph.get(algorithm_name, {}).get('communities', [])
        
        if not communities:
            print(f"No communities found for the '{algorithm_name}' algorithm.")
            continue

        # Create a dictionary to map nodes to their respective community
        node_community_map = {}
        for i, community in enumerate(communities):
            for node in community:
                node_community_map[node] = i  # Assign each node to a community

        # Assign the community membership as a node attribute
        nx.set_node_attributes(G, node_community_map, f'{algorithm_name}_membership')

    return G
