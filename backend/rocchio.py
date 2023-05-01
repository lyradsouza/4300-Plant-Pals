from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def rocchio(query, descriptions, plant_ids, relevant_descs, irrelevant_descs, a=0.8, b=0.3, c=0.3, clip = False):


    plant_desc_to_id = d = dict(zip(descriptions, plant_ids))

    n_feats = 5000
    input_doc_matrix = np.empty([len(descriptions) + 1, n_feats])

    tfidf_vec = TfidfVectorizer(stop_words = 'english', min_df = 0.0, 
                                 max_df = 1.0, max_features = n_feats,
                                norm = 'l2')

    doc_list = [d for d in descriptions]
    doc_list.append(query)
    input_doc_matrix = tfidf_vec.fit_transform(doc_list).toarray()


    # Retrieve our initial query
    q0 = input_doc_matrix[-1]
    
    # Set up the term for relevant documents 
    rel = 0
    if len(relevant_descs) > 0:
        dr = np.zeros([len(input_doc_matrix[0])])
        for d in relevant_descs:
            id = plant_desc_to_id[d]
            dr = dr + input_doc_matrix[id]
        rel = b * (dr / len(relevant_descs))

    
    # Set up the term for irrelevant documents 
    irrel = 0
    if len(irrelevant_descs) > 0:
        dnr = np.zeros([len(input_doc_matrix[0])])
        for d in irrelevant_descs:
            id = plant_desc_to_id[d]
            dnr = dnr + input_doc_matrix[id]
        irrel = c * (dnr / len(irrelevant_descs))
    
    
    # Create our revised query 
    q1 = a * q0 + rel - irrel    


    # Clip nonzero values if required
    if clip:
        q1[q1 < 0] = 0

    sims = []
    for i in range(len(descriptions)):
        if type(descriptions[i]) == str:     
          terms_desc = input_doc_matrix[i]
          terms_query = q1
          sims.append(np.dot(terms_desc, terms_query))
        else:
          sims.append(0)
    
    id_sim_dict = dict(zip(plant_ids, sims))
    ranked = sorted(id_sim_dict.items(), key = lambda x:x[1], reverse = True)
    ranked = [x[0] for x in ranked]

    return ranked[:12]
    
            
