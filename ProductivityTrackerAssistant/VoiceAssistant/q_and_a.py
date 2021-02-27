
class QandA:
	def __init__(self):
		with open("ques.txt", "r") as f1:
			qlines=f1.readlines()

		with open("ques.txt", "r") as f1:
			alines=f1.readlines()

		self.__QUES = []
		self.__ANS = []

		for qline in qlines:
			self.__QUES.append(qline.strip())
		for aline in alines:
			self.__ANS.append(aline.strip())

	def get_ques(self):
		return self.__QUES

	def get_ans(self, index):
		return self.__ANS[index]