#from spacy.lang.es import Spanish


#nlp = Spanish()


#doc = nlp("¿Cómo estás?")

#print(doc.text)



import spacy

nlp = spacy.load("es_core_news_lg")


doc = nlp("Ella comió pizza")

''''
	PRON -> pronombre 
	VERB  -> verbo
	NOUN  -> Sustantivo


	token.text -> devuelve la palabra
	token.pos_ -> devuelve que tipo de palabra es ( SUs , verb, etc)

	token.dep_ -> devuelve la dependencia de loas letras

'''

for token in doc : 
	print(token.text , token.pos_,token.dep_,token.head.text )


''''

	Acceder a las entidades del modelo
'''

doc = nlp("Camila está aqui y tiene un telefono Chile ")

for ent in doc.ents:
	print(ent.text,ent.label_)

'''
	para obtener mas detalles de un tag

	spacy.explain(tag)
'''
#print(spacy.explain("MISC"))





#Importar el matcher
from spacy.matcher import Matcher


matcher = Matcher(nlp.vocab)


# se añade el patron al matcher
#Donde busca el lema "comprar" estableciendo que es un verbo
# y debe contener a su vez un sustantivo
pattern = [
		   {'LEMMA':'comprar'},
		   {"POS":"DET","OP":"?"},
		   {'POS':'NOUN'}
		  ]

"""

	{'OP':"!"} NEGACION : encuentra 0 valores
	{'OP':"?"} Opcional : encuentra 0 o 1 veces
	{'OP':"+"} Encuentra 1 o mas veces
	{'OP':"*"} Encuentra 0 o mas veces 
-

"""



matcher.add("COMPRAR_PATTERN",None,pattern)

doc = nlp("Hola soy camilo , me gusta comprar pelotas . Tambien comprare una pelota roja")

matches = matcher(doc)

for match_id , start , end in matches:
	matched_span = doc[start:end]
	print(matched_span.text)