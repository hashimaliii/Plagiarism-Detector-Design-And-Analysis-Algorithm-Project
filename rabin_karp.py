from typing import List, Dict, Set, Optional, Tuple
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabinKarp:
    def __init__(self, base: int = 256, prime: int = 101):
        """
        Initialize Rabin-Karp algorithm with configurable base and prime numbers.
        
        Args:
            base: Base for the hash function (default: 256 for ASCII)
            prime: Prime number for modulo operation (default: 101)
        """
        self.base = base
        self.prime = prime
        self._hash_cache = {}  # Cache for hash values
        self._performance_metrics = {
            'total_operations': 0,
            'cache_hits': 0,
            'processing_time': 0
        }
    
    def _compute_hash(self, text: List[str], start: int, length: int) -> int:
        """
        Compute rolling hash for a window of tokens.
        Uses caching to improve performance for repeated computations.
        """
        cache_key = (tuple(text[start:start+length]), start, length)
        if cache_key in self._hash_cache:
            self._performance_metrics['cache_hits'] += 1
            return self._hash_cache[cache_key]
        
        hash_value = 0
        for i in range(length):
            hash_value = (hash_value * self.base + hash(text[start + i])) % self.prime
        
        self._hash_cache[cache_key] = hash_value
        self._performance_metrics['total_operations'] += 1
        return hash_value
    
    def find_matches(self, text: List[str], pattern: List[str], 
                    min_similarity: float = 0.8) -> List[Tuple[int, float]]:
        """
        Find all matches of pattern in text using Rabin-Karp algorithm.
        Returns list of (start_index, similarity_score) tuples.
        
        Args:
            text: List of tokens to search in
            pattern: List of tokens to search for
            min_similarity: Minimum similarity threshold (0.0 to 1.0)
        
        Returns:
            List of tuples containing (start_index, similarity_score)
        """
        if not text or not pattern:
            logger.warning("Empty text or pattern provided")
            return []
        
        if len(pattern) > len(text):
            logger.warning("Pattern longer than text")
            return []
        
        start_time = time.time()
        matches = []
        pattern_hash = self._compute_hash(pattern, 0, len(pattern))
        
        # Precompute first window hash
        window_hash = self._compute_hash(text, 0, len(pattern))
        
        # Calculate power for rolling hash
        power = 1
        for _ in range(len(pattern) - 1):
            power = (power * self.base) % self.prime
        
        # Slide the pattern over text
        for i in range(len(text) - len(pattern) + 1):
            if window_hash == pattern_hash:
                # Verify match and calculate similarity
                similarity = self._calculate_similarity(
                    text[i:i+len(pattern)], pattern)
                if similarity >= min_similarity:
                    matches.append((i, similarity))
            
            # Calculate hash for next window
            if i < len(text) - len(pattern):
                window_hash = (self.base * (window_hash - hash(text[i]) * power) + 
                             hash(text[i + len(pattern)])) % self.prime
        
        self._performance_metrics['processing_time'] = time.time() - start_time
        return matches
    
    def _calculate_similarity(self, text_window: List[str], 
                            pattern: List[str]) -> float:
        """
        Calculate similarity between text window and pattern.
        Uses token-level comparison with position weighting.
        """
        if len(text_window) != len(pattern):
            return 0.0
        
        matches = 0
        total_weight = 0
        
        for i, (t, p) in enumerate(zip(text_window, pattern)):
            # Give more weight to matches in the middle of the pattern
            weight = 1.0 + 0.5 * (1 - abs(i - len(pattern)/2) / (len(pattern)/2))
            if t == p:
                matches += weight
            total_weight += weight
        
        return matches / total_weight if total_weight > 0 else 0.0
    
    def find_all_matches(self, text: List[str], patterns: List[List[str]], 
                        min_similarity: float = 0.8,
                        max_workers: int = 4) -> Dict[Tuple[int, int], float]:
        """
        Find all matches of multiple patterns in text using parallel processing.
        
        Args:
            text: List of tokens to search in
            patterns: List of patterns to search for
            min_similarity: Minimum similarity threshold
            max_workers: Maximum number of parallel workers
        
        Returns:
            Dictionary mapping (pattern_index, start_index) to similarity score
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_pattern = {
                executor.submit(self.find_matches, text, pattern, min_similarity): i
                for i, pattern in enumerate(patterns)
            }
            
            for future in as_completed(future_to_pattern):
                pattern_index = future_to_pattern[future]
                try:
                    matches = future.result()
                    for start_index, similarity in matches:
                        results[(pattern_index, start_index)] = similarity
                except Exception as e:
                    logger.error(f"Error processing pattern {pattern_index}: {str(e)}")
        
        return results
    
    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics."""
        return {
            'total_operations': self._performance_metrics['total_operations'],
            'cache_hits': self._performance_metrics['cache_hits'],
            'cache_hit_ratio': (self._performance_metrics['cache_hits'] / 
                              self._performance_metrics['total_operations'] 
                              if self._performance_metrics['total_operations'] > 0 else 0),
            'processing_time': self._performance_metrics['processing_time']
        }
    
    def clear_cache(self):
        """Clear the hash cache to free memory."""
        self._hash_cache.clear()
        self._performance_metrics = {
            'total_operations': 0,
            'cache_hits': 0,
            'processing_time': 0
        } 