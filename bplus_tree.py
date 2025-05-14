from typing import List, Dict, Optional, Tuple, Any
import math
import logging
import json
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BPlusTreeNode:
    def __init__(self, is_leaf: bool = True):
        self.keys: List[str] = []
        self.values: List[Dict] = []
        self.children: List['BPlusTreeNode'] = []
        self.is_leaf = is_leaf
        self.next: Optional['BPlusTreeNode'] = None  # For leaf nodes
        self.parent = None

class BPlusTree:
    def __init__(self, order: int = 4):
        """
        Initialize B+ Tree with configurable order.
        
        Args:
            order: Maximum number of children per node
        """
        self.root = None
        self.order = order
        self.min_keys = math.ceil(order / 2) - 1
        self.max_keys = order - 1
        self._performance_metrics = {
            'insertions': 0,
            'deletions': 0,
            'searches': 0,
            'splits': 0,
            'merges': 0,
            'processing_time': 0
        }
    
    def insert(self, key: Any, value: Any) -> bool:
        """
        Insert a key-value pair into the tree.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        
        Returns:
            bool: True if insertion was successful
        """
        start_time = time.time()
        
        try:
            if self.root is None:
                self.root = BPlusTreeNode(is_leaf=True)
                self.root.keys = [key]
                self.root.values = [value]
                self._performance_metrics['insertions'] += 1
                return True
            
            # Find the leaf node where the key should be inserted
            leaf = self._find_leaf(key)
            
            # Insert the key-value pair
            if key in leaf.keys:
                # Update existing value
                idx = leaf.keys.index(key)
                leaf.values[idx] = value
            else:
                # Insert new key-value pair
                idx = self._find_insertion_index(leaf.keys, key)
                leaf.keys.insert(idx, key)
                leaf.values.insert(idx, value)
                self._performance_metrics['insertions'] += 1
            
            # Check if the node needs to be split
            if len(leaf.keys) > self.max_keys:
                self._split_node(leaf)
            
            self._performance_metrics['processing_time'] += time.time() - start_time
            return True
            
        except Exception as e:
            logger.error(f"Error inserting key {key}: {str(e)}")
            return False
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the tree.
        
        Args:
            key: The key to search for
        
        Returns:
            The value associated with the key, or None if not found
        """
        start_time = time.time()
        self._performance_metrics['searches'] += 1
        
        try:
            if self.root is None:
                return None
            
            leaf = self._find_leaf(key)
            if key in leaf.keys:
                idx = leaf.keys.index(key)
                self._performance_metrics['processing_time'] += time.time() - start_time
                return leaf.values[idx]
            
            self._performance_metrics['processing_time'] += time.time() - start_time
            return None
            
        except Exception as e:
            logger.error(f"Error searching for key {key}: {str(e)}")
            return None
    
    def delete(self, key: Any) -> bool:
        """
        Delete a key from the tree.
        
        Args:
            key: The key to delete
        
        Returns:
            bool: True if deletion was successful
        """
        start_time = time.time()
        
        try:
            if self.root is None:
                return False
            
            leaf = self._find_leaf(key)
            if key not in leaf.keys:
                return False
            
            # Remove the key-value pair
            idx = leaf.keys.index(key)
            leaf.keys.pop(idx)
            leaf.values.pop(idx)
            self._performance_metrics['deletions'] += 1
            
            # Check if the node needs to be merged or redistributed
            if len(leaf.keys) < self.min_keys and leaf != self.root:
                self._handle_underflow(leaf)
            
            self._performance_metrics['processing_time'] += time.time() - start_time
            return True
            
        except Exception as e:
            logger.error(f"Error deleting key {key}: {str(e)}")
            return False
    
    def range_search(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """
        Search for all keys in the range [start_key, end_key].
        
        Args:
            start_key: The lower bound of the range
            end_key: The upper bound of the range
        
        Returns:
            List of (key, value) tuples in the range
        """
        results = []
        try:
            if self.root is None:
                return results
            
            # Find the leaf node containing start_key
            leaf = self._find_leaf(start_key)
            
            # Traverse leaf nodes until we find a key greater than end_key
            while leaf is not None:
                for i, key in enumerate(leaf.keys):
                    if start_key <= key <= end_key:
                        results.append((key, leaf.values[i]))
                    elif key > end_key:
                        return results
                leaf = leaf.next
            
            return results
            
        except Exception as e:
            logger.error(f"Error in range search: {str(e)}")
            return results
    
    def _find_leaf(self, key: Any) -> BPlusTreeNode:
        """Find the leaf node where a key should be inserted."""
        node = self.root
        while not node.is_leaf:
            idx = self._find_insertion_index(node.keys, key)
            node = node.children[idx]
        return node
    
    def _find_insertion_index(self, keys: List[Any], key: Any) -> int:
        """Find the index where a key should be inserted in a sorted list."""
        for i, k in enumerate(keys):
            if key < k:
                return i
        return len(keys)
    
    def _split_node(self, node: BPlusTreeNode):
        """Split a node that has exceeded the maximum number of keys."""
        self._performance_metrics['splits'] += 1
        
        mid = len(node.keys) // 2
        new_node = BPlusTreeNode(is_leaf=node.is_leaf)
        
        # Split keys and values/children
        new_node.keys = node.keys[mid:]
        node.keys = node.keys[:mid]
        
        if node.is_leaf:
            new_node.values = node.values[mid:]
            node.values = node.values[:mid]
            new_node.next = node.next
            node.next = new_node
        else:
            new_node.children = node.children[mid:]
            node.children = node.children[:mid]
            for child in new_node.children:
                child.parent = new_node
        
        # Update parent
        if node == self.root:
            self.root = BPlusTreeNode(is_leaf=False)
            self.root.keys = [new_node.keys[0]]
            self.root.children = [node, new_node]
            node.parent = self.root
            new_node.parent = self.root
        else:
            parent = node.parent
            idx = parent.children.index(node)
            parent.keys.insert(idx, new_node.keys[0])
            parent.children.insert(idx + 1, new_node)
            new_node.parent = parent
            
            if len(parent.keys) > self.max_keys:
                self._split_node(parent)
    
    def _handle_underflow(self, node: BPlusTreeNode):
        """Handle a node that has fallen below the minimum number of keys."""
        self._performance_metrics['merges'] += 1
        
        parent = node.parent
        idx = parent.children.index(node)
        
        # Try to borrow from left sibling
        if idx > 0:
            left_sibling = parent.children[idx - 1]
            if len(left_sibling.keys) > self.min_keys:
                self._borrow_from_left(node, left_sibling, parent, idx)
                return
        
        # Try to borrow from right sibling
        if idx < len(parent.children) - 1:
            right_sibling = parent.children[idx + 1]
            if len(right_sibling.keys) > self.min_keys:
                self._borrow_from_right(node, right_sibling, parent, idx)
                return
        
        # Merge with sibling
        if idx > 0:
            self._merge_nodes(parent.children[idx - 1], node, parent, idx)
        else:
            self._merge_nodes(node, parent.children[idx + 1], parent, idx + 1)
    
    def _borrow_from_left(self, node: BPlusTreeNode, left_sibling: BPlusTreeNode, 
                         parent: BPlusTreeNode, idx: int):
        """Borrow a key from the left sibling."""
        if node.is_leaf:
            node.keys.insert(0, left_sibling.keys.pop())
            node.values.insert(0, left_sibling.values.pop())
            parent.keys[idx - 1] = node.keys[0]
        else:
            node.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = left_sibling.keys.pop()
            node.children.insert(0, left_sibling.children.pop())
            node.children[0].parent = node
    
    def _borrow_from_right(self, node: BPlusTreeNode, right_sibling: BPlusTreeNode, 
                          parent: BPlusTreeNode, idx: int):
        """Borrow a key from the right sibling."""
        if node.is_leaf:
            node.keys.append(right_sibling.keys.pop(0))
            node.values.append(right_sibling.values.pop(0))
            parent.keys[idx] = right_sibling.keys[0]
        else:
            node.keys.append(parent.keys[idx])
            parent.keys[idx] = right_sibling.keys.pop(0)
            node.children.append(right_sibling.children.pop(0))
            node.children[-1].parent = node
    
    def _merge_nodes(self, left: BPlusTreeNode, right: BPlusTreeNode, parent: BPlusTreeNode, idx: int):
        """Merge two nodes."""
        if left.is_leaf:
            left.keys.extend(right.keys)
            left.values.extend(right.values)
            left.next = right.next
        else:
            left.keys.append(parent.keys.pop(idx - 1))
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            for child in right.children:
                child.parent = left
        
        parent.children.pop(idx)
        
        if parent == self.root and len(parent.keys) == 0:
            self.root = left
            left.parent = None
        elif len(parent.keys) < self.min_keys and parent != self.root:
            self._handle_underflow(parent)
    
    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics."""
        return {
            'insertions': self._performance_metrics['insertions'],
            'deletions': self._performance_metrics['deletions'],
            'searches': self._performance_metrics['searches'],
            'splits': self._performance_metrics['splits'],
            'merges': self._performance_metrics['merges'],
            'processing_time': self._performance_metrics['processing_time']
        }
    
    def save_tree(self, filepath: str):
        """Save the tree to a file."""
        try:
            data = self._serialize_node(self.root)
            with open(filepath, 'w') as f:
                json.dump(data, f)
            logger.info(f"Tree saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving tree: {str(e)}")
    
    def load_tree(self, filepath: str):
        """Load the tree from a file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.root = self._deserialize_node(data)
            logger.info(f"Tree loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading tree: {str(e)}")
    
    def _serialize_node(self, node: Optional[BPlusTreeNode]) -> Dict:
        """Serialize a node to a dictionary."""
        if node is None:
            return None
        
        return {
            'keys': node.keys,
            'values': node.values if node.is_leaf else None,
            'is_leaf': node.is_leaf,
            'children': [self._serialize_node(child) for child in node.children] 
                       if not node.is_leaf else None
        }
    
    def _deserialize_node(self, data: Dict) -> Optional[BPlusTreeNode]:
        """Deserialize a dictionary to a node."""
        if data is None:
            return None
        
        node = BPlusTreeNode(is_leaf=data['is_leaf'])
        node.keys = data['keys']
        node.values = data['values']
        
        if not node.is_leaf:
            node.children = [self._deserialize_node(child) for child in data['children']]
            for child in node.children:
                child.parent = node
        
        return node
    
    def clear(self):
        """Clear the tree and reset metrics."""
        self.root = None
        self._performance_metrics = {
            'insertions': 0,
            'deletions': 0,
            'searches': 0,
            'splits': 0,
            'merges': 0,
            'processing_time': 0
        } 