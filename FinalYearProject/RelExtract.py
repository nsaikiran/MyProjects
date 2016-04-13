#! /usr/bin/python
import nltk

from nltk.sem import relextract
from nltk.corpus import ieer

docs=ieer.parsed_docs('NYT_19980315')
tree=docs[1].text

print "%s"%tree



pairs=relextract.tree2semi_rel(tree)
print len(pairs)
print pairs[80]
#exit()
for s,tree in pairs[80:83]:
	print('("...%s", %s)' % (" ".join(s[-5:]),tree))
print "It's ... ",s

for fileid in ieer.fileids(): print fileid

print isinstance(tree,nltk.tree.Tree)

#we can concatenate strings
print "%s"%"".join(["ad","asd"][-5:])
#print tree.label()

#for leaves in tree.leaves():
	#print isinstance(leaves,nltk.tree.Tree)

reldicts = relextract.semi_rel2reldict(pairs)

for r in reldicts:
	print '='*30
	print(r['subclass'],':',r['subjtext'])
	print (r['filler'])
	print (r['objclass'],':',r['objtext'])

print '-'*35

print relextract.rtuple(reldicts[0])
print '(('*40

for k, v in sorted(reldicts[0].items()):
	print(k, '=>', v)
print '))'*40
for k,v in sorted(reldicts[1].items()):
	print(k,'=>',v)

print '%%'*30
print reldicts[0].items()



#Testing..
tree=docs[1].text
print tree.label()
print len(tree.leaves())
print type(tree.leaves()[0])
print tree.leaves()[0]

for l in tree.leaves():
	if isinstance(l,nltk.tree.Tree):
		print l
