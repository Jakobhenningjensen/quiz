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
            self.questions = (q[0] for q in self.questions) #Spørgsmål
                       
        except OSError:
            print("Questions are not found is not found!")
          
           
        self.teams=teams
        self.score=np.zeros(len(teams),dtype=int)
        
        
        #Shufle the questions and save the correct answer
        self.ans_true = [p[0] for p in self.answers] #Correct answer
        [shuffle(p) for p in self.answers] #shuffle the answers
        self.answers = iter(self.answers)
        
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
    window.geometry(f"{int(screen_width*0.5)}x{int(screen_height*0.5)}")
    
    frame_score = tkinter.Frame(window)
    frame_score.pack(anchor="w")


    ###  Print the score-board ###
    #title
    score_title = tkinter.Label(frame_score,text="Score")
    score_title.config(font=("Courier",40))
    score_title.grid(row=0,column=0)

    #
    #Scores
    for i,(team,scores) in enumerate(zip(q.teams,q.score)):
        score = tkinter.Label(frame_score,text=f"{team}: {scores}")
        score.config(font=("Courier",20))
        score.grid(row=i+1,column=0)

    
    
    
    
    
    ## Create the question,asnwers etc ##

    #Frame
    frame_questions = tkinter.Frame(window,bg="white")
    frame_questions.pack(side=tkinter.TOP)

    #Functions for updating the question and answers
    def nextQuestion():
        try:
            question_box.configure(text = q.questions.__next__())
        except StopIteration:
            question_box.configure(text = "<The End>")
    
   
    def nextAnswer():
        try:
            cur_answers = q.answers.__next__()
            for ans,but in zip(cur_answers,radio_buttons_dict.values()):
                but.configure(text = ans)
        except StopIteration:
                
                for but in radio_buttons_dict.values():
                    but.configure(text = "")
    
    def nexts():
        """
        Updates questions and answers
        """
        nextAnswer()
        nextQuestion()



        

    #Box with the question
    question_box = tkinter.Message(frame_questions,bg = "lightblue",text = q.questions.__next__(),font=("Helvetica",20),justify=tkinter.LEFT,aspect=200,relief=tkinter.SUNKEN) #Initialize with the first question
    question_box.pack()


    #Radio buttons for the different answer-choices
    chosen_answer = tkinter.IntVar()
    radio_buttons_dict =  {"radio_"+str(i):tkinter.Radiobutton(frame_questions,text=ans,variable=chosen_answer,value=i) for i,ans in enumerate(q.answers.__next__())} #Create dictionary of buttons - initialize with the first answers


    #Print the radio buttons to the creen
    for but in radio_buttons_dict.values():
        but.pack()



    #Create button for next question and answer
    tkinter.Button(text="Next question!",bg="green",command=nexts).pack()


    window.mainloop()
    

if __name__=="__main__":
    #create_gui(2)
    main()
    
    
