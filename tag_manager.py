class RefreshableDB:
	def __init__(self):
		self.refresh_interval = 5
	
	def force_refresh(self,query):
		pass

	# Returns None if no recent updates within the refresh_interval
	def last_update(self,query):
		pass

	def add_cache(self, query):
		pass

	def get_cache(self, query):
		pass

	def get(self, query):
		pass

class TagManager(RefreshableDB):
	pass