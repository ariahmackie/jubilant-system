#main object is observed by observers
# if main object changes, observers find out via update method()
# main object doesn't care about what observers do
# observers don't pay attention to other observers

#for subscription service, social media, RSS feeds, email

class Subject:
	"""That which is being observed"""
	def __init__(self):
		self._observer_list = []

	def subscribe(self, observer):
		self._observer_list.append(observer)

	def print_observers(self):
		for observer in self._observer_list:
			print("User", observer)

	def notify_observers(self, *args, **kwargs):
		for observer in self._observer_list:
			observer.notify(self, *args, **kwargs)

	def unsubscribe(self, observer):
		self._observer_list.remove(observer)

class Observer:
	def __init__(self, Subject):
		Subject.subscribe(self)

	def notify(self, Subject, *args, **kwargs):
		print ("Received", args, kwargs, "From", Subject)

rss_feed = Subject()

subscriber1 = Observer(rss_feed)
subscriber2 = Observer(rss_feed)
subscriber3 = Observer(rss_feed)
rss_feed.print_observers()

rss_feed.notify_observers("A summary of Today's news. Both subscribers are notified", kw ="From Pittsburg Daily")

rss_feed.unsubscribe(subscriber1)

rss_feed.print_observers()
rss_feed.notify_observers("Second post. Not seen by subscriber 1", kw = "From the Daily")

