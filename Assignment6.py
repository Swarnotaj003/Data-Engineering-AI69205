# Assignment-6
import spacy
import heapq
import sys

class StructuralSimilarityQuery:
    """
    In this assignment the goal is to find structurally similar sentences to a given sentence. A
    sentence (say s1) is structurally similar to another sentence (say s2), if they both have the
    same named entities as well as have similar parts of speech (POS) sequence present in them.
    """
    def __init__(self):
        """
        Load the spaCy English language model
        """
        self.nlp = spacy.load("en_core_web_sm")

    def read_file(self, filename):
        """
        Reads sentences from a file.
        Returns:
            list of tuples (line_number, sentence).
        """
        sentences = []
        with open(filename, 'r') as file:
            for index, line in enumerate(file, start=1):
                sentence = line.strip()
                if sentence:
                    sentences.append((index, sentence))
        return sentences

    def get_named_entities(self, sentence):
        """
        Extracts named entity types from the given sentence.
        Uses `spaCy's Named Entity Recognition (NER)`.
        """
        doc = self.nlp(sentence)
        entities = set()
        for ent in doc.ents:
            entities.add(ent.label_)
        return entities

    def get_pos_tags(self, sentence):
        """
        Extracts the Part-of-Speech (POS) tags from a sentence.
        Uses `spaCy's POS tagger` to assign a POS tag to each token in the given sentence.
        """
        doc = self.nlp(sentence)
        pos_tags = []
        for token in doc:
            pos_tags.append(token.pos_)
        return pos_tags

    def create_ngrams(self, pos_tags, n=3):
        """
        Creates n-gram chunks from a POS-tag sequence.
        These chunks have an overlap of (n - 2) tags.
        """
        if n <= 0:
            return []
        if len(pos_tags) < n:
            return [pos_tags]

        overlap = n - 2
        ngrams = []
        for i in range(0, len(pos_tags) - n + 1, n - overlap):
            chunk = pos_tags[i: i + n]
            ngrams.append(chunk)
        return ngrams

    def calculate_jaccard_similarity(self, set1, set2):
        """
        Calculates Jaccard similarity between two sets.
        `Jaccard similarity` = (set1 INTERSECTION set2) / (set1 UNION set2)
        """
        union = set1 | set2
        if len(union) == 0:
            return 0.0
        
        intersection = set1 & set2
        return len(intersection) / len(union)

    def calculate_pos_score(self, pos1, pos2, n=3):
        """
        Calculates similarity between POS sequences of two sentences
        `POS score` = sum of Jaccard similarity scores of chunk pairs
        """
        chunks1 = self.create_ngrams(pos1, n)
        chunks2 = self.create_ngrams(pos2, n)
        pos_score = 0.0

        # compare each pair of corresponding chunks
        for chunk1, chunk2 in zip(chunks1, chunks2):
            pos_score += self.calculate_jaccard_similarity(set(chunk1), set(chunk2))
        return pos_score

    def calculate_similarity(self, sentence1, sentence2):
        """
        Calculate structural similarity between two sentences
        `similarity` = `named_entity_score` + `pos_score`
        """
        entities1 = self.get_named_entities(sentence1)
        entities2 = self.get_named_entities(sentence2)
        named_entity_score = self.calculate_jaccard_similarity(entities1, entities2)

        pos1 = self.get_pos_tags(sentence1)
        pos2 = self.get_pos_tags(sentence2)
        pos_score = self.calculate_pos_score(pos1, pos2)

        return named_entity_score + pos_score

    def find_top_k_similar(self, query_sentence, database, k=5):
        """
        Finds the top k structurally similar sentences from the database.
        Returns:
            list of (line_number, score), sorted by score descending.
        """
        heap = []
        for index, sentence in database:
            score = self.calculate_similarity(sentence, query_sentence)
            item = (score, index)
            if len(heap) < k:
                heapq.heappush(heap, item)
            elif score > heap[0][0]:
                heapq.heapreplace(heap, item)

        results = []
        while heap:
            score, index = heapq.heappop(heap)
            results.append((index, score))

        results.reverse()   # descending order
        return results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 Assignment6.py <database_filename> <query_filename>")
        sys.exit(1)

    # USE: python3 Assignment6.py files/database.txt files/query.txt
    _, database_file, query_file = sys.argv
    ssq = StructuralSimilarityQuery()
    database = ssq.read_file(database_file)
    queries = ssq.read_file(query_file)

    print("Query index\tDatabase index\tSimilarity score")

    for query_index, query in queries:
        results = ssq.find_top_k_similar(query, database, k=5)
        for result in results:
            database_index, similarity_score = result
            print(f"{query_index}\t\t{database_index}\t\t{similarity_score:.4f}")
