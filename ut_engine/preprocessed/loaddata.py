import collections
def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(line.strip().split(","))
    fp.close()
    return data

def load_user_brandlist(input_file):
	f = open(input_file)
	user_brandlist = {}
	for line in f:
		data = line.split()
		user_brandlist[data[0]] = data[1:]
	f.close()
	return user_brandlist

def load_pop(pop_file):
    pop = {}
    fp = open(pop_file)
    for line in fp:
        item, score = line.split()
        pop[item] = float(score)
    fp.close()
    return pop

def load_action(data_file):
    action = {}
    fp = open(data_file)
    for line in fp:
        user, item, rank, month, day = line.split(',')
        if rank != "1":
            if user in action:
                action[user][item] = 1
            else:
                action[user] = {item : 1}
    fp.close()
    return action

def load_like(like_file):
    like = collections.defaultdict(lambda: collections.defaultdict(float))
    fp = open(like_file)
    for line in fp:
        user = line.split()[0]
        items = line.split()[1].split(",")
        for record in items:
            item, score = record.split(":")
            like[user][item] = float(score)
    fp.close()
    return like


def load_bonus(bonus_file):
    bonus = collections.defaultdict(lambda: collections.defaultdict(int))
    fp = open(bonus_file)
    for line in fp:
        user, item = line.split()[0], line.split()[1]
        bonus[user][item] = int(line.split()[2])
    fp.close()
    return bonus

def load_topk(input_file):
    topk = {}
    f = open(input_file)
    for line in f:
        user, k = line.split()
        topk[user] = int(k)
    f.close()
    return topk