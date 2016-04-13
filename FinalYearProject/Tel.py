#! /usr/bin/python
import nltk

"""
Find how appropriate arguments to this function
"""
# sents=nltk.corpus.indian.tag_sents()	#all indian tagged sentences

print nltk.corpus.indian.fileids()
# To print all the data about telugu.
#print nltk.corpus.indian.raw('telugu.pos')

#for senteneces in nltk.corpus.indian.sents('telugu.pos'):
#	print sentences

nltk.Text(nltk.corpus.indian.words('telugu.pos')).collocations()


# To print all available telugu words in the corpus
for words in nltk.corpus.indian.words('telugu.pos'):print words

#Collect all tagged sentences 
postaggedsents=nltk.corpus.indian.tagged_sents('telugu.pos')


a=postaggedsents[10]
b=nltk.ne_chunk(a,binary=True)
print type(b)
for w in b:
	for z in w:
		print z,
	print '\n'
#Do named entity chunking
#print nltk.ne_chunk(postaggedsents[:10],binary=True)



# IOB model
# word tag chunk
print "I'm here"
for sents in postaggedsents:
	for wordtagchunk in nltk.chunk.tree2conllstr(nltk.ne_chunk(sents,binary=True)).split('\n'):
		print wordtagchunk.split()
			

#for w in s.split('\n'):
#	print w.split()


