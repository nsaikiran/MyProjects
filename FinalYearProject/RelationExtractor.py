#! /usr/bin/python

import nltk,codecs,re
from nltk.sem import relextract
from nltk.corpus import ieer

def extract_entities(text):
	tree=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize( nltk.sent_tokenize(text)[24] )))
	pairs=relextract.tree2semi_rel(tree)
	for sent,tree in pairs:	
		 print('("...%s", %s)' % (" ".join(sent[0][-5:]),tree))

	reldicts = relextract.semi_rel2reldict(pairs)

	for r in reldicts:
	        print '='*30
		print(r['subjclass'],':', r['subjtext'])
		print (r['filler'])
		print (r['objclass'],':', r['objtext'])


def createDoc(text):#To create a DOCUMENT by combining all the chunked sentences.
	chunkedSents=list()
	for sent in nltk.sent_tokenize(text):
		chunkedSents+=[chunk for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))]
	docTree=nltk.Tree('DOCUMENT',chunkedSents)
	pairs=relextract.tree2semi_rel(docTree)

	for sent,tree in pairs:
		print '("...%s", %s)' % (' '.join([word for word,tag in sent][-5:]),tree) # To print
	
	reldicts = relextract.semi_rel2reldict(pairs)
	
	return reldicts

	for r in reldicts:
	        print '='*30
		print(r['subjclass'],':', r['subjtext'])
		print (r['filler'])
		print (r['objclass'],':', r['objtext'])


def extractRel(reldicts,subjclass,objclass,window,pattern):
	format="[%s: %r] %s [%s: %r]"
	relfilter = lambda x: (x['subjclass'] == subjclass and
        	                 len(x['filler'].split()) <= window and
    	                  pattern.match(x['filler']) and
                           x['objclass'] == objclass)
	for reldict in list(filter(relfilter, reldicts)):
		#print(relextract.rtuple(rel))
		print format % (reldict['subjclass'],reldict['subjtext'],reldict['untagged_filler'],reldict['objclass'],reldict['objtext'])
	




#data = "testdatapolitics.txt"
#data = "testdataentertainment.txt"
data = "testdatabusiness.txt"

dicts=createDoc(codecs.open(data,"r","utf-8").read())

import RelationRules as rr
window=5 # allowable words in filler

ROLES	= re.compile(rr.roles,re.VERBOSE|re.IGNORECASE)
RELATION= re.compile(rr.relation,re.VERBOSE|re.IGNORECASE)
PERSONPLACE = re.compile(rr.personplace,re.VERBOSE|re.IGNORECASE)
DISTANCE= re.compile(rr.distance,re.VERBOSE|re.IGNORECASE)

print "FILE:: ",data
print "====== Relations of PERSON and ORGANIZATION ===="
extractRel(dicts,'PERSON','ORGANIZATION',window,ROLES)
print "====== Relations of PERSON and PERSON	======="
extractRel(dicts,'PERSON','PERSON',window,RELATION)
print "====== Relations of PERSON and LOCATION	======="
extractRel(dicts,'PERSON','LOCATION',window,PERSONPLACE)
extractRel(dicts,'PERSON','GPE',window,PERSONPLACE)
print "====== Relations related to DISTANCE	======="
extractRel(dicts,'ORGANIZATION','GPE',window,DISTANCE)
extractRel(dicts,'LOCATION','LOCATION',window,DISTANCE)
extractRel(dicts,'GPE','GPE',window,DISTANCE)
