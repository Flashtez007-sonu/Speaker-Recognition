
def model():
    import pickle
    import os
    import numpy as np
    from scipy.io.wavfile import read
    from sklearn.mixture import GaussianMixture
    from featureextraction import extract_features
    import warnings
    import sys

    warnings.filterwarnings("ignore")
     
    #path to training data
    source   = "speakers\\"  

    #path where training speakers will be saved
    dest = "trainmodels\\"

    folders=os.listdir(source)
    #print(folders)
    train_file = "development.txt"
    features_file = "features.txt"

    for fold in folders:
        files=os.listdir(source+fold)
        for file in files:
            #print(file)
            if os.path.exists(train_file):
                file_paths = open(train_file,'a+')
                file_paths.write(fold+"/"+file+"\n")
            else:
                file_paths = open(train_file,'w')
                file_paths.write(fold+"/"+file+"\n")
                file_paths.close() 

    file_paths = open(train_file,'r')
    count = 0
    features = np.asarray(())
    features_file_features= open(features_file,'a+')

    #print(features)
    for path in file_paths:
        path = path.strip()
        print (path)
        print(features)
        # read the audio 
        sr,audio = read(source + path)
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        # when features of 5 files of speaker are concatenated, then do model training
        #if count == -1:
        
        #print("hhhhhhhh")
        print(features)
        
        for s in features:
            out_arr = np.array_str(s)
            features_file_features.write(out_arr)
        #sys.exit("Error message")
        gmm = GaussianMixture(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
        gmm.fit(features)
            # dumping the trained gaussian model
        picklefile = path.split("/")[0]+".gmm"
        pickle.dump(gmm,open(dest + picklefile,'wb'))
        print (' modeling completed for speaker:',picklefile," with data point = ",features.shape)
        features = np.asarray(())
        count = 0
        count = count + 1
        
