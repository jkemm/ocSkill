from SPARQLWrapper import SPARQLWrapper, JSON

# import oc.config as c

action_words = ["hometown"]
detail_words = ["thal", "innsbruck"]

sparql = SPARQLWrapper('http://graphdb.sti2.at:8080/repositories/kgbook')
sparql.setCredentials('oc1920', 'Oc1920!')
sparql.setReturnFormat(JSON)

SEARCH_FRITZ = """
        PREFIX schema: <http://schema.org/>
            SELECT ?name 
            WHERE {
                ?person schema:name ?name .
                ?person schema:birthDate "1950-01-01" .
            }
        """

SEARCH_WHAT_IS_QUERY = """ PREFIX schema: <http://schema.org/>
            SELECT * 
            WHERE {
                ?x schema:name ?name.
                ?x schema:description ?des .
                FILTER (lcase(str(?name)) = "%s")
            }"""

SEARCH_WHAT_ARE_QUERY = """ PREFIX schema: <http://schema.org/>
            SELECT * 
            WHERE {
                ?x schema:name ?name.
                ?x schema:description ?des .
                FILTER (lcase(str(?name)) = "%s")
            }"""


def what_is_handle(name):
    bindings = search(name, SEARCH_WHAT_IS_QUERY)
    if len(bindings) > 0:
        return bindings[0]['des']['value']
    return "No entry"


def what_are_handle(name):
    bindings = search(name, SEARCH_WHAT_ARE_QUERY)
    if len(bindings) > 0:
        return bindings[0]['des']['value']
    #remoe last element of list -> graphs is now graph
    elif len(search(name[:-1], SEARCH_WHAT_ARE_QUERY)) > 0:
        bindings = search(name[:-1], SEARCH_WHAT_ARE_QUERY)
        return bindings[0]['des']['value']
    #remove last two elements of string -> boxes is now box
    elif len(search(name[:-2], SEARCH_WHAT_ARE_QUERY)) > 0:
        bindings = search(name[:-2], SEARCH_WHAT_ARE_QUERY)
        return bindings[0]['des']['value']

    return "no entry"


def search_fritz():
    sparql.setQuery(SEARCH_FRITZ)
    result = sparql.query().convert()
    bindings = result['results']['bindings']
    n = bindings[0]['name']['value']
    if len(n) > 0:
        return n
    return "fail"


def search(name, query):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return result['results']['bindings']
    return "fail"  # result['results']['bindings']