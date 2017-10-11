# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
# 中文情况下，只有通过分词才能产生词云
import jieba
import jieba.analyse as analyse
import os

class FilmcloudPipeline(object):
    def process_item(self, item, spider):

        print item

        # 生成词云
        # 分词
        cut_text = " ".join(jieba.cut(item['summary']))
        # cut_text = " ".join(analyse.extract_tags(item['summary'], topK=20, withWeight=False))

        cut_text += " " + item["name"] + " " + item["score"] + " "+ item["director"]
        font = r'SourceHanSansCN-ExtraLight.otf'
        wordcloud = WordCloud(background_color='black', scale=1.5, font_path=font, width=1000, height=1000,
                              max_words=200).generate(cut_text)

        plt.imshow(wordcloud)
        plt.axis('off')
        # plt.show()
        # 保存图片
        if not os.path.exists(os.curdir + "/cloud_image/"):
            os.mkdir(os.curdir + "/cloud_image/")
        path = os.curdir+"/cloud_image/"
        image_cloud_fileName = u'%s_cloud.jpg'%(item["name"])
        image_cloud_fileName = path + image_cloud_fileName
        print image_cloud_fileName
        print wordcloud.to_file(image_cloud_fileName)

        return item
