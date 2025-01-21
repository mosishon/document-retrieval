# Inverted Index and Document Retrieval Project

This repository contains an implementation of an **Inverted Index** for document retrieval, developed as part of an Information Retrieval course. The project demonstrates core concepts in text processing, document indexing, and query handling, with a focus on efficiency and modular design. Below is an overview of the project, its capabilities, and how to use it.

---

## Features

- **Inverted Index Construction**: Efficiently indexes documents and stores term frequencies.
- **TF-IDF Calculation**: Computes Term Frequency-Inverse Document Frequency for terms across documents.
- **Boolean Query Support**:
  - `AND` Query: Finds documents containing all specified terms.
  - `OR` Query: Finds documents containing any of the specified terms.
  - `NOT` Query: Excludes documents containing a specific term.
- **Wildcard Queries**: Supports simple and regex-based wildcard queries (e.g., `*` and `?` patterns).
- **Document Ranking**: Ranks documents based on normalized TF-IDF scores for query terms.
- **Preprocessing Tools**:
  - Tokenization
  - Case normalization (convert text to lowercase/uppercase)
  - Removal of unnecessary characters (e.g., punctuation).

---

## Code Overview

### `InvertedIndex`
The core class that implements an inverted index for efficient document retrieval.

#### Methods:
- **`add_document(doc_id, words)`**: Adds a document with its words to the index.
- **`and_query(*words)`**: Performs an AND query on the index.
- **`or_query(*words)`**: Performs an OR query on the index.
- **`not_query(word)`**: Performs a NOT query to exclude documents.
- **`tf(word, doc_id)`**: Calculates the Term Frequency (TF) of a word in a specific document.
- **`idf(word)`**: Calculates the Inverse Document Frequency (IDF) of a word across documents.
- **`tf_idf(word, doc_id)`**: Computes the TF-IDF score for a word in a specific document.
- **`rank_query(*words)`**: Ranks documents based on their TF-IDF scores for the given words.
- **`wildcard_query(pattern)`**: Retrieves documents matching a wildcard pattern.

### `Document`
A helper class to represent and preprocess documents.

#### Features:
- Handles case normalization, tokenization, and unnecessary character removal.
- Automatically assigns unique IDs to each document.
- Provides properties for document length and word count.

---

## How to Use

### Prerequisites
- Python 3.8+

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/mosishon/document-retrieval.git
   cd inverted-index-project
   ```
2. Prepare text files (`Doc1.txt`, `Doc2.txt`, ..., `Doc10.txt`) and place them in the project directory.

### Running the Code

1. Add documents to the inverted index:
   ```python
   doc1 = Document(open("Doc1.txt").read())
   index = InvertedIndex()
   index.add_document(doc1.doc_id, doc1.remove_unnecessary_cahrs().to_lower().tokenize())
   ```
2. Perform queries:
   - Boolean Query:
     ```python
     results = index.and_query("term1", "term2")
     print("Documents containing both terms:", results)
     ```
   - TF-IDF Ranking:
     ```python
     ranked_results = index.rank_query("term1", "term2")
     print("Ranked Documents:", ranked_results)
     ```
   - Wildcard Query:
     ```python
     wildcard_results = index.wildcard_query("term*")
     print("Documents matching pattern:", wildcard_results)
     ```

---
## Possible Improvements

- **Stopword Removal**: Exclude common words (e.g., "the", "is") to improve retrieval precision.
- **Stemming/Lemmatization**: Normalize words to their root forms.
- **Scalability**: Optimize for large datasets by using external storage systems (e.g., databases).
- **User Interface**: Add a web-based or command-line interface for ease of use.

---

## Skills Demonstrated

- **Python** for object-oriented programming.
- Implementation of fundamental **Information Retrieval** techniques.
- Application of **TF-IDF** for document ranking.
- Regular expressions for wildcard search.
- Modular and extensible code design.

---


