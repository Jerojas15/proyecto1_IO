
class Number:

	def __init__(self, n=0, M=0):
		self.n = n
		self.M = M

	def __str__(self):
		s = ""
		if(self.n == 0 and self.M == 0):
			return "0"

		if(self.n != 0):
			s += str(self.n)
		if(self.M != 0):
			if(self.M > 0):
				s+= "+"
			s += str(self.M) + "M"

		return s


	def __lt__(self, other):

		if(self.M == other.M):
			return self.n < other.n
		return self.M < other.M

	def __add__(self, other):
		newN = self.n + other.n
		newM = self.M + other.M

		return Number(newN, newM)

	def __iadd__(self, other):
		self.n += other.n
		self.M += other.M

		return self

	def __sub__(self, other):
		newN = self.n - other.n
		newM = self.M - other.M
		
		return Number(newN, newM)

	def __isub__(self, other):
		self.n -= other.n
		self.M -= other.M
		
		return self

	def __mul__(self, other):
		newN = self.n * other.n
		newM = self.M * other.M

		return Number(newN, newM)

	def __imul__(self, other):
		self.n *= other.n
		self.M *= other.M

		return self

	def __truediv__(self, other):
		newN = self.n / other.n
		newM = self.M / other.M

		return Number(newN, newM)

	def __itruediv__(self, other):
		self.n /= other.n
		self.M /= other.M

		return self
