import math

HOROF_EZAFE_JAHAT_HAZF = [".", ",", "!", ","]


class InvertedIndex:
    def __init__(self):
        self.__data_dict: dict[str, set] = {}
        self.__tf_dict: dict[str, dict[int, int]] = {}  # Term Frequency per document
        self.__doc_count = 0  # Total number of documents

    def add_document(self, doc_id: int, words: list[str]):
        """
        Add a document to this inverted index
        """
        self.__doc_count += 1
        word_count = {}

        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
            if word not in self.__data_dict:
                self.__data_dict[word] = set()
            self.__data_dict[word].add(doc_id)

        for word, count in word_count.items():
            if word not in self.__tf_dict:
                self.__tf_dict[word] = {}
            self.__tf_dict[word][doc_id] = count

    def get(self, word: str) -> set:
        return self.__data_dict.get(word, set())

    @property
    def data(self):
        return self.__data_dict

    def combine(self, inverted_index: "InvertedIndex") -> "InvertedIndex":
        """
        Combine two different inverted index to current
        """

        for key, value in inverted_index.__data_dict.items():
            if key in self.__data_dict:
                self.__data_dict[key].update(value)
            else:
                s = set()
                for item in value:
                    s.add(item)
                self.__data_dict[key] = s
        return self

    def from_dict(self, data: dict):
        """
        Create inverted index from dictionary
        """
        for key, value in data.items():
            if key in self.__data_dict:
                self.__data_dict[key].update(value)
            else:
                self.__data_dict[key] = value
        return self

    def and_query(self, *words: str) -> set:
        if not words:
            return set()

        res_set = self.__data_dict.get(words[0], set())
        for word in words[1:]:
            res_set &= self.get(word)
        return res_set

    def or_query(self, *words: str) -> set:
        if not words:
            return set()

        result_set = self.get(words[0])

        for word in words[1:]:
            result_set |= self.get(word)

        return result_set

    def not_query(self, word: str) -> set:
        all_docs = set()
        for doc_set in self.__data_dict.values():
            all_docs.update(doc_set)

        return all_docs - self.get(word)

    def tf(self, word: str, doc_id: int) -> float:
        """Calculate Term Frequency (TF)"""
        return self.__tf_dict.get(word, {}).get(doc_id, 0)

    def idf(self, word: str) -> float:
        """Calculate Inverse Document Frequency (IDF)"""
        doc_count_with_word = len(self.__data_dict.get(word, []))
        if doc_count_with_word == 0:
            return 0
        return math.log(self.__doc_count / doc_count_with_word)

    def tf_idf(self, word: str, doc_id: int) -> float:
        """Calculate TF-IDF for a word in a specific document"""
        return self.tf(word, doc_id) * self.idf(word)

    def rank_query_normalized(self, *words: str) -> list[tuple[int, float]]:
        """Rank documents based on TF-IDF of the query words but normalized result"""
        ranks = self.rank_query(*words)
        max_ranks = max(ranks, key=lambda x: x[1])[1]
        return [(i[0], i[1] / max_ranks) for i in ranks]

    def rank_query(self, *words: str) -> list[tuple[int, float]]:
        """Rank documents based on TF-IDF of the query words"""
        scores = {}
        for word in words:
            for doc_id in self.__data_dict.get(word, []):
                scores[doc_id] = scores.get(doc_id, 0) + self.tf_idf(word, doc_id)

        # Sort documents by score in descending order
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def wildcard_query(self, pattern: str) -> set:
        import re

        regex_pattern = pattern.replace("*", ".*").replace("?", ".")
        regex = re.compile(f"^{regex_pattern}$")

        result_set = set()
        for word in self.__data_dict.keys():
            if regex.match(word):
                result_set.update(self.__data_dict[word])

        return result_set

    def simple_wildcard_query(self, pattern: str) -> set:
        def matches(word: str, pattern: str) -> bool:
            p_idx, w_idx = 0, 0
            while p_idx < len(pattern) and w_idx < len(word):
                if pattern[p_idx] == "*":
                    if p_idx == len(pattern) - 1:
                        return True
                    p_idx += 1
                    while w_idx < len(word) and not matches(
                        word[w_idx:], pattern[p_idx:]
                    ):
                        w_idx += 1
                    return w_idx < len(word)
                elif pattern[p_idx] == "?" or pattern[p_idx] == word[w_idx]:
                    p_idx += 1
                    w_idx += 1
                else:
                    return False

            while p_idx < len(pattern) and pattern[p_idx] == "*":
                p_idx += 1

            return p_idx == len(pattern) and w_idx == len(word)

        result_set = set()
        for word in self.__data_dict.keys():
            if matches(word, pattern):
                result_set.update(self.__data_dict[word])

        return result_set


class Document:
    last_doc_id: int = 0
    all_docs: list["Document"] = []

    def __init__(self, data: str):
        self.__text = data
        self.__unnecessary_chars = HOROF_EZAFE_JAHAT_HAZF
        Document.last_doc_id = Document.last_doc_id + 1
        self.__doc_id = self.last_doc_id
        Document.all_docs.append(self)

    @property
    def length(self):
        return len(self.__text)

    @property
    def words_count(self):
        return len(self.__text.split())

    @property
    def text(self):
        return self.__text

    @property
    def doc_id(self):
        return self.__doc_id

    def to_lower(self) -> "Document":
        """
        convert text to lower case
        """
        self.__text = self.__text.lower()
        return self

    def to_upper(self) -> "Document":
        """
        convert text to upper case
        """
        self.__text = self.__text.upper()
        return self

    def tokenize(self) -> "Document":
        """
        split text to words(tokenize)
        """
        return self.__text.split()

    def remove_unnecessary_cahrs(self) -> "Document":
        """
        Remove  unnecessary characters (HOROF_EZAFE_JAHAT_HAZF)
        """
        # PRE PROCCESS
        for word in self.__unnecessary_chars:
            self.__text = self.__text.replace(word, "")
        return self

    def to_inverted_index(self) -> InvertedIndex:
        """
        Create inverted index from this document
        """
        dic = {}
        val = set([self.doc_id])
        for word in self.tokenize():
            dic[word] = val
        return InvertedIndex().from_dict(dic)


doc1 = Document(open("Doc1.txt").read())
doc2 = Document(open("Doc2.txt").read())
doc3 = Document(open("Doc3.txt").read())
doc4 = Document(open("Doc4.txt").read())
doc5 = Document(open("Doc5.txt").read())
doc6 = Document(open("Doc6.txt").read())
doc7 = Document(open("Doc7.txt").read())
doc8 = Document(open("Doc8.txt").read())
doc9 = Document(open("Doc9.txt").read())
doc10 = Document(open("Doc10.txt").read())

index = InvertedIndex()
index.add_document(doc1.doc_id, doc1.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc2.doc_id, doc2.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc3.doc_id, doc3.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc4.doc_id, doc4.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc5.doc_id, doc5.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc6.doc_id, doc6.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc7.doc_id, doc7.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc8.doc_id, doc8.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc9.doc_id, doc9.remove_unnecessary_cahrs().to_lower().tokenize())
index.add_document(doc10.doc_id, doc10.remove_unnecessary_cahrs().to_lower().tokenize())
