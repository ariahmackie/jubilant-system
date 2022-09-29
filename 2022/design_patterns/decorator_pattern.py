# what - an object with core functionality has its functionaity altered by other objects decorating it.
# allows for behaviors with multiple options

class DisplayText:
	def __init__(self, txt):
		self._txt = txt
		
	def display(self):
		return self._txt

class CapsDecorator(DisplayText):
	"""Wraps Display Text to make it in all caps"""
	
	def __init__(self,  wrap):
		self._wrap = wrap

	def display(self):
		return self._wrap.display().upper()

class  BoldDecorator(DisplayText):
	def __init__(self, wrap):
		self._wrap = wrap

	def display(self):
		return "<b>{}</b>".format(self._wrap.display())


if __name__ == '__main__':
	original_txt = DisplayText("Hello World")
	decorated_txt = CapsDecorator(BoldDecorator(original_txt))

	print("original text: ",  original_txt.display())
	print("decorated text: ", decorated_txt.display())
