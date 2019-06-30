#Main For Gui
#Input is a file in the same directory , with name of ip.txt
#The file has Reviews separated by a '\n' {LineFeed}
from webui.ProcessReviewClass_GUI_List import ProcessReview

#--Main---------------------------------------------------------------
class ReviewList:

        def final_score(self):
                final_dict={}
                pro = ProcessReview()							#Create Object
                ipfile=open("E:\\androsent\\webui\\ip.txt").read()
                ipfile=ipfile.split('\n')

                total_score=0
                review_no=1

                for ip in ipfile :
                        review=ip									#get review
                        result=pro.getSentiment(review)				#GetSentiment
                        total_score+=result["OverallScore"]			
                        final_dict['total_score']=total_score
                        final_dict[str(review_no)]=result			#Add to final dict , indexed via review no.
                        review_no+=1
                
                return final_dict
        def score_for_chart(self,final_dict):
                nli=[]
                no=1
                for review_no in final_dict.keys():
                        if review_no=='total_score':
                                continue
                nli.append([no,final_dict[review_no]['OverallScore']])
                no+=1
                return {'chart_score':nli}

                

