import json
from text_splitter import TextSplitter
from book import Book
from utils.config import get_config
from exceptions import TextSplitterError
from utils.logging_setup import logger

def save_chunks_to_json(chunks, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([chunk.__dict__ for chunk in chunks], f, indent=2)
        logger.info(f"Successfully saved {len(chunks)} chunks to {output_file}")
    except IOError as e:
        logger.error(f"Error saving chunks to {output_file}: {str(e)}")
        raise TextSplitterError(f"Unable to save chunks to {output_file}") from e

def main():
    logger.info("Starting book processing")
    config = get_config()
    logger.debug(f"Using configuration: {config}")
    try:
        splitter = TextSplitter(max_chunk_size=config.max_chunk_size)
        book = Book(config.input_directory, config.book_title, splitter)
        chunks = book.process()
        save_chunks_to_json(chunks, config.output_file)
        logger.info("Book processing completed successfully")
    except TextSplitterError as e:
        logger.error(f"An error occurred during processing: {str(e)}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")