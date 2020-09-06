def result1():
    import os
    import pickle
    import numpy as np
    from scipy.io.wavfile import read
    from featureextraction import extract_features
    import warnings
    warnings.filterwarnings("ignore")
    import time

    #path to training data
    source   = "voice/"   

    #path where training speakers will be saved
    modelpath = "trainmodels/"
    test_file = "development.txt"
    file_paths = open(test_file,'r')
    gmm_files = [os.path.join(modelpath,fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]
    #print(gmm_files)
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    #print(models)
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]


    for path in file_paths:
        path = path.strip()
        print("Testing Audio: ", path)
        print(path)
        
        sr,audio = read( source+path)
        vector   = extract_features(audio,sr)
        log_likelihood = np.zeros(len(models))
        for i in range(len(models)):
            gmm    = models[i]  #checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
            winner = np.argmax(log_likelihood)
            print(log_likelihood)
            if path == path:
                print ("\tdetected as - ", speakers[winner])
                print (" Speaker identified. ")
            else:
                print ("\t speaker is not detected")
        break
    #result(speakers[winner])
        #time.sleep(1.0)

    
