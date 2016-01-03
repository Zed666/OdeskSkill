#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Граббер заданий, который подсчитывает и выводит самые востребованные скиллы с Odesk
"""

#Пустой глобальный скилл словарь
MYSKILLS = {};
#Счетчик количество сграбленного
SX = 0;

#Импорт модулей
from bs4 import BeautifulSoup;
import requests;
import random;
import time;
print "=" * 20;
print "Odesk Skill Grabber";
print "=" * 20;

#Основной цикл, от 1 страницы до последней +1
for x in range(1,56):
	#Засыпаем на определенное время
	SleepRandom = random.randint(1,3);
	print "*" * 10;
	print ("Sleep in %i" % SleepRandom);
	time.sleep(SleepRandom);
	#Запрашиваем страницу
	print ("Parsing page number %i" % x);
	r  = requests.get("https://www.upwork.com/o/jobs/browse/?q=python&page=" + str(x));
	#Запихиваем в суп ответ
	soup = BeautifulSoup(r.text)
	#Ищем поле работы
	for x in soup.findAll("article", {"class": "job-tile js-similar-tile"}):
		#Если есть что сграбили 
		if x.find("h2", {"class": "m-sm-bottom"}).text.strip() != "":
			#Вывод заголовка
			#print ("Grabbing is %s" % x.find("h2", {"class": "m-sm-bottom"}).text.strip());
			#Счетчик
			SX += 1;
		#Пустой список скиллов
		SkillList = [];
		#Ищем все скиллы
		for skill in x.findAll("a", {"class": "o-tag-skill"}):
			#Добавляем его в список
			SkillList.append(skill.text[:-1]);
			#Если список больше 0
		if len(SkillList) > 0:
		#Если этот скилл есть в скилл листе то (тут явный костыль)
			if '\n{{ skill.prettyName }}' in SkillList:
				#Обнуляем скилллист
				SkillList = [];
			else:
				#Иначе проходимся по массиву скиллов
				for Skill in SkillList:
					#Если Скилл есть в глобальном словаре скиллов то
					if Skill in MYSKILLS:
						#Прибавляем к нему 1
						MYSKILLS[Skill] = MYSKILLS[Skill] + 1;
					else:
						#Иначе, записываем навык и прибавляем к нему 1
						MYSKILLS[Skill] = 1;
		#Скиллов нет
		else:
			#Выодим что скиллов нет
			#print ("No Skills %s" % x.find("h2", {"class": "m-sm-bottom"}).text.strip());
			pass;
		#Очищаем список
		SkillList = [];

#Сортируем и выводим глобальный скилл словарь
print "*" * 10;
b = list(MYSKILLS.items());
b.sort(key=lambda item: item[1], reverse=True);
print "*" * 20;
print "Grabbing " + str(SX) + " jobs";
print "*" * 20;
print ("Top 20 skills");
print "*" * 20;
sk = 0;
for item in b:
	#Выводим процент
	print(item[0] +' => '+ str( (item[1] * 100) / SX) + " %");
	#Счетчик топ 20
	sk += 1;
	if sk > 19:
		break;
print "*" * 20;
