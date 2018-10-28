# -*- coding: utf-8 -*-
"""
@author: Vinit Seth, Aadhavan Sadasivam, Manjusha Ravindranath

###Have to write file description###
"""

from scipy.io import loadmat
import os
import csv

def getMeta(matfile):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018


    ************* Method Description ******************

    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Returns Dictoinary which contains following values at index

    study - gives the name of the fMRI study

    subject - gives the identifier for the human subject

    ntrials - gives the number of trials in this dataset

    nsnapshots -  gives the total number of images in the dataset

    nvoxels - gives the number of voxels (3D pixels) in each image

    dimx - gives the maximum x coordinate in the brain image. The minimum x
    coordinate is x=1.  meta.dimy and meta.dimz give the same information for the y
    and z coordinates.
    """

    meta = {}
    meta['study'] = matfile['meta'][0][0]['study'][0].encode('utf-8')
    meta['subject'] = matfile['meta'][0][0]['subject'][0].encode('utf-8')
    meta['ntrials'] = matfile['meta'][0][0]['ntrials'][0][0]
    meta['nsnapshots'] = matfile['meta'][0][0]['nsnapshots'][0][0]
    meta['nvoxels'] = matfile['meta'][0][0]['nvoxels'][0][0]
    meta['dimx'] = matfile['meta'][0][0]['dimx'][0][0]
    meta['dimy'] = matfile['meta'][0][0]['dimy'][0][0]
    meta['dimz'] = matfile['meta'][0][0]['dimz'][0][0]

    return meta


def getInfoFromList(matfile, trialNumber):

    """
    Author:- Manjusha Ravindranath
    Date:- 09/23/2018

    Input:
        matFileData: loaded mat data file of a subject
        trialNumber: trial Number we want info on
    Output:
        The trial info of the subject corresponding to the trial Number
    info(18)
     mint: 894
     maxt: 948
     cond: 2
     firstStimulus: 'P'
     sentence: ''It is true that the star is below the plus.''
     sentenceRel: 'below'
     sentenceSym1: 'star'
     sentenceSym2: 'plus'
     img: sap
     actionAnswer: 0
     actionRT: 3613

    info.mint gives the time of the first image in the interval (the minimum time)

    info.maxt gives the time of the last image in the interval (the maximum time)

    info.cond has possible values 0,1,2,3.  Cond=0 indicates the data in this
    segment should be ignored. Cond=1 indicates the segment is a rest, or fixation
    interval.  Cond=2 indicates the interval is a sentence/picture trial in which
    the sentence is not negated.  Cond=3 indicates the interval is a
    sentence/picture trial in which the sentence is negated.

    info.firstStimulus: is either 'P' or 'S' indicating whether this trail was
    obtained during the session is which Pictures were presented before sentences,
    or during the session in which Sentences were presented before pictures.  The
    first 27 trials have firstStimulus='P', the remained have firstStimulus='S'.
    Note this value is present even for trials that are rest trials.  You can pick
    out the trials for which sentences and pictures were presented by selecting just
    the trials trials with info.cond=2 or info.cond=3.

    info.sentence gives the sentence presented during this trial.  If none, the
    value is '' (the empty string).  The fields info.sentenceSym1,
    info.sentenceSym2, and info.sentenceRel describe the two symbols mentioned in
    the sentence, and the relation between them.

    info.img describes the image presented during this trial.  For example, 'sap'
    means the image contained a 'star above plus'.  Each image has two tokens, where
    one is above the other.  The possible tokens are star (s), plus (p), and dollar
    (d).

    info.actionAnswer: has values -1 or 0.  A value of 0 indicates the subject is
    expected to press the answer button during this trial (either the 'yes' or 'no'
    button to indicate whether the sentence correctly describes the picture).  A
    value of -1 indicates it is inappropriate for the subject to press the answer
    button during this trial (i.e., it is a rest, or fixation trial).

    info.actionRT: gives the reaction time of the subject, measured as the time at
    which they pressed the answer button, minus the time at which the second
    stimulus was presented.  Time is in milliseconds.  If the subject did not press
    the button at all, the value is 0.

    """

    info = {}

    info['mint'] = matfile['info'][0][trialNumber]['mint'][0][0]
    info['maxt'] = matfile['info'][0][trialNumber]['maxt'][0][0]
    info['cond'] = matfile['info'][0][trialNumber]['cond'][0][0]
    info['firstStimulus'] = matfile['info'][0][trialNumber]['firstStimulus'][0][0]
    sentence = matfile['info'][0][trialNumber]['sentence']

    if sentence.size > 0 :
        info['sentence']=sentence[0][:].encode('utf-8')
    else:
        info['sentence']=''

    sentenceRel = matfile['info'][0][trialNumber]['sentenceRel']
    if sentenceRel.size > 0 :
        info['sentenceRel'] = sentenceRel[0][:].encode('utf-8')
    else:
        info['sentenceRel']=''
    sentenceSym1=matfile['info'][0][trialNumber]['sentenceSym1']
    if sentenceSym1.size > 0:
        info['sentenceSym1'] = sentenceSym1[0][:].encode('utf-8')
    else:
        info['sentenceSym1']=''
    sentenceSym2= matfile['info'][0][trialNumber]['sentenceSym2']
    if sentenceSym2.size > 0:
        info['sentenceSym2'] = sentenceSym2[0][:].encode('utf-8')
    else:
        info['sentenceSym2']=''
    img = matfile['info'][0][trialNumber]['img']
    if img.size > 0:
        info['img'] = img[0][0]
    else:
        info['img']=''

    info['actionAnswer'] = matfile['info'][0][trialNumber]['actionAnswer'][0][0]
    info['actionRT'] = matfile['info'][0][trialNumber]['actionRT'][0][0]


    return info


def getInfo(matfile, meta):
    """
    Author:- Manjusha Ravindranath
    Date:- 09/23/2018

    Input:
        matFileData: loaded mat data file of a subject
        meta: meta data about the subject
    Output:
        A 2d list containing all the trial info of the subject

    There are 54 trials.

    Get all trials in range from 0 th row to 53th row in trialIndices
    """

    trialInfoList = []
    trialIndices = meta['ntrials']
    for infoitem in range (0, trialIndices):
        trial = getInfoFromList(matfile,infoitem);
        trialInfoList.append(trial);
    return trialInfoList

def getData(matFileData, meta):
    """
    Author:- Aadhavan Sadasivam
    Date:- 09/23/2018

    Input:
        matFileData: loaded mat data file of a subject
        meta: meta data about the subject
    Output:
        A 2d list containing all the trial data of the subject
    """
    data = matFileData['data']
    data_array = []
    for item in data:
        data_array.append(item[0].tolist())
    return data_array

if __name__ == "__main__":

    matFilePath = "Data/Subject-05710/data-starplus-05710-v7.mat"
    matFileData = loadmat(matFilePath)

    meta = getMeta(matFileData)
    info = getInfo(matFileData, meta)
    data = getData(matFileData, meta)

    #write meta to the folder
    with open('Data/ExtractedData/Subject-05710/meta.data', 'w') as f:
        for key in meta.keys():
            f.write("%s:%s\n" % (key, str(meta[key])))
    #
    #write all the trials into seperate sub folders inside a subject
    for i in range(meta['ntrials']):
        trialDir = 'Data/ExtractedData/Subject-05710/Trial'+str(i+1)
        os.mkdir(trialDir)

        with open(trialDir+'/info.data', 'w') as f:
            for key in info[i].keys():
                f.write("%s:%s\n" % (key, str(info[i][key])))

        with open(trialDir+'/data.csv', 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerows(data[i])
