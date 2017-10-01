import pickle


redditData = pickle.load(open( "data.p", "rb" ))


for i in redditData["data"] : print(i)
print(len(redditData["ids"]))


#pickle.dump( redditData, open( "data.p", "wb" ) )


