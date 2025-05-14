import streamlit as st
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from plagiarism_detector import PlagiarismDetector
import tempfile
import shutil
import json
from datetime import datetime
import base64
from io import BytesIO

def create_similarity_heatmap(similarity_matrix, submission_ids):
    """Create a heatmap of similarity scores."""
    df = pd.DataFrame(similarity_matrix, index=submission_ids, columns=submission_ids)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(df, cmap='YlOrRd')
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Similarity Score", rotation=-90, va="bottom")
    
    # Set labels
    ax.set_xticks(range(len(submission_ids)))
    ax.set_yticks(range(len(submission_ids)))
    ax.set_xticklabels(submission_ids, rotation=45, ha='right')
    ax.set_yticklabels(submission_ids)
    
    # Add text annotations
    for i in range(len(submission_ids)):
        for j in range(len(submission_ids)):
            text = ax.text(j, i, f"{df.iloc[i, j]:.2f}",
                         ha="center", va="center", color="black")
    
    plt.tight_layout()
    return fig

def create_cluster_graph(clusters, similarity_matrix, submission_ids):
    """Create a graph visualization of clusters."""
    G = nx.Graph()
    
    # Add nodes
    for i, submission_id in enumerate(submission_ids):
        G.add_node(submission_id)
    
    # Add edges for similar submissions
    for i in range(len(submission_ids)):
        for j in range(i + 1, len(submission_ids)):
            if similarity_matrix[i][j] > 0:
                G.add_edge(submission_ids[i], submission_ids[j], 
                          weight=similarity_matrix[i][j])
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    
    # Draw edges with varying thickness based on similarity
    edges = G.edges()
    weights = [G[u][v]['weight'] * 2 for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=weights)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos)
    
    plt.title("Similarity Graph")
    plt.axis('off')
    return plt.gcf()

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_html_report(clusters, similarity_matrix, submission_ids, similarity_threshold, window_size):
    """Generate a comprehensive HTML report."""
    # Create heatmap and graph
    heatmap_fig = create_similarity_heatmap(similarity_matrix, submission_ids)
    graph_fig = create_cluster_graph(clusters, similarity_matrix, submission_ids)
    
    # Convert figures to base64
    heatmap_img = fig_to_base64(heatmap_fig)
    graph_img = fig_to_base64(graph_fig)
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plagiarism Detection Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .section {{ margin-bottom: 30px; }}
            .cluster {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .file-info {{ margin-left: 20px; }}
            .visualization {{ text-align: center; margin: 20px 0; }}
            .visualization img {{ max-width: 100%; height: auto; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f5f5f5; }}
            .timestamp {{ color: #666; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Plagiarism Detection Report</h1>
            <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>Analysis Parameters</h2>
            <ul>
                <li>Similarity Threshold: {similarity_threshold}</li>
                <li>Window Size: {window_size}</li>
                <li>Total Files Analyzed: {len(submission_ids)}</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Detected Clusters</h2>
    """
    
    # Add clusters
    for cluster in clusters:
        html += f"""
            <div class="cluster">
                <h3>Cluster {cluster['cluster_id']}</h3>
                <p><strong>Submissions:</strong> {', '.join(cluster['submissions'])}</p>
                <div class="file-info">
                    <h4>Files:</h4>
                    <ul>
        """
        
        for metadata in cluster['metadata']:
            html += f"""
                        <li>
                            <strong>{metadata['file_name']}</strong> ({metadata['language']})<br>
                            Size: {metadata['file_size']} bytes<br>
                            Modified: {metadata['modified_time']}
                        </li>
            """
        
        html += """
                    </ul>
                </div>
            </div>
        """
    
    # Add visualizations
    html += f"""
        <div class="section">
            <h2>Similarity Analysis</h2>
            <div class="visualization">
                <h3>Similarity Matrix</h3>
                <img src="data:image/png;base64,{heatmap_img}" alt="Similarity Matrix">
            </div>
            <div class="visualization">
                <h3>Similarity Graph</h3>
                <img src="data:image/png;base64,{graph_img}" alt="Similarity Graph">
            </div>
        </div>
    """
    
    # Add detailed similarity matrix
    html += """
        <div class="section">
            <h2>Detailed Similarity Matrix</h2>
            <table>
                <tr>
                    <th>File 1</th>
                    <th>File 2</th>
                    <th>Similarity Score</th>
                </tr>
    """
    
    for i, id1 in enumerate(submission_ids):
        for j, id2 in enumerate(submission_ids):
            if i < j and similarity_matrix[i][j] > 0:
                html += f"""
                    <tr>
                        <td>{id1}</td>
                        <td>{id2}</td>
                        <td>{similarity_matrix[i][j]:.2f}</td>
                    </tr>
                """
    
    html += """
            </table>
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    st.set_page_config(page_title="Plagiarism Detector", layout="wide")
    
    st.title("Code Plagiarism Detector")
    st.write("Upload code files or provide a directory to analyze for potential plagiarism.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    similarity_threshold = st.sidebar.slider(
        "Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Minimum similarity score to consider two submissions as similar"
    )
    
    window_size = st.sidebar.slider(
        "Window Size",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        help="Size of the sliding window for code comparison"
    )
    
    # File upload section
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose code files to analyze",
        accept_multiple_files=True,
        type=['py', 'java', 'cpp', 'c', 'h', 'js', 'ts', 'rb']
    )
    
    if uploaded_files:
        # Create a temporary directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
            
            # Initialize detector
            detector = PlagiarismDetector(
                similarity_threshold=similarity_threshold,
                window_size=window_size
            )
            
            # Process files
            processed_count = detector.process_directory(temp_dir)
            st.success(f"Processed {processed_count} files")
            
            # Find clusters
            clusters = detector.find_plagiarism_clusters()
            
            # Display results
            st.header("Results")
            
            # Show clusters
            st.subheader("Detected Clusters")
            for cluster in clusters:
                with st.expander(f"Cluster {cluster['cluster_id']}"):
                    st.write("Submissions:", ", ".join(cluster['submissions']))
                    st.write("Files:")
                    for metadata in cluster['metadata']:
                        st.write(f"- {metadata['file_name']} ({metadata['language']})")
                        st.write(f"  Size: {metadata['file_size']} bytes")
                        st.write(f"  Modified: {metadata['modified_time']}")
            
            # Show similarity matrix
            st.subheader("Similarity Matrix")
            submission_ids, similarity_matrix = detector.get_similarity_matrix()
            fig = create_similarity_heatmap(similarity_matrix, submission_ids)
            st.pyplot(fig)
            
            # Show cluster graph
            st.subheader("Similarity Graph")
            graph_fig = create_cluster_graph(clusters, similarity_matrix, submission_ids)
            st.pyplot(graph_fig)
            
            # Generate and download HTML report
            st.header("Download Report")
            html_report = generate_html_report(
                clusters, similarity_matrix, submission_ids,
                similarity_threshold, window_size
            )
            
            st.download_button(
                label="Download HTML Report",
                data=html_report,
                file_name="plagiarism_report.html",
                mime="text/html"
            )

if __name__ == "__main__":
    main() 