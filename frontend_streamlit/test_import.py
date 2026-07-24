import time

start = time.time()

from data.map.world.world_capitals import WORLD_CAPITALS_QUESTIONS

print("Loaded")
print("Questions:", len(WORLD_CAPITALS_QUESTIONS))
print("Time:", time.time() - start)