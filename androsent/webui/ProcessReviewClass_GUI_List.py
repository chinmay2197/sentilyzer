#MINIMAL class for GUI
#Subclass of ProcessReviewClass_CLI
#For other comments , more functions and debug notes , refer ProcessReviewClass_CLI


import nltk
#--Class ---------------------------------------------------------------
class ProcessReview:
	#--Variables -------------------------------------------------------
	global debug
	score=0
	debug=0
	global noun_dict
	noun_dict={}
	enhancers_1 = ['generally','usually','quite','exceedingly','extra','inordinately','singularly','significantly','distinctly','particularly','eminently','really','truly','mightily','thoroughly','most','so','too','terrifically','awfully','terribly','devilishly','majorly','seriously','desperately','mega','oh-so','damn','damned','jolly']
	enhancers_2 = ['very','too','always','primarily','extremely','exceptionally','especially','tremendously','immensely','vastly','hugely','extraordinarily','excessively','overly','over','abundantly','outstandingly','decidedly','supremely','highly','remarkably','ultra','frightfully']
	diminishers = ['moderately','averagely','somewhat','rather','fairly','reasonably','comparatively','relatively','to a limited extent/degree','to a certain degree','to some extent','within reason','within limits','tolerably','passably','adequately','satisfactorily; informalpretty','kind of','to a great extent','sort of']
	inverter	= ['not','no']
	inverter_2	= ['never']
	
	useful = ['JJ','JJR','JJS',							#Adjectives
			  'RB','RBR','RBS',							#Adverbs	: comparative and superlative
			  'VB','VBD','VBG','VBN','VBP','VBZ',		#verbs		: enjoyed etc
			  'NN','NNS','NNP','NNPS']					#nouns
											
	ignore = ['no']
	#--Functions --------------------------------------------------------
		
	def __init__(self):								#Bring in lists , cache to memory
		global pos_words
		global neg_words
		global noun_list
		pos_words=open("E:\\androsent\\webui\\positive.txt").read()
		neg_words=open("E:\\androsent\\webui\\negative.txt").read()
		noun_list=open("E:\\androsent\\webui\\noun_list.txt").read()
		noun_list=noun_list.split('\n')
		pos_words=pos_words.split('\n')			#split words from new line
		neg_words=neg_words.split('\n')
		global debug							#To check op :: Refer 10_CLI for running eg
		debug=0
	
                
                
	def preprocess(self,sentence):
		#Change Sentence to lower case
		sentence=sentence.lower()
		#Skip if optimization not required
		if debug==0:
			return sentence
		#Tokenize and remove Useless Words	@noun-identification-cost
		sent=nltk.word_tokenize(sentence)
		tag=nltk.pos_tag(sent)
		
		removed=1
		
		while(removed==1):	#cause tag.remove() shifts the elements ahead, 
							#but for loop does not rewind.		
							#Thus , infinite looping till Removal is possible.	
			removed=0
			for i in tag:
				if i[1] not in self.useful :
					if i[0] not in self.ignore:
						tag.remove(i)
						removed=1
		
		return sentence

	def removeStops(self,tag):
		
		removed=1
		while(removed==1):
			removed=0
			for i in tag:
				if i[1] not in self.useful :
					if i[0] not in self.ignore:
						tag.remove(i)
						removed=1
						
	def findSign(self,x):
		if(x>0):
			return 1
		elif(x<0):
			return -1
		else:
			return 0
	
	def scoreSent(self,sent):						#operate Sentence wise
		modifier=0;
		multiplier=1;
		sent=nltk.word_tokenize(sent)				#Not possible in preprocess cause will remove '.'
		tagged=nltk.pos_tag(sent)
	
		self.removeStops(tagged)					#here cause SENTENCES need to be tagged.
	
		
		noun_present_flag=0
		init_score=self.score
	
		for i in tagged :
			if i[0] in noun_list and noun_present_flag==0:
														#if not first noun in the sentence
				noun=i[0]
				noun_present_flag=1
			elif i[0] in self.inverter:
				multiplier=-1;
			elif i[0] in self.inverter_2:
				multiplier=-1;
				modifier=+2;
			elif i[0] in pos_words:
				self.score=self.score+((2+modifier)*multiplier)
				modifier=0
				multiplier=1
			elif i[0] in neg_words:
				self.score=(self.score+(-2-modifier)*multiplier)
				modifier=0
				multiplier=1
			elif i[0] in self.enhancers_1:
				modifier=+1
			elif i[0] in self.enhancers_2:
				modifier=+2
			elif i[0] in self.diminishers:
                                modifier-=1
		
			global noun_dict
			if(noun_present_flag==1):
				if((noun in noun_dict) == False):
					noun_dict[noun]=(self.score-init_score)		#Add new key-value pair to dict
				else:
					noun_dict[noun]+=(self.score-init_score)
					#Modify value of pair to dict
				init_score=self.score

	def getSentiment(self,review):
		
		
		review=self.preprocess(review)
		sentences=review.split('.')			#Split to sentences
		for sent in sentences :				#Score Each sentence.
			self.scoreSent(sent)
		
		global noun_dict
		retdict = {"OverallScore":self.score , "NounScore":noun_dict}	#return dictionary
		
		self.score=0
		noun_dict={}
		
		return retdict
		
