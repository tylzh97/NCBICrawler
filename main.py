# !/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = '__Lizhenghao__'

__version__ = '0.0.1'

import requests
import datetime
import os


# NCBI 单个下载
class NCBI(object):
    def __init__(self, cyt):
        self.name = cyt
        self.base_url = 'https://www.ncbi.nlm.nih.gov/nuccore/{0}.1/?report=fasta'.format(cyt)
        self.fasta_url = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={0}&db=nuccore&report=fasta'
        self.data = ''
        self.uid = ''
        if cyt:
            self.get_fasta_url()

    def get_fastauid(self):
        if not self.uid:
            rep = requests.get(self.base_url)
            con = rep.content.decode('utf-8')
            exp = con.index('ncbi_uid=')
            ans = con[exp: exp+30]
            uid = ans[9: ans.index('&')]
            self.uid = uid
        return self.uid

    def get_fasta_url(self):
        if self.uid:
            self.fasta_url = self.fasta_url.format(self.uid)
        else:
            self.fasta_url = self.fasta_url.format(self.get_fastauid())
        return self.fasta_url

    def get_fasta_data(self):
        if not self.data:
            rep = requests.get(self.fasta_url)
            self.data = rep.content.decode('utf-8')
        return self.data

    def save(self, path=os.path.dirname(os.path.abspath(__file__))):
        print(path)
        fpath = os.path.join(path, self.name + '.fasta')
        if not os.path.exists(fpath):
            fp = open(fpath, 'w')
            fp.write(self.get_fasta_data())
            fp.close()
        else:
            raise FileExistsError("file %s is already exists!" % (fpath))
        return True


# NCBI 批量下载
class NCBI_batch(NCBI):
    def __init__(self, cyt_list, poly=False):
        self.cyt_list = cyt_list
        self.poly = poly
        self.ncbi_list = []
        self.get_ncbi_list()

    def get_ncbi_list(self):
        if not self.ncbi_list:
            for i in self.cyt_list:
                self.ncbi_list.append(NCBI(i))
        return self.ncbi_list

    def save_batch(self):
        try:
            if self.poly:
                data = ''
                for i in self.get_ncbi_list():
                    data = data + i.get_fasta_data()
                temp_ncbi = NCBI(0)
                temp_ncbi.name = 'poly_' + str(datetime.datetime.now()).replace(' ', '-').split('.')[0].replace(':', '-')
                temp_ncbi.data = data
                temp_ncbi.save()
            else:
                for i in self.get_ncbi_list():
                    i.save()
        except:
            return False
        return True

    def save(self):
        self.save_batch()


if __name__ == '__main__':
    lst = ['EU839418', 'EU839419', 'EU839420', 'EU839421', 'EU839422',
           'EU839423', 'EU839424', 'EU839425', 'EU839426', 'EU839427',
           'EU839428', 'EU839429', 'EU839430', 'EU839431', 'EU839432',
           'EU839433', 'EU839434', 'EU839435', 'EU839436', 'EU839437',
           'EU839438', 'EU839439', 'EU839440', 'EU839441', 'EU839442',
           'EU839443', 'EU839444', 'EU839445']
    temp = NCBI_batch(lst, poly=True)
    temp.save_batch()
