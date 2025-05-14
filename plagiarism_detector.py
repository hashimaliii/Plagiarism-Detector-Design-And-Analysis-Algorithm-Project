from typing import List, Dict, Set, Tuple, Optional
import os
from code_parser import CodeParser
from rabin_karp import RabinKarp
from similarity_graph import SimilarityGraph
from bplus_tree import BPlusTree
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlagiarismDetector:
    def __init__(self, similarity_threshold: float = 0.7, window_size: int = 5):
        """
        Initialize the plagiarism detector.
        
        Args:
            similarity_threshold: Minimum similarity score to consider submissions similar (0.0 to 1.0)
            window_size: Size of the sliding window for code comparison
        """
        self.parser = CodeParser()
        self.rabin_karp = RabinKarp()
        self.similarity_graph = SimilarityGraph(similarity_threshold=similarity_threshold)
        self.metadata_store = BPlusTree()
        self.window_size = window_size
        self.submissions: Dict[str, List[str]] = {}  # submission_id -> tokens
    
    def add_submission(self, file_path: str, submission_id: str) -> bool:
        """
        Add a submission to the detector.
        
        Args:
            file_path: Path to the submission file
            submission_id: Unique identifier for the submission
        
        Returns:
            bool: True if submission was added successfully
        """
        try:
            # Parse the file
            tokens = self.parser.parse_file(file_path)
            if tokens is None:
                logger.error(f"Failed to parse file: {file_path}")
                return False
            
            # Get file metadata
            metadata = self.parser.get_metadata(file_path)
            metadata['tokens'] = tokens
            
            # Add to similarity graph
            self.similarity_graph.add_file(submission_id, metadata)
            
            # Store metadata
            self.metadata_store.insert(submission_id, metadata)
            
            # Compare with existing submissions
            self._compare_with_existing(submission_id, tokens)
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding submission {submission_id}: {str(e)}")
            return False
    
    def _compare_with_existing(self, submission_id: str, tokens: List[str]):
        """Compare a submission with all existing submissions."""
        # Get all existing submissions
        existing_submissions = self.metadata_store.range_search("", "zzzzzzzzzz")
        
        for existing_id, metadata in existing_submissions:
            if existing_id == submission_id:
                continue
            
            # Compare tokens using sliding window
            existing_tokens = metadata['tokens']
            matches = self.rabin_karp.find_matches(tokens, existing_tokens)
            
            if matches:
                # Calculate overall similarity
                similarity = max(score for _, score in matches)
                self.similarity_graph.add_similarity(submission_id, existing_id, similarity)
    
    def process_directory(self, directory_path: str) -> int:
        """
        Process all code files in a directory.
        
        Args:
            directory_path: Path to the directory containing submissions
        
        Returns:
            int: Number of files processed successfully
        """
        processed_count = 0
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.py', '.java', '.cpp', '.c', '.h', '.js', '.ts', '.rb')):
                    file_path = os.path.join(root, file)
                    submission_id = f"{os.path.splitext(file)[0]}_{processed_count}"
                    
                    if self.add_submission(file_path, submission_id):
                        processed_count += 1
        
        return processed_count
    
    def find_plagiarism_clusters(self) -> List[Dict]:
        """
        Find clusters of similar submissions.
        
        Returns:
            List of dictionaries containing cluster information
        """
        clusters = self.similarity_graph.find_clusters()
        result = []
        
        for i, cluster in enumerate(clusters):
            # Get metadata for each submission in the cluster
            cluster_metadata = []
            for submission_id in cluster:
                metadata = self.metadata_store.search(submission_id)
                if metadata:
                    cluster_metadata.append(metadata)
            
            result.append({
                'cluster_id': i,
                'submissions': list(cluster),
                'metadata': cluster_metadata
            })
        
        return result
    
    def get_similarity_matrix(self) -> Tuple[List[str], List[List[float]]]:
        """
        Get the similarity matrix for all submissions.
        
        Returns:
            Tuple of (submission_ids, similarity_matrix)
        """
        # Get all submissions
        submissions = self.metadata_store.range_search("", "zzzzzzzzzz")
        submission_ids = [s[0] for s in submissions]
        
        # Create similarity matrix
        n = len(submission_ids)
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Fill matrix with similarity scores
        for i, id1 in enumerate(submission_ids):
            for j, id2 in enumerate(submission_ids):
                if i != j:
                    similar_files = self.similarity_graph.find_similar_files(id1)
                    for similar_id, score in similar_files:
                        if similar_id == id2:
                            matrix[i][j] = score
                            break
        
        return submission_ids, matrix
    
    def get_submission_metadata(self, submission_id: str) -> Dict:
        """Get metadata for a specific submission."""
        return self.metadata_store.search(submission_id) or {} 