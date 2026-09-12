import numpy as np
import string

"""
ASSIGNMENT 5
Application of Hashing in NLP

Write Python program for the problem below.
You are given a set of text documents and your goal is to find the most similar text document with respect to a query text. 
The similarity is computed between two text documents, 𝑑𝑑1 and 𝑑𝑑2 as follows: 
 similarity(d1, d2) = Σ_{w∈V} p(w|d1) * log(p(w|d1) / p(w|d2))

Where V is the vocabulary (all the words except the stopwords), 𝑝(𝑤|𝑑) is the probability of the word w in d. 
𝑝(𝑤|𝑑)=(number of times w appears in d + 1) / (total number of words in d + |𝑉|)
Where |V| is the number of distinct words in the entire document collection.

Your objective is to represent each document in a hash table/dictionary and when the query comes in, search for each 
query word in each of the documents to find the probability. Finally compute the similarity score. 
You may any other method more efficient than what is outlined above.
The stopword list is given here: https://gist.github.com/sebleier/554280

Input format: Your program will take the following input: 
(i) file (where one line means one document) with the sentences, (ii) The query text.
Output: It will print the most similar document (to the query) on screen.
"""

class DocumentQuerySelector:    
    def __init__(self):
        """
        Fetch the list of English stopwords
        """
        self.stopwords = set()
        with open("files/NLTK_english_stopwords", 'r') as file:
            sw_list = file.read().split()
            for stopword in sw_list:
                self.stopwords.add(stopword)

    def build_vocabulary(self, doc):
        """
        Build the vocabulary of words from the given doc
        """
        voc = {}
        doc = doc.lower()
        doc = doc.translate(str.maketrans("", "", string.punctuation))  # remove punctuations
        words = doc.split()
        for word in words:
            if word in self.stopwords:
                continue
            voc[word] = voc.get(word, 0) + 1
        return voc
    
    def count_total_words(self, voc):
        """
        Count the total words in the given vocabulary
        """
        count = 0
        for word in voc.keys():
            count += voc[word]
        return count

    def similarity_score(self, v1, v2, voc, count1, count2):
        """
        Compute similarity score between vocabularies v1 and v2 of text docs
        given global vocabulary 'voc' and total word count of each vocabulary
        """
        similarity = 0.0
        vocab_size = len(voc)   # count of distinct words in global vocabulary
        for word in voc:
            p_w_given_d1 = (v1.get(word, 0) + 1) / (count1 + vocab_size)
            p_w_given_d2 = (v2.get(word, 0) + 1) / (count2 + vocab_size)
            similarity += p_w_given_d1 * np.log(p_w_given_d1 / p_w_given_d2)
        return similarity
    
    def fetch_most_similar_doc(self, docs, query):
        """
        Fetch the document which is most similar to the query text
        """
        # initialize individual doc representation
        vocabularies = [self.build_vocabulary(doc) for doc in docs]
        word_counts = [self.count_total_words(voc) for voc in vocabularies]

        # total doc representation
        total_doc = ' '.join(docs)
        total_vocabulary = self.build_vocabulary(total_doc)

        # query representation
        query_voc = self.build_vocabulary(query)
        query_count = self.count_total_words(query_voc)

        # to store the most similar doc
        best_doc = ''
        best_similarity = float('inf')

        # compare all docs using similarity score
        for i in range(len(docs)):
            curr_similarity = self.similarity_score(
                query_voc, vocabularies[i], total_vocabulary, query_count, word_counts[i]
            )
            if curr_similarity < best_similarity:
                best_doc = docs[i]
                best_similarity = curr_similarity
        return best_doc


if __name__ == "__main__":
    docs = []
    n = int(input("No. of docs: "))
    for i in range(n):
        doc = input(f"\nEnter doc {i}:\n")
        docs.append(doc)
    query = input("\nQuery text:\n")

    dqs = DocumentQuerySelector()
    best_doc = dqs.fetch_most_similar_doc(docs, query)
    print("\nMost similar doc:\n" + best_doc)