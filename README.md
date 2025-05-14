# Plagiarism Detection System

A robust and efficient plagiarism detection system for source code, built with Python. This system uses advanced algorithms and data structures to detect code similarity and potential plagiarism.

## Features

- **Multi-language Support**: Supports Python, Java, C/C++, JavaScript, TypeScript, and Ruby
- **Efficient Code Parsing**: Robust parsing with comment and whitespace handling
- **Advanced Similarity Detection**: Uses Rabin-Karp algorithm for efficient string matching
- **Graph-based Analysis**: Similarity graph with clustering capabilities
- **Persistent Storage**: B+ Tree implementation for efficient data storage and retrieval
- **Real-time Processing**: Parallel processing support for faster analysis
- **Comprehensive Testing**: Extensive test suite with coverage reporting
- **Modern UI**: Streamlit-based user interface for easy interaction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plagiarism-detection.git
cd plagiarism-detection
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit interface:
```bash
streamlit run app.py
```

2. Upload code files or directories for analysis
3. View similarity results and clusters
4. Export results as needed

## System Architecture

### Components

1. **Code Parser (`code_parser.py`)**
   - Language-specific parsing
   - Comment and whitespace handling
   - Metadata extraction

2. **Rabin-Karp Algorithm (`rabin_karp.py`)**
   - Efficient string matching
   - Parallel processing support
   - Performance optimization with caching

3. **Similarity Graph (`similarity_graph.py`)**
   - Graph-based similarity representation
   - Clustering using DBSCAN
   - Performance metrics tracking

4. **B+ Tree (`bplus_tree.py`)**
   - Efficient data storage
   - Range queries support
   - Persistent storage capabilities

### Performance Optimizations

- Hash caching in Rabin-Karp algorithm
- Parallel processing for large datasets
- Efficient graph operations with NetworkX
- Optimized B+ Tree operations

## Testing

Run the test suite:
```bash
pytest test_plagiarism_detection.py
```

Run with coverage:
```bash
pytest --cov=. test_plagiarism_detection.py
```

## Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NetworkX for graph operations
- scikit-learn for clustering algorithms
- Streamlit for the web interface 