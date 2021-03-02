# To calculate srting similarity using Cosine Similarity Algorithm



import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words("english")
# print(stopwords)
del(stopwords[stopwords.index("all")])



class CosineSimilarity:

	def __init__(self):
		self.vectors = None
		self.treshold = 0.5


	def cosine_sim_vectors(self, vec1, vec2):
		vec1 = vec1.reshape(1,-1)
		vec2 = vec2.reshape(1,-1)
		return cosine_similarity(vec1,vec2)[0][0]


	def string_to_vector(self, text_list):
		vectorizer = CountVectorizer().fit_transform(text_list)
		self.vectors = vectorizer.toarray()
		print(self.vectors)



class TextMatching(CosineSimilarity):


	def __init__(self, text_list):
		CosineSimilarity.__init__(self)

		self.text_list = text_list
		self.matched_text_index = -1


	def __clean_text(self, text):
		text = ''.join([word for word in text if word not in string.punctuation])
		text = text.lower()
		text = ' '.join([word for word in text.split() if word not in stopwords])

		return text


	def set_matched_text_index(self, cleaned_list):
		self.string_to_vector(cleaned_list)
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
			self.matched_text_index = max_index
		else:
			self.matched_text_index = -1


	def match_text(self, ipQue): # returns matched question index. index can be whole number if matched else -1.
		cleaned_list = list(map(self.__clean_text, self.text_list))
		ipQueCleaned = list(map(self.__clean_text, [ipQue]))
		print(ipQueCleaned)
		cleaned_list.append(ipQueCleaned[0])
		self.set_matched_text_index(cleaned_list)  # to get the matched question index if probablity above 0.5, else will return -1


	def get_matched_text_index(self):
		return self.matched_text_index