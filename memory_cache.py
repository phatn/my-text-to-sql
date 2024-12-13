class Cache:
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.data = []

    def add(self, item):
        if len(self.data) >= self.max_size:
            # Remove the oldest item (FIFO behavior)
            self.data.pop(0)
        self.data.append(item)

    def get(self):
        return self.data


cache = Cache()


async def add_to_cache(item):
    cache.add(item)
