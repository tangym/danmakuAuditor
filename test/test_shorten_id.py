import time
import uuid
import json
import shorten_id as sid

shortens = {}
for j in range(50000):
    uid = uuid.uuid1()
    for i in range(128):
        s = sid.shorten(uid.bytes, i + 1)
        if s in shortens:
            shortens[s] += 1
        else:
            shortens[s] = 1
        #print(s, shortens[s])
        #time.sleep(0.0001)
    if j % 500 == 0:
        print(j / 50000 * 100, '%\b\r')

with open('test_shorten_id_dumps.json', 'w') as f:
    f.write(json.dumps(shortens))

count = 0
maximum = 0
for key in shortens:
    if shortens[key] > 1:
        count += 1
        if shortens[key] > maximum:
            maximum = shortens[key]
            max_key = key
print('================')
print('rate: %1.1f%%' % (count / len(shortens) * 100))
print('%d %s' % (count, max_key))



