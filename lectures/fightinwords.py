import numpy as np
from   sklearn.feature_extraction.text import CountVectorizer
import string
exclude = set(string.punctuation)

def basic_sanitize(in_string):
    '''Returns a very roughly sanitized version of the input string.'''  
    in_string = ''.join([ch for ch in in_string if ch not in exclude])
    in_string = in_string.lower()
    in_string = ' '.join(in_string.split())
    return in_string

def bayes_compare_language(l1, l2, features = None, ngram = 1, prior=.01, prior_weight = None, cv = None, vocab = None):
    '''
    Arguments:
    - l1, l2; a list of strings from each language sample, 
       or a list of index positions corresponding to each sample in the supplied counts matrix
    - features: array of precomputed feature data, if not working from string input
    - ngram; an int describing up to what n gram you want to consider (1 is unigrams,
    2 is bigrams + unigrams, etc). Ignored if a custom CountVectorizer is passed.
    - prior; either a float describing a uniform prior, or a vector describing a prior
    over vocabulary items. If you're using a predefined vocabulary, make sure to specify that
    when you make your CountVectorizer object.
    - prior_weight; if not None, then amount by which to multiply priors after normalizing
    - cv; a sklearn.feature_extraction.text.CountVectorizer object, if desired.
    - vocab; a list of terms corresponding to the columns in features data, if not None

    Returns:
    - A list of length |Vocab| where each entry is a (n-gram, zscore) tuple.'''

    if features is None: # working with strings, not precomputed counts
        l1 = [basic_sanitize(l) for l in l1]
        l2 = [basic_sanitize(l) for l in l2]
        if cv is None:
            cv = CountVectorizer(decode_error = 'ignore', min_df = 10, max_df = .5, ngram_range=(1,ngram),
                    binary = False,
                    max_features = 15000)
            cv.fit(l1+l2)
        counts_mat = cv.transform(l1+l2).toarray()
        vocab_size = len(cv.vocabulary_)
    else:
        counts_mat = features
        vocab_size = counts_mat.shape[1]
    # Now sum over languages...
    print("Vocab size is {}".format(vocab_size))
    if type(prior) is float:
        priors = np.array([prior for i in range(vocab_size)])
    else:
        priors = prior
    z_scores = np.empty(priors.shape[0])
    count_matrix = np.empty([2, vocab_size], dtype=np.float32)
    if features is None:
        count_matrix[0, :] = np.sum(counts_mat[:len(l1), :], axis = 0)
        count_matrix[1, :] = np.sum(counts_mat[len(l1):, :], axis = 0)
    else:
        count_matrix[0, :] = np.sum(counts_mat[l1, :], axis = 0)
        count_matrix[1, :] = np.sum(counts_mat[l2, :], axis = 0)
    #normalize and weight counts and priors if indicated
    # if not normalizing, priors are effectively weighted by wordcount of baseline corpus
    #  relative to wordcount of sample corpora
    if prior_weight:
        priors = priors/np.linalg.norm(priors, ord=1) * prior_weight
        count_matrix = count_matrix/np.linalg.norm(count_matrix, ord=1, axis=1, keepdims=True)
    a0 = np.sum(priors)
    n1 = np.sum(count_matrix[0,:])
    n2 = np.sum(count_matrix[1,:])
    print("Comparing language...")
    for i in range(vocab_size):
        #compute delta
        term1 = np.log((count_matrix[0,i] + priors[i])/(n1 + a0 - count_matrix[0,i] - priors[i]))
        term2 = np.log((count_matrix[1,i] + priors[i])/(n2 + a0 - count_matrix[1,i] - priors[i]))        
        delta = term1 - term2
        #compute variance on delta
        var = 1./(count_matrix[0,i] + priors[i]) + 1./(count_matrix[1,i] + priors[i])
        #store final score
        z_scores[i] = delta/np.sqrt(var)
    if cv:
        index_to_term = {v:k for k,v in cv.vocabulary_.items()}
    else:
        index_to_term = {v:k for v,k in enumerate(vocab)}
    sorted_indices = np.argsort(z_scores)
    return_list = []
    for i in sorted_indices:
        return_list.append((index_to_term[i], z_scores[i]))
    return return_list