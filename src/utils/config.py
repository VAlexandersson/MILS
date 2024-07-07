import yaml
import argparse
from dataclasses import dataclass

@dataclass
class Config:
    max_chunk_size: int
    input_directory: str
    book_title: str
    output_file: str
    log_file: str
    log_level: str
    log_max_size: int
    log_backup_count: int

def load_config(config_file: str) -> Config:
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)
    return Config(**config_data)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process a book into chunks")
    parser.add_argument('--config', default='config.yaml', help='Path to the configuration file')
    parser.add_argument('--max-chunk-size', type=int, help='Override max chunk size')
    parser.add_argument('--input-directory', help='Override input directory')
    parser.add_argument('--book-title', help='Override book title')
    parser.add_argument('--output-file', help='Override output file')
    return parser.parse_args()

def get_config():
    args = parse_arguments()
    config = load_config(args.config)
    
    if args.max_chunk_size:
        config.max_chunk_size = args.max_chunk_size
    if args.input_directory:
        config.input_directory = args.input_directory
    if args.book_title:
        config.book_title = args.book_title
    if args.output_file:
        config.output_file = args.output_file
    
    return config

