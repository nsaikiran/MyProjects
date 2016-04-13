#! /usr/bin/python

import nltk,codecs
data = "testcorpus.txt"#"tester.txt"
"""
for lines in open(data):pass
	#print lines

for sentences in nltk.sent_tokenize(codecs.open(data,"r","utf-8").read()):pass
	#print sentences


sentences = [ sentence for sentence in nltk.sent_tokenize(codecs.open(data,"r","utf-8").read()) ]

taggedsentences=[nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]

#taggedsentences=nltk.pos_tag_sents(sentences)
print taggedsentences[10]
ne_chunked_sentences=[nltk.ne_chunk(taggedsentence) for taggedsentence in taggedsentences]
#ne_chunked_sentences=nltk.ne_chunk_sents(taggedsentences)

#for chunk in  nltk.ne_chunk(taggedsentences):
#	if hasattr(chunk,'node'):
#		print chunk.node,' '.join(c[0] for c in chunk.leaves())
"""

def extract_entities(text):
	print "called"
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
		# The ne_chunk examines the morphology ofa word. Hence in the above sent.lower() [normalized form] wno't work
			#print type(chunk)
			if isinstance(chunk,nltk.tree.Tree):
				print chunk.label(),chunk.leaves()


extract_entities(codecs.open(data,"r","utf-8").read())

"""
print ne_chunked_sentences[10]
ne_chunked_sentences_iob=[nltk.tree2conllstr(ne_chunked_sentence) for ne_chunked_sentence in ne_chunked_sentences]



for sent in ne_chunked_sentences_iob:pass
	#print sent
#print ne_chunked_sentences_iob
t=('w','t','c')
for sentences in ne_chunked_sentences_iob:
	for words in sentences.split('\n'):
		if words.split()[-1] != unicode('O'):pass
		#	print words
"""
"""
t=('w','t','c')
named_entities=[ ]

for dicts in named_entities:
	print dicts 
"""

"""
nltk.tag.pos_tag = nltk.pos_tag Ref:/_modules/nltk/tag.html
"""
"""
to find default tagger of the nltk. like pos_tag.
nltk.tag._POS_TAGGER
"""


