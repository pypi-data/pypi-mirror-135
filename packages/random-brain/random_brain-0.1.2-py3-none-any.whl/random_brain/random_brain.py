# test file
import os
import pickle
import numpy as np
import keras


# Class to act as random brain for neural networks
class random_brain:
    # Init needed data structures/ global vars here
    def __init__(self):
        # brain items
        self.brain = {} #{'file name':'model object'}

    # save brain
    def save_brain(self, path='random_brain.pkl'):
        return 0
        if '.pkl' in path:
            with open(path, 'wb') as f:
                pickle.dump(self.brain, f, pickle.HIGHEST_PROTOCOL)
        else:
            raise Exception('Path mush be in format \'xxxxx.pkl\'')

    # load brain
    def load_brain(self, path='random_brain.pkl'):
        return 0
        if '.pkl' in path:
            with open(path, 'rb') as f:
                self.brain = pickle.load(f)
        else:
            raise Exception('Path mush be in format \'xxxxx.pkl\'') 

    # Import models (keras)  # format of saved model: model.save(os.getcwd()+'/saved models/model.h5') 
    # This will not handle duplicates
    def import_models(self, model_path=None):
        # ignore if no model has been selected
        if model_path == None:
            print('No model selected, skipping')
            return

        # check if singular model or dir
        if '.h5' not in model_path:
            dir = os.listdir(model_path)
            for model in dir:
                try:
                    self.brain[model] = keras.models.load_model(os.path.join(model_path, model))
                except:
                    # print(f'Unable to import {model}, skipping')
                    pass
        else:
            # this is a single file
            # these next 2 lines are a bit barbaric but work for me. Need to convert this to something better and more robust like regex
            model_path_name = model_path.replace('/', ' ')
            model_path_name = model_path_name.replace('\\', ' ').split(' ')[-1]
            
            self.brain[model_path_name] = keras.models.load_model(model_path)

    # Show imported models
    def show_brain(self):
        # print(self.brain)
        return list(self.brain.keys())

    # Clear list or one item
    def clear_brain(self, item_list=[]):
        # clearing one item or many
        # print(self.brain)
        if item_list == []:
            self.brain = {}
        else:
            for item in item_list:
                try:
                    del self.brain[item]
                except:
                    raise Exception(f'Unable to remove item: {item}')

    # get votes
    def vote(self, yTest=[], threaded=False):
        votes = []

        for model in self.brain.values():
             votes.append(model.predict(yTest))

        return np.stack(votes) 

    # make predictions
    def predict(self, yTest=[],threaded=False, classes=None):
        print('Please note that predict is still under construction/testing. I would recommend using random_brain.vote() until predict() is completed')
        votes = []

        for model in self.brain.values():
            votes.append(model.predict(yTest))

        votes = np.stack(votes)

        # find average of votes
        votes = votes.mean(axis=0)

        if classes == None:
            # this is regression
            return votes
        else:
            # this is for classification only
            return keras.utils.np_utils.to_categorical(votes, num_classes=classes)
            
