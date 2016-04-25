#! /usr/bin/python

import nltk,codecs,re
from nltk.sem import relextract
from nltk.corpus import ieer

def extract_entities(text):
	print "called"
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

	

	"""def improve(reldicts):
		for dicts in reldicts:
			print len(nltk.sent_tokenize(dicts['filler']))
	improve(reldicts)
	"""
	#print pairs[0]
	#print pairs[1]
	#print pairs[2]
	#for sent,tree in pairs[0]:
	#	print sent,tree 
		#print('("...%s", %s)' % (" ".join(sent[0][-5:]),tree))
	#tree=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize( nltk.sent_tokenize(text)[24] )))
	#l=[chunk for chunk in tree]
	#print "%s"%docTree
	"""	
	print tree.label()
	print tree.leaves()
	print tree"""

		# The ne_chunk examines the morphology ofa word. Hence in the above sent.lower() [normalized form] wno't work
			#print type(chunk)
			#if isinstance(chunk,nltk.tree.Tree):
			#	print chunk.label(),chunk.leaves()
data="testcorpuspol.txt"#"testcorpusent.txt"#"testcorpus.txt"

def extractRel(reldicts,subjclass,objclass,window,pattern):

	relfilter = lambda x: (x['subjclass'] == subjclass and
        	                 len(x['filler'].split()) <= window and
    	                  pattern.match(x['filler']) and
                           x['objclass'] == objclass)
	for rel in list(filter(relfilter, reldicts)):
		print(relextract.rtuple(rel))
	
dicts=createDoc(codecs.open(data,"r","utf-8").read())
# Match pattern in filler

import RelationRules as rr
ROLES = re.compile(rr.roles, re.VERBOSE)
IN = re.compile(r'.*\bin\b(?!\b.+ing\b)')
FROM=re.compile(r'.*\bfrom\b.*')
pattern=ROLES
subjclass='PERSON'#'ORGANIZATION'
objclass='ORGANIZATION'#'GPE'
window=5
print "====== Relations of ROLES ===="
extractRel(dicts,'PERSON','ORGANIZATION',window,ROLES)
print "====== Relations of IN ======="
extractRel(dicts,'ORGANIZATION','GPE',window,IN)
print "====== From Relation =============="
extractRel(dicts,'PERSON','ORGANIZATION',5,FROM)


RELATION=re.compile(rr.relation,re.VERBOSE)
print "=========== RELATION ============"
extractRel(dicts,'PERSON','PERSON',window,RELATION)

