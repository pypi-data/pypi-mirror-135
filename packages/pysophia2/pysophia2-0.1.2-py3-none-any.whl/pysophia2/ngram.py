import numpy as np
from spacy import load as LOAD
from spacy.matcher import Matcher
from collections import Counter
import matplotlib.pyplot as plt
from spacy import util as util
import subprocess
from datetime import datetime


ngram_vars={
    "nlp":"",
    "matcher":""
}
plt.rcParams['figure.figsize'] = [8, 6]
def setup():
    global ngram_vars
    ngram_vars["nlp"] = LOAD('es_core_news_md', disable=['parser','ner','textcat','...'] )
    ngram_vars["matcher"] = Matcher(ngram_vars["nlp"].vocab)

    pattern_1 = [{"POS": "NOUN"},{"LOWER": "de"}, {"POS": "NOUN"}]
    pattern_2 = [{"POS": "NOUN"}, {"POS": "ADJ"}]

    ngram_vars["matcher"].add("NOUN-de-NOUN", [pattern_1])
    ngram_vars["matcher"].add("NOUN-ADJ", [pattern_2])   
    
if not util.is_package("es_core_news_md"):
    subprocess.run("python -m spacy download es_core_news_md")
    print("...instalando el modelo de lenguaje 'es_core_news_md', por favor reiniciar el kernel y vuelva a importar la librería")
else:
    setup()


def get_keywords(dataFrame):
    """Add a new column to the dataFrame with all the keywords defined as NOUN or fit with the spacy Matcher.
    
     Args:
        dataFrame (dataFrame, required): dataFrame with news in PySophia2 structure
        
    Returns:
        None
    """
    new_row=np.zeros(len(dataFrame.index))
    dataFrame['keywords']=new_row
    for index,row in dataFrame.iterrows():
        text=row["text"]
        filteredText=''.strip()
        tokens = ngram_vars["nlp"](text.lower())
        '''tokens = [token
                 for token in tokens
                 if not token.is_stop and not token.is_punct]'''
        for token in tokens:
            if token.pos_ == "NOUN" :
                filteredText=filteredText+str(token.text.lower().strip())+","
                
        matches = ngram_vars["matcher"](tokens)
        for mach_id, start, end in matches:
            span = tokens[start:end]
            filteredText=filteredText+str(span.text.lower().strip())+","
        dataFrame.loc[index,'keywords']=filteredText
        
def get_frequency(dataFrame):
    
    """Create a dictionary with the frequency for the terms in Keyword column.
    
     Args:
        dataFrame (dataFrame, required): dataFrame with news in PySophia2 structure
        
    Returns:
        Dict: it has a Counter with the times that each word appears on the keywords for the news.
    """
    
    if "keywords" not in dataFrame:
        get_keywords(dataFrame)
    concept_freq_total=Counter({})

    for index, row in dataFrame.iterrows():
        arreglo=row["keywords"].split(",")
        arreglo.pop()
        arreglo=list(dict.fromkeys(arreglo))#elimina los duplicados para contar una vez por noticia cada palabra
        concept_freq = Counter(arreglo)
        concept_freq_total = concept_freq_total + concept_freq
    return {"total_news":len(dataFrame),"total_elements": sum(concept_freq_total.values()), "dictionary": concept_freq_total}

def group_by_date(dataFrame, granularity):
    """Group a set of news by a period.
    
     Args:
        dataFrame (dataFrame, required): dataFrame with news in PySophia2 structure
        granularity (string, required): could be day/month/year. Default: Month
        
    Returns:
        group_by: return a pandas groupby struct with all the news grouped by a period.
    """
    if granularity == "month":
        return dataFrame.groupby(by=["month","year"])
    if granularity == "year":
        return dataFrame.groupby(by=["year"])
    if granularity == "day":
        return dataFrame.groupby(by=["date"])
    
    
def calculateDist(dataset,group_by="month"):
    """Calculte the frequency distribution for a pysophia2 dataset grouped in periods.
    
     Args:
        dataset (dataFrame, required): dataFrame with news in PySophia2 structure
        group_by (string, required): could be day/month/year. Default: Month
        
    Returns:
        Sophia2WordDistributionStruct: a struct with the frecuency of keywords for each periods in a set of news.
    """
    if "keywords" not in dataset:
        get_keywords(dataset)
    dataset_=dataset.copy()
    dataset_["month"]=dataset_['date'].apply(lambda x: x.split("-")[1])
    dataset_["year"]=dataset_['date'].apply(lambda x: x.split("-")[0])
    gb_dataset=group_by_date(dataset_, group_by)
    pySophia2WordDistribution = {}
    if group_by == "day":
        for key, ds in gb_dataset:
            pySophia2WordDistribution[datetime.strptime(key, '%Y-%m-%d').strftime("%Y/%m/%d")] = get_frequency(ds)
    elif group_by == "month":
        for (month,year), ds in gb_dataset:
            pySophia2WordDistribution[(str(year)+"/"+str(month))] = get_frequency(ds)
    elif group_by == "year":
        for year, ds in gb_dataset:
            pySophia2WordDistribution[str(year)] = get_frequency(ds)
    else: return "Wrong granularity parameter, please use 'day', 'month' or 'year' as granularity parameter instead of "+group_by
    
    return pySophia2WordDistribution

def view(word_distribution, words, annotate=False, normalize=True): 
    fig, ax = plt.subplots()
    """Graph the frecuency term for a set of words, it could be normalized by the news in each period, or calculated in total times appearances.
    
     Args:
        word_distribution (Sophia2WordDistribution, required): struct calculated through calculateDist function.
        words ([string], required): words to be displayed on the graph.
        annotate (bool,optional): show the point over the graph. Default: False.
        normalize=(bool, optional): allow to normalize the quantity of appearances by the total news in that period. Default: True.
        
    Returns:
        None
    """
    ngram_dictionary={}
    for palabra in words:
        ngram_dictionary[palabra]=[]
        keys=[]
        if normalize==True:
            for key in word_distribution:
                keys.append(key)
                ngram_dictionary[palabra].append(word_distribution[key]["dictionary"][palabra]/word_distribution[key]["total_news"])
        else:    
            for key in word_distribution:
                keys.append(key)
                ngram_dictionary[palabra].append(word_distribution[key]["dictionary"][palabra])
        ax.plot(keys,ngram_dictionary[palabra],label=palabra)
        ax.legend(loc=5, bbox_to_anchor=(1.3, 0.5), fancybox=True, shadow=True )
        ax.set_title("PySophia2 NGramViewer")
        if(annotate):
            for xy in zip(keys, ngram_dictionary[palabra]):                               
                ax.annotate(('%.2f' % xy[1]), xy=xy, textcoords='data')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.tick_params(axis='x', rotation=90)
    
    
def freq(word_distribution,top_n=None, words=None, graph=True, normalize=True):
    
    """return the frequency for a top_n words or a arbitrary array of words. It can be graphed.
    
     Args:
        word_distribution (Sophia2WordDistribution, required): struct calculated through calculateDist function.
        top_n (int,optional): quantity of the top words you want to get.
        words ([string], required): list words.
        graph (bool, optional): activate or deactivate the graph. Default: True
        normalize (bool, optional): activate or deactivate normalization in frequency on the graph. Default: True
        
    Returns:
        None
    """
    concept_freq_total=Counter({})
    total_news=0
    for a in word_distribution:
        concept_freq_total= concept_freq_total + word_distribution[a]["dictionary"]
        total_news=total_news+word_distribution[a]["total_news"]
    if not normalize:
        total_news=1
    if top_n==None and words ==None:
        print("debes pasar como argumento top_n o un arreglo words")
    elif top_n!=None and words !=None:
        print("debes pasar como argumento top_n o un arreglo words, no ambos")
    elif top_n!=None:
        top=concept_freq_total.most_common(top_n)
        if graph:
            fig, ax = plt.subplots()
        
            x = [x[0] for x in top]
            y = [x[1]/total_news for x in top]
            ax.bar(x,y)
            ax.set_title("Term frecuency top %i words" %(top_n))
            ax.tick_params(axis='x', rotation=90)
        return top
    elif words!=None:
        y = []
        wlist=[]
        for word in words:
            y.append(concept_freq_total[word]/total_news)
            wlist.append((word,concept_freq_total[word]))
        if graph:
            fig, ax = plt.subplots()
            ax.bar(words,y)
            ax.set_title("Term frecuency bar graph")
            ax.set_ylabel('Frequency', fontsize=12)
            ax.tick_params(axis='x', rotation=90)
        return wlist
        
        