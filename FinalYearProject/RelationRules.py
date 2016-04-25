# To match only desired words use \sword\s
# To get all the other token including matched one use .*

#PER ORG
roles=r"""(.*(founder|
	analyst|
	actor|
	artist|
	assistant|
	attender|
	captain|
	(chief\s)?(executive\sofficer)|
	driver|
	doctor|
	director|
	designer|
	employee|
	from|
	investor|
	student|
	teacher|
	finance officer|
	(software\s)?engineer|
	cricketer|
	writer|
	researcher|
	director|
	economist|
	editor|
	executive|
	head|
	lawyer|
	lead(er)?|
	librarian|
	minister|
	mentor|
	member|
	owner|
	player|
	politician
	president|
	programmer|
	producer|
	professor|
	librarian|
	governer|
	speaker|
	Spokes(wo)?man))"""

# PER PER
relation=r"""(.*('s\s)?(wife|	#
	husband|
	son|		# can use \bson\b
	daughter|
	brother|
	sister|
	grandfather|
	grandmother|
	cousin|
	aunt|
	uncle|
	employer|
	supervisor|
	friend|
	love(d)?(r)?
	))
"""
# PER GPE
# PER LOC
personplace=r"""
	(.*(from|		# can use .* to match whole character before the word
	live(s)?|
	resident|
	born|
	('s)?(\b)native(\b)place|
	is(\b)in
	))
"""
# GPE GPE
# LOC LOC
# ORG GPE
distance=r"""(.*(
	\bnear\b
	\bin\b
	))"""
