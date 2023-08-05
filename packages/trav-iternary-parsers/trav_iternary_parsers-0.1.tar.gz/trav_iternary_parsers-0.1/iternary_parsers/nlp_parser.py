import docx
# NLP spacy libs
import spacy
import re



def docx_parser(docx_file):
    """
    This module will get a DOCX file and scrap all the Day data from it
    and then store it into a dict format, ex: {'Day 1 to singapore': 'XYZ DETAILS'}
    :param: docx_file
    :return: Dict
    """
    try:
        doc = docx.Document(docx_file)
        all_paras = doc.paragraphs

        final_data = {}

        data = ' '.join(text_.text.lower() for text_ in all_paras)
        data_ = data + "day fake"

        # TODO: MODIFIY REGEX. ADD MORE POSSIBLE PATTERNS
        pattern = r"day\s[0-9][0-9]|day\s[0-9]|day[0-9]|day[0-9][0-9]|day\sfake"
        result = re.findall(pattern, data_)

        for count, val in enumerate(result):
            if count == len(result) - 1:
                break

            ind = data_.index(result[count])
            next_ind = data_.index(result[count + 1])

            day_data = data_[ind:next_ind]
            final_data[result[count]] = day_data

        return final_data

    except Exception as e:
        return e

def location_parser(text_data):
    """
    This module will get a text data and scrap all the locations tags from the text
    :param data:
    :return:
    """

    try:
        nlp_wk = spacy.load('xx_ent_wiki_sm')
        doc = nlp_wk(text_data)
        final_data = {}

        for entity in doc.ents:
            if entity.label_ in final_data.keys():
                final_data[entity.label_].append(entity.text)
            else:
                final_data[entity.label_] = [entity.text]

        if 'LOC' in final_data.keys():
            loc_list = final_data['LOC']
            res = list(set(loc_list))
            final_data['LOC'] = res

        return final_data

    except Exception as e:
        return e


# obj = DataParser()

# r1 = obj.docx_parser(
#     docx_file=r'D:\Downloads\Korea 7days_August 2021- March 2022.docx')

# # r2 = obj.location_parser(text_data=r1['day7'])
# print(r1)
