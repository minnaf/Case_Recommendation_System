import pandas as pd
import numpy as np
import re
import spacy
from gensim.models.doc2vec import Doc2Vec
import string
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en_core_web_lg')

from sklearn.metrics.pairwise import cosine_similarity



def stop_word_remove(tokenized_text):
        token_list = []
        for token in tokenized_text:
            token_list.append(token.text)
            filtered_sentence =[]
        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False:
                    filtered_sentence.append(word)
        return filtered_sentence


def clean_test_input(test_text, model):
    test_input = test_text.lower().translate(str.maketrans('  ', '  ', string.punctuation)).replace('\n', ' ').replace('•', ' ').replace('“', ' ').replace('”', ' ')
    test_input = nlp.tokenizer(test_input)
    test_input = stop_word_remove(test_input)
    test_vector = model.infer_vector(test_input)
    top_10_similar_cases = model.docvecs.most_similar([test_vector])
    input_vector = pd.DataFrame(test_vector).T
    return input_vector



def cosine_text_similarity(text_vector, case_date, combined_df, clean_data_df):
    alpha = -0.07 #weight of date and type of court

    text_similarity = cosine_similarity(combined_df.iloc[:, 2:], text_vector)
    rec_df = pd.DataFrame({'_id': clean_data_df['_id'], 'date': combined_df['decision_date'], 'similarity': list(text_similarity)})
    rec_df['similarity'] = rec_df['similarity'].apply(lambda x: x[0])
    rec_df['date_similarity'] = rec_df['date'].apply(lambda x: abs(x - case_date)/ 100)
    rec_df['tot_similarity'] = rec_df['similarity'] + (alpha * rec_df['date_similarity'])
    rec_df = rec_df.sort_values(by = 'tot_similarity', ascending=False).reset_index().loc[0:15]
    rec_df.drop(['index'], axis = 1, inplace = True)

    _ids = []
    for i in rec_df['_id']:
        _ids.append(i)

    #print(_ids)
    _index_values = []
    for i in _ids:
        temp = (str(clean_data_df.loc[clean_data_df['_id'] == f'{i}']['case_name']))
        temp2 = temp.split()[0]
        _index_values.append(int(temp2))


    case_list = []
    for j, i in enumerate(_index_values):
        case_list.append(f"{j+1} -- {clean_data_df['case_name'][i]}")       

        case_list.append(f"{clean_data_df['majority_opinion'][i]}")
        
    
    return(case_list)
        
