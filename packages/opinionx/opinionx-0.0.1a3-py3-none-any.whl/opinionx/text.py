import jieba
from nerkit.StanzaApi import StanzaWrapper
from quick_crawler.page import quick_save_csv
sw=StanzaWrapper()

def get_opinion(text,user_dictionary_path="",opinion_words='',lang='zh'):
    if user_dictionary_path!="":
        jieba.load_userdict(user_dictionary_path)
    # opinion_words=['表示','认为','说','介绍','提出','透露','指出','强调','：']
    if len(text)<30:
        return []
    list_sentence=sw.tokenize_sentence(text,lang=lang)
    list_result=[]
    list_seg=[]
    list_ner=[]
    for sentence in list_sentence:
        # print(sentence)
        if len(sentence)<30:
            continue
        sentence=sentence.strip()
        sub_sentences=sentence.split("\n")
        for sub_sentence in sub_sentences:
            sub_sentence=sub_sentence.strip()
            if len(sub_sentence)<=20:
                continue
            ners=sw.ner_chinese(sub_sentence)
            words=jieba.cut(sub_sentence,cut_all=False)
            found_opinion=False
            list_word=[]
            for w in words:
                list_word.append(w)
                if w in opinion_words:
                    found_opinion=True
            found_person=False
            for item in ners:
                if item['type']=='PERSON':
                    found_person=True
                    break
            if found_person and found_opinion and len(list_word)>20:
                list_result.append(sub_sentence)
                # print(sub_sentence)
                # print(' '.join(list_word))
                list_seg.append(list_word)
                list_ner.append(ners)
                # print()
    return list_result,list_seg,list_ner

def add_leader_alias_names(leader_csv_path):
    list_leader_name = open(leader_csv_path, 'r', encoding='utf-8').readlines()
    list_leader_name_alias = []
    for name in list_leader_name:
        name = name.strip()
        if '·' in name:
            names = name.split("·")
            for n in names:
                if len(n) <= 1:
                    continue
                list_leader_name_alias.append(n)
            list_leader_name_alias.append(name)
        else:
            list_leader_name_alias.append(name)
    # print(list_leader_name_alias)
    for n in list_leader_name_alias:
        jieba.add_word(n)
    return list_leader_name_alias


def get_leader_opinions(text,save_path="",search_keywords_path="search_keywords.csv",leader_path="g20_leaders.csv",user_dict_paths=None):
    if user_dict_paths!=None:
        for path in user_dict_paths:
            jieba.load_userdict(path)

    list_leader_name_alias=add_leader_alias_names(leader_path)

    sw = StanzaWrapper(auto_download_en=False, auto_download_zh=False)
    # sw.download(lang='zh',verbose=False)

    search_keywords = [w.strip() for w in open(search_keywords_path, "r", encoding='utf-8').readlines()]
    g20_leaders = [w.strip() for w in open(leader_path, "r", encoding='utf-8').readlines()]
    # print("loading dictionaries...")
    # print(search_keywords)
    # print(g20_leaders)
    # print()

    if len(text)<30:
        return []
    found_keywords=False
    for k in search_keywords:
        if k in text:
            found_keywords=True
            break
    if not found_keywords:
        return []

    list_sentence=sw.tokenize_sentence(text,lang='zh')
    list_result=[]
    for sentence in list_sentence:
        # print(sentence)
        if len(sentence)<20:
            continue
        sentence=sentence.strip()
        sub_sentences=sentence.split("\n")

        for sub_sentence in sub_sentences:
            sub_sentence=sub_sentence.strip()
            # print(sub_sentence)
            if len(sub_sentence)<=20:
                continue
            # ners=sw.ner_chinese(sub_sentence)
            # words=jieba.cut(sub_sentence,cut_all=False)
            list_word=[]
            found_a_leader=False
            found_keyword=False
            first_leader=""
            first_keyword=""
            for name in list_leader_name_alias:
                if name in sub_sentence:
                    found_a_leader=True
                    first_leader=name
                    break
            for k in search_keywords:
                if k in sub_sentence:
                    first_keyword=k
                    found_keyword=True
                    break

            if found_a_leader and found_keyword and len(sub_sentence)>20:
                # print(sub_sentence)
                model={
                    "opinion":sub_sentence,
                    "first_found_keyword":first_keyword,
                    "first_found_leader":first_leader
                }
                list_result.append(model)
                # print(' '.join(list_word))
                # print()
    if save_path!="":
        quick_save_csv(save_path,list_result)

    return list_result