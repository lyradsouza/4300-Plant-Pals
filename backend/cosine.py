import math
import re

def tokenize(text):
  """Tokenizes text into lowercase individual terms."""
  return [x for x in re.findall(r"[a-z]+", text.lower())]

def get_all_terms(data, query):
  """"Returns all tokens in the given dataset and query."""
  tokens = tokenize(query)
  for d in data:
    if type(d) == str:
      tokens.extend(tokenize(d))
  return tokens

def doc_to_vec(term_list, terms):
    """Creates count dictionary for dataset."""
    d = {}
    for v in terms:
        d[v] = term_list.count(v)
    return d

def query_to_vec(term_list, terms):
    """Creates count dictionary for query."""
    d = {}
    for v in terms:
        d[v] = term_list.count(v)
    return d

def dot(d, q):
    """Returns dot product of A and B."""
    sum=0
    for v in d:
      sum+=d[v] * q[v]
    return sum

def norm(d):
    """Returns norm of A."""
    sum = 0
    for v in d:
        sum += d[v]**2
    return math.sqrt(sum)


def cosine_similarity(query, description, all_descriptions):
    """ Returns cosine similarity between query and description, using dataset.

    """
    allwords = get_all_terms(all_descriptions, query)

    A = query_to_vec(tokenize(query), allwords)
    B = doc_to_vec(tokenize(description), allwords)
    if ((norm(A) * norm(B)) == 0):
      return 0
    return float(dot(A, B)) / (norm(A) * norm(B))

def create_ranked_list(query, descriptions, plant_ids):
    """Calls cosine similarity on all descriptions and returns ranked list of results."""
    sim = []
    for d in descriptions:
      if type(d) == str:
        c = cosine_similarity(query, d, descriptions)
        sim.append(c)
    id_sim_dict = dict(zip(plant_ids, sim))
    ranked = sorted(id_sim_dict.items(), key = lambda x:x[1], reverse = True)
    return [x[0] for x in ranked]
   






    
     


