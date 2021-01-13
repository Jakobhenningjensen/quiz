#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:31:51 2019

@author: jakob
"""
import numpy as np
from time import sleep
from random import shuffle
import tkinter

class quiz():
    def __init__(self,teams,file = "questions.txt"):
        #Teams: vector tmer navne
        #File: fil med spørgsmål med formatet "Spørgsmål, korrekt svar, svar2,svar3,svar4....
        
        try:
            self.questions = np.loadtxt(file,delimiter=",",encoding="ISO-8859-1",dtype="str")
            self.answers = [q[1:] for q in self.questions] #Alle svar (første er det korrekte)
            self.questions=[q[0] for q in self.questions ] #Spørgsmål
                       
        except OSError:
            print("Questions are not found is not found!")
          
           
        self.teams=teams
        self.score=np.zeros(len(teams),dtype=int)
        
        
        #Shufle the questions and save the correct answer
        self.ans_true = [p[0] for p in self.answers] #Correct answer
        [shuffle(p) for p in self.answers] #shuffle the answers 
        
    def start(self):
        c=1 #Count for questions
        t=0 #Count for teams
        n_questions = len(self.questions)
        for ques,ans,true_answer,in zip(self.questions,self.answers,self.ans_true):
            
            team=self.teams[t] #Current team to answer

            #### Print the question ####
            print("---------------------------------")
            print(f"-------- Question {c} of {n_questions} -------------")
            print("---------------------------------\n\n")
            print(f"Score: {self.score}")
            
            print(f"Hold {team}: "+ques+"\n")
            
             
            
            ##### Print the possible answers ####
            for i,a in enumerate(ans,start=1):
                print(f"{i}) "+a)
                
            

            # Making sure input is correct
            ans_false = True
            while ans_false:
                ans_in =input("Answer:")
            
                try:
                    ans_in = int(ans_in)
                    ans_false=False
                except ValueError:
                    print("Input a single number!")
                    
            #Checker om svaret er korrekt
            if true_answer==ans[ans_in-1]:
                print("Correct!")
                self.score[t]+=1
            else:
                print(f"Wrong, the correct answer is: {true_answer}")
            
            #Next team
            t+=1
            if t==len(self.teams):
                t=0
            c+=1
            sleep(2.5)

        #All questions have been asked - print the winner
        self.winner = self.score.argmax()
        print(f"The winner is: {self.teams[self.winner]}")
        return(None)
        

def main():
    n_teams = int(input("How many teams are you?"))
    teams=[]
    for i in range(n_teams):
        teams.append(input(f"Please write the name of team {i+1}: "))
    q = quiz(teams)
    create_gui(q)
    #q.start()



def create_gui(q):
    """
    Function that creates the GUI for the quiz

    Inputs
    -------
    q: quiz-object

    """
    window = tkinter.Tk()
    window.title("The Quizzzzz")
    #Get resolution of screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    frame = tkinter.Frame(window)
    frame.pack(fill=tkinter.BOTH,expand=True)


    ###  Print the score-board ###
    #title
    score_title = tkinter.Label(frame,text="Score")
    score_title.config(font=("Courier",40))
    score_title2 = tkinter.Label(frame,text="Score2")
    score_title2.config(font=("Courier",40))
    #score_title.grid(side=tkinter.TOP,anchor="w")
    score_title.grid(row=0,column=0)
    score_title2.grid(row=1,column=0)

    """
    #
    #Scores
    for team,scores in zip(q.teams,q.score):
        score = tkinter.Label(frame,text=f"{team}: {scores}")
        score.config(font=("Courier",20))
        score.pack(side=tkinter.TOP,anchor="w")


    ### Print the question ###




    tkinter.Button(frame, text = "Start!",command=q.start,bg="green").pack(anchor="s") #Start button
    tkinter.Canvas(frame,bg="green",height=screen_height*1/4,width=screen_height*1/4).place(relx=1.0,rely=0.0) #Scoreboard """
    window.mainloop()
    

if __name__=="__main__":
    create_gui(2)
    #main()
    
    
