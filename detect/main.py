from detect_ath import CountWeirdo, ReadData

read_data = ReadData('../data')
x_fa, x_bu = read_data.read_data()
data = x_fa
test = CountWeirdo(data)
result = test.Get_Tendency()

print(type(result))

print('top 2: ' + str(result[0]))
print('top 1: ' + str(result[1]))

with open('../data/information_family.txt') as f1,\
     open('../data/information_business.txt') as f2:
    f1=f1.read()
    f1=f1.split('\n')
    res=[]
    for i in range(2):
        if result[i] != None:
            for j in result[i]:
                index=j[0]
                inform=f1[index]
                inform=inform.split('____')
                data = {
                    'name': inform[0],
                    'location': inform[1],
                    'level': i+1,
                }
                res.append(data)
    print(res)
