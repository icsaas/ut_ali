import json,os
from collections import defaultdict as ddict
from store.output import output_item,output_mans,output_msortpop,output_mbonus,output_filter,output_likematrix
from preprocessed import dataprocess
from preprocessed.loaddata import load_data,load_user_brandlist,load_pop,load_like,load_action,load_bonus,load_topk

class Model(object):
    def __init__(self, conffilepath='config/config.json',raw_file='../data/t_alibaba_data.csv',outputfile='../data/t_alibaba_data_processed.csv',submit_dir="../output/latest"):
        conffile = file(conffilepath)
        config = json.load(conffile)
        conffile.close()
        self.filter_pop_month = map(lambda x: str(x), config["popmonth"])
        self.filter_like_month = map(lambda x: str(x), config["likemonth"])
        self.min_topk = config["mintopk"]
        self.max_topk = config["maxtopk"]
        self.repeat = config["repeatbuy"]
        self.dynamic = config["dynamic"]
        self.decay = config["decay"]
        self.bonus = config["bonus"]
        self.month_score = config["monthscore"]
        self.rank_score = config["rankscore"]
        dataprocess.format_file(raw_file=raw_file,outputfile=outputfile)
        self.original_input_file = "../data/t_alibaba_data_processed.csv"
        self.submit_dir=submit_dir
    def process_filter(self,filter_type="pop"):
        output_file = "%s/filter_%s_month.csv" % (self.result_dir, filter_type)
        months=" ".join(self.filter_pop_month)
        output_filter(self.original_input_file, output_file, months)
        return output_file

    def process_gen_pop(self, input_file):
        pop_file = "%s/pop.txt" % self.result_dir
        data = load_data(input_file)
        pop = {}
        for record in data:
            pop[record[1]] = 0.0
        for record in data:
            pop[record[1]] += self.month_score[int(record[3])] * self.rank_score[int(record[2])]

        score_sum = 0.0
        for item in pop:
            score_sum += pop[item]
        for item in pop:
            pop[item] /= score_sum
        output_item(pop_file, pop)
        return pop_file

    def process_gen_like(self, input_file):
        output_file = "%s/like.txt" % self.result_dir
        data = load_data(input_file)
        self.rank_score = [0.2, 1.0, 0.5, 0.8]   #amazing thing ,when not using original rank_score
        matrix = ddict(lambda:ddict(float))
        buy = ddict(lambda:ddict(int))
        action = ddict(lambda:ddict(int))
        months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        most_recent_day = max([sum(months[0:int(item[3])]) + int(item[4]) for item in data])

        for record in data:
            user, item, rank, month, day = record
            buy[user][item] += 1 if rank == 1 else 0
            action[user][rank] += 1
        for record in data:
            user, item, rank, month, day = record
            day = sum(months[0:int(month)]) + int(day)
            gain = self.rank_score[int(rank)] * (1.0 \
                   if self.dynamic == 0 or rank == 1   \
                   else max(0.97 ** (action[user][rank] - 1), 0.4)) * (1.0 \
                   if self.decay == 0
                   else 0.99 ** (most_recent_day - day))
            matrix[user][item] += gain
        if self.repeat == 1:
            for user in buy:
                for item in buy[user]:
                    if buy[user][item] == 1:
                        matrix[user][item] -= 0.4
                    elif buy[user][item] > 2:
                        matrix[user][item] += buy[user][item]
        for user in matrix:
            sum_score = sum(matrix[user].values())
            for item in matrix[user]:
                matrix[user][item] /= sum_score

        output_likematrix(output_file, matrix)
        return output_file

    def process_gen_bonus(self, input_file):
        bonus_file = "%s/bonus.txt" % self.result_dir
        months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        bonuses = ddict(lambda: ddict(int))
        data = load_data(input_file)
        most_recent_day = max([sum(months[0:int(item[3])])+int(item[4]) for item in data])
        for record in data:
            if most_recent_day - (sum(months[0:int(record[3])])+int(record[4])) < self.bonus:
                user, item = record[0], record[1]
                bonuses[user][item] += 1
        output_mbonus(output_file=bonus_file, bonus=bonuses)
        return bonus_file

    def process_sort_pop(self,filter_pop_input_file,filter_like_input_file):
        pop_file = self.process_gen_pop(filter_pop_input_file)
        like_file = self.process_gen_like(filter_like_input_file)
        bonus_file = self.process_gen_bonus(filter_like_input_file)
        sort_file = "%s/sort.txt" % self.result_dir
        pop = load_pop(pop_file)
        like = load_like(like_file)
        action = load_action(filter_like_input_file)
        bonus = load_bonus(bonus_file)
        matrix = {}
        for user in action:
            items = []
            bias = sum([pop[item] * like[user][item] for item in action[user]]) * 0.01
            for item in action[user]:
                items.append((pop[item] * like[user][item] + bonus[user][item] * bias, item))
            matrix[user] = map(lambda x: x[1], sorted(items, reverse = True))
        output_msortpop(sort_file, matrix)  #output popular order file
        return sort_file


    def process_gen_topk(self,sort_file,filter_like_input_file):
        topk_file = "%s/topk.txt" % self.result_dir
        data = load_data(filter_like_input_file)
        user_brandlist = load_user_brandlist(sort_file)
        buycnt = {}
        for r in data:
		    user, brand, behavior, month, day = r[0],r[1],r[2],int(r[3]),int(r[4])
		    if user not in buycnt:
			    buycnt[user] = [0, 0, 0, 0, 0, 0]
		    if behavior == '1':
			    buycnt[user][month-4] += 1
			    #add the total buy behavior
			    buycnt[user][5] += 1
        buyrate = {}
        for user in buycnt:
		    buyrate[user] = int((buycnt[user][2] + buycnt[user][3] + buycnt[user][4]) / 2.5)
        result = {}
        for user in user_brandlist:
		    list_len = len(user_brandlist[user])
		    topK = min(list_len, min(self.max_topk, buyrate[user]))
		    if topK < self.min_topk:
			    topK = min(list_len, self.min_topk)
		    result[user] = topK
        output_item(topk_file, result)
        return topk_file

    def process_gen_ans(self,sort_file,topk_file):
        ans_file = "%s/submit.txt" % self.result_dir
        topk = load_topk(topk_file)
        user_brandlist = load_user_brandlist(sort_file)
        result = ddict(list)
        for user in user_brandlist:
            k = topk[user]
            if k == 0:
                continue
            result[user] = user_brandlist[user][:k]
        output_mans(ans_file, result)
        return ans_file

    def clear_files(self, ans_file):
        submit_file = self.submit_dir + \
                '/' + 'result.txt'
        cmd = "mv %s %s" % ( ans_file, submit_file)
        os.system(cmd)
        #cmd = "cp config.json %s" % (submit_path+'/')
        #run_cmd(cmd)
        cmd = "rm -rf %s" % self.result_dir
        os.system(cmd)
    def builddir(self):
        result_dir = "../output/tmp"
        os.mkdir(result_dir)
        return result_dir
    def run(self):
        self.result_dir=self.builddir()
        filter_pop_input_file = self.process_filter("pop")   #process popular items
        filter_like_input_file = self.process_filter("like") #process like items
        sort_file=self.process_sort_pop(filter_pop_input_file,filter_like_input_file)  #sort popular
        topk_file=self.process_gen_topk(sort_file,filter_like_input_file)              #generate topk like items
        ans_file=self.process_gen_ans(sort_file,topk_file)
        self.clear_files(ans_file)


