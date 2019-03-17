#!/usr/bin/env python3

import re


def make_stat(filename):
    stat = {'M': {}, 'F': {}}
    year = ''
    years = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            result = re.findall('href=.*/>(.*)</a>|<h3>(.*)</h3>', line)
            # print(result)
            for occurence in result:
                if occurence[0] == '':
                    year = occurence[1]
                    years.append(year)
                    stat['M'][year] = {}
                    stat['F'][year] = {}
                    # print(year, years[year])
                else:
                    name_parts = occurence[0].split()
                    surname = name_parts[0]
                    name = name_parts[1]
                    sex_letter = 'M'
                    if (name[-1] == 'а' or name[-1] == "я" or
                        name == 'Любовь') and name != 'Илья' \
                            and name != 'Никита' and name != 'Лёва':
                        sex_letter = 'F'
                    if stat[sex_letter][year].__contains__(name):
                        stat[sex_letter][year][name] = \
                            stat[sex_letter][year][name] + 1
                    else:
                        stat[sex_letter][year][name] = 1
    return stat


def extract_years(stat):
    return sorted(stat['M'].keys())


def extract_general(stat):
    general_list = []
    male = extract_general_male(stat)
    female = extract_general_female(stat)
    for man in male:
        general_list.append(man)
    for man in female:
        general_list.append(man)

    general = sorted(general_list, reverse=True, key=lambda kv: kv[1])
    return general


def extract_general_male(stat):
    general_dict = {}
    for year in stat['M'].keys():
        for man in stat['M'][year].keys():
            if general_dict.__contains__(man):
                general_dict[man] = general_dict[man] + stat['M'][year][man]
            else:
                general_dict[man] = stat['M'][year][man]
    general = sorted(general_dict.items(), reverse=True, key=lambda kv: kv[1])
    return general


def extract_general_female(stat):
    general_dict = {}
    for year in stat['F'].keys():
        for man in stat['F'][year].keys():
            if general_dict.__contains__(man):
                general_dict[man] = general_dict[man] + stat['F'][year][man]
            else:
                general_dict[man] = stat['F'][year][man]
    general = sorted(general_dict.items(), reverse=True, key=lambda kv: kv[1])
    return general


def extract_year(stat, year):
    year_stat = []
    for man in stat['M'][year]:
        year_stat.append((man, stat['M'][year][man]))

    for man in stat['F'][year]:
        year_stat.append((man, stat['F'][year][man]))

    year_stat = sorted(year_stat, reverse=True, key=lambda kv: kv[1])
    return year_stat


def extract_year_male(stat, year):
    year_stat = []
    for man in stat['M'][year]:
        year_stat.append((man, stat['M'][year][man]))

    year_stat = sorted(year_stat, reverse=True, key=lambda kv: kv[1])
    return year_stat


def extract_year_female(stat, year):
    year_stat = []
    for man in stat['F'][year]:
        year_stat.append((man, stat['F'][year][man]))

    year_stat = sorted(year_stat, reverse=True, key=lambda kv: kv[1])
    return year_stat


if __name__ == '__main__':
    pass
