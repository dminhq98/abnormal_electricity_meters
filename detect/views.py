from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .detect_ath import CountWeirdo, ReadData
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Create your views here.

class Screen1(View):

    def get(self,request):
        read_data = ReadData('data')
        x_fa, x_bu = read_data.read_data()
        # data = x_fa
        test_fa = CountWeirdo(x_fa)
        test_bu = CountWeirdo(x_bu)
        result_fa = test_fa.Get_Tendency()
        result_bu = test_bu.Get_Tendency()
        # print(result)
        with open('data/information_family.txt') as f1, \
                open('data/information_business.txt') as f2:
            f1 = f1.read()
            f1 = f1.split('\n')
            f2 = f2.read()
            f2 = f2.split('\n')
            res = []
            res1=[]
            res2=[]
            stt=0
            for i in range(3):
                if result_fa[i] != None:
                    for j in result_fa[i]:
                        index = j[0]
                        if index not in res1:
                            stt += 1

                            inform = f1[index]
                            inform = inform.split('____')
                            data = {
                                'stt':stt,
                                'name': inform[0],
                                'location': inform[1],
                                'level': i + 1,
                            }
                            res1.append(index)
                            res.append(data)

                if result_bu[i] != None:
                    for j in result_bu[i]:

                        index = j[0]
                        if index not in res2:
                            stt += 1
                            inform = f2[index]
                            inform = inform.split('____')
                            data = {
                                'stt':stt,
                                'name': inform[0],
                                'location': inform[1],
                                'level': i + 1,
                            }
                            res2.append(index)
                            res.append(data)
            # print(res)
        paginator = Paginator(res, 5)

        pageNumber = request.GET.get('page')
        try:
            res = paginator.page(pageNumber)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)
        return render(request,'manhinh1.html',{'res':res})

class Screen2(View):
    def get(self,request):
        list_file=os.listdir('data')
        mouth=[]
        for file in list_file:
            if '.txt' in file and 'data' in file and '2018' not in file:
                mouth.append(file)
        res=[]
        stt=0
        for m in mouth:
            if 'family' in m:
                path=os.path.join('data',m)
                print(path)
                year=m.split('.')[0]
                year=year.split('_')[-1]
                with open(path) as f:
                    f = f.read()
                    mou = f.split('\n')[0]
                    mou = mou.split('   ')
                    mou = mou[1:]
                    for mu in range(1,len(mou)+1):
                        stt+=1
                        data={
                            'stt':stt,
                            'mouth':mu,
                            'year':year,
                        }

                        res.append(data)
        res.reverse()
        for r in res:
            r['stt']=stt-r['stt']+1
        paginator = Paginator(res, 5)

        pageNumber = request.GET.get('page')
        try:
            res = paginator.page(pageNumber)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)

        return render(request,'manhinh2.html',{'res':res})

class Screen3(View):

    def get(self,request,num, format=None):
        # print(request['stt'])
        list_file = os.listdir('data')
        mouth = []
        for file in list_file:
            if '.txt' in file and 'data' in file and '2018' not in file:
                mouth.append(file)
        res = []
        stt = 0
        for m in mouth:
            if 'family' in m:
                path = os.path.join('data', m)
                print(path)
                year = m.split('.')[0]
                year = year.split('_')[-1]
                with open(path) as f:
                    f = f.read()
                    mou = f.split('\n')[0]
                    mou = mou.split('   ')
                    mou = mou[1:]
                    for mu in range(1, len(mou) + 1):
                        stt += 1
                        data = {
                            'stt': stt,
                            'mouth': mu,
                            'year': year,
                        }

                        res.append(data)
        res.reverse()
        for r in res:
            r['stt'] = stt - r['stt'] + 1

        date=res[num-1]
        print(date)
        read_data = ReadData('data')
        x_fa, x_bu = read_data.read_data()
        # data = x_fa
        test_fa = CountWeirdo(x_fa)
        test_bu = CountWeirdo(x_bu)
        result_fa = test_fa.Get_Tendency()
        result_bu = test_bu.Get_Tendency()
        # print(result)
        with open('data/information_family.txt') as f1, \
                open('data/information_business.txt') as f2:
            f1 = f1.read()
            f1 = f1.split('\n')
            f2 = f2.read()
            f2 = f2.split('\n')
            res = []
            stt = 0
            for i in range(3):
                if result_fa[i] != None:
                    for j in result_fa[i]:
                        mouth=j[1]
                        if mouth == date['mouth']:
                            stt += 1
                            index = j[0]
                            inform = f1[index]
                            inform = inform.split('____')
                            data = {
                                'stt': stt,
                                'id':index,
                                'type':1,
                                'name': inform[0],
                                'location': inform[1],
                                'level': i + 1,
                            }
                            # if data not in res:
                            res.append(data)

                if result_bu[i] != None:
                    for j in result_bu[i]:
                        mouth = j[1]
                        if mouth == date['mouth']:
                            stt += 1
                            index = j[0]
                            inform = f2[index]
                            inform = inform.split('____')
                            data = {
                                'stt': stt,
                                'id': index,
                                'type': 2,
                                'name': inform[0],
                                'location': inform[1],
                                'level': i + 1,
                            }
                            # if data not in res:
                            res.append(data)
            # print(res)
        paginator = Paginator(res, 5)

        pageNumber = request.GET.get('page')
        try:
            res = paginator.page(pageNumber)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)
        return render(request,'manhinh3.html' ,{'res': res,'mouth':date['mouth'],'id':num})

class Screen4(View):
    #
    # def get(self,request):
    #
    #     return render(request,'manhinh4.html')

    def post(self, request):
        from ast import literal_eval
        item = request.POST['item']
        mouth=request.POST['mouth']
        id=request.POST['id']
        item=literal_eval(item)
        print(type(item))
        with open('data/data_family_2019.txt') as f1, \
                open('data/data_small_business_2019.txt') as f2:
            if item['type'] == 1:
                f=f1.read()
            else:
                f=f2.read()
            f=f.split('\n')
            m=f[item['id']]
            meter=m.split('   ')[1:]

        return render(request, 'manhinh4.html',{'item':item,'meter':meter,'mouth':mouth,'id':id})