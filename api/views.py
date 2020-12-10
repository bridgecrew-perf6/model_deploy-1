from django.shortcuts import render

# Create your views here.

from sklearn import metrics

#Import necessary libraries
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import numpy as np

# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)

@api_view(["POST"])
def predict_diabetictype(request): 
    try:
        age = request.data.get('age',60)
        bs_fast = request.data.get('bs_fast',4.6)
        bs_pp = request.data.get('bs_pp',3.8)
        plasma_r = request.data.get('plasma_r',6.4)
        plasma_f = request.data.get('plasma_f',6.1)
        hbA1c = request.data.get('hbA1c',65)
        fields = [age,bs_fast,bs_pp,plasma_r,plasma_f,hbA1c]
        print(fields)
        if not None in fields:
            #Datapreprocessing Convert the values to float
            age = float(age)
            bs_fast = float(bs_fast)
            bs_pp = float(bs_pp)
            plasma_r = float(plasma_r)
            plasma_f = float(plasma_f)
            hbA1c = float(hbA1c)
            result = [age,bs_fast,bs_pp,plasma_r,plasma_f,hbA1c]
            #Passing data to model & loading the model from disks
            model_path = 'ml_model/model.pkl'
            classifier = pickle.load(open(model_path, 'rb'))
            prediction = classifier.predict([result])[0]
            conf_score =  np.max(classifier.predict_proba([result]))*100
            predictions = {
                'error' : '0',
                'message' : 'Successfull',
                'prediction' : prediction,
                'confidence_score' : conf_score
            }
        else:
            predictions = {
                'error' : '1',
                'message': 'Invalid Parameters'                
            }
    except Exception as e:
        predictions = {
            'error' : '2',
            "message": str(e)
        }
    
    return Response(predictions)

from sklearn.cluster import KMeans
def kmeansClustering(X, n_clusters):

    kmeans = KMeans(n_clusters)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    silhouette_score=metrics.silhouette_score(X, y_kmeans)
    
    return y_kmeans, kmeans.inertia_, silhouette_score

def train_knn_model(data,k):
    # load dataset

    X = data
    y_kmeans, ssd_kmeans, silhouette_score = kmeansClustering(X, n_clusters=k)
    pickle.dump(y_kmeans,open("ml_model/kmeans_result.pkl", "wb"))

    return y_kmeans, ssd_kmeans, silhouette_score

import json

@api_view(["POST"])
def kmeans(request):
    try:
        #k = request.data.get('k',2)
        data = json.loads(request.body)
        print("data", data)
        #train_data = request.GET.get('data', [[1,1],[1,2],[2,1],[2,2],[10,10],[10,11],[11,10],[11,11]])
        k = data['k']
        train_data = data['train']
        #train_data = request.GET.get('data')
        fields = [k,train_data]
        print("fields",fields)
        if k is not None:
            #Datapreprocessing Convert the values to float
            k = int(k)
            print("k",k)
            train_data = np.array(train_data)
            train_data = list(filter(any,train_data))
            train_data = [list(filter(None, lst)) for lst in train_data]
            print("train_data",train_data)
            y_kmeans, ssd_kmeans, silhouette_score = train_knn_model(train_data,k)
            predictions = {
                'error' : '0',
                'message' : 'Successfull',
                'y_kmeans' : y_kmeans.reshape(-1,1),
                'ssd' : ssd_kmeans,
                'silhouette_score' : silhouette_score
            }
        else:
            predictions = {
                'error' : '1',
                'message': 'Invalid Parameters'                
            }
    except Exception as e:
        predictions = {
            'error' : '2',
            "message": str(e)
        }
    
    return Response(predictions)
<<<<<<< HEAD


from sklearn.cluster import DBSCAN
def dbscan_cluster(X, eps, min_samples):
    
    model = DBSCAN(eps, min_samples)
    # fit model and predict clusters
    y_db = model.fit_predict(X)

    silhouette_score=metrics.silhouette_score(X, y_db)

    pickle.dump(y_db,open("ml_model/dbscan_result.pkl", "wb"))

    return y_db, silhouette_score

@api_view(["POST"])
def db_scan(request):
    try:
        #k = request.data.get('k',2)
        data = json.loads(request.body)
        print("data", data)
        #train_data = request.GET.get('data', [[1,1],[1,2],[2,1],[2,2],[10,10],[10,11],[11,10],[11,11]])
        eps = data['eps']
        min_samples = data['min_samples']
        train_data = data['train']
        #train_data = request.GET.get('data')
        fields = [eps, min_samples,train_data]
        print("fields",fields)
        if eps is not None:
            #Datapreprocessing Convert the values to float
            eps = float(eps)
            print("eps",eps)
            min_samples = int(min_samples)
            print("min_samples",min_samples)
            train_data = np.array(train_data)
            print("train_data",train_data)
            y_db, silhouette_score = dbscan_cluster(train_data,eps, min_samples)
            predictions = {
                'error' : '0',
                'message' : 'Successfull',
                'y_db' : y_db.reshape(-1,1),
                'silhouette_score' : silhouette_score
            }
        else:
            predictions = {
                'error' : '1',
                'message': 'Invalid Parameters'                
            }
    except Exception as e:
        predictions = {
            'error' : '2',
            "message": str(e)
        }
    
    return Response(predictions)
=======
>>>>>>> 0bf98736acf0c55e7795785736e58f0396bfcb19
