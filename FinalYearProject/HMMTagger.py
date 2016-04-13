#! /usr/bin/python

import nltk

from nltk.corpus import treebank

from nltk.tag.hmm import *

import codecs
#print treebank.fileids()
tagged_sents=treebank.tagged_sents()

tags=set()
words=set()

sentences=[]
for sent in tagged_sents:
	for i in range(len(sent)):
		word,tag=sent[i]
		word=word.lower()
		words.add(word)
		tags.add(tag)
		sent[i]=(word,tag)
	sentences+=[sent]

tags=list(tags)
#tags=[str(tag) for tag in tags]
words=list(words)
print tags

trainer = HiddenMarkovModelTrainer(tags,words)

#hmm will be a hmm tagger
tagger = trainer.train_supervised(sentences)

def tag(hmm):
	data="testcorpus.txt"#"tester.txt"
	sentences = [ sentence.lower() for sentence in nltk.sent_tokenize(codecs.open(data,"r","utf-8").read()) ]
	sentences_word=[nltk.word_tokenize(sentence) for sentence in sentences]
	
	
	"""
 	labelled_sequences, tag_set, symbols = nltk.tag.hmm.load_pos(20000)
    	trainer = HiddenMarkovModelTrainer(tag_set, symbols)
    	hmm = trainer.train_supervised(labelled_sequences[10:],
                    estimator=lambda fd, bins: LidstoneProbDist(fd, 0.1, bins))
	"""
	tagged_sents=[hmm.tag(sentence) for sentence in sentences_word]
	
	#print tagged_sents[10]
	#print nltk.pos_tag(sentences_word[10])
	

	print tagged_sents[0]
	sentences=[sentence for sentence in nltk.sent_tokenize(codecs.open(data,"r","utf-8").read()) ]
	sentences=[nltk.word_tokenize(sentence) for sentence in sentences]
	
	for index in range(len(sentences)):
		for index2 in range(len(sentences[index])):
			tagged_sents[index][index2]=list(tagged_sents[index][index2])
			tagged_sents[index][index2][0]=sentences[index][index2]
			tagged_sents[index][index2]=tuple(tagged_sents[index][index2])

	print '\n\n\n'
	print tagged_sents[0]
	
	
	print "normal"
	for sent in tagged_sents:
		for chunk in nltk.ne_chunk(sent):
			#print type(chunk)
			if isinstance(chunk,nltk.tree.Tree):
				print chunk.label(),chunk.leaves()

	"""
	for chunk
	ne_chunked_sents=[nltk.ne_chunk(sentence) for sentence in tagged_sents]
	
	print ne_chunked_sents[10]

	ne_chunked_sents_iob=[nltk.tree2conllstr(sentence) for sentence in ne_chunked_sents]
	
	print ne_chunked_sents_iob[10]
	
	for sentences in ne_chunked_sents_iob:
		for words in sentences.split('\n'):print words[-1]
			#if words.split()[-1] != unicode('O'):
			#print words[-1]
	"""	

print "Training done\n"
tag(tagger)
