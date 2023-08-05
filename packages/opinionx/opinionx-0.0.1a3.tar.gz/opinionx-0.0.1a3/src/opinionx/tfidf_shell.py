import os

from opinionx.tfidf import *

# current_path = os.path.dirname(os.path.realpath(__file__))

def run_tfidf_shell(input_folder,output_folder, user_dict_path="", font_path="",is_html=True):
    # data
    # source_csv_file = f"{current_path}/news_list_chinese.csv"  # contain the FileId field in the csv file
    # raw_data_folder = f"{current_path}/raw_data"  # contain txt files with name starting with FileId, e.g. xxxx-xxxx-xxxx.txt
    list_files=[]
    for file in os.listdir(input_folder):
        list_files.append(os.path.join(input_folder,file))

    # custom dictionary
    keywords_path = f"{output_folder}/keywords_user.pickle"
    # keyword_file_list = "cnki_data.txt;cnki_data1.txt;cnki_data2.txt"
    keyword_file_list_folder = user_dict_path
    keyword_flist=[]
    for file in os.listdir(keyword_file_list_folder):
        keyword_flist.append(file)
    keyword_file_list=';'.join(keyword_flist)

    # corpus data path to save
    save_corpus_path = f"{output_folder}/corpus.pickle"

    # export keywords path
    save_freq_filepath = f"{output_folder}/keywords_freq.pickle"
    save_tfidf_path = f"{output_folder}/keywords_tfidf.pickle"

    run_tfidf_model(list_files,keywords_path,keyword_file_list,keyword_file_list_folder,save_corpus_path,save_freq_filepath,save_tfidf_path,is_html=is_html)

    # export keywords
    export_keywords(save_freq_filepath,save_tfidf_path,f"{output_folder}/keywords_freq.csv",f"{output_folder}/keywords_tfidf.csv")

    export_keywords_dictionary(keyword_file_list, keyword_file_list_folder, f"{output_folder}/keywords_user.csv")

    # create wordcloud
    run_wordcloud(save_corpus_path, f"{output_folder}/word_cloud_auto.jpg",font_path=font_path)

