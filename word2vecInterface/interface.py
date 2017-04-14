import re,sys,gensim, os, cPickle
from Tkinter import *
# sys.path.append('/u/home/d/datduong/')
from func2cleanASentence import * 
from func2getSimOf2GoTerms import * ## import functions needed to compare go terms 
from SentenceSimilarity import * ## import functions needed to compare go terms 


os.chdir("/Users/IreneZhou/UCLA/17 Spring/word2vec/word2vec2compareGenes/word2vecInterface")


FILE = open("goAnnotOboOwlBioProcClean.cPickle", 'r')
goAnnot2 = cPickle.load(FILE)
FILE.close()

print "loading gensim library, and the already trained word model from 15GB of Pubmed open access articles (may take 1-2 minutes)"

model = gensim.models.Word2Vec.load("modelWord2Vec")
bigram = gensim.models.phrases.Phraser.load('bigram.data')
trigram = gensim.models.phrases.Phraser.load('trigram.data')

print "finished loading."


def main(model,bigram,trigram): 

	main_win = Tk()
	main_win.geometry('295x375+400+280')
	main_win.resizable(False, False)
	main_win.title(u'word2vec')

	intro_label = Label(main_win, text="Please enter two Go id numbers, \n sentences, or phrases that you \n want to compare")
	
	intro_label.place(x = 30, y = 40)

	entry_list = []

	id1_entry_var = StringVar()
	id1_entry = Entry(main_win,textvariable = id1_entry_var)
	id1_entry.place(x = 30, y = 160,width = 230, height = 30)
	entry_list.insert(1,id1_entry_var)

	id2_entry_var = StringVar()
	id2_entry = Entry(main_win,textvariable = id2_entry_var)
	id2_entry.place(x = 30, y = 120,width = 230, height = 30)
	entry_list.insert(0, id2_entry_var)

	result_label = Label(main_win, text="")
	result_label.place(x=60, y=280)

	def on_submit_button():

		if not entry_list[0].get() or not entry_list[1].get():
			result = ""
		elif entry_list[0].get().isdigit() and entry_list[1].get().isdigit():
			try:
				result = w2v2GoTerms(entry_list[0].get(), entry_list[1].get(), goAnnot2, 
					hausdorffDistModWted, model, bigram, trigram, toTrigram=0)
			except Exception, e:
				result = "No Go term has id " + str(e)[1:-1] + "."			
		else:
			try:
				s1 = keepOnlyWordsInModel (cleanASentence(entry_list[0].get()),model)
				s2 = keepOnlyWordsInModel (cleanASentence(entry_list[1].get()),model)
				result = hausdorffDistModWted (s1, s2,model) 
			except Exception, e:
				result = "words not found in trained data"
		result_label["text"] = result


	submit_button = Button(main_win, text =u'Calculate Similarity Score', width=25, command = on_submit_button)
	submit_button.place(x = 30, y = 220)

	main_win.mainloop()

	# print w2v2GoTerms (entry_list[0],entry_list[1],goAnnot2,hausdorffDistModWted,model,bigram,trigram,toTrigram=0)


main(model,bigram,trigram)	

