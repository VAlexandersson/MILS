from typing import List, Tuple, Iterator
from enum import Enum, auto
from utils.logging_setup import logger
from chunk import Chunk
from exceptions import FileProcessingError, TextSplitterError
import json
import os


class MarkdownState(Enum):
    HEADING = auto()
    CONTENT = auto()

class TextSplitter:
    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size
        self.separators = ['\n\n', '\n', '. ']

    def process_markdown_file(self, file_path: str, book_title: str, start_order: int) -> Tuple[List[Chunk], int]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except IOError as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise FileProcessingError(f"Unable to read file {file_path}") from e

        chapter = os.path.basename(file_path).replace('.md', '')
        chunks = []
        chunk_order = start_order

        for heading_list, content in self.parse_markdown(content):
            new_chunks = self.create_chunks(content, book_title, chapter, heading_list, chunk_order)
            chunks.extend(new_chunks)
            chunk_order += len(new_chunks)

        logger.info(f"Processed file {file_path}: created {len(chunks)} chunks")
        return chunks, chunk_order

    def parse_markdown(self, content: str) -> Iterator[Tuple[List[str], str]]:
        lines = content.split('\n')
        state = MarkdownState.CONTENT
        current_content = []
        heading_list = []

        for line in lines:
            if line.startswith('#'):
                if state == MarkdownState.CONTENT and current_content:
                    yield heading_list, '\n'.join(current_content)
                    current_content = []

                state = MarkdownState.HEADING
                level = self.get_heading_level(line)
                heading_text = line.strip('#').strip()
                heading_list = self.update_heading_list(heading_list, (level, heading_text))
            else:
                state = MarkdownState.CONTENT
                if line.strip():  # Only add non-empty lines
                    current_content.append(line)

        if current_content:
            yield heading_list, '\n'.join(current_content)

    @staticmethod
    def get_heading_level(line: str) -> int:
        return len(line.split()[0])

    @staticmethod
    def update_heading_list(heading_list: List[str], new_heading: Tuple[int, str]) -> List[str]:
        new_level, new_text = new_heading
        return heading_list[:new_level-1] + [new_text]

 

    def create_chunks(self, content: str, book_title: str, chapter: str, heading_list: List[str], start_order: int) -> List[Chunk]:
        chunks = []
        current_chunk = ""
        chunk_order = start_order

        for paragraph in content.split('\n\n'):
            if len(current_chunk) + len(paragraph) > self.max_chunk_size and current_chunk:
                chunks.append(self.create_chunk(current_chunk, book_title, chapter, heading_list, chunk_order))
                chunk_order += 1
                current_chunk = ""

            if len(paragraph) > self.max_chunk_size:
                if current_chunk:
                    chunks.append(self.create_chunk(current_chunk, book_title, chapter, heading_list, chunk_order))
                    chunk_order += 1
                    current_chunk = ""
                chunks.extend(self.split_large_paragraph(paragraph, book_title, chapter, heading_list, chunk_order))
                chunk_order += len(chunks) - len(chunks)
            else:
                current_chunk += (paragraph + "\n\n")

        if current_chunk:
            chunks.append(self.create_chunk(current_chunk, book_title, chapter, heading_list, chunk_order))

        return chunks

    def create_chunk(self, content: str, book_title: str, chapter: str, heading_list: List[str], order: int) -> Chunk:
        return Chunk(
            content=content.strip(),
            book=book_title,
            chapter=chapter,
            headings=heading_list.copy(),
            order=order
        )

    def split_large_paragraph(self, paragraph: str, book_title: str, chapter: str, heading_list: List[str], start_order: int) -> List[Chunk]:
        chunks = []
        current_chunk = ""
        chunk_order = start_order

        for sentence in paragraph.split('. '):
            if len(current_chunk) + len(sentence) > self.max_chunk_size and current_chunk:
                chunks.append(self.create_chunk(current_chunk, book_title, chapter, heading_list, chunk_order))
                chunk_order += 1
                current_chunk = ""

            current_chunk += sentence + ". "

        if current_chunk:
            chunks.append(self.create_chunk(current_chunk, book_title, chapter, heading_list, chunk_order))

        return chunks


def save_chunks_to_json(chunks: List[Chunk], output_file: str):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([chunk.__dict__ for chunk in chunks], f, indent=2)
        logger.info(f"Successfully saved {len(chunks)} chunks to {output_file}")
    except IOError as e:
        logger.error(f"Error saving chunks to {output_file}: {str(e)}")
        raise TextSplitterError(f"Unable to save chunks to {output_file}") from e
