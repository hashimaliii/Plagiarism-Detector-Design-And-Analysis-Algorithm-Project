from typing import List, Dict, Set, Tuple, Optional
import networkx as nx
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityGraph:
    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize similarity graph with configurable threshold.
        
        Args:
            similarity_threshold: Minimum similarity score to create an edge (0.0 to 1.0)
        """
        self.graph = nx.Graph()
        self.similarity_threshold = similarity_threshold
        self._performance_metrics = {
            'total_edges': 0,
            'total_nodes': 0,
            'processing_time': 0,
            'clustering_time': 0
        }
    
    def add_file(self, file_id: str, metadata: Dict):
        """Add a file node to the graph with its metadata."""
        self.graph.add_node(file_id, **metadata)
        self._performance_metrics['total_nodes'] += 1
    
    def add_similarity(self, file1_id: str, file2_id: str, similarity: float):
        """Add an edge between two files if similarity exceeds threshold."""
        if similarity >= self.similarity_threshold:
            self.graph.add_edge(file1_id, file2_id, weight=similarity)
            self._performance_metrics['total_edges'] += 1
    
    def find_similar_files(self, file_id: str, min_similarity: Optional[float] = None) -> List[Tuple[str, float]]:
        """
        Find all files similar to the given file.
        
        Args:
            file_id: ID of the file to find similarities for
            min_similarity: Optional minimum similarity threshold
        
        Returns:
            List of (file_id, similarity) tuples
        """
        if file_id not in self.graph:
            logger.warning(f"File {file_id} not found in graph")
            return []
        
        threshold = min_similarity if min_similarity is not None else self.similarity_threshold
        similar_files = []
        
        for neighbor in self.graph.neighbors(file_id):
            similarity = self.graph[file_id][neighbor]['weight']
            if similarity >= threshold:
                similar_files.append((neighbor, similarity))
        
        return sorted(similar_files, key=lambda x: x[1], reverse=True)
    
    def find_clusters(self, eps: float = 0.2, min_samples: int = 2) -> List[Set[str]]:
        """
        Find clusters of similar files using DBSCAN algorithm.
        
        Args:
            eps: Maximum distance between samples in a cluster
            min_samples: Minimum number of samples in a cluster
        
        Returns:
            List of sets containing file IDs in each cluster
        """
        if not self.graph.nodes():
            return []
        
        start_time = time.time()
        
        # Convert graph to distance matrix
        nodes = list(self.graph.nodes())
        n = len(nodes)
        distance_matrix = np.zeros((n, n))
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i != j:
                    if self.graph.has_edge(node1, node2):
                        # Convert similarity to distance (1 - similarity)
                        distance_matrix[i, j] = 1 - self.graph[node1][node2]['weight']
                    else:
                        distance_matrix[i, j] = 1.0
        
        # Apply DBSCAN clustering
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
        labels = clustering.fit_predict(distance_matrix)
        
        # Group files by cluster
        clusters = defaultdict(set)
        for node, label in zip(nodes, labels):
            if label != -1:  # -1 indicates noise points
                clusters[label].add(node)
        
        self._performance_metrics['clustering_time'] = time.time() - start_time
        return list(clusters.values())
    
    def get_connected_components(self) -> List[Set[str]]:
        """Get connected components in the similarity graph."""
        return list(nx.connected_components(self.graph))
    
    def get_most_similar_pairs(self, top_k: int = 10) -> List[Tuple[str, str, float]]:
        """Get top K most similar file pairs."""
        edges = [(u, v, d['weight']) for u, v, d in self.graph.edges(data=True)]
        return sorted(edges, key=lambda x: x[2], reverse=True)[:top_k]
    
    def get_file_metrics(self, file_id: str) -> Dict:
        """Get metrics for a specific file."""
        if file_id not in self.graph:
            return {}
        
        neighbors = list(self.graph.neighbors(file_id))
        similarities = [self.graph[file_id][n]['weight'] for n in neighbors]
        
        return {
            'degree': len(neighbors),
            'avg_similarity': np.mean(similarities) if similarities else 0,
            'max_similarity': max(similarities) if similarities else 0,
            'min_similarity': min(similarities) if similarities else 0
        }
    
    def get_graph_metrics(self) -> Dict:
        """Get overall graph metrics."""
        return {
            'total_nodes': self._performance_metrics['total_nodes'],
            'total_edges': self._performance_metrics['total_edges'],
            'avg_degree': np.mean([d for n, d in self.graph.degree()]) if self.graph.nodes() else 0,
            'density': nx.density(self.graph),
            'clustering_coefficient': nx.average_clustering(self.graph),
            'processing_time': self._performance_metrics['processing_time'],
            'clustering_time': self._performance_metrics['clustering_time']
        }
    
    def save_graph(self, filepath: str):
        """Save the graph to a file."""
        try:
            nx.write_gpickle(self.graph, filepath)
            logger.info(f"Graph saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving graph: {str(e)}")
    
    def load_graph(self, filepath: str):
        """Load the graph from a file."""
        try:
            self.graph = nx.read_gpickle(filepath)
            self._performance_metrics['total_nodes'] = len(self.graph.nodes())
            self._performance_metrics['total_edges'] = len(self.graph.edges())
            logger.info(f"Graph loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading graph: {str(e)}")
    
    def clear(self):
        """Clear the graph and reset metrics."""
        self.graph.clear()
        self._performance_metrics = {
            'total_edges': 0,
            'total_nodes': 0,
            'processing_time': 0,
            'clustering_time': 0
        } 