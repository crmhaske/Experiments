#Christie Haskell

from psychopy import *
from pyglet.window import key
import csv,uuid,random,time,psychopy.info,pygame

#Stimuli parameters
stimType="raisedCos"
maskType="circle"
spatialFreq=2
contrast=0.7
stimSize=1.5
maskSize=1.8
numDots=200
dotSize=1
fixSize=0.3
respSize=1.2
probeSize=1.5
stimDist=2.1
fixColour="white"

#Get subject number
userid=raw_input("Subject #: ")
while True:
    try:
        int(userid)
        break
    except ValueError:
        print("Value must be an integer number")
        userid=raw_input("Subject #: ")
        
#Get cue type
cueType=raw_input("Cue Type (none; exo: exogeneous; endo: endogenous): ")
while cueType !="none" and cueType !="exo" and cueType !="endo":
    print("Only none, exo, and endo are valid responses")
    cueType=raw_input("Cue Type (none; exo: exogeneous; endo: endogenous): ")
    
#Get experiment type
exp=int(raw_input("Experiment #: "))

#Cueing probabilities
if exp==1 or exp==2:
    validProb=1
    neutProb=0.5
elif exp==3:
    validProb=0.8
    neutProb=0.5
elif exp==4:
    validProb=0.5
    neutProb=0.5
#if cueType=="exo" or cueType=="endo":
#    validProb=raw_input('Probability of Valid Cue ( 0 to 1): ')
#    while True:
#        try:
#            validProb=float(validProb)
#            if validProb<0.0 or validProb>1.0:
#                print("Value must be a number and between 0 and 1")
#                validProb=float(raw_input('Probability of Valid Cue ( 0 to 1): '))
#            else:
#                break
#        except ValueError:
#            print("Value must be a number and between 0 and 1")
#            validProb=raw_input('Probability of Valid Cue ( 0 to 1): ')

#Create window
scrx=1024
scry=768
#scrx=800
#scry=600
winUnits = "deg"
monitorType="brittlab1"
#monitorType="testMonitor"
fullscreen=True
expWin = visual.Window((scrx,scry),allowGUI=True,winType='pyglet',monitor=monitorType,units=winUnits,screen=0,fullscr=fullscreen, color = [0,0,0], waitBlanking = True)
expWin.setMouseVisible(False)
keyState=key.KeyStateHandler()
expWin.winHandle.push_handlers(keyState)

#Cueing parameters
if cueType=="endo" or cueType=="exo":
    approxCueTime=0.05
    approxCueInterval=0.05
    approxSOA=approxCueTime+approxCueInterval
    if cueType=="exo":
        cueSize=0.3
        cueColour="black"
        cueShape="circle"
        cueOffset=1.5
    else:
        cueSize=0.5
        cueWidth=3
        cueColour="white"

if exp==1:
    #Trial paramters
    numBlocks = 8
    numTrials = 75
    numPractice = 15
elif exp==2 or exp==3 or exp==4:
    #Trial parameters
    numBlocks = 6
    numTrials = 75
    numPractice = 15
elif exp==5:
    #Trial parameters
    numBlocks = 10
    numTrials = 50
    numPractice=15

#Monitor paramters and timings
refreshRate=84.0
frameLength=1/refreshRate
approxTimeFix1=0.4
approxTimeStim=0.15
if exp==5:
    approxTimeFix2a=0.5
    approxTimeFix2b=1
    approxTimeFix2c=3
    approxTimeFix2d=6
    approxTimeFix2="na"
else:
    approxTimeFix2=0.5
approxTimeMask=0.2

#Determine number of frames based off of refreshRate
frameFix1=int(approxTimeFix1/frameLength)
frameStim=int(approxTimeStim/frameLength)
if exp==5:
    frameFix2a=int(approxTimeFix2a/frameLength)
    frameFix2b=int(approxTimeFix2b/frameLength)
    frameFix2c=int(approxTimeFix2c/frameLength)
    frameFix2d=int(approxTimeFix2d/frameLength)
    frameFix2="na"
else:
    frameFix2=int(approxTimeFix2/frameLength)
frameMask=int(approxTimeMask/frameLength)
if cueType=="exo" or cueType=="endo":
    frameCue=int(approxCueTime/frameLength)-1
    frameCueInterval=int(approxCueInterval/frameLength)-1

#Determine timing based on number of frames
timeFix1=frameFix1*frameLength
timeStima=frameStim*frameLength
if exp==5:
    timeFix2a=frameFix2a*frameLength
    timeFix2b=frameFix2b*frameLength
    timeFix2c=frameFix2c*frameLength
    timeFix2d=frameFix2d*frameLength
    timeFix2=0.5
    timeFix2seq=0.5
else:
    timeFix2=frameFix2*frameLength
    timeFix2seq=timeFix2
timeMaska=frameMask*frameLength
if cueType=="exo" or cueType=="endo":
    cueTime=frameCue*frameLength
    cueInterval=frameCueInterval*frameLength
    
#Feedback sound files
#http://www.freesound.org/people/Bertrof/sounds/131660/
right = psychopy.sound.SoundPygame(value='correct.wav')
#http://www.freesound.org/people/Bertrof/sounds/131657/
wrong=psychopy.sound.SoundPygame(value='wrong.wav')

#General variables to save
Dict_Gen = {
    'scrx': scrx,
    'scry': scry,
    'winUnits': winUnits,
    'refreshRate':refreshRate,
    'stimType': stimType,
    'maskType': maskType,
    'spatialFreq': spatialFreq,
    'contrast': contrast,
    'stimSize': stimSize,
    'maskSize': maskSize,
    'fixSize': fixSize,
    'respSize': respSize,
    'probeSize': probeSize,
    'probePos':"na",
    'probePosX':"na",
    'probePosY':"na",
    'stimDist': stimDist,
    'fixColour': fixColour,
    'numTrials': numTrials,
    'numPractice': numPractice,
    'numBlocks':numBlocks,
    'userid': userid,
    'monitorType':monitorType,
    'approxTimeFix1':approxTimeFix1,
    'approxTimeStim':approxTimeStim,
    'approxTimeFix2':approxTimeFix2,
    'approxTimeMask':approxTimeMask,
    'numDots':numDots,
    'dotSize':dotSize,
    'correct':"na",
    'tFix1':"na",
    'tStim1':"na",
    'tStim2':"na",
    'tFix2':"na",
    'tFix3':'na',
    'tMask1':"na",
    'tMask2':"na",
    'numSwitch':'na',
    'practice': "na",
    'trialnum': "na",
    'blocknum':"na",
    'orient':"na",
    'stimPos':"na",
    'stimPos2':"na",
    'stimPosX':"na",
    'stimPosY':"na",
    'stimPos2X':"na",
    'stimPos2Y':"na",
    'stimOri':"na",
    'stimOri2':"na",
    'tRespOn':"na",
    'tRespOff':"na",
    'tRespAble':"na",
    'tFix1On':"na",
    'tStim1On':"na",
    'tStim2On':"na",
    'tFix2On':"na",
    'tFix3On':"na",
    'tMask1On':"na",
    'tMask2On':"na",
    'RTres':"na",
    'msRTres':"na",
    'RTtot':"na",
    'msRTtot':"na",
    'judgori':"na",
    'angdiff':"na",
    'blockType':"na",
    'stimResp':"na",
    'cueType':cueType,
    'Experiment':"na",
    'tIntTrial':"na"
}

#Variables to save if cueing
if cueType=="endo" or cueType=="exo":
    Dict_Cue={
        'validCue':"na",
        'cuePos':'na',
        'cuePosX':'na',
        'cuePosY':'na',
        'atStimNotCued':'na',
        'approxCueTime':approxCueTime,
        'approxSOA':approxSOA,
        'SOA':"na",
        'validProb':validProb,
        'approxCueInterval':approxCueInterval,
        'cueSize':cueSize,
        'cueColour':cueColour,
        'tCueOn':"na",
        'tCue':"na",
        'tCueIntOn':"na",
        'tCueInt':"na",
        'neutProb':neutProb
    }
else:
    Dict_Cue={
        'validCue':"na",
        'cuePos':'na',
        'cuePosX':'na',
        'cuePosY':'na',
        'atStimNotCued':'na',
        'approxCueTime':'na',
        'approxSOA':'na',
        'SOA':'na',
        'validProb':'na',
        'approxCueInterval':'na',
        'cueSize':'na',
        'cueColour':'na',
        'tCueOn':"na",
        'tCue':"na",
        'tCueIntOn':"na",
        'tCueInt':"na"

    }

#Variables to save if exogeneous cueing
if cueType=="exo":
    Dict_Exo={
        'cueShape': cueShape,
        'cueOffset':cueOffset
    }
else:
    Dict_Exo={
        'cueShape': "na",
        'cueOffset':"na"
    }

#Variables to save if endogenous cueing
if cueType=="endo":
    Dict_Endo={
        'cueWidth':cueWidth
    }
else:
    Dict_Endo={
        'cueWidth':"na"
    }

if exp==5:
    order=[timeFix2a,timeFix2b,timeFix2c,timeFix2d]
    random.shuffle(order)
    delay1=order[0]
    delay2=order[1]
    delay3=order[2]
    delay4=order[3]
    Dict_E5={
        'delay1':"na",
        'delay2':"na",
        'delay3':"na",
        'delay4':"na",
        'delay':"na"
    }

#Create dictionary, and create and open datafile
if cueType=="exo":
    if exp==1:
        exstr="exp1a"
        exper="1a"
    elif exp==2:
        exper="2a"
        exstr="exp2a"
    elif exp==3:
        exper="3a"
        exstr="exp3a"
    elif exp==4:
        exper="4a"
        exstr="exp4a"
elif cueType=="endo":
    exstr="exp6a"
    exper="6a"
elif cueType=="none":
    if exp==5:
        exstr="exp5a"
        exper="5a"

if exp==5:
    dict = dict(Dict_Gen.items()+Dict_Cue.items()+Dict_Exo.items()+Dict_Endo.items()+Dict_E5.items())
else:
    dict = dict(Dict_Gen.items()+Dict_Cue.items()+Dict_Exo.items()+Dict_Endo.items())
dict['Experiment']=exper
tfn = "../data/" + userid + "_" +str(uuid.uuid4())+"_"+exstr+".dat"
#tfn = userid + "_" +str(uuid.uuid4())+"_"+exstr+".dat"
f = open(tfn,"w")
cdw = csv.DictWriter(f,fieldnames = dict.keys(),quoting = csv.QUOTE_MINIMAL)
cdw.writeheader()

#create fixation dot/X, probe, stimuli, cue, mask, and response stimulus
if cueType=="endo":
    fixationTR = psychopy.visual.ShapeStim(expWin,vertices =([0,0],[cueSize,cueSize]),lineColor=cueColour)
    fixationTL = psychopy.visual.ShapeStim(expWin,vertices =([0,0],[-cueSize,cueSize]),lineColor=cueColour)
    fixationBR = psychopy.visual.ShapeStim(expWin,vertices =([0,0],[cueSize,-cueSize]),lineColor=cueColour)
    fixationBL = psychopy.visual.ShapeStim(expWin,vertices =([0,0],[-cueSize,-cueSize]),lineColor=cueColour)
else:
    fixation = visual.PatchStim(expWin, size=fixSize, mask=stimType,pos=[0,0], sf=0, color=fixColour)
probe=psychopy.visual.Rect(win=expWin, width=probeSize, height=probeSize)
grating=visual.PatchStim(win=expWin, tex="sin",mask=stimType, size=stimSize,sf=spatialFreq,contrast=contrast)
grating2=visual.PatchStim(win=expWin, tex="sin",mask=stimType, size=stimSize,sf=spatialFreq,contrast=contrast)
maskBack=visual.PatchStim(win=expWin, size=maskSize, mask=maskType, sf=0, color="black")
maskBack2=visual.PatchStim(win=expWin, size=maskSize, mask=maskType, sf=0, color="black")
respStim=visual.PatchStim(win=expWin, tex="sin",mask=stimType, size=respSize,pos=[0,0], sf=spatialFreq,contrast=contrast,ori=0)
if cueType=="exo":
    if exp==1:
        cue=visual.PatchStim(expWin, size=cueSize, mask=cueShape, sf=0, color=cueColour)
    elif exp==2 or exp==3 or exp==4:
        cue1=visual.PatchStim(expWin, size=cueSize, mask=cueShape, sf=0, color=cueColour)
        cue2=visual.PatchStim(expWin, size=cueSize, mask=cueShape, sf=0, color=cueColour)
        cue3=visual.PatchStim(expWin, size=cueSize, mask=cueShape, sf=0, color=cueColour)
        cue4=visual.PatchStim(expWin, size=cueSize, mask=cueShape, sf=0, color=cueColour)
elif cueType=="endo":
    cue=psychopy.visual.ShapeStim(expWin,lineColor=cueColour,lineWidth=cueWidth)

#Trials
for blocknum in range(0, numBlocks + 1):
    #Determine if trial is practice
    if blocknum == 0 and numPractice == 0:
        continue
    if blocknum == 0:
        curnumtrials = numPractice
        blockType="setOne"
        practice = True
        validCue = "na"
    elif blocknum == 1:
        curnumtrials = numPractice
        practice = True
        blockType = "seq"
        validCue="na"
    elif blocknum==2:
        curnumtrials = numPractice
        practice = True
        blockType = "simul"
        validCue="na"
    else:
        curnumtrials = numTrials
        practice = False
    if blocknum == 0:
        notdone=True
        blockLabel=psychopy.visual.TextStim(expWin,text="Practice: Set Size One; press the space bar to begin",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
        while notdone:
            blockLabel.draw()
            expWin.flip()
            if keyState[key.SPACE] == True:
                break
       
        expClock = core.Clock()
        #Set Size One
        for trialnum in range(1, curnumtrials + 1):
            if practice==True and trialnum<3:
                timeStim=1
                timeMask=1
            else:
                timeStim=timeStima
                timeMask=timeMaska
            
            if exp==5:
                timeFix2==timeFix2a

            #Stimulus orientation and position
            stimOri=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
            stimPos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
            
            #Set stimulus orientation and position, mask position, and probe visual settings and position
            grating.setPos(stimPos)
            grating.setOri(stimOri)
            maskBack.setPos(stimPos)
            probe.setLineColor("white")
            probe.setFillColor([0,0,0])
            probe.setPos(stimPos)
            
            #Generate random noise
            maskNoise=visual.DotStim(win=expWin, nDots = numDots, fieldShape = maskType,fieldSize = maskSize,dotSize = dotSize, signalDots = 'same', noiseDots='position',color = 'white')
            maskNoise.setFieldPos(stimPos)
            
            #Position of exogenous block dot cue
            if cueType=="exo" and practice==False:
                if random.random()<=neutProb:
                    if random.random()<=validProb:
                        cuePosX=stimPos[0]
                        if stimPos[1]>0:
                            cuePosY=stimPos[1]+cueOffset
                        else:
                            cuePosY=stimPos[1]-cueOffset
                        cuePos=[cuePosX,cuePosY]
                        validCue="true"
                    else:
                        validCue="false"
                        cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                        while cuePos==stimPos:
                            cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                        cuePosX=cuePos[0]
                        cuePosY=cuePos[1]
                        if cuePos[1]>0:
                            cuePosY=cuePos[1]+cueOffset
                        else:
                            cuePosY=cuePos[1]-cueOffset
                        cuePos=[cuePosX,cuePosY]
                    if exp==1:
                        cue.setPos(cuePos)
                    elif exp==2 or exp==3 or exp==4:
                        cuePos1=cuePos
                        if stimPos[1]>0:
                            cuePos2=[cuePosX,stimPos[1]-cueOffset]
                            if stimPos[0]>0:
                                cuePos3=[stimPos[0]-cueOffset,stimPos[1]]
                                cuePos4=[stimPos[0]+cueOffset,stimPos[1]]
                            else:
                                cuePos3=[stimPos[0]+cueOffset,stimPos[1]]
                                cuePos4=[stimPos[0]-cueOffset,stimPos[1]]
                        else:
                            cuePos2=[cuePosX,stimPos[1]+cueOffset]
                            if stimPos[0]>0:
                                cuePos3=[stimPos[0]+cueOffset,stimPos[1]]
                                cuePos4=[stimPos[0]-cueOffset,stimPos[1]]
                            else:
                                cuePos3=[stimPos[0]-cueOffset,stimPos[1]]
                                cuePos4=[stimPos[0]+cueOffset,stimPos[1]]
                        cue1.setPos(cuePos1)
                        cue2.setPos(cuePos2)
                        cue3.setPos(cuePos3)
                        cue4.setPos(cuePos4)
                else:
                    validCue="neutral"
                    cuePosX="na"
                    cuePosY="na"
                    cuePos="na"
            #Position of endogenous cue
            elif cueType=="endo" and practice==False:
                if random.random()<=neutProb:
                    if random.random()<=validProb:
                        validCue="true"
                        if stimPos[0]>0:
                            if stimPos[1]>0:
                                cue.setVertices([[0,0],[cueSize,cueSize]])
                                cuePos="top right"
                            elif stimPos[1]<0:
                                cue.setVertices([[0,0],[cueSize,-cueSize]])
                                cuePos="bottom right"
                        elif stimPos[0]<0:
                            if stimPos[1]>0:
                                cue.setVertices([[0,0],[-cueSize,cueSize]])
                                cuePos="top left"
                            elif stimPos[1]<0:
                                cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                cuePos="bottom left"
                    else:
                        validCue="false"
                        cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                        while cueDir==stimPos:
                            cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                        if cueDir[0]>0:
                            if cueDir[1]>0:
                                cue.setVertices([[0,0],[cueSize,cueSize]])
                                cuePos="top right"
                            elif cueDir[1]<0:
                                cue.setVertices([[0,0],[cueSize,-cueSize]])
                                cuePos="bottom right"
                        elif cueDir[0]<0:
                            if cueDir[1]>0:
                                cue.setVertices([[0,0],[-cueSize,cueSize]])
                                cuePos="top left"
                            elif cueDir[1]<0:
                                cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                cuePos="bottom left"
                else:
                        validCue="neutral"
                        cuePosX="na"
                        cuePosY="na"
                        cuePos="na"
            
            #Used to determine between trial time
            if trialnum != 1:
                tTrialEndPrev=tRespOff
                            
            #Fixation dot/X for timeFix1
            if cueType=="endo":
                fixationTR.draw()
                fixationTL.draw()
                fixationBR.draw()
                fixationBL.draw()
            else:
                fixation.draw()
            expWin.flip()
            tFix1On=expClock.getTime()
            while True:
                curtime=expClock.getTime()-tFix1On
                if curtime>=timeFix1:
                    break
                    
            #Cue slides if cueing
            if cueType=="exo" or cueType=="endo":
                if validCue != "neutral" and practice==False:
                    #Cue displayed for cueTime
                    if cueType=="endo":
                        fixationTR.draw()
                        fixationTL.draw()
                        fixationBR.draw()
                        fixationBL.draw()
                    else:
                        fixation.draw()
                    if exp==1:
                        cue.draw()
                    elif exp==2 or exp==3 or exp==4:
                        cue1.draw()
                        cue2.draw()
                        cue3.draw()
                        cue4.draw()
                    expWin.flip()
                    tCueOn=expClock.getTime()
                    while True:
                        curtime=expClock.getTime()-tCueOn
                        if curtime>=cueTime:
                            break
                
                    #Fixation dot/X for cueInterval
                    if cueType=="endo":
                        fixationTR.draw()
                        fixationTL.draw()
                        fixationBR.draw()
                        fixationBL.draw()
                    else:
                        fixation.draw()
                    expWin.flip()
                    tCueIntOn=expClock.getTime()
                    while True:
                        curtime=expClock.getTime()-tCueIntOn
                        if curtime>=cueInterval:
                            break

            #Sinusodial grating for 150ms
            if cueType=="endo":
                fixationTR.draw()
                fixationTL.draw()
                fixationBR.draw()
                fixationBL.draw()
            else:
                fixation.draw()
            #generate random sinusodial grating orientation
            grating.draw()
            expWin.flip()
            tStim1On=expClock.getTime()
            while True:
                curtime=expClock.getTime()-tStim1On
                if curtime>=(timeStim):
                    break

            #Mask for 200ms
            if cueType=="endo":
                fixationTR.draw()
                fixationTL.draw()
                fixationBR.draw()
                fixationBL.draw()
            else:
                fixation.draw()
            maskBack.draw()
            maskNoise.draw()
            expWin.flip()
            tMask1On=expClock.getTime()
            while True:
                curtime=expClock.getTime()-tMask1On
                if curtime>=timeMask:
                    break

            #Fixation dot/X for 500ms
            if cueType=="endo":
                fixationTR.draw()
                fixationTL.draw()
                fixationBR.draw()
                fixationBL.draw()
            else:
                fixation.draw()
            expWin.flip()
            tFix2On=expClock.getTime()
            while True:
                curtime=expClock.getTime()-tFix2On
                if curtime>=timeFix2:
                    break

            #Response slide
            notdone=True
            judgOri=90
            numSwitch=0
            keyLeft=False
            keyRight=False
            first=True
           
            respStim.draw()
            probe.draw()
            expWin.flip()
            tRespAble=expClock.getTime()
        
            while notdone:
                if keyState[key.RIGHT] == True:
                    if first==True:
                        tRespOn=expClock.getTime()
                        first=False
                    if keyLeft==True:
                        numSwitch+=1
                    keyRight=True
                    keyLeft=False
                    judgOri -= 1
                if keyState[key.LEFT] == True:
                    if first==True:
                        tRespOn=expClock.getTime()
                        first=False
                    if keyRight==True:
                        numSwitch+=1
                    keyRight=False
                    keyLeft=True
                    judgOri += 1
                if keyState[key.ESCAPE] == True:
                    quit()
                if keyState[key.RETURN] == True or keyState[key.UP] == True:
                    if first==True:
                        tRespOn=expClock.getTime()
                        first=False
                    notdone = False
                    tRespOff=expClock.getTime()
                    RTres=tRespOff-tRespOn
                    RTtot=tRespOff-tRespAble
                    dict['practice'] = practice
                    dict['trialnum']=trialnum
                    dict['blocknum']=blocknum
                    dict['blockType']=blockType
                    dict['orient']=stimOri
                    dict['stimOri']=stimOri
                    if cueType=="exo" or cueType=="endo":
                        if practice==False:
                            dict['atStimNotCued']="na"
                            dict['validCue']=validCue
                            if validCue=="true" or validCue=="false":
                                dict['tCueOn']=tCueOn
                                dict['tCue']=tCueIntOn-tCueOn
                                dict['tCueIntOn']=tCueIntOn
                                dict['tCueInt']=tStim1On-tCueIntOn
                                dict['SOA']=dict['tCue']+dict['tCueInt']
                            else:
                                dict['tCueOn']="na"
                                dict['tCue']="na"
                                dict['tCueIntOn']="na"
                                dict['tCueInt']="na"
                                dict['SOA']="na"
                    if cueType=="endo" and practice==False:
                        dict['cuePos']=cuePos
                    if cueType=="exo" and practice==False:
                        dict['cuePosX']=cuePosX
                        dict['cuePosY']=cuePosY
                        if validCue=="false" or validCue=="true":
                            if cuePos[0]>0:
                                if cuePos[1]>0:
                                    dict['cuePos']='top right'
                                else:
                                    dict['cuePos']='bottom right'
                            elif cuePos[0]<0:
                                if cuePos[1]>0:
                                    dict['cuePos']='top left'
                                else:
                                    dict['cuePos']='bottom left'
                        else:
                            dict['cuePos']='na'
                    dict['numSwitch']=numSwitch
                    dict['tFix1On']=tFix1On
                    if practice==False:
                        if cueType=="exo" or cueType=="endo":
                            if validCue=="neutral":
                                dict['tFix1']=tStim1On-tFix1On
                            else:
                                dict['tFix1']=tCueOn-tFix1On
                        else:
                            dict['tFix1']=tStim1On-tFix1On
                    dict['tStim1On']=tStim1On
                    dict['tStim1']=tMask1On-tStim1On
                    dict['tFix2On']=tFix2On
                    dict['tFix2']=tRespAble-tFix2On
                    dict['tMask1On']=tMask1On
                    dict['tMask1']=tFix2On-tMask1On
                    dict['stimOri2']="na"
                    dict['stimPosX']=stimPos[0]
                    dict['stimPosY']=stimPos[1]
                    if stimPos[0]>0:
                        if stimPos[1]>0:
                            dict['stimPos']='top right'
                        else:
                            dict['stimPos']='bottom right'
                    elif stimPos[0]<0:
                        if stimPos[1]>0:
                            dict['stimPos']='top left'
                        else:
                            dict['stimPos']='bottom left'
                    dict['probePos']=dict['stimPos']
                    dict['probePosX']=stimPos[0]
                    dict['probePosY']=stimPos[1]
                    dict['stimPos2']="na"
                    dict['stimPos2X']="na"
                    dict['stimPos2Y']="na"
                    dict['stimResp']="na"
                    dict['tRespAble']=tRespAble
                    dict['tRespOn']=tRespOn
                    dict['tRespOff']=tRespOff
                    dict['RTres']=RTres
                    dict['msRTres']=RTres*1000
                    dict['RTtot']=RTtot
                    dict['msRTtot']=RTtot*1000
                    if judgOri<=90:
                        dict['judgori']=90-judgOri
                    else:
                        dict['judgori']=270-judgOri
                    dict['angdiff']=(dict['judgori'] - dict['orient'] + 90) % 180 - 90
                    if dict['angdiff'] <= 10 and dict['angdiff'] >= -10:
                        correct=True
                    else:
                        correct=False
                    if practice==True:
                        if correct==True:
                            right.play()
                        else:
                            wrong.play()
                    dict['correct']=correct
                    if trialnum ==1:
                        dict['tIntTrial']="na"
                    else:
                        dict['tIntTrial']=tFix1On-tTrialEndPrev
                    cdw.writerow(dict)
                    break

                respStim.setOri(90 - judgOri)
                respStim.draw()
                probe.draw()
                expWin.flip()
    else:
        if blocknum==1:
            blockType=="seq"
        elif blocknum==2:
            blockType=="simul"
        elif blocknum==3 or blocknum==5 or blocknum==7 or blocknum==9:
            blockType=random.choice(["seq","simul"])
        elif blocknum==4 or blocknum==6 or blocknum==8 or blocknum==10:
            if blockType=="seq":
                blockType="simul"
            else:
                blockType="seq"
        if exp==5 and practice==False:
            if blocknum==1 or blocknum==2:
                timeFix2=timeFix2a
            if blocknum==3 or blocknum==4:
                timeFix2=delay1
                delay=delay1
            elif blocknum==5 or blocknum==6:
                timeFix2=delay2
                delay=delay2
            elif blocknum==7 or blocknum==8:
                timeFix2=delay3
                delay=delay3
            elif blocknum==9 or blocknum==10:
                timeFix2=delay4
                delay=delay4

        #Sequential trials
        if blockType=="seq":
            if blocknum==1:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Practice: Sequential; press the space bar to begin",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
            else:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Sequential: press the space bar to begin",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
                    
            for trialnum in range(1, curnumtrials + 1):
                if practice==True and trialnum<3:
                    timeStim=1
                    timeMask=1
                else:
                    timeStim=timeStima
                    timeMask=timeMaska
                
                #Position of grating 1, grating 2, and response probe
                stimPos=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                stimPos2=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                stimOri=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                stimOri2=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                if stimPos == stimPos2:
                   while stimPos == stimPos2:
                       stimPos2=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                if stimOri==stimOri2:
                    while stimOri==stimOri2:
                        stimOri2=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                probePos=random.choice([stimPos,stimPos2])
                
                #Set stimulus orientation and position, mask position, and probe visual settings and position
                grating.setPos(stimPos)
                grating.setOri(stimOri)
                grating2.setPos(stimPos2)
                grating2.setOri(stimOri2)
                maskBack.setPos(stimPos)
                maskBack2.setPos(stimPos2)
                probe.setLineColor("white")
                probe.setFillColor([0,0,0])
                probe.setPos(probePos)
                
                #Generate random noise
                maskNoise=visual.DotStim(win=expWin, nDots = numDots, fieldShape = maskType,fieldSize = maskSize,dotSize = dotSize, signalDots = 'same', noiseDots='position',color = 'white')
                maskNoise2=visual.DotStim(win=expWin, nDots = numDots, fieldShape = maskType,fieldSize = maskSize,dotSize = dotSize, signalDots = 'same', noiseDots='position',color = 'white')
                maskNoise.setFieldPos(stimPos)
                maskNoise2.setFieldPos(stimPos2)
                
                #Determine which stimulus is the target
                if probePos==stimPos:
                    stimResp=1
                else:
                    stimResp=2
                    
                #Exogenous black dot cue position
                if cueType=="exo" and practice==False:
                    if random.random()<=neutProb:
                        if random.random()<=validProb:
                            cuePosX=probePos[0]
                            if probePos[1]>0:
                                cuePosY=probePos[1]+cueOffset
                            else:
                                cuePosY=probePos[1]-cueOffset
                            cuePos=[cuePosX,cuePosY]
                            validCue="true"
                            atStimNotCued="valid"
                        else:
                            validCue="false"
                            cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            while cuePos==probePos:
                                cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            cuePosX=cuePos[0]
                            cuePosY=cuePos[1]
                            if stimResp==1:
                                if  cuePos==stimPos2:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            elif stimResp==2:
                                if  cuePos==stimPos:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            if cuePos[1]>0:
                                cuePosY=cuePos[1]+cueOffset
                            else:
                                cuePosY=cuePos[1]-cueOffset
                            cuePos=[cuePosX,cuePosY]
                        if exp==1:
                            cue.setPos(cuePos)
                        elif exp==2 or exp==3 or exp==4:
                            cuePos1=cuePos
                            if cuePos1[0] > 0:
                                if cuePos1[1]>0:
                                    cuePos2=[stimDist,stimDist-cueOffset]
                                    cuePos3=[stimDist-cueOffset,stimDist]
                                    cuePos4=[stimDist+cueOffset,stimDist]
                                elif cuePos1[1]<0:
                                    cuePos2=[stimDist,-stimDist+cueOffset]
                                    cuePos3=[stimDist-cueOffset,-stimDist]
                                    cuePos4=[stimDist+cueOffset,-stimDist]
                            elif cuePos1[0]< 0:
                                if cuePos1[1]>0:
                                    cuePos2=[-stimDist,stimDist-cueOffset]
                                    cuePos3=[-stimDist-cueOffset,stimDist]
                                    cuePos4=[-stimDist+cueOffset,stimDist]
                                elif cuePos1[1]<0:
                                    cuePos2=[-stimDist,-stimDist+cueOffset]
                                    cuePos3=[-stimDist-cueOffset,-stimDist]
                                    cuePos4=[-stimDist+cueOffset,-stimDist]
                            cue1.setPos(cuePos1)
                            cue2.setPos(cuePos2)
                            cue3.setPos(cuePos3)
                            cue4.setPos(cuePos4)
                    else:
                        validCue="neutral"
                        cuePosX="na"
                        cuePosY="na"
                        cuePos="na"
                        atStimNotCued="na"
                #Endogenous cue for cueTime
                elif cueType=="endo" and practice==False:
                    if random.random()<=neutProb:
                        if random.random()<=validProb:
                            validCue="true"
                            atStimNotCued="valid"
                            if probePos[0]>0:
                                if probePos[1]>0:
                                    cue.setVertices([[0,0],[cueSize,cueSize]])
                                    cuePos="top right"
                                elif probePos[1]<0:
                                    cue.setVertices([[0,0],[cueSize,-cueSize]])
                                    cuePos="bottom right"
                            elif probePos[0]<0:
                                if probePos[1]>0:
                                    cue.setVertices([[0,0],[-cueSize,cueSize]])
                                    cuePos="top left"
                                elif probePos[1]<0:
                                    cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                    cuePos="bottom left"
                        else:
                            validCue="false"
                            cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            while cueDir==stimPos:
                                cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            if stimResp==1:
                                if cueDir==stimPos2:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            elif stimResp==2:
                                if cueDir==stimPos:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            if cueDir[0]>0:
                                if cueDir[1]>0:
                                    cue.setVertices([[0,0],[cueSize,cueSize]])
                                    cuePos="top right"
                                elif cueDir[1]<0:
                                    cue.setVertices([[0,0],[cueSize,-cueSize]])
                                    cuePos="bottom right"
                            elif cueDir[0]<0:
                                if cueDir[1]>0:
                                    cue.setVertices([[0,0],[-cueSize,cueSize]])
                                    cuePos="top left"
                                elif cueDir[1]<0:
                                    cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                    cuePos="bottom left"
                    else:
                        validCue="neutral"
                        cuePosX="na"
                        cuePosY="na"
                        cuePos="na"
                        atStimNotCued="na"
             #Used to determine between trial time
                if trialnum != 1:
                    tTrialEndPrev=tRespOff
                
                #Fixation dot for 400ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                expWin.flip()
                tFix1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tFix1On
                    if curtime>=timeFix1:
                        break
                 
                 #Cue slides if cueing
                if cueType=="exo" or cueType=="endo":
                    if validCue != "neutral" and practice==False:
                        #Cue displayed for cueTime
                        if cueType=="endo":
                            fixationTR.draw()
                            fixationTL.draw()
                            fixationBR.draw()
                            fixationBL.draw()
                        else:
                            fixation.draw()
                        if exp==1:
                            cue.draw()
                        elif exp==2 or exp==3 or exp==4:
                            cue1.draw()
                            cue2.draw()
                            cue3.draw()
                            cue4.draw()
                        expWin.flip()
                        tCueOn=expClock.getTime()
                        while True:
                            curtime=expClock.getTime()-tCueOn
                            if curtime>=cueTime:
                                break
                    
                        #Fixation dot/X for cueInterval
                        if cueType=="endo":
                            fixationTR.draw()
                            fixationTL.draw()
                            fixationBR.draw()
                            fixationBL.draw()
                        else:
                            fixation.draw()
                            if exp==2 or exp==3 or exp==4:
                                cue1.draw()
                                cue2.draw()
                                cue3.draw()
                                cue4.draw()
                        expWin.flip()
                        tCueIntOn=expClock.getTime()
                        while True:
                            curtime=expClock.getTime()-tCueIntOn
                            if curtime>=cueInterval:
                                break
  
                #Sinusodial grating for 150ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                #generate random sinusodial grating orientation and position
                grating.draw()
                if exp==2 or exp==3 or exp==4:
                    if validCue!="neutral" and practice==False:
                        cue1.draw()
                        cue2.draw()
                        cue3.draw()
                        cue4.draw()
                expWin.flip()
                tStim1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tStim1On
                    if curtime>=(timeStim):
                        break

                #Mask for 200ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                #generate random mask
                maskBack.draw()
                maskNoise.draw()
                expWin.flip()
                tMask1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tMask1On
                    if curtime>=timeMask:
                        break

                #Fixation dot/X for 500ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                expWin.flip()
                tFix2On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tFix2On
                    if curtime>=timeFix2seq:
                        break

                #Sinusodial grating for 150ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                grating2.draw()
                expWin.flip()
                tStim2On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tStim2On
                    if curtime>=(timeStim):
                        break

                #Mask for 200ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                maskBack2.draw()
                maskNoise2.draw()
                expWin.flip()
                tMask2On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tMask2On
                    if curtime>=timeMask:
                        break

                #Fixation dot/X for 500ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                expWin.flip()
                tFix3On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tFix3On
                    if curtime>=timeFix2:
                        break
            
                #Response slide
                tRespStart=expClock.getTime()
                notdone=True
                judgOri=90
                numSwitch=0
                keyLeft=False
                keyRight=False
                first=True
                
                respStim.draw()
                probe.draw()
                expWin.flip()
                tRespAble=expClock.getTime()
        
                while notdone:
                    if keyState[key.RIGHT] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        if keyLeft==True:
                            numSwitch+=1
                        keyRight=True
                        keyLeft=False
                        judgOri -= 1
                    if keyState[key.LEFT] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        if keyRight==True:
                            numSwitch+=1
                        keyRight=False
                        keyLeft=True
                        judgOri += 1
                    if keyState[key.ESCAPE] == True:
                        quit()
                    if keyState[key.RETURN] == True or keyState[key.UP] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        notdone = False
                        tRespOff=expClock.getTime()
                        RTres=tRespOff-tRespOn
                        RTtot=tRespOff-tRespAble
                        dict['practice'] = practice
                        dict['trialnum']=trialnum
                        dict['blocknum']=blocknum
                        dict['numSwitch']=numSwitch
                        dict['blockType']=blockType
                        if probePos==stimPos:
                            dict['orient']=stimOri
                        else:
                            dict['orient']=stimOri2
                        dict['stimOri']=stimOri
                        dict['stimOri2']=stimOri2
                        if stimPos[0]>0:
                            if stimPos[1]>0:
                                dict['stimPos']='top right'
                            else:
                                dict['stimPos']='bottom right'
                        elif stimPos[0]<0:
                            if stimPos[1]>0:
                                dict['stimPos']='top left'
                            else:
                                dict['stimPos']='bottom left'
                        if stimPos2[0]>0:
                            if stimPos2[1]>0:
                                dict['stimPos2']='top right'
                            else:
                                dict['stimPos2']='bottom right'
                        elif stimPos2[0]<0:
                            if stimPos2[1]>0:
                                dict['stimPos2']='top left'
                            else:
                                dict['stimPos2']='bottom left'
                        dict['stimPosX']=stimPos[0]
                        dict['stimPosY']=stimPos[1]
                        dict['stimPos2X']=stimPos2[0]
                        dict['stimPos2Y']=stimPos2[1]
                        if stimResp==1:
                            dict['probePos']=dict['stimPos']
                        elif stimResp==2:
                            dict['probePos']=dict['stimPos2']
                        dict['probePosX']=probePos[0]
                        dict['probePosY']=probePos[1]
                        dict['stimResp']=stimResp
                        if cueType=="exo" or cueType=="endo":
                            if practice==False:
                                dict['atStimNotCued']=atStimNotCued
                                dict['validCue']=validCue
                                if validCue=="true" or validCue=="false":
                                    dict['tCueOn']=tCueOn
                                    dict['tCue']=tCueIntOn-tCueOn
                                    dict['tCueIntOn']=tCueIntOn
                                    dict['tCueInt']=tStim1On-tCueIntOn
                                    dict['SOA']=dict['tCue']+dict['tCueInt']
                                else:
                                    dict['tCueOn']="na"
                                    dict['tCue']="na"
                                    dict['tCueIntOn']="na"
                                    dict['tCueInt']="na"
                                    dict['SOA']="na"
                        if cueType=="endo" and practice==False:
                            dict['cuePos']=cuePos
                        if cueType=="exo" and practice==False:
                            dict['cuePosX']=cuePosX
                            dict['cuePosY']=cuePosY
                            if validCue=="false" or validCue=="true":
                                if cuePos[0]>0:
                                    if cuePos[1]>0:
                                        dict['cuePos']='top right'
                                    else:
                                        dict['cuePos']='bottom right'
                                elif cuePos[0]<0:
                                    if cuePos[1]>0:
                                        dict['cuePos']='top left'
                                    else:
                                       dict['cuePos']='bottom left'
                            else:
                                dict['cuePos']='na'
                        dict['tFix1On']=tFix1On
                        if practice==False:
                            if cueType=="endo" or cueType=="exo":
                                if validCue=="neutral":
                                    dict['tFix1']=tStim1On-tFix1On
                                else:
                                    dict['tFix1']=tCueOn-tFix1On
                            else:
                                dict['tFix1']=tStim1On-tFix1On
                        dict['tStim1On']=tStim1On
                        dict['tStim1']=tMask1On-tStim1On
                        dict['tFix2On']=tFix2On
                        dict['tFix2']=tStim2On-tFix2On
                        dict['tMask1On']=tMask1On
                        dict['tMask1']=tFix2On-tMask1On
                        dict['tStim2On']=tStim2On
                        dict['tStim2']=tMask2On-tStim2On
                        dict['tFix3On']=tFix3On
                        dict['tFix3']=tRespAble-tFix3On
                        dict['tMask2On']=tMask2On
                        dict['tMask2']=tFix3On-tMask2On
                        dict['tRespAble']=tRespAble
                        dict['tRespOn']=tRespOn
                        dict['tRespOff']=tRespOff
                        dict['RTres']=RTres
                        dict['msRTres']=RTres*1000
                        dict['RTtot']=RTtot
                        dict['msRTtot']=RTtot*1000
                        if exp==5 and practice==False:
                            dict['delay1']=delay1
                            dict['delay2']=delay2
                            dict['delay3']=delay3
                            dict['delay4']=delay4
                            dict['delay']=delay
                        if judgOri<=90:
                           dict['judgori']=90-judgOri
                        else:
                           dict['judgori']=270-judgOri
                        dict['angdiff']=(dict['judgori'] - dict['orient'] + 90) % 180 - 90
                        if dict['angdiff'] <= 10 and dict['angdiff'] >= -10:
                            correct=True
                        else:
                            correct=False
                        if practice==True:
                            if correct==True:
                                right.play()
                            else:
                                wrong.play()
                        dict['correct']=correct
                        if trialnum ==1:
                            dict['tIntTrial']="na"
                        else:
                            dict['tIntTrial']=tFix1On-tTrialEndPrev
                        cdw.writerow(dict)
                        break

                    respStim.setOri(90 - judgOri)
                    probe.draw()
                    respStim.draw()
                    expWin.flip()
            if blocknum==numBlocks:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Experiment complete (space bar to exit)",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
                    
       #Simultaneous trials
        elif blockType=="simul":
            if blocknum==2:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Practice: Simultaneous; press the space bar to begin",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
            else:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Simultaneous: press the space bar to begin",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
                    
            for trialnum in range(1, curnumtrials + 1):
                if practice==True and trialnum<3:
                    timeStim=1
                    timeMask=1
                else:
                    timeStim=timeStima
                    timeMask=timeMaska
                #Position of grating 1, grating 2, and response probe
                stimPos=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                stimPos2=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                stimOri=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                stimOri2=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                if stimPos == stimPos2:
                   while stimPos == stimPos2:
                       stimPos2=random.choice([[stimDist,stimDist],[-stimDist,stimDist],[stimDist,-stimDist],[-stimDist,-stimDist]])
                if stimOri==stimOri2:
                    while stimOri==stimOri2:
                        stimOri2=random.choice([10,24,38,52,66,80,100,114,128,142,156,170])
                probePos=random.choice([stimPos,stimPos2])
                
                #Set stimulus orientation and position, mask position, and probe visual settings and position
                grating.setPos(stimPos)
                grating.setOri(stimOri)
                grating2.setPos(stimPos2)
                grating2.setOri(stimOri2)
                maskBack.setPos(stimPos)
                maskBack2.setPos(stimPos2)
                probe.setLineColor("white")
                probe.setFillColor([0,0,0])
                probe.setPos(probePos)
                
                #Generate random noise
                maskNoise=visual.DotStim(win=expWin, nDots = numDots, fieldShape = maskType,fieldSize = maskSize,dotSize = dotSize, signalDots = 'same', noiseDots='position',color = 'white')
                maskNoise2=visual.DotStim(win=expWin, nDots = numDots, fieldShape = maskType,fieldSize = maskSize,dotSize = dotSize, signalDots = 'same', noiseDots='position',color = 'white')
                maskNoise.setFieldPos(stimPos)
                maskNoise2.setFieldPos(stimPos2)
                
                #Determine which stimulus is the target
                if probePos==stimPos:
                    stimResp=1
                else:
                    stimResp=2
                    
                #Exogenous black dot cue position
                if cueType=="exo" and practice==False:
                    if random.random()<=neutProb:
                        if random.random()<=validProb:
                            cuePosX=probePos[0]
                            if probePos[1]>0:
                                cuePosY=probePos[1]+cueOffset
                            else:
                                cuePosY=probePos[1]-cueOffset
                            cuePos=[cuePosX,cuePosY]
                            validCue="true"
                            atStimNotCued="valid"
                        else:
                            validCue="false"
                            cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            while cuePos==probePos:
                                cuePos=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            cuePosX=cuePos[0]
                            cuePosY=cuePos[1]
                            if stimResp==1:
                                if  cuePos==stimPos2:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            elif stimResp==2:
                                if  cuePos==stimPos:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            if cuePos[1]>0:
                                cuePosY=cuePos[1]+cueOffset
                            else:
                                cuePosY=cuePos[1]-cueOffset
                            cuePos=[cuePosX,cuePosY]
                        if exp==1:
                            cue.setPos(cuePos)
                        elif exp==2 or exp==3 or exp==4:
                            cuePos1=cuePos
                            if cuePos1[0] > 0:
                                if cuePos1[1]>0:
                                    cuePos2=[stimDist,stimDist-cueOffset]
                                    cuePos3=[stimDist-cueOffset,stimDist]
                                    cuePos4=[stimDist+cueOffset,stimDist]
                                elif cuePos1[1]<0:
                                    cuePos2=[stimDist,-stimDist+cueOffset]
                                    cuePos3=[stimDist-cueOffset,-stimDist]
                                    cuePos4=[stimDist+cueOffset,-stimDist]
                            elif cuePos1[0]< 0:
                                if cuePos1[1]>0:
                                    cuePos2=[-stimDist,stimDist-cueOffset]
                                    cuePos3=[-stimDist-cueOffset,stimDist]
                                    cuePos4=[-stimDist+cueOffset,stimDist]
                                elif cuePos1[1]<0:
                                    cuePos2=[-stimDist,-stimDist+cueOffset]
                                    cuePos3=[-stimDist-cueOffset,-stimDist]
                                    cuePos4=[-stimDist+cueOffset,-stimDist]
                            cue1.setPos(cuePos1)
                            cue2.setPos(cuePos2)
                            cue3.setPos(cuePos3)
                            cue4.setPos(cuePos4)
                    else:
                        validCue="neutral"
                        cuePosX="na"
                        cuePosY="na"
                        cuePos="na"
                        atStimNotCued="na"
                #Endogenous cue for cueTime
                elif cueType=="endo" and practice==False:
                    if random.random()<=neutProb:
                        if random.random()<=validProb:
                            validCue="true"
                            atStimNotCued="valid"
                            if probePos[0]>0:
                                if probePos[1]>0:
                                    cue.setVertices([[0,0],[cueSize,cueSize]])
                                    cuePos="top right"
                                elif probePos[1]<0:
                                    cue.setVertices([[0,0],[cueSize,-cueSize]])
                                    cuePos="bottom right"
                            elif probePos[0]<0:
                                if probePos[1]>0:
                                    cue.setVertices([[0,0],[-cueSize,cueSize]])
                                    cuePos="top left"
                                elif probePos[1]<0:
                                    cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                    cuePos="bottom left"
                        else:
                            validCue="false"
                            cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            while cueDir==stimPos:
                                cueDir=random.choice([[stimDist,stimDist],[stimDist,-stimDist],[-stimDist,stimDist],[-stimDist,-stimDist]])
                            if stimResp==1:
                                if cueDir==stimPos2:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            elif stimResp==2:
                                if cueDir==stimPos:
                                    atStimNotCued="true"
                                else:
                                    atStimNotCued="false"
                            if cueDir[0]>0:
                                if cueDir[1]>0:
                                    cue.setVertices([[0,0],[cueSize,cueSize]])
                                    cuePos="top right"
                                elif cueDir[1]<0:
                                    cue.setVertices([[0,0],[cueSize,-cueSize]])
                                    cuePos="bottom right"
                            elif cueDir[0]<0:
                                if cueDir[1]>0:
                                    cue.setVertices([[0,0],[-cueSize,cueSize]])
                                    cuePos="top left"
                                elif cueDir[1]<0:
                                    cue.setVertices([[0,0],[-cueSize,-cueSize]])
                                    cuePos="bottom left"
                    else:
                        validCue="neutral"
                        cuePosX="na"
                        cuePosY="na"
                        cuePos="na"
                        atStimNotCued="na"
                 #Used to determine between trial time
                if trialnum != 1:
                    tTrialEndPrev=tRespOff
                
                
                #Fixation dot/X for 400ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                expWin.flip()
                tFix1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tFix1On
                    if curtime>=timeFix1:
                        break

                #Cue slides if cueing
                if cueType=="exo" or cueType=="endo":
                    if validCue != "neutral" and practice==False:
                        #Cue displayed for cueTime
                        if cueType=="endo":
                            fixationTR.draw()
                            fixationTL.draw()
                            fixationBR.draw()
                            fixationBL.draw()
                        else:
                            fixation.draw()
                        if exp==1:
                            cue.draw()
                        elif exp==2 or exp==3 or exp==4:
                            cue1.draw()
                            cue2.draw()
                            cue3.draw()
                            cue4.draw()
                        expWin.flip()
                        tCueOn=expClock.getTime()
                        while True:
                            curtime=expClock.getTime()-tCueOn
                            if curtime>=cueTime:
                                break
                    
                        #Fixation dot/X for cueInterval
                        if cueType=="endo":
                            fixationTR.draw()
                            fixationTL.draw()
                            fixationBR.draw()
                            fixationBL.draw()
                        else:
                            fixation.draw()
                            if exp==2 or exp==3 or exp==4:
                                cue1.draw()
                                cue2.draw()
                                cue3.draw()
                                cue4.draw()
                        expWin.flip()
                        tCueIntOn=expClock.getTime()
                        while True:
                            curtime=expClock.getTime()-tCueIntOn
                            if curtime>=cueInterval:
                                break

               #Two sinusodial gratings for 150ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                if exp==2 or exp==3 or exp==4:
                    if validCue!="neutral" and practice==False:
                        cue1.draw()
                        cue2.draw()
                        cue3.draw()
                        cue4.draw()
                #generate random sinusodial grating orientation and position
                grating.draw()
                grating2.draw()
                expWin.flip()
                tStim1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tStim1On
                    if curtime>=(timeStim):
                        break

                #Mask for 200ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                #generate random mask
                maskBack.draw()
                maskNoise.draw()
                maskBack2.draw()
                maskNoise2.draw()
                expWin.flip()
                tMask1On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tMask1On
                    if curtime>=timeMask:
                        break

                #Fixation dot/X for 500ms
                if cueType=="endo":
                    fixationTR.draw()
                    fixationTL.draw()
                    fixationBR.draw()
                    fixationBL.draw()
                else:
                    fixation.draw()
                expWin.flip()
                tFix2On=expClock.getTime()
                while True:
                    curtime=expClock.getTime()-tFix2On
                    if curtime>=timeFix2:
                        break
            
                #Response slide
                notdone=True
                judgOri=90
                numSwitch=0
                keyLeft=False
                keyRight=False
                first=True
                
                respStim.draw()
                probe.draw()
                expWin.flip()
                tRespAble=expClock.getTime()
                
                while notdone:
                    if keyState[key.RIGHT] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        if keyLeft==True:
                            numSwitch+=1
                        keyRight=True
                        keyLeft=False
                        judgOri -= 1
                    if keyState[key.LEFT] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        if keyRight==True:
                            numSwitch+=1
                        keyRight=False
                        keyLeft=True
                        judgOri += 1
                    if keyState[key.ESCAPE] == True:
                        quit()
                    if keyState[key.RETURN] == True or keyState[key.UP] == True:
                        if first==True:
                            tRespOn=expClock.getTime()
                            first=False
                        notdone = False
                        tRespOff=expClock.getTime()
                        RTres=tRespOff-tRespOn
                        RTtot=tRespOff-tRespAble
                        dict['practice'] = practice
                        dict['trialnum']=trialnum
                        dict['blocknum']=blocknum
                        dict['numSwitch']=numSwitch
                        dict['blockType']=blockType
                        if probePos==stimPos:
                            dict['orient']=stimOri
                        else:
                            dict['orient']=stimOri2
                        dict['stimOri']=stimOri
                        dict['stimOri2']=stimOri2
                        if stimPos[0]>0:
                            if stimPos[1]>0:
                                dict['stimPos']='top right'
                            else:
                                dict['stimPos']='bottom right'
                        elif stimPos[0]<0:
                            if stimPos[1]>0:
                                dict['stimPos']='top left'
                            else:
                                dict['stimPos']='bottom left'
                        if stimPos2[0]>0:
                            if stimPos2[1]>0:
                                dict['stimPos2']='top right'
                            else:
                                dict['stimPos2']='bottom right'
                        elif stimPos2[0]<0:
                            if stimPos2[1]>0:
                                dict['stimPos2']='top left'
                            else:
                                dict['stimPos2']='bottom left'
                        dict['stimPosX']=stimPos[0]
                        dict['stimPosY']=stimPos[1]
                        dict['stimPos2X']=stimPos2[0]
                        dict['stimPos2Y']=stimPos2[1]
                        if stimResp==1:
                            dict['probePos']=dict['stimPos']
                        elif stimResp==2:
                            dict['probePos']=dict['stimPos2']
                        dict['probePosX']=probePos[0]
                        dict['probePosY']=probePos[1]
                        dict['stimResp']=stimResp
                        if cueType=="exo" or cueType=="endo":
                            if practice==False:
                                dict['atStimNotCued']=atStimNotCued
                                dict['validCue']=validCue
                                if validCue=="true" or validCue=="false":
                                    dict['tCueOn']=tCueOn
                                    dict['tCue']=tCueIntOn-tCueOn
                                    dict['tCueIntOn']=tCueIntOn
                                    dict['tCueInt']=tStim1On-tCueIntOn
                                    dict['SOA']=dict['tCue']+dict['tCueInt']
                                else:
                                    dict['tCueOn']="na"
                                    dict['tCue']="na"
                                    dict['tCueIntOn']="na"
                                    dict['tCueInt']="na"
                                    dict['SOA']="na"
                        if cueType=="endo" and practice==False:
                            dict['cuePos']=cuePos
                        if cueType=="exo" and practice==False:
                            dict['cuePosX']=cuePosX
                            dict['cuePosY']=cuePosY
                            if validCue=="false" or validCue=="true":
                                if cuePos[0]>0:
                                    if cuePos[1]>0:
                                        dict['cuePos']='top right'
                                    else:
                                        dict['cuePos']='bottom right'
                                elif cuePos[0]<0:
                                    if cuePos[1]>0:
                                        dict['cuePos']='top left'
                                    else:
                                        dict['cuePos']='bottom left'
                            else:
                                dict['cuePos']='na'
                        dict['tFix1On']=tFix1On
                        if practice==False:
                            if cueType=="endo" or cueType=="exo":
                                if validCue=="neutral":
                                    dict['tFix1']=tStim1On-tFix1On
                                else:
                                    dict['tFix1']=tCueOn-tFix1On
                            else:
                                dict['tFix1']=tStim1On-tFix1On
                        dict['tStim1On']=tStim1On
                        dict['tStim1']=tMask1On-tStim1On
                        dict['tStim2On']="na"
                        dict['tStim2']="na"
                        dict['tFix2On']=tFix2On
                        dict['tFix2']=tRespAble-tFix2On
                        dict['tMask1On']=tMask1On
                        dict['tMask1']=tFix2On-tMask1On
                        dict['tFix3On']="na"
                        dict['tFix3']="na"
                        dict['tMask2On']="na"
                        dict['tMask2']="na"
                        dict['tRespAble']=tRespAble
                        dict['tRespOn']=tRespOn
                        dict['tRespOff']=tRespOff
                        dict['RTres']=RTres
                        dict['msRTres']=RTres*1000
                        dict['RTtot']=RTtot
                        dict['msRTtot']=RTtot*1000
                        if exp==5 and practice==False:
                            dict['delay1']=delay1
                            dict['delay2']=delay2
                            dict['delay3']=delay3
                            dict['delay4']=delay4
                            dict['delay']=delay
                        if judgOri<=90:
                            dict['judgori']=90-judgOri
                        else:
                            dict['judgori']=270-judgOri
                        dict['angdiff']=(dict['judgori'] - dict['orient'] + 90) % 180 - 90
                        if dict['angdiff'] <= 10 and dict['angdiff'] >= -10:
                            correct=True
                        else:
                            correct=False
                        if practice==True:
                            if correct==True:
                                right.play()
                            else:
                                wrong.play()
                        dict['correct']=correct
                        if trialnum ==1:
                            dict['tIntTrial']="na"
                        else:
                            dict['tIntTrial']=tFix1On-tTrialEndPrev
                        cdw.writerow(dict)
                        break

                    respStim.setOri(90 - judgOri)
                    probe.draw()
                    respStim.draw()
                    expWin.flip()
            if blocknum==numBlocks:
                notdone=True
                blockLabel=psychopy.visual.TextStim(expWin,text="Experiment complete (space bar to exit)",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
                while notdone:
                    blockLabel.draw()
                    expWin.flip()
                    if keyState[key.SPACE] == True:
                        break
f.close()
