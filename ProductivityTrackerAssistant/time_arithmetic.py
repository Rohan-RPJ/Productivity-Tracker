

class TimeArithmetic:
	"""Perform arithmetic funtions on time of string format 'x-h y-m z-s' """

	def __init__(self):
		self.initial_time = "0-h 0-m 0-s"
		

	def add_time(self, t1, t2):  # time t1 and t2 will be in 'x-h x-m x-s' format
		t1_h, t1_m, t1_s = [int(t.split('-')[0]) for t in t1.split()]
		t2_h, t2_m, t2_s = [int(t.split('-')[0]) for t in t2.split()]
		secs = (t1_s + t2_s)
		mins = (t1_m + t2_m + secs//60)
		hrs = (t1_h + t2_h + mins//60)
		secs %= 60
		mins %= 60
		time_added = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"

		return time_added 


	def sub_time(self, t1, t2):  # returns t1-t2
		t1_h, t1_m, t1_s = [int(t.split('-')[0]) for t in t1.split()]
		t2_h, t2_m, t2_s = [int(t.split('-')[0]) for t in t2.split()]
		secs = (t1_s - t2_s)
		mins = (t1_m - t2_m + secs//60)
		hrs = (t1_h - t2_h + mins//60)
		secs %= 60
		mins %= 60
		time_sub = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"

		return time_sub 