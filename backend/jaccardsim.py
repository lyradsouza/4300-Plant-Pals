import numpy as np
import re

def jaccard_similarity(plant_ids, descriptions, query):
  num_plants = len(plant_ids)
  arr = np.zeros((num_plants, num_plants))
  query_tokens = set(re.findall(r'[A-Za-z]+',query.lower()))
  
  sim_measures = []
  for descrip in descriptions:
    descrip_tokens = set(re.findall(r'[A-Za-z]+',descrip.lower())) 
    numerator = len(query_tokens.intersection(descrip_tokens)) #and
    denominator = len(query_tokens.union(descrip_tokens)) #or
    if denominator == 0:
      sim_measures.append(0)
    else:
      sim_measures.append(numerator/denominator)
    

  id_sim_dict = dict(zip(plant_ids, sim_measures))
  #ranked = sorted(id_sim_dict.items(), key=lambda x:x[1], reverse=True)
  #[x[0] for x in ranked]
  
  return id_sim_dict