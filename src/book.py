from text_splitter import TextSplitter, Chunk
from exceptions import TextSplitterError, FileProcessingError
from utils.logging_setup import logger
from typing import List
import os

class Book:
    def __init__(self, directory: str, title: str, splitter: TextSplitter):
        self.directory = directory
        self.title = title
        self.splitter = splitter

    def process(self) -> List[Chunk]:
        all_chunks = []
        next_order = 0

        try:
            markdown_files = sorted([f for f in os.listdir(self.directory) if f.endswith('.md')])
        except OSError as e:
            logger.error(f"Error accessing directory {self.directory}: {str(e)}")
            raise TextSplitterError(f"Unable to access directory {self.directory}") from e

        for file_name in markdown_files:
            file_path = os.path.join(self.directory, file_name)
            try:
                chunks, next_order = self.splitter.process_markdown_file(file_path, self.title, next_order)
                all_chunks.extend(chunks)
            except FileProcessingError as e:
                logger.warning(f"Skipping file {file_path} due to processing error: {str(e)}")
                continue

        logger.info(f"Processed book '{self.title}': created {len(all_chunks)} total chunks")
        return all_chunks
