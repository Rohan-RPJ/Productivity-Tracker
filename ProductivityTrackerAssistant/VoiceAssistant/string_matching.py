# To calculate srting similarity using Cosine Similarity Algorithm

from q_and_a import QandA

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words("english")
print(stopwords)
del(stopwords[stopwords.index("all")])

class CosineSimilarity:
	def __init__(self):
		self.vectors = None
		self.treshold = 0.5

	def cosine_sim_vectors(self,vec1,vec2):
		vec1 = vec1.reshape(1,-1)
		vec2 = vec2.reshape(1,-1)
		return cosine_similarity(vec1,vec2)[0][0]

	def __string_to_vector(self, strings_list):
		vectorizer = CountVectorizer().fit_transform(strings_list)
		self.vectors = vectorizer.toarray()
		print(self.vectors)

	def get_matched_string_index(self, strings_list):
		self.__string_to_vector(strings_list)
		# self.__match_strings()
		max_index = -1
		max_val = 0
		for i in range(len(self.vectors)-1):
			val = self.cosine_sim_vectors(self.vectors[i],self.vectors[-1])
			print(val)
			if val > max_val:
				max_index = i
				max_val = val

		if max_val >= self.treshold:
			return max_index
		else:
			return -1


class QuestionMatching(QandA, CosineSimilarity):
	def __init__(self, ipQue):
		QandA.__init__(self)
		CosineSimilarity.__init__(self)

		self.__ques = self.get_ques()
		self.ipQue = ipQue
		self.__question_index = -1

	def __clean_string(self, text):
		text = ''.join([word for word in text if word not in string.punctuation])
		text = text.lower()
		text = ' '.join([word for word in text.split() if word not in stopwords])

		return text

	def match_question(self): # returns matched question index. index can be whole number if matched else -1.
		cleaned_list = list(map(self.__clean_string, self.__ques))
		ipQueCleaned = list(map(self.__clean_string, [self.ipQue]))
		print(ipQueCleaned)
		cleaned_list.append(ipQueCleaned[0])
		self.__question_index = self.get_matched_string_index(cleaned_list)  # to get the matched question index if probablity above 0.5, else will return -1

	def get_question_index(self):
		return self.__question_index

	def get_matched_ans(self):
		i = self.get_question_index()
		if i != -1:
			return self.get_ans(i)
		return None


