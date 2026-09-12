import spacy
import heapq
import sys

"""
ASSIGNMENT 6

In this assignment the goal is to find structurally similar sentences to a given sentence. A sentence (say s1) is 
structurally similar to another sentence (say s2), if they both have the same named entities as well as have similar 
parts of speech (POS) sequence present in them.

Specifically, the similarity value between s1 and s2 is computed as below:
Score (s1, s2) = 
    (𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑐𝑜𝑚𝑚𝑜𝑛 𝑛𝑎𝑚𝑒𝑑 𝑒𝑛𝑡𝑖𝑡𝑦 𝑡𝑦𝑝𝑒𝑠 𝑏𝑒𝑡𝑤𝑒𝑒𝑛 𝑠1 𝑎𝑛𝑑 𝑠2) / (|𝑢𝑛𝑖𝑜𝑛 𝑜𝑓 𝑛𝑎𝑚𝑒𝑑 e𝑛𝑡𝑖𝑡𝑦 𝑡𝑦𝑝𝑒𝑠 𝑖𝑛 𝑠1 𝑎𝑛𝑑 𝑠2|) 
    + POS score (s1, s2)
    
POS score (s1, s2) = sum of scores of all n-gram chunks (with overlap length n-2) between s1 and s2 based on their POS tags.

Score of two POS tag chunks coming from s1 and s2 is the Jaccard similarity between the POS tags of s1 and s2.

Use any tool (you may feel comfortable with) for named entity recognition and POS tags.
Given a set of sentence and a query sentence, you need to return top 5 sentences structurally similar to the query sentence.
Create your own sample data to test the model.

Input data files (first file containing a set of sentences (call this database file), the second file containing a set of 
query sentences) will be supplied from command line.
The output should be printed on screen as space separated three column file, where the first column is the id/line no of the 
query sentence and the second column is the id/line no of the sentence coming from the database file and third column is the 
similarity score in descending order.
"""

class StructuralSimilarityQuery:
    def __init__(self):
        """
        Load the spaCy English language model
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_cache = dict()    # sentence -> (named entities set, POS tags list)

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

    def analyze_sentence(self, sentence):
        """
        Extracts named entity types and POS tags from the given sentence using spaCy
        """
        if sentence in self.sentence_cache:
            return self.sentence_cache[sentence]

        doc = self.nlp(sentence)
        entities = set()
        pos_tags = []
        for token in doc:
            pos_tags.append(token.pos_)
        for ent in doc.ents:
            entities.add(ent.label_)
        self.sentence_cache[sentence] = (entities, pos_tags)
        return entities, pos_tags

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
        chunk_sets1 = [set(chunk) for chunk in chunks1]
        chunk_sets2 = [set(chunk) for chunk in chunks2]
        pos_score = 0.0

        # compare every pair of chunks
        for chunk1 in chunk_sets1:
            for chunk2 in chunk_sets2:
                pos_score += self.calculate_jaccard_similarity(chunk1, chunk2)
        return pos_score

    def calculate_similarity(self, sentence1, sentence2):
        """
        Calculate structural similarity between two sentences
        `similarity` = `named_entity_score` + `pos_score`
        """
        entities1, pos1 = self.analyze_sentence(sentence1)
        entities2, pos2 = self.analyze_sentence(sentence2)
        named_entity_score = self.calculate_jaccard_similarity(entities1, entities2)
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
