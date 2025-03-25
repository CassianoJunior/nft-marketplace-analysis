import pandas as pd
import numpy as np
import networkx as nx


def create_robust_graph(df):
  """
  Create a graph with comprehensive weight handling

  Parameters:
  - df: Input DataFrame

  Returns:
  NetworkX DiGraph with processed weights
  """
  G = nx.DiGraph()

  for index, row in df.iterrows():
    weight = row["Price_USD"]

    # Use log transformation to handle extremely small values
    normalized_weight = np.log1p(weight)

    G.add_edge(row["Seller_address"], row["Buyer_address"], weight=normalized_weight)

  return G


def analyze_shortest_paths(G):
  """
  Analyze shortest paths in the graph with robust error handling

  Parameters:
  - G: NetworkX DiGraph
  """
  print("\n--- Análise de Caminhos Mínimos ---")

  try:
    # Find connected components
    components = list(nx.weakly_connected_components(G))
    largest_component = max(components, key=len)

    # Create subgraph of the largest component
    G_largest = G.subgraph(largest_component)

    # Sample nodes from the largest component
    sample_nodes = list(G_largest.nodes)[:100]

    path_lengths = []
    for node in sample_nodes:
      try:
        # Use all-pairs shortest path lengths to avoid single-source issues
        lengths = dict(nx.multi_source_dijkstra_path_length(G_largest, {node}))
        path_lengths.extend(list(lengths.values()))
      except Exception as path_error:
        print(f"Path calculation error for node {node}: {path_error}")

    if path_lengths:
      print(f"Média do tamanho dos caminhos mínimos: {np.mean(path_lengths):.2f}")
      print(f"Mediana do tamanho dos caminhos mínimos: {np.median(path_lengths):.2f}")
      print(f"Desvio padrão: {np.std(path_lengths):.2f}")

      print(f"\nTotal de componentes conectados: {len(components)}")
      print(f"Tamanho do maior componente: {len(largest_component)}")
    else:
      print("Nenhum caminho válido encontrado.")

  except Exception as e:
    print(f"Erro na análise de caminhos: {e}")


# Read the CSV
df = pd.read_csv("./Data_API_sample.csv")

# Create robust graph
G = create_robust_graph(df)

# Analyze paths
analyze_shortest_paths(G)
