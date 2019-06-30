from webui.GUI_List import ReviewList
from webui.reviewshow import init,prompt,ProcessReview 
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
#from webui.forms import LoginForm
from webui.reviewshow import init 
from nltk import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create your views here.
def index(request)  :
    return render(request,'home.html')



def samsung(request):
   return render(request, 'samsung.html')
      
def samsung_show(request):
   review=""
   phone_model=""
   vs=""
   result={}   
   print(request.POST)
   print(result)
   if request.method == "POST" and request.POST:
      #Get the posted form
      init()
      pro=ProcessReview()
      review=request.POST.get('review_text','')
  #    phone_model=request.POST.get('phone_model','')	  
      #review=sent_tokenize(review)
     # analyzer=SentimentIntensityAnalyzer()
     # vs=analyzer.polarity_scores(review)
      result=pro.getSentiment(review)
      print(result)
      #noun=result.NounScore
      #overall=result.OverallScore
   return render(request, 'samsung.html', {"review":review,"result":result})
    


def SaveProfile(request):
    status="file is not selected yet..!"
    suc_status=""
    if request.method == 'POST':
        status=request.FILES.get('file',False)
        if status != False:
            suc_status="successfully uploaded!."
            handle_uploaded_file(request.FILES['file'],request)
        else:
            status="please select a file..!"
    return render(request, 'upload.html', {"status":status,"suc_status":suc_status})



def handle_uploaded_file(f,request):
    fo=open('E:\\androsent\\webui\\ip.txt', 'wb+')
    with  fo as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handle_ip_file(request):
    RList=ReviewList()
    mydict=RList.final_score();
    ipfile=open("E:\\androsent\\webui\\noun_list.txt").read()
    loc=ipfile.split('\n')
    tot_score=mydict['total_score']   
    mydict.pop('total_score',0)
    ans_dict={}
    value=0
    for init  in loc:
        ans_dict[init]=0

    for index in mydict.keys():
        for noun in mydict[index]['NounScore'].keys():
            ans_dict[noun]+=mydict[index]['NounScore'][noun];
    print(ans_dict)
    for init in loc:
            ans_dict[init]=(ans_dict[init]/len(mydict))
    print(ans_dict)
    
    re=ReviewList()
    final_dict=re.final_score()

    nli=[]
    no=1
    for review_no in final_dict.keys():
        if review_no=='total_score':
                continue
        nli.append([no,final_dict[review_no]['OverallScore']])
        no+=1

    return render(request,'upload.html',{"mydict":mydict,"ans_dict":ans_dict,"tot_score":tot_score,"chart_score":nli})










    
