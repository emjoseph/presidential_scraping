import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time
import nltk
import pandas as pd
from nltk.corpus import stopwords

stopwords_english = set(stopwords.words('english'))
word_count_dictionary = {}
word_count_df = pd.DataFrame(columns=['Word', 'Count'])

impeachment_proceeding_date = []
no_words = 0

stop_words_manual = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]
with open('trump_remarks_w_text.json') as trump_remarks_file:
    trump_remarks = json.load(trump_remarks_file)

    for i in range(len(trump_remarks)):
        remark = trump_remarks[i]

        # Only analyzes statements post impeachment
        print(remark['time'])
        if remark['time'] == "Sep 23, 2019":
            print("Pre-Impeachment - Break out")
            break

        if 'text' in remark:
            remark_text = remark['text']

            # Some basic filtering
            remark_text = remark_text.replace('\n', ' ')
            remark_text = remark_text.replace('.', ' .')
            remark_text = remark_text.replace(';', ' ;')
            remark_text = remark_text.replace(':', ' :')
            remark_text = remark_text.replace(',', ' ,')
            remark_text = remark_text.replace('?', ' ?')
            remark_text = remark_text.replace('(', ' (')
            remark_text = remark_text.replace(')', ' )')
            remark_text = remark_text.replace('’', '\'')
            remark_text = remark_text.replace('“', '')
            remark_text = remark_text.replace(u'\xa0', u' ')
            remark_words = remark_text.split(' ')

            for word in remark_words:
                no_words += 1
                word = word.lower()
                if word not in stop_words_manual and len(word) > 3:
                    if word in word_count_dictionary:
                        word_count_dictionary[word] += 1

                        df_index = word_count_df[word_count_df['Word'] == word].index.values.astype(int)[0]
                        word_count_df.loc[df_index, 'Count'] = word_count_df.loc[df_index, 'Count'] + 1

                    else:
                        word_count_dictionary[word] = 1
                        word_count_df = word_count_df.append({"Word": word, "Count": 1}, ignore_index=True)

    print(word_count_dictionary)

    # Save word count dictionary to json file
    with open('trump_word_count.json', 'w') as file:
        json.dump(word_count_dictionary, file, indent=4, ensure_ascii=True)

    word_count_df = word_count_df.sort_values(by=['Count'], ascending=False)
    print(word_count_df)
    word_count_df.to_csv(r'trump_word_count.csv')

    print(f"Total of # of words: {no_words}")


