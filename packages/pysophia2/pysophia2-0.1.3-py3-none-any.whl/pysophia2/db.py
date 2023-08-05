import pandas as pd
import mariadb
import sys
from elasticsearch import Elasticsearch



columns = ['id', 'country', 'media_outlet', 'url', 'title', 'text', 'date', 'year', 'journalist', 'month']

sql_vars={
    "__username__":"",
    "__password__": "",
    "__cursor__":None,
    "__host__": "45.79.130.8",
    "__port__": 14096,
    "__database__":"Sun"

}

elastic_vars = {
    "__ip__" : "45.56.113.162",
    "__port__": 9200,
    "__user__": "elastic",
    "__password__": "uZCxWGE35lD3lhc",
    "__es__": Elasticsearch(
        ["45.56.113.162:9200"],
        http_auth=("elastic",
                   "uZCxWGE35lD3lhc"),
        timeout=60
        )
    
}

############ 0 LOGGING #############
def set_elastic_vars(__ip__=None, __port__=None, __user__= None, __password__= None):
    """Set the variables used for ElasticSearch connection

    Args:
        __ip__ (int, optional): ElasticSearch host ip. Defaults to "None".
        __port__ (int, optional): ElasticSearch port. Defaults to "None".
        __user__ (str, optional): ElastichSearch username. Defaults to "None".
        __password__ (str, optional): ElasticSearch password. Defaults to "None".
        
    Return:
        None
    
    """
    arguments=locals()
    has_changed=False
    global elastic_vars
    for a,b in arguments.items():
        if (b is not None):
            elastic_vars[a]=b
            has_changed=True
    if has_changed:
        host= elastic_vars["__ip__"]+":"+str(elastic_vars["__port__"])
        elastic_vars["__es__"] = Elasticsearch([host],
                                               http_auth=(elastic_vars["__user__"],
                                                          elastic_vars["__password__"]))

def login(__username__="", __password__="", __host__=None, __port__=None, __database__=None): #45.79.130.8 #45.56.109.120
    """login into Sun database through a mariadb sql adapter.

    Args:
        __username__ (str, required): username for database. Defaults to "sophia2api".
        __password__ (str, required): password for database. Defaults to "".
        __host__ (str, optional): host ip. Defaults to "45.79.130.8".
        __port__ (int, optional): host port. Defaults to 14096.
        __database__ (str, optional): database to connect. Defaults to "Sun".
    
    Returns: 
        None
    """

    arguments=locals()
    global sql_vars

    for a,b in arguments.items():
        if (b is not None):
            sql_vars[a]=b
    
    return connect_sun()

def connect_sun():
    """connect to sun
    Returns:
        feedback message
    """
    global sql_vars
    try:
        conn = mariadb.connect(
            user=sql_vars["__username__"],
            password=sql_vars["__password__"],
            host=sql_vars["__host__"],
            port=sql_vars["__port__"],
            database=sql_vars["__database__"]
        )
        sql_vars["__cursor__"] = conn.cursor()
        return "successful connection"
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return "connection could not be established"

def __connection_validator():
    if sql_vars["__cursor__"] is None: sys.exit("connect to the database first with: db.login(user,password)")

############ 1 INFO #############

def list_countries():
    """provides a list with all the countries that currently have media outlets in Sun.
    
    Args:
        __username__ (str, required): username for database. Defaults to "sophia2api".

    Returns:
        [string]: [country_name]
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT DISTINCT country FROM news")
    return [x[0] for x in sql_vars["__cursor__"].fetchall()]

def list_media_outlets(countries=["all"]): 
    """provides a list with all media outlets that currently have media outlets in Sun.

    Returns:
        [string]: [media_outlet]
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    if "all" in countries: countries=list_countries()
    media_outlets=[]
    for country in countries:
        sql_vars["__cursor__"].execute("SELECT DISTINCT media_outlet FROM news WHERE country=?",(country,))
        for media_outlet in sql_vars["__cursor__"].fetchall():
            media_outlets.append((country, media_outlet[0]))
    return pd.DataFrame(media_outlets,columns=["country", "media_outlet_name"])


def stats_countries():
    """Provides a list the countries and it's news quantity in Sun.

    Returns:
        df: country;news_quantity
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT country, count(id) FROM news GROUP BY country")
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "quantity"])
    

def stats_countries_by_date(_from, _to):
    """Provides a list the countries and it's news quantity between a date.
    
     Args:
        __from (string, required): ElasticSearch host ip. It must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): ElasticSearch host ip. It must be passed as a string with the following format: YYYY/MM/DD.
        
    Returns:
        df: country;news_quantity
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT country, count(id) FROM news WHERE date >= ? AND date <= ? GROUP BY country",(_from,_to))
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "quantity"])
    

def stats_media_outlet(country=None):
    """Provides a list the media outlets and it's news quantity in Sun.
        country (string, optional): country name.

    Returns:
        df: media_outlet;news_quantity
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    if country is not None:
        sql_vars["__cursor__"].execute("SELECT country, media_outlet, count(id) FROM news WHERE country = ? GROUP BY media_outlet",(country,))
    else:
        sql_vars["__cursor__"].execute("SELECT country, media_outlet, count(id) FROM news GROUP BY media_outlet")
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "media_outlet_name", "quantity"])


############ 2 DATASETS #############

def last_n(n=1):
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT *, month(date) as month FROM news ORDER BY ID DESC LIMIT ?" , (n,))
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(), columns=columns)

def get_dataset(country, _from, _to, keywords=None, keywords_operator="or", phrase= False):
    """Provides a dataset of news from the specified country in a period between two dates.
    
     Args:
        country (string, required): country from the list_countries. 
        from_ (string, required):  It must be passed as a string with the following format: YYYY/MM/DD.
        to_ (string, required): It must be passed as a string with the following format: YYYY/MM/DD.
        keywords (string, optional): a list of words separated by space. 
        keywords_operator(string, optional): allow match the news that have all the words passed on keywords or just one word is enought to retrieve the news must be or|and 
        
    Returns:
        df: PySophia2DataSet
    """
    global elastic_vars
    
    if phrase:
        must=[{"match_phrase": {
            "text":{"query": keywords
                   }
        }
              }]
    else:
        must=[{"match": {
            "text":{"query": keywords,
                    "operator": keywords_operator}
        }
              }]
        
    
    if keywords==None or keywords=="":
                query = {
            "query": { 
                "bool": {
                    "filter":[
                        {"range":{
                            "date":{
                                "gte": _from,
                                "lt": _to
                                }
                            }
                        },
                        {"term":{
                            "country": country
                            }
                        }
                        ]
                    }
                }
            }
    else:
        
        query = {
            "query": { 
                "bool": {
                    "must": must,
                    "filter":[
                        {"range":{
                            "date":{
                                "gte": _from,
                                "lt": _to
                                }
                            }
                        },
                        {"term":{
                            "country": country
                            }
                        },
                        ]
                    }
                }
            }
                   
                

    res = elastic_vars["__es__"].search(index="news", query=query["query"], size=10000)
    n_news = res['hits']['total']['value']
    if n_news == 10000:
        print("Se encontraron mas de %d noticias, por favor acotar la fecha de busqueda" % n_news)
    else:
        print("Son %d noticias encontradas..." % n_news)
    
    data = {'id_news':[],'country':[],'media_outlet':[],'url':[],'title':[],'text':[],'date':[],'search':[]}
    df = pd.DataFrame(data)
    
    for hit in res['hits']['hits']:
        id_news = hit['_source']['id_news']
        country = hit['_source']['country']
        media_outlet = hit['_source']['media_outlet']
        url = hit['_source']['url']
        title = hit['_source']['title']
        text = hit['_source']['text']
        date = hit['_source']['date']
        search = keywords
    
        new_row = {'id_news':id_news, 'country':country, 'media_outlet':media_outlet, 'url':url, 'title':title, 'text':text, 'date':date, 'search':search}
    
        df = df.append(new_row, ignore_index=True)
    
    return df
    
def export_to_csv(df, name="default"):
    """Export a dataframe to csv file, basically a pandas's to_csv function wrapper.
    
     Args:
        df: dataframe.
        name: desired name for the file. 
    Returns:
        None
    """
    df.to_csv(name,sep=";")
    print("dataset saved as"+name+".csv")
    
## METODOS FUNCIONALIDAD 3

def popularity(sources, _from, _to):
    """provides a dataframe with all the sources and it's popularity between two dates, grouped by month.
    
    Args:
        sources ([string], required): list of sources for get it's popularity
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        dataFrame: dataframe with every source an it's popularity
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    rows=[]
    for name in sources:
        sql_vars["__cursor__"].execute("SELECT s.source_name, SUM(popularity_en), SUM(popularity_es), SUM(popularity_fr), SUM(popularity_it), SUM(popularity_pt), MONTH(popularity_date), YEAR(popularity_date) FROM has_popularity LEFT JOIN source s ON s.id_source = has_popularity.id_source WHERE s.source_name = ? AND popularity_date >= ? AND popularity_date <= ? GROUP BY MONTH(popularity_date), YEAR(popularity_date) ORDER BY (popularity_date)",(name,_from,_to))
        for row in sql_vars["__cursor__"].fetchall():
            rows.append(row)
    return pd.DataFrame(rows,columns=["source","popularity_en","popularity_es","popularity_fr","popularity_it","popularity_pt", "month", "year"])

def mentions(sources=['Gabriel Boric','José Antonio Kast'],_from="2020-01-01",_to="2021-12-31"):
    
    """provides a dataframe with the news for the sources.
    
    Args:
        sources ([string], required): list of sources for get it's news
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        df: PySophia2DataSet
    """
    rows=[]
    for name in sources:
        sql_vars["__cursor__"].execute("SELECT s.source_name, n.id ,n.country, n.media_outlet, n.url, n.title, n.`text`, n.`date` FROM mention  LEFT JOIN source s ON s.id_source=mention.id_source LEFT JOIN news n ON n.id =mention.id_news WHERE s.source_name = ? AND n.`date` >= ? AND n.`date` <= ?",(name,_from,_to))
        for row in sql_vars["__cursor__"].fetchall():
            rows.append(row)
    _df=pd.DataFrame(rows,columns=["source","id_news","country","media_outlet","url","title", "text", "date"])
    _df['date']=_df['date'].astype(str)
    return _df

def list_sources(country = "Chile",_from="2020-01-01",_to="2021-12-31"):
    """provide a list with all the sources for a country in a period between two dates.
    
    Args:
        country (string, required): country.
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        [string]: list with all the sources.
    """
    sources=[]
    sql_vars["__cursor__"].execute("SELECT DISTINCT s.source_name FROM mention LEFT JOIN source s ON s.id_source=mention.id_source LEFT JOIN news n ON n.id =mention.id_news WHERE n.country = ? AND n.`date` >= ? AND n.`date` <= ?",(country,_from,_to))     
    for source in sql_vars["__cursor__"].fetchall():
        sources.append(source)
    return sources

def gender(country = "Chile",_from="2020-01-01",_to="2021-12-31"):
    """provides a dataframe with the quantities of news for eatch gender .
    
    Args:
        country (string, required): country.
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        df: summary dataset
    """
    rows=[]
    sql_vars["__cursor__"].execute("SELECT s.source_gender, COUNT(s.source_gender), MONTH (n.`date`), YEAR(n.`date`) FROM mention LEFT JOIN source s ON s.id_source=mention.id_source LEFT JOIN news n ON n.id =mention.id_news WHERE n.country = ? AND n.`date` >= ? AND n.`date` <= ? GROUP BY MONTH(n.`date`), YEAR(n.`date`)",(country,_from,_to))     
    for row in sql_vars["__cursor__"].fetchall():
        rows.append(row)
    return pd.DataFrame(rows,columns=["gender","news","month","year"])

def top_mentions(country="Chile", top_n=10,_from="2020-01-01",_to="2021-12-31"): 
    """provide a dataframe with the top_n ranking of sources mentioned in a peroid .
    
    Args:
        country (string, required): the country for calculate the ranking.
        top_n (int, required): the lenght of the ranking.
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        df: top n sources list. 
    """
    rows=[]
    sql_vars["__cursor__"].execute("SELECT s.source_name, count(n.id) FROM mention LEFT JOIN source s ON s.id_source = mention.id_source LEFT JOIN news n ON n.id = mention.id_news WHERE n.country = ? AND n.`date` >= ? AND n.`date` <= ? GROUP BY s.source_name ORDER BY count(n.id) DESC LIMIT ?",(country,_from,_to,top_n))     
    for row in sql_vars["__cursor__"].fetchall():
        rows.append(row)
    return pd.DataFrame(rows,columns=["source","mentions"])

def top_popularity(top_n=10,_from="2020-01-01",_to="2021-12-31"): 
    """provide a dataframe with the top_n sources in a peroid .
    
    Args:
        top_n ([int], required): list of sources for get it's news.
        __from (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): it must be passed as a string with the following format: YYYY/MM/DD.
    Returns:
        df: top n sources.
    """
    rows=[]
    sql_vars["__cursor__"].execute("SELECT s.source_name, (SUM(popularity_pt)+SUM(popularity_fr)+SUM(popularity_it)+SUM(popularity_es)+SUM(popularity_en)) AS TotalPop FROM has_popularity LEFT JOIN source s ON s.id_source = has_popularity.id_source WHERE popularity_date >= ? AND popularity_date <= ? GROUP BY s.source_name ORDER BY TotalPop DESC LIMIT ?",(_from,_to,top_n))     
    for row in sql_vars["__cursor__"].fetchall():
        rows.append(row)
    return pd.DataFrame(rows,columns=["source","popularity"])
