from PIL import Image, JpegImagePlugin
import matplotlib.pyplot as plt
import numpy as np
import os
from random import random


class PictureCloud():
    def __init__(self, srcfile='src_50', desfile='des.jpg',resultname='liutao', eta=10):
        #If eta=0, you get a totally unordered figure. On the contrary, if eta=inf, funcion most_likely_prob will
        #convert to function most_likely.
        self.srcfile = srcfile
        self.desfile = desfile
        self.resultname=resultname
        self.eta = eta

    def convert2array(self, rgb):
        if isinstance(rgb, JpegImagePlugin.JpegImageFile):
            rgb = np.array(rgb)
        nparr = []
        gray = 0
        for x in range(len(rgb)):
            x_row = []
            for y in range(len(rgb)):
                x_row.append(int(rgb[x][y][0] * 0.3 + rgb[x][y][1] * 0.59 + rgb[x][y][2] * 0.11))
                gray = gray + int(rgb[x][y][0] * 0.3 + rgb[x][y][1] * 0.59 + rgb[x][y][2] * 0.11)
            nparr.append(x_row)
        return nparr, gray
        pass

    def most_likely(self, target, src):
        # target is np.array,src should be pre calculated.
        diff = []
        for i in range(len(src)):
            diff.append(abs(src[i] - np.sum(target)))
        tmpdic = dict(zip(range(len(src)), diff))
        for i in range(len(src)):
            if tmpdic[i] == min(diff):
                return i
        return -1
        pass

    def most_likely_prob(self, target, src, std_div):
        diff2 = []
        diff = []
        for i in range(len(src)):
            diff2.append(np.exp(-self.eta * (abs(src[i] - np.sum(target)) / std_div)))
        for i in range(len(src)):
            diff.append(diff2[i] / sum(diff2))
        flag = random()
        t = 0
        for i in range(len(src)):
            t = t + diff[i]
            if t >= flag:
                return i
        return -1
        pass

    def pictureCloud(self):
        srcfile = self.srcfile
        path = os.path.join(os.getcwd(), srcfile)
        files = os.listdir(path)
        srcnum = 0
        for file in files:
            if not os.path.isdir(file):
                srcnum = srcnum + 1
        gray = []
        src = []
        npsrc = []
        for i in range(1, srcnum + 1):
            src.append(Image.open(os.path.join(srcfile, str(i) + '.jpg')))
            rgb = np.array(src[i - 1])
            arr, g = self.convert2array(rgb)
            npsrc.append(arr)
            gray.append(g)
        gray_std = np.std(gray)
        srclen_x = src[0].size[0]
        srclen_y = src[0].size[1]

        des = Image.open(self.desfile)
        deslen_x = des.size[0]
        deslen_y = des.size[1]
        plt.figure('des')
        plt.imshow(des)
        plt.axis('off')
        result = np.zeros((deslen_x, deslen_y))
        result_img = des.crop((0,0,int(deslen_x / srclen_x)*srclen_x,int(deslen_y / srclen_y)*srclen_y))
        for i in range(int(deslen_x / srclen_x)):
            for j in range(int(deslen_y / srclen_y)):
                box = (i * srclen_x, j * srclen_y, (i + 1) * srclen_x, (j + 1) * srclen_y)
                block = np.array(des.crop(box))
                small_pic, tempg = self.convert2array(block)
                minDiff = self.most_likely_prob(small_pic, gray, gray_std)
                result_img.paste(src[minDiff], box)
        plt.figure(self.resultname+'_colored')
        plt.imshow(result_img)
        result_img.save(self.resultname+'_colored.jpg')
        plt.axis('off')
        plt.figure(self.resultname+'_gray')
        gray_result = result_img.copy().convert('L')
        plt.imshow(gray_result, cmap='gray')
        result_img.save(self.resultname + '_gray.jpg')
        plt.axis('off')
        plt.show()

if __name__=="__main__":
    testClass=PictureCloud()
    testClass.pictureCloud()