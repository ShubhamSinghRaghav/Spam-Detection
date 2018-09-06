from django.shortcuts import render
from django.http import HttpResponse
from . import spam_dete
import glob
import os
import numpy as np
# Create your views here.
e_mails_test=[]
def index(request):
	context = {

	}
	#reka()
	if request.method == 'POST':
		queryset = request.POST
		e_mails_test.append(queryset['defer'])
		resoo=reef()
		print(resoo[0][1])
		 

		context['un_spam'] = resoo[0][1]*100
		#contra.append(e_mails_test[0])
		del e_mails_test[:]
		#print(queryset['defer'])
		#print(reka())
		
		# TERA METHOD
		# REDIRECT
	# context={
 #      'un_spam':resoo
	# } 
	return render(request,'detector/index.html',context)
	# return HttpResponse("homepage")
 
 # def result(request):
 # 	return render(request,'detector/result.html',contra)


###############################################################################################
###############################################################################################
#def reka():

def letters_only(astr):
  return astr.isalpha()

def clean_text(docs):
  cleaned_docs = []
  for doc in docs:
    cleaned_docs.append(' '.join([lemmatizer.lemmatize(word.lower()) for word in doc.split() if letters_only(word) and word not in all_names]))
  return cleaned_docs    



def get_label_index(labels):
  from collections import defaultdict
  label_index=defaultdict(list)
  for index,label in enumerate(labels):
      label_index[label].append(index)
  return label_index

    

def get_prior(label_index):
  prior={label: len(index) for label, index in label_index.items()}
  total_count=sum(prior.values())
  for label in prior:
      prior[label]/=float(total_count)
  return prior
    


def get_likelihood(term_document_matrix, label_index,smoothing=0):  
  likelihood={}
  for label, index in label_index.items():
      likelihood[label]=term_document_matrix[index,:].sum(axis=0) + smoothing
      likelihood[label]=np.asarray(likelihood[label])[0]
      total_count=likelihood[label].sum()
      likelihood[label]=likelihood[label]/float(total_count)
  return likelihood    


def get_posterior(term_document_matrix,prior,likelihood):	
  num_docs=term_document_matrix.shape[0]
  posteriors=[]
  for i in range(num_docs):
      posterior={key: np.log(prior_label) for key, prior_label in prior.items()}
      for label,likelihood_label in likelihood.items():
          term_document_vector=term_document_matrix.getrow(i)
          counts=term_document_vector.data
          indices=term_document_vector.indices
          for count, index in zip(counts, indices):
              posterior[label]+=np.log(likelihood_label[index])*count
      min_log_posterior = min(posterior.values())
      for label in posterior:
          try:
              posterior[label]=np.exp(posterior[label]-min_log_posterior)
          except:
              posterior[label] = float('inf')
      sum_posterior=sum(posterior.values())
      for label in posterior:
          if posterior[label] == float('inf'):
              posterior[label] = 1.0
          else:
              posterior[label]/=sum_posterior
      posteriors.append(posterior.copy())
  return posteriors





###############################################################################################3
e_mails, labels = [], []
file_path=os.getcwd()+'/dataset/spam'
for filename in glob.glob(os.path.join(file_path,'*.txt')):
  with open(filename,'r',encoding="ISO-8859-1") as infile:
    e_mails.append(infile.read())
    labels.append(1)
            
  file_path1=os.getcwd()+'/dataset/ham'
  for filename in glob.glob(os.path.join(file_path1,'*.txt')):
      with open(filename,'r',encoding="ISO-8859-1") as infile:
          e_mails.append(infile.read())
          labels.append(0)
            
from nltk.corpus import names 
from nltk.stem import WordNetLemmatizer
all_names=set(names.words())
lemmatizer=WordNetLemmatizer()
cleaned_emails=clean_text(e_mails)
from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(stop_words="english", max_features=500)
terms_docs=cv.fit_transform(cleaned_emails)          
feature_names=cv.get_feature_names()
label_index=get_label_index(labels)
prior=get_prior(label_index)
smoothing=1
likelihood=get_likelihood(terms_docs,label_index,smoothing)
# e_mails_test=[
#         '''Subject: get discount
#         please ccall and contact s for further details
#         we will you get best possible price or deal that suits you
#         thanks
#         andy moore
#         '''
#         ]    
def reef():
	cleaned_test=clean_text(e_mails_test)
	terms_docs_test=cv.transform(cleaned_test) 
	posterior=get_posterior(terms_docs_test,prior,likelihood)  
	#resoo.append(posterior)
	#print(posterior)
	return posterior     

    

         
              
    
