import numpy as np


class ReadData():

    def __init__(self, path_data):
        self.path = path_data

    @staticmethod
    def read_txt(path):
        with open(path, encoding='utf-8', errors='ignore') as file:
            lines = file.read().splitlines()
            mx = []
            for line in lines:
                mx.append(line.split())
        return mx

    def read_data(self):
        x_fa = [] # matrix of family's datapoint
        x_bu = [] # matrix of business's datapoint

        x_fa_18 = self.read_txt('{}/data_family_2018.txt'.format(self.path)) # matrix of family's datapoint in 2018
        x_fa_19 = self.read_txt('{}/data_family_2019.txt'.format(self.path)) # matrix of family's datapoint in 2019
        x_bu_18 = self.read_txt('{}/data_small_business_2018.txt'.format(self.path)) # matrix of business's datapoint in 2018
        x_bu_19 = self.read_txt('{}/data_small_business_2019.txt'.format(self.path)) # matrix of business's datapoint in 2019
        
        x_fa.extend([x_fa_18, x_fa_19])
        x_bu.extend([x_bu_18, x_bu_19])
        x_fa = np.array(x_fa, dtype = 'float64')
        x_bu = np.array(x_bu, dtype = 'float64')
        return x_fa, x_bu

class CountWeirdo:

    def __init__(self, data):
        self._data = data
        self._mx = np.delete(self._data, 0, 2)
        self._mx_2019 = np.delete(self._mx, 0, 0) # ma tran du lieu nam 2019
        self._mx_2018 = np.delete(self._mx, 1, 0) # ma tran du lieu nam 2018
    
    # Ham tinh xu huong cua khu vuc theo thang
    def Tendency_group(self):
        # Y = len(self._mx)
        N = self._mx.shape[1]
        # M = self._mx.shape[2]

        # thang 1/2019 so voi 12/2018
        c_per = [(self._mx[1, :, 0]*1/self._mx[0, :, 11])] 
        # ty le thang sau so voi thang truoc tu thang 1 nam 2019 den thang 12 nam 2019 
        for i in range(1,12):
            c_per.append(self._mx_2019[0, :, i]/self._mx_2019[0, :, i-1])
        c_per = np.array(c_per) #(kich thuoc 12x1500)
        # print(c_per.shape)
        c = np.sum(c_per, axis = 1)/N # Trung binh muc thay doi cua 12 thang so voi thang truoc do (kich thuoc 12x1)
        c = np.expand_dims(c, axis = 0)
        # print('shape of c'+str(c.shape))
        d0 = (c-1).transpose()*(c_per-1) # d0 la % thay doi cua thang do so voi trung binh 12x1500
        d2 = d0/abs(d0)
        d2 = abs((d2 - 1) / 2 - 0.5) + 1
        # print(d0.shape)
        d00 = abs(c_per.transpose()-c) # d00 la muc chenh lech so voi trung binh  1500x12
        d1 = d00*d2.transpose()
        # print(d1)
        return d1
    
    # Ham tinh chenh lech muc tang theo nam
    def Tendency_year(self):
        # print(self._mx_2018.shape)
        # trung binh muc tang cua 1 gia dinh trong nam (kich thuoc 1500x1)
        c = self._mx_2019/self._mx_2018
        # print("C: {}".format(c))
        c0 = np.squeeze(c, axis= 0)
        # print(c.shape)
        c = np.sum(c0, axis = 1)/12 # trung binh
        # print(c)
        c = np.expand_dims(c, axis= 1)
        # c0 : trung binh cac thang so voi cung thang nam truoc cua moi gia dinh
        # print(c0.shape)

        # sai lech moi thang cua moi gia dinh so voi muc trung binh nam
        d2 = abs(c0-c)
        # print("D2: {}".format(d2))
        return d2
    
    def Tendency_present(self):
        # ti le thay doi thang sau so voi thang truoc tinh tu thang 1 nam 2019
        # print(self._mx_2019[:, :, 0].shape)

        d0 = [(self._mx_2019[:, :, 0]-self._mx_2018[:, :, 11])/self._mx_2018[:, :, 11]]
        for i in range(1,12):
            d0.append((self._mx_2019[:, :, i]-self._mx_2019[:, :, i-1])/self._mx_2019[:, :, i-1])
        d0 = np.array(d0)
        d3 = np.squeeze(d0, axis= 1).transpose()
        # print(d3.shape)
        # print("D3: {}".format(d3))
        return d3
    
    # Ham chuan hoa ma tran, do dai chieu dai nhat la 1
    def Standardized_Matrix(self, matrix):
        
        stand_mx = matrix/np.amax(abs(matrix))
        return stand_mx

    # Chuan hoa 3 ma tran sai so kich thuoc 1500x12 thanh 1 ma tran sai so 1500x12x3
    def Matrix_Tendency(self, d1, d2, d3):
        d1 = self.Standardized_Matrix(d1)
        d1 = np.expand_dims(d1, axis= 2)
        d2 = self.Standardized_Matrix(d2)
        d2 = np.expand_dims(d2, axis= 2)
        d3 = self.Standardized_Matrix(d3)
        d3 = np.expand_dims(d3, axis= 2)

        d4 = np.concatenate((d1, d2, d3), axis = 2)
        # print(d4.shape)
        return d4
    
    # Tinh khoang cach Euclide va lay ra top gia tri cao nhat
    def Get_Tendency(self):
        d1 = self.Tendency_group()
        d2 = self.Tendency_year()
        d3 = self.Tendency_present()
        matrix = self.Matrix_Tendency(d1, d2, d3)
        ten_mx = np.linalg.norm(matrix, axis= 2)
        tb = 4.7*np.sum(ten_mx, axis= None)/(ten_mx.shape[0]*ten_mx.shape[1]) # quy dinh muc bat thuong
        max = np.amax(ten_mx) # lay gia tri bat thuong cao nhat
        # tb3 = (max-tb)/3 +tb # muc bat thuong 3 (hoi bat thuong)
        tb2 = (max-tb)*0.65+tb # muc bat thuong 2 (kha bat thuong) (lon hon muc 2 la rat bat thuong)
        # print(tb)
        # print(tb3)
        # print(tb2)

        top1 = np.sort(ten_mx, axis= None)[-60:]
        # print(len(top1))
        top_mot = []
        top_hai = []
        # top_ba = []

        for i in range(len(top1)):
            if (top1[i] >= tb) and (top1[i] < tb2):
                top_hai.append(top1[i])
            elif top1[i] >= tb2 and top1[i] < max:
                top_mot.append(top1[i])
            # elif top1[i] >= tb2 and top1[i] <= max:
            #     top_mot.append(top1[i])

        try:
            result2 = np.where((ten_mx <= top_hai[-1]) & (ten_mx >= top_hai[0]))
            listOfCoordinates2 = list(zip(result2[0], result2[1]))
        except:
            listOfCoordinates2 = None

        try:
            result1 = np.where((ten_mx <= top_mot[-1]) & (ten_mx >= top_mot[0]))
            listOfCoordinates1 = list(zip(result1[0], result1[1]))
        except:
            listOfCoordinates1 = None

        # try:
        #     result3 = np.where((ten_mx <= top_ba[-1]) & (ten_mx >= top_ba[0]))
        #     listOfCoordinates3= list(zip(result3[0], result3[1]))

        # except:
        #     # result = 0
        #     listOfCoordinates3 = None
        # print(listOfCoordinates)
        return listOfCoordinates1,listOfCoordinates2 # tb, ten_mx[1], top1


#======================================================================================
# kết quả trả về và cách chạy class

# read_data = ReadData('data')
# x_fa, x_bu = read_data.read_data()
# data = x_fa
# # data = x_bu
# test = CountWeirdo(data)
# d1 = test.Tendency_group()
# d2 = test.Tendency_year()
# d3 = test.Tendency_present()
# d4 = test.Matrix_Tendency(d1, d2, d3)
# result = test.Get_Tendency(d4)

# print(result)
