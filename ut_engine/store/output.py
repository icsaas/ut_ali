#calctopk,filter,mpop
def output_item(output_file, pop):
    fp = open(output_file, "w")
    for item in pop:
        fp.write(item + ' ' + str(pop[item]) + '\n')
    fp.close()

#mans
def output_mans(ans_file, result):
    f = open(ans_file, "w")
    for user in result:
        f.write(user + '\t' + result[user][0])
        for i in xrange(1, len(result[user])):
            f.write(',' + result[user][i]);
        f.write('\n')
    f.close()


#msortpop
def output_msortpop(output_file, matrix):
    fp = open(output_file, "w")
    for user in matrix:
        fp.write(user + " ")
        for i in range(len(matrix[user])):
            fp.write(matrix[user][i] + " ")
        fp.write("\n")
    fp.close()

#mbonus
def output_mbonus(output_file, bonus):
    fp = open(output_file, "w")
    for user in bonus:
        for item in bonus[user]:
            fp.write("%s %s %d\n" % (user, item, bonus[user][item]))
    fp.close()

#mfilterinput
def output_filter(input_file, output_file, months):
    fin = open(input_file)
    fout = open(output_file, "w")
    for line in fin:
        user, item, rank, month, day = line.strip().split(",")
        if not month in months:
            continue
        month = str(4 + int(month) - int(max(months)))
        fout.write("%s,%s,%s,%s,%s\n" % (user, item, rank, month, day))
    fout.close()
    fin.close()

#mlikematrix
def output_likematrix(output_file, matrix):
    fp = open(output_file, "w")
    for user in matrix:
        fp.write(user + ' ')
        items = matrix[user].items()
        line = ["%s:%s" % (str(item[0]), str(item[1])) for item in items]
        fp.write(",".join(line) + "\n")
    fp.close()



