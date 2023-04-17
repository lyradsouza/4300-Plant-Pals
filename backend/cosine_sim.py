from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Can play around a little with parameters for vectorizer 

def cosine_similarity(query, descriptions, plant_ids):
    n_feats = 5000

    doc_by_vocab = np.empty([len(descriptions) + 1, n_feats])

    tfidf_vec = TfidfVectorizer(stop_words = 'english', min_df = 0.0, 
                                 max_df = 1.0, max_features = n_feats,
                                norm = 'l2')

    doc_list = [d for d in descriptions]
    doc_list.append(query)
    doc_by_vocab = tfidf_vec.fit_transform(doc_list).toarray()

    sims = []
    for i in range(len(descriptions)):
        if type(descriptions[i]) == str:     
          terms_desc = doc_by_vocab[i]
          terms_query = doc_by_vocab[-1]
          sims.append(np.dot(terms_desc, terms_query))
        else:
          sims.append(0)
    
    id_sim_dict = dict(zip(plant_ids, sims))
    ranked = sorted(id_sim_dict.items(), key = lambda x:x[1], reverse = True)
    return [x[0] for x in ranked]

