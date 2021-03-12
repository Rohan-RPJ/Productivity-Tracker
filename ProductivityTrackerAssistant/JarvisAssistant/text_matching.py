# To calculate srting similarity using Cosine Similarity Algorithm



import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# stopwords = stopwords.words("english")
# print(stopwords)

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
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
		# print(self.vectors)



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
			# print(val)
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