import os
import subprocess
from collections import defaultdict
import hashlib

# List of repository URLs to clone
REPO_URLS = [
    "https://github.com/rlfagan/juice-shop",
    "https://github.com/rlfagan/repo2"
]

# Directory to clone the repos into
BASE_DIR = "./cloned_repos"

# Function to clone repositories
def clone_repos(repo_urls, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for url in repo_urls:
        repo_name = url.split('/')[-1]
        repo_path = os.path.join(base_dir, repo_name)
        if not os.path.exists(repo_path):
            try:
                print(f"Cloning {repo_name}...")
                subprocess.run(["git", "clone", url, repo_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error cloning {url}: {e}")

# Function to get the lines of code in a file
def get_loc_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()

# Function to calculate the hash of a line of code
def hash_line(line):
    return hashlib.md5(line.encode()).hexdigest()

# Function to find duplicate LOC across repos
def find_duplicate_loc(repo_paths):
    line_hash_map = defaultdict(list)
    total_loc = 0
    duplicate_loc = 0
    unique_lines = set()

    for repo_path in repo_paths:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):  # Adjust for the specific file types you want to check
                    file_path = os.path.join(root, file)
                    try:
                        loc_in_file = get_loc_in_file(file_path)
                        total_loc += len(loc_in_file)
                        
                        for line in loc_in_file:
                            line_hash = hash_line(line.strip())
                            if line_hash in line_hash_map:
                                duplicate_loc += 1
                            line_hash_map[line_hash].append(file_path)
                            unique_lines.add(line_hash)
                    
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    # Normalized (deduplicated) LOC is the number of unique hashes (lines)
    normalized_loc = len(unique_lines)

    return total_loc, duplicate_loc, normalized_loc

# Calculate cost based on LOC (adjust the price per line)
def calculate_cost(total_loc, normalized_loc, price_per_loc):
    cost = normalized_loc * price_per_loc
    return cost

# Main function to run the script
def main():
    # Clone repositories
    clone_repos(REPO_URLS, BASE_DIR)

    # Adjust the price per line of code here
    price_per_loc = 0.10  # Example price per LOC

    # Analyze cloned repositories
    repo_paths = [os.path.join(BASE_DIR, repo.split('/')[-1]) for repo in REPO_URLS]
    total_loc, duplicate_loc, normalized_loc = find_duplicate_loc(repo_paths)
    
    cost = calculate_cost(total_loc, normalized_loc, price_per_loc)

    print(f"Total Lines of Code: {total_loc}")
    print(f"Duplicate Lines of Code: {duplicate_loc}")
    print(f"Normalized (Unique) Lines of Code: {normalized_loc}")
    print(f"Total Cost based on unique LOC: ${cost:.2f}")

if __name__ == "__main__":
    main()
