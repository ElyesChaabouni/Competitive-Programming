#This is a simple script to help you create a mashup while also choosing the ratings of the problems.
#It also guarantees that none of the users with the specified problems has solved the problems.

#To use this script, simply modify the arrays containing the ratings pf the problems, 
#and the array containing the handles
import requests as req
import json
import time
import random

#Problem ratings and multiplicities for this example
#Rating - Nb problems
#1800   - 1
#1900   - 4
#2000   - 5
#2100   - 2
#2200   - 2
#2300   - 1

#modify this array to set the number of problems for each rating
ratings = [[1800, 1], [1900, 4], [2000, 5], [2100, 2], [2200, 2], [2300, 1]]

#This array should contain the handles of all the participants in the mashup
handles = ['Handle1', 'Handle2']

with req.Session() as s:
	p = s.get('https://codeforces.com/api/problemset.problems')
	if json.loads(p.text)['status'] != 'OK':
		exit()
	probs = filter(lambda x: ('rating' in x) and ('contestId' in x) and ('index' in  x), json.loads(p.text)['result']['problems'])
	probs1={}
	for x in probs:
		prob_name = str(x['contestId'])+x['index']
		if (x['rating'] not in probs1):
			probs1[x['rating']]=set()
		probs1[x['rating']].add(prob_name)
	#time.sleep(2) #TODO Check if this is needed, in case CF API doesn't accept the second GET request
	solved = set()	
	for handle in handles:
		p = s.get('https://codeforces.com/api/user.status?handle=' + handle)
		if json.loads(p.text)['status'] != 'OK':
			print('Failed to fetch the submissions for handle "' + handle + '"')
			continue
		solved_by_handle = set(map(lambda x: str(x['problem']['contestId'])+x['problem']['index'], filter(lambda x: (x['verdict'] == 'OK') and ('rating' in x['problem']) and ('contestId' in x['problem']) and ('index' in  x['problem']), json.loads(p.text)['result'])))
		for x in solved_by_handle:
			solved.add(x)
	for x in probs1:
		probs1[x] = probs1[x].difference(solved)
	res = []
	for r in ratings:
		res.extend(random.choices(list(probs1[r[0]]), k=r[1]))
	random.shuffle(res)
	print(res)
