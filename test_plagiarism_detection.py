import unittest
import os
import tempfile
import shutil
from pathlib import Path
from code_parser import CodeParser
from rabin_karp import RabinKarp
from similarity_graph import SimilarityGraph
from bplus_tree import BPlusTree

class TestCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = CodeParser()
        self.test_dir = tempfile.mkdtemp()
        
        # Create test files
        self.python_file = os.path.join(self.test_dir, "test.py")
        with open(self.python_file, "w") as f:
            f.write("""
            # This is a test file
            def hello():
                print("Hello, World!")
                
            if __name__ == "__main__":
                hello()
            """)
        
        self.java_file = os.path.join(self.test_dir, "test.java")
        with open(self.java_file, "w") as f:
            f.write("""
            // This is a test file
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_parse_python_file(self):
        tokens = self.parser.parse_file(self.python_file)
        self.assertIsNotNone(tokens)
        self.assertGreater(len(tokens), 0)
        self.assertIn("def", tokens)
        self.assertIn("hello", tokens)
    
    def test_parse_java_file(self):
        tokens = self.parser.parse_file(self.java_file)
        self.assertIsNotNone(tokens)
        self.assertGreater(len(tokens), 0)
        self.assertIn("public", tokens)
        self.assertIn("class", tokens)
    
    def test_parse_nonexistent_file(self):
        tokens = self.parser.parse_file("nonexistent.py")
        self.assertIsNone(tokens)
    
    def test_get_metadata(self):
        metadata = self.parser.get_metadata(self.python_file)
        self.assertEqual(metadata['file_name'], "test.py")
        self.assertEqual(metadata['language'], "Python")

class TestRabinKarp(unittest.TestCase):
    def setUp(self):
        self.rabin_karp = RabinKarp()
    
    def test_find_matches(self):
        text = ["def", "hello", "(", ")", ":", "print", "(", '"Hello"', ")"]
        pattern = ["def", "hello", "(", ")", ":"]
        matches = self.rabin_karp.find_matches(text, pattern)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], 0)  # Start index
        self.assertGreater(matches[0][1], 0.8)  # Similarity score
    
    def test_find_all_matches(self):
        text = ["def", "hello", "(", ")", ":", "print", "(", '"Hello"', ")"]
        patterns = [
            ["def", "hello", "(", ")", ":"],
            ["print", "(", '"Hello"', ")"]
        ]
        matches = self.rabin_karp.find_all_matches(text, patterns)
        self.assertEqual(len(matches), 2)
    
    def test_performance_metrics(self):
        text = ["def", "hello", "(", ")", ":", "print", "(", '"Hello"', ")"]
        pattern = ["def", "hello", "(", ")", ":"]
        self.rabin_karp.find_matches(text, pattern)
        metrics = self.rabin_karp.get_performance_metrics()
        self.assertGreater(metrics['total_operations'], 0)
        self.assertGreaterEqual(metrics['cache_hits'], 0)

class TestSimilarityGraph(unittest.TestCase):
    def setUp(self):
        self.graph = SimilarityGraph()
    
    def test_add_file_and_similarity(self):
        self.graph.add_file("file1", {"name": "test1.py"})
        self.graph.add_file("file2", {"name": "test2.py"})
        self.graph.add_similarity("file1", "file2", 0.9)
        
        similar_files = self.graph.find_similar_files("file1")
        self.assertEqual(len(similar_files), 1)
        self.assertEqual(similar_files[0][0], "file2")
        self.assertEqual(similar_files[0][1], 0.9)
    
    def test_find_clusters(self):
        # Add some files with similarities
        for i in range(5):
            self.graph.add_file(f"file{i}", {"name": f"test{i}.py"})
        
        # Create two clusters
        self.graph.add_similarity("file0", "file1", 0.9)
        self.graph.add_similarity("file1", "file2", 0.9)
        self.graph.add_similarity("file3", "file4", 0.9)
        
        clusters = self.graph.find_clusters()
        self.assertEqual(len(clusters), 2)
    
    def test_graph_metrics(self):
        self.graph.add_file("file1", {"name": "test1.py"})
        self.graph.add_file("file2", {"name": "test2.py"})
        self.graph.add_similarity("file1", "file2", 0.9)
        
        metrics = self.graph.get_graph_metrics()
        self.assertEqual(metrics['total_nodes'], 2)
        self.assertEqual(metrics['total_edges'], 1)

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree()
    
    def test_insert_and_search(self):
        self.tree.insert("key1", {"value": 1})
        self.tree.insert("key2", {"value": 2})
        
        result = self.tree.search("key1")
        self.assertEqual(result["value"], 1)
        
        result = self.tree.search("key2")
        self.assertEqual(result["value"], 2)
    
    def test_delete(self):
        self.tree.insert("key1", {"value": 1})
        self.tree.insert("key2", {"value": 2})
        
        self.assertTrue(self.tree.delete("key1"))
        self.assertIsNone(self.tree.search("key1"))
        self.assertIsNotNone(self.tree.search("key2"))
    
    def test_range_search(self):
        for i in range(5):
            self.tree.insert(f"key{i}", {"value": i})
        
        results = self.tree.range_search("key1", "key3")
        self.assertEqual(len(results), 3)
    
    def test_save_and_load(self):
        # Insert some data
        for i in range(5):
            self.tree.insert(f"key{i}", {"value": i})
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            self.tree.save_tree(f.name)
            
            # Create new tree and load data
            new_tree = BPlusTree()
            new_tree.load_tree(f.name)
            
            # Verify data
            for i in range(5):
                result = new_tree.search(f"key{i}")
                self.assertEqual(result["value"], i)
        
        # Clean up
        os.unlink(f.name)

if __name__ == '__main__':
    unittest.main() 