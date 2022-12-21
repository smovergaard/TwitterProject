import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random
import powerlaw


#Takes csv and makes a dictionary with edge information: keys are IDs and values are lists of IDs

def fileToGDict(f):
        G_dict={}
        i=1
        with open(f) as csvfile:
                reader = csv.reader(csvfile, dialect='excel', delimiter=',')
                for row in reader:
                        items=1
                        for item in row:
                                items+=1
                        i = 1
                        for item in row:
                                if i == 0:
                                        G_dict[ID].append(int(item))
                                else:
                                        ID = int(item)
                                        if abs(items-np.minimum(1000,D_dict[ID]["following"])) < 5:
                                                G_dict[ID]=[]
                                                i = 0
                                        else:
                                                break
        return G_dict



#Takes csv and makes a dict of dicts with basic information: keys are IDs and vales are dicts with "verified", "followers" and "following" as keys

def fileToDDict(f):
        D_dict={}
        i=0
        with open(f) as csvfile:
                reader = csv.reader(csvfile, dialect='excel', delimiter=',')
                for row in reader:
                        i = 0
                        for item in row:
                                if i == 1:
                                        D_dict[ID]["verified"] = item
                                        i = 2
                                elif i == 2:
                                        D_dict[ID]["followers"] = int(item)
                                        i = 3
                                elif i == 3:
                                        D_dict[ID]["following"] = int(item)
                                else:
                                        ID = int(item)
                                        D_dict[ID]={}
                                        i = 1
        return D_dict



#Takes a graph and evaluates returns the weighted triangle count

def weightedTriangles(G):
        count = 0
        sigs = {}
        Gu=G.to_undirected()
        for ID in nx.nodes(G):
                sigs[ID]=[]
                count += 1
        count = 0
        for ID in nx.nodes(G):
                for following in nx.neighbors(Gu,ID):
                        for following1 in nx.neighbors(Gu,following):
                                if G.has_edge(ID,following1):
                                        if following*following1 not in sigs[ID] and ID*following1 not in sigs[following]:
                                                sigs[ID].append(following*following1)
                                                sigs[following].append(ID*following1)
                                                count+=(1/((G.nodes[ID]["followers"]+1)*(G.nodes[following]["followers"]+1)*(G.nodes[following1]["followers"]+1)))
                                elif G.has_edge(following1,ID):
                                        if following*following1 not in sigs[ID] and ID*following1 not in sigs[following]:
                                                sigs[ID].append(following*following1)
                                                sigs[following].append(ID*following1)
                                                count+=(1/((G.nodes[ID]["followers"]+1)*(G.nodes[following]["followers"]+1)*(G.nodes[following1]["followers"]+1)))
        return count


#Finds the weighted triangle count on subgraphs of different sizes

def WTlist():

	#Making filters for graph views

	rand={}
	for i in nx.nodes(G):
        	rand[i]=random.randint(0,999)

	def filter100(i_d):
        	if i_d in G_dict:
                	if rand[i_d] < 100:
                        	return True

	def filter500(i_d):
        	if i_d in G_dict:
                	if rand[i_d] < 500:
                        	return True

	def filter50(i_d):
        	if i_d in G_dict:
                	if rand[i_d] < 50:
                        	return True

	def filter200(i_d):
        	if i_d in G_dict:
                	if rand[i_d] < 200:
                        	return True
	
	#Making graph views
	
	Gprime100=nx.subgraph_view(G,filter_node=filter100)
	Gprime500=nx.subgraph_view(G,filter_node=filter500)
	Gprime50=nx.subgraph_view(G,filter_node=filter50)
	Gprime200=nx.subgraph_view(G,filter_node=filter200)

	
	#Getting WT counts on every view

	n100=nx.number_of_nodes(Gprime100)
	w100=weightedTriangles(Gprime100)

	n500=nx.number_of_nodes(Gprime500)
	w500=weightedTriangles(Gprime500)

	n50=nx.number_of_nodes(Gprime50)
	w50=weightedTriangles(Gprime50)

	n200=nx.number_of_nodes(Gprime200)
	w200=weightedTriangles(Gprime200)

	n1000=nx.number_of_nodes(Gprime)
	w1000=weightedTriangles(Gprime)

	wCounts=[w50,w100,w200,w500,w1000]
	nCounts=[n50,n100,n200,n500,n1000]

	return nCounts, wCounts



#Takes file and makes lists with the follower and following counts

def fileToList(f):
	followerCounts = []
	followingCounts = []
	with open(f) as csv_file:
		reader = csv.reader(csv_file, dialect='excel')
		for id, verificationStatus, followerCount, followingCount in reader:
			f1 = int(followerCount)
			f2 = int(followingCount)
			followerCounts.append(f1)
			followingCounts.append(f2)
	return followerCounts, followingCounts


#Uses scipy and powerlaw libraries to find the powerlaw exponent of the graph

def powerLaw(l):
	Ys, bin_edges = np.histogram(l, 9999999, (1.0, 10000000.0))
	Xs=np.linspace(1.0,10000000,9999999)
	
	
	def f(x,a,b,c):
        	return  b*((x-c)**a)
	
	params, cov = curve_fit(f,Xs,Ys,[-2,10000,-1],bounds=([-5,1,-100000],[0,100000000,10000000]))
	Ys2=f(Xs,*params)
	
	gamma=powerlaw.Fit(Ys2[0:9999])
	
	return gamma.power_law.alpha, Xs, Ys, Ys2
	

def Main():
	Gfile = 'G_data.csv'
	Dfile = 'D_data.csv'

	#Making dicts
	
	global D_dict
	D_dict = fileToDDict(Dfile)
	
	global G_dict
	G_dict = fileToGDict(Gfile)


	#Making NetworksX graph from dicts

	global G 
	G = nx.DiGraph(G_dict)
	nx.set_node_attributes(G,D_dict)
	
	
	#Gprime is the subgraph containing every node with edge information

	def filter(i_d):
		if i_d in G_dict:
			return True

	global Gprime
	Gprime = nx.subgraph_view(G,filter_node=filter)

	print("Nodes with basic information: " + str(nx.number_of_nodes(G)))
	print("Nodes with edge information: " + str(nx.number_of_nodes(Gprime)))

	print("Number of edges in subgraph: " + str(nx.number_of_edges(Gprime)))
	print("Average clustering in subgraph: " + str(nx.average_clustering(Gprime.to_undirected())))
	"""
	X,Y = WTlist()

	plt.plot(X,Y,marker='o', color='b')
	plt.title("Weighted Triangle Counts on " + str(Dfile))
	plt.xlabel("subgraph node count")
	plt.ylabel("W")
	plt.yscale("log")
	plt.xscale("log")
	plt.show(block=True)
	"""
	followerCounts, followingCounts = fileToList(Dfile)
	
	print("Average following: " + str(np.average(followingCounts)))
	print("Median following: " + str(np.median(followingCounts)))
	print("Average followers: " + str(np.average(followerCounts)))
	print("Median followers: " + str(np.median(followerCounts)))
	
	gamma, Xs, Ys, Ys2 = powerLaw(followerCounts)
	print("Powerlaw gamma: " + str(gamma))
	
	plt.plot(Xs[0:4999], Ys[0:4999], c ='c', label='Distribution')
	plt.plot(Xs[0:4999],Ys2[0:4999], c ='black', label='Fit')
	plt.title("Powerlaw fit on " + str(Dfile))
	plt.xlabel("degree")
	plt.ylabel("count")
	plt.legend()
	plt.show(block=True)
	
Main()
