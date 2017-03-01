# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/darshan/.spyder2/.temp.py
"""
import matplotlib.pyplot as plt
from random import randint
import random
print "This program simulates 802.11 WiFi backoff Algorithm "

DIFS = 52 #the standard 52 microseconds
SIFS = 9  #standard 9 microseconds
ACK = 9   #standard 9 microseconds
numpackets = [] # stores number of packets each device wants to transmit
collisions=0    #stores number of collisions
CW=[]           #stores contention window size
CWW=[]          #store current selection of each device from the contention window
ma=2            
idle=False
x=0
y=0
t=0
p=0.7
l=0.0
th=0.0
lo=0.0
l1=0.0
th1=0.0
lo1=0.0
l2=0.0
th2=0.0
lo2=0.0
num=[]
throughput=[]
latency=[]
coll=[]

def original():
    #This routine or method simulates the original wifi 802.11 MAC protocol   
    
    #python requires global declaration for variables that are not local
    global y
    global DIFS #the standard 52 microseconds
    global SIFS #standard 9 microseconds
    global ACK    
    global numpackets
    global collisions
    global CW
    global CWW
    global ma
    global idle
    global x
    global y
    global t
    global l
    global th
    global lo
    global num
    global num1
    global me
    
    l=0.0
    th=0.0
    lo=0.0
    
    print "Enter the number of devices in this simulation "
    x=input()
    numpackets=[0]*x
    CWW = [2000]*x
    CW = [4]*x
    num=[0]*x
    print "Select the time slot for transmitting one packet for each device (Remains same for each device)"
    y=input()
    print "the simulation starts now with time " + str(t)

    
        
    while True:
        print "time = " +str(t)
        
        # give a call to firsttime routine to initialize the simulation parameters    
        if t==0:
            firstTime()

        #this will calculate the contention window for each devices and packages if it is not already initialized
        contentionWindow()
        
        
        #if idle==True:
        
        for i in range(ma):
            
            check=0
            unit=[]
            first=-1
            for j in range(x):
                print "Current contention window of device "+str(j)+" is "+str(CWW[j])
                if (CWW[j])==i and (numpackets[j])!=0:
                    first=j
                    check=check+1
                    unit.append(j)
            #the next part of code checks if the device j was the only device or not and if yes, it transmits
            if check == 1:
                transmit(first)
                SIFS1()
                ACK1()
                DIFS1()
                break
            #this checks for collision and if it happened sends a jam signal
            elif check > 1:
                collision(unit,i)
            
                break
            #checks if nobody was active ? Increments time by one time slot
            elif (check)==0:
                for k in range(x):
                    if CWW[k] != 0:
                        CWW[k]=CWW[k]-1
                t=t+1
                l=l+1
                break
    
            #condition to exit, that is check is everybody done transmitting?
        check1=0
        for i in range(x):
            if numpackets[i]!=0:
                check1=1
        if check1==0:
            #caculates the final parameters
            for i in range(x):
                lo=lo+num[i]*y/2
            th=lo/(lo+l)
        
            final()
            throughput.append(th)
            latency.append(l)
            coll.append(collisions)
            ppersis()
            break
    
    
  
def pvpersis():
    #This routine is formed to implement modified 802.11 MAC protocol which is efficient as compared to     
    print 'this program will now simulate p-persistent (variable p) backoff algorithm'
    
    global y
    global DIFS #the standard 52 microseconds
    global SIFS #standard 9 microseconds
    global ACK    
    global numpackets
    global collisions
    global CW
    global CWW
    global ma
    global idle
    global x
    global y
    global t
    global p
    global th2
    global l2
    global lo2
    global num
    t=0
    ma=4
    collisions=0
    
    th2=0.0
    l2=0.0
    lo2=0.0
    
    get=0
    print "Enter the number of devices in this simulation (maximum 5)"
    x=input()

    print "Select the time slot for transmitting one packet for each device "
    y=input()
    print "the simulation starts now with time " + str(t)

       
    for i in range(x):
        numpackets[i]=0    
    
    for i in range(x):
        CWW[i]=2000

    for i in range(x):
        CW[i]=4
        
    while True:
        print "t = " +str(t)
        
            # give a call to firsttime routine to initialize the simulation parameters
        if t==0:
            firstTime()

        #this will calculate the contention window for each devices and packages if it is not already initialized
        contentionWindow()
        
        #the next part of code we do to check how many devices are active at this time (which should be an assumption)
        # This will give us the best possible performance of the algorithm        
        ok=0.0
        for k in range(x):
            if (CWW[k])==0:
                ok=ok+1
        if ok>0:
            p=1/ok
        elif ok==0:
            p=1

        
        #if idle==True:
        
        for i in range(ma):
           
            check=0
            unit1=[]
            first=-1
            for j in range(x):
                print "Current contention window of device "+str(j)+" is "+str(CWW[j])
                #this will calculate random number which will be compared with p to make transmission decision
                get=random.uniform(0,1) 
                
                if CWW[j]==i and get>p:
                    #decides not to transmit and waits for one more time slots (for efficiency we have taken one)
                    CWW[j]=CWW[j]+1
                    
                    
                if (CWW[j])==i and (numpackets[j])!=0 and (get)<=(p):
                    first=j
                    check=check+1
                    unit1.append(j)
                
                #the next part of code checks if the device j was the only device or not and if yes, it transmits
            if check == 1:
                transmit(first)
                SIFS1()
                ACK1()
                DIFS1()
                break
                #this checks for collision and if it happened sends a jam signal
            elif check > 1:
                collision(unit1,i)
                break
                #checks if nobody was active ? Increments time by one time slot
            elif (check)==0:
                for k in range(x):
                    if CWW[k] != 0:
                        CWW[k]=CWW[k]-1
                t=t+1
                l2=l2+1
                break
                
    
            #condition to exit, that is check is everybody done transmitting?
        check1=0
        for i in range(x):
            if numpackets[i]!=0:
                check1=1
        if check1==0:
            #caculates the final parameters
            for i in range(x):
                lo2=lo2+num[i]*(y)
            th2=lo2/(lo2+l2)
            print str(lo2)+" "+str(l2)+" "+str(th2) 
            throughput.append(th2)
            latency.append(l2)
            coll.append(collisions)
            axr=[1,2,3]
            fig=plt.figure()
                        
            ax1=fig.add_subplot(1,1,1)
            plt.title('Comparison of throughputs')
            plt.xlabel('1-original 2-fixed p  3-variable')            
            plt.ylabel('Throughputs')            
            ax1.bar(axr,throughput)
            
            fig2=plt.figure()
            ax2=fig2.add_subplot(1,1,1)
            plt.title('Comparison of latency')
            plt.xlabel('1-original 2-fixed p  3-variable')            
            plt.ylabel('Latencies')            
            ax2.bar(axr,latency)
            
            fig3=plt.figure()
            ax3=fig3.add_subplot(1,1,1)
            plt.title('Comparison of collisions')
            plt.xlabel('1-original 2-fixed p  3-variable')            
            plt.ylabel('collisions')
            ax3.bar(axr,coll)
            
            final()
            break
        

def transmit(h):
    #this routine is called by the algorithm when a device is allowed to tansmit data packet without collision
    global t
    global numpackets
    global CWW
    t=t+y
    
    #after transmission initializes next packet
    print "one packet of device " +str(h)+" is transmitted"
    numpackets[h]=numpackets[h]-1
    print str(numpackets[h])+" more packets of device " + str(h) + " remaining"
    if (numpackets[h])!=0:
        CWW[h]=2000
        CW[h]=4
        
def DIFS1():
    #Routine for sending DIFS frame
    global t
    global l
    global th
    global lo    
    t=t+DIFS
    
    print "DIFS frame being sent.  time after that is t = " + str(t)
    
def SIFS1():
    #Routine for sending SIFS frame
    global t
    global l
    global th
    global lo
    t=t+SIFS
    print "SIFS frame being sent. time after that is = " + str(t)
    
def ACK1():
    #Routine for sending ACK frame
    global t
    global load
    global throughput
    global latency
    global l
    global th
    global lo    
    t=t+ACK
    print "ACK frame recieved at time t = " + str(t)
    
def collision(h,g):
    #this routine is called when the collision happens
    global t
    global collisions
    global CW
    global CWW
    global ma
    global l
    global th
    global lo
    global l1
    global l2
    
    t=t+y
    l=l+y
    l1=l1+y
    l2=l2+y
    print "collision happens"
    collisions=collisions+1
    for i in range(len(h)):
        print i
        temp=h[i]        
        CW[temp]=CW[temp]*2
        CWW[temp]=2000
        
    ma=ma*2


def firstTime():
    #This is called as soon as the simulation starts to initialize the program parameters
    global t
    global x
    global numpackets
    global num
        
    for i in range(x):
        print "Enter number of packets device " +str(i)+ "needs to send "
        numpackets[i]=input()
        num[i]=numpackets[i]
    print "The router sends DIFS frame at t=0 "
    t=t+DIFS
    print "t=" +str(t)
    print "At this time the " +str(x)+ "devices start competing for WIFI medium using a typical contention window of (0,1)"
       # idle=True

def contentionWindow():
    #this method initiates the waiting time based on Contention window for each new packet
    global CWW
    global CW
    global l
    global th
    global lo
    
    for i in range(x):
            if CWW[i]==2000:
                
                CWW[i]=randint(0,CW[i]-1)
                print "Device " +str(i)+ "randomly selects " +str(CWW[i])+ "from the contention window (0,"+str(CW[i]-1)+")"
    

def final():
    #this routine is the last routine of the program that is executed before ending the simulation
    #it calculates the final parameters as output
    global t
    global collisions
    print "The simulation ends at time t = " + str(t)
    print "The total number of collisions that took place = " + str(collisions)

def ppersis():
    print 'this program will now simulate p-persistent backoff algorithm'
    
    global y
    global DIFS #the standard 52 microseconds
    global SIFS #standard 9 microseconds
    global ACK    
    global numpackets
    global collisions
    global CW
    global CWW
    global ma
    global idle
    global x
    global y
    global t
    global p
    global l1
    global lo1
    global th1
    global num
    t=0
    ma=4
    collisions=0
    
    get=0
    print "Enter the number of devices in this simulation (maximum 5)"
    x=input()

    print "Select the time slot for transmitting one packet for each device "
    y=input()
    print "the simulation starts now with time " + str(t)

       
    for i in range(x):
        numpackets[i]=0    
    
    for i in range(x):
        CWW[i]=2000

    for i in range(x):
        CW[i]=4
        
    while True:
        print "t = " +str(t)
        
            # give a call to firsttime routine to initialize the simulation parameters
        if t==0:
            firstTime()

        #this will calculate the contention window for each devices and packages if it is not already initialized
        contentionWindow()
        ok=0.0
        for k in range(x):
            if (CWW[k])==0:
                ok=ok+1
        #the next part of code we do to check how many devices are active at this time (which should be an assumption)
        # This will give us the best possible performance of the algorithm
        if ok>0:
            p=0.2
        elif ok==0:
            p=1
        
        
        #if idle==True:
        
        for i in range(ma):
           
            check=0
            
            unit2=[]
            first=-1
            for j in range(x):
                                 
                get=random.uniform(0,1)
                
                if CWW[j]==i and get>p:
                    CWW[j]=CWW[j]+1
                    
                    
                if (CWW[j])==i and (numpackets[j])!=0 and (get)<=(p):
                    first=j
                    check=check+1
                    unit2.append(j)
                
            #the next part of code checks if the device j was the only device or not and if yes, it transmits    
            if check == 1:
                transmit(first)
                SIFS1()
                ACK1()
                DIFS1()
                break
            #this checks for collision and if it happened sends a jam signal    
            elif check > 1:
                collision(unit2,i)
            #checks if nobody was active ? Increments time by one time slot
                break
            elif (check)==0:
                for k in range(x):
                    if CWW[k] != 0:
                        CWW[k]=CWW[k]-1
                t=t+1
                l1=l1+1
                break
                
    
            #condition to exit, that is check is everybody done transmitting?
        check1=0
        for i in range(x):
            if numpackets[i]!=0:
                check1=1
        if check1==0:
            #caculates the final parameters
            for i in range(x):
                lo1=lo1+num[i]*y
            th1=lo1/(lo1+l1)
            print str(lo1)+" "+str(l1)+" "+str(th1)
            final()
            throughput.append(th1)
            latency.append(l1)
            coll.append(collisions)
            pvpersis()
            break
        
print "This program can simulate the three backoff algorithms "
original()
 #print "Enter choice 1.)original exponential backoff 2.)p-persistant backoff with fixed p 3.)p-persisten backoff with variable p")
#if usrchoice==1:    
#    original()
#elif usrchoice==2:
#    ppersis()
#elif usrchoice==3:
#    pvpersis()
    
        