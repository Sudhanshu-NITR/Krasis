import nltk
import os

def download_nltk_data():
    """
    Downloads minimal NLTK data required for the application.
    Avoids downloading 'all' which is huge.
    """
    # Create a local directory for NLTK data to ensure it's found
    # We use a directory within the project or a standard location
    nltk_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Add this directory to NLTK's search path
    nltk.data.path.append(nltk_data_dir)

    print(f"[*] Checking/Downloading NLTK data to {nltk_data_dir}...")
    
    # The specific packages required by BM25Encoder / LangChain
    required_packages = [
        'punkt',
        'punkt_tab',     # Newer NLTK versions split this out
        'stopwords',
        'averaged_perceptron_tagger', 
    ]

    for package in required_packages:
        try:
            # check if already exists to avoid redundant downloads logs
            nltk.download(package, download_dir=nltk_data_dir, quiet=True)
            print(f"    - {package}: OK")
        except Exception as e:
            print(f"    - {package}: Failed ({e})")

if __name__ == "__main__":
    download_nltk_data()
