from __future__ import print_function
import nltk

def init():						#Bring in lists , Ask for debug
	global pos_words
	global neg_words
	#try:
	pos_words=open("E:\\androsent\\webui\\positive.txt").read()
	#except:
	#	print("Positive Database not present")
		#sys.exit()
	#try:
	neg_words=open("E:\\androsent\\webui\\negative.txt").read()
	#except:
	#	print("Negative Database not present")
		#sys.exit()

	global debug

	#while(True):
		#print("Debug? [1/0]:")
	debug=0#input()
		#if(debug=='1' or debug=='0'):
		#	break
	pos_words=pos_words.split('\n')			#split words from new line
	neg_words=neg_words.split('\n')

def prompt():					#Ask Review
	#ORIGINAL = """This is a good movie. This is not bad. This is too great and awesome. Worse. 	best."""
	#print("\nSentence is:")
	#print(ORIGINAL)
	print("Enter A review :")
	ORIGINAL=input()
	return ORIGINAL

#--Class ---------------------------------------------------------------
class ProcessReview:
	#--Variables -------------------------------------------------------
	score=0
	debug=0
	global noun_dict
	noun_dict={"":0}
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
	
	def preprocess(self,sentence):
		#Change Sentence to lower case
		sentence=sentence.lower()
		return sentence

	def findSign(self,x):
		if(x>0):
			return 1
		elif(x<0):
			return -1
		else:
			return 0
	
	def scoreSent(self,sent):			#operate Sentence wise
		modifier=0;
		multiplier=1;
		sent=nltk.word_tokenize(sent)				#Not possible in preprocess cause will remove '.'
		tagged=nltk.pos_tag(sent)
		
		global score
		noun_present_flag=0
		init_score=self.score
	
		for i in tagged :
			if i[0] in self.inverter:
				multiplier=-1;
			elif i[0] in self.inverter_2:
				multiplier=-1;
				modifier+=2;
			elif i[0] in pos_words:
				self.score=self.score+((2+modifier)*multiplier)
				modifier=0
				multiplier=1
			elif i[0] in neg_words:
				self.score=(self.score+(-2-modifier)*multiplier)
				modifier=0
				multiplier=1
			elif i[0] in self.enhancers_1:
				modifier+=1
			elif i[0] in self.enhancers_2:
				modifier+=2
			elif i[0] in self.diminishers:
                                modifier-=1
			elif i[1] in ('NN' , 'NNS') and noun_present_flag==0 and i[0] != 'i':
														#if not first noun in the sentence
									#useful for eg when i , problem in same sentence as problem is considered a noun. 
				noun=i[0]
				noun_present_flag=1
		
			global noun_dict
			if(noun_present_flag==1):
				if((noun in noun_dict) == False):
					noun_dict[noun]=(self.score-init_score)	#Add new key-value pair to dict
				else:
					noun_dict[noun]+=(self.score-init_score)	#Modify value of pair to dict
			

	def getSentiment(self,review):
	#	noun_dict={"":0}
		noun_dict.clear()
		review=self.preprocess(review)
		sentences=review.split('.')			#Split to sentences
		for sent in sentences :				#Score Each sentence.
			self.scoreSent(sent)
		global noun_dict
		retdict = {"OverallScore":self.score , "NounScore":noun_dict}	#return dictionary
		
		self.score=0
		noun_dict={}
		
		return retdict
