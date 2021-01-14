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
from tkinter import messagebox

class quiz():
    def __init__(self,teams,file = "questions.txt"):
        #Teams: vector tmer navne
        #File: fil med spørgsmål med formatet "Spørgsmål, korrekt svar, svar2,svar3,svar4....
        
        try:
            self.questions = np.loadtxt(file,delimiter=",",encoding="ISO-8859-1",dtype="str")
            self.answers = [q[1:] for q in self.questions] #All answers svar (the first is the correct)
            self.questions = (q[0] for q in self.questions) #the question

        
        except OSError:
            print("Questions are not found is not found!")
          
        
        #Team info
        self.teams=teams
        self.n_teams = len(teams)
        self.score=np.zeros(len(teams),dtype=int)
        
        
        #Save the correct answer and make the answers iterable instead of list
        self.ans_true = [p[0] for p in self.answers] #Correct answer
        self.ans_true = iter(self.ans_true)
        [np.random.shuffle(p) for p in self.answers] #Shuffle the answers
        self.answers = iter(self.answers) #Make it an iterator

        #Define variables for current answers/questions
        self.cur_team = 0
        self.cur_answers = self.answers.__next__()
        self.cur_answer_true = self.ans_true.__next__()
        self.cur_question = self.questions.__next__()

    def get_team(self):
        """
        return the current team
        """



    def update_next_question(self):
        """
        Gives the next question and answer self.cur_answer and self.cur_answer_true to the next 
        """

        try:
            self.cur_answers = self.answers.__next__()
            self.cur_answer_true = self.ans_true.__next__()
            self.cur_question = self.questions.__next__()
            self.cur_team +=1
            
            if self.cur_team == self.n_teams: #Reset the team if we are at the end
                self.cur_team = 0
        except StopIteration: #We are done - return empty answers
            self.cur_answers = [""]*len(self.cur_answers)
            self.cur_question = "<The End>"


        

        
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
    score_dict = {i:tkinter.Label(frame_score,text=0,font=("Courier",20)) for i in range(len(q.teams))} 
    for i,label in enumerate(score_dict.values()):       
        label.grid(row=i+1,column=1)
    
    #Teams
    team_dict = {team:tkinter.Label(frame_score,text=f"{team}:",font=("Courier",20)) for team in q.teams} 
    for i,label in enumerate(team_dict.values()):       
        label.grid(row=i+1,column=0)

    
    
    ## Create the question,asnwers etc ##

    #Frame
    frame_questions = tkinter.Frame(window,bg="white")
    frame_questions.pack(side=tkinter.TOP)

    
    def check_pressed_answer(answer_idx):
        """
        Check if the marked answer is correct - return 1 if it is true, else zero
        """
        correct_answer = q.cur_answer_true

        if q.cur_answers[answer_idx] == correct_answer:
            messagebox.showinfo(message="CORRECT!")
            return 1
        messagebox.showerror(message=f"Wrong, the correct answer is: {correct_answer}")
        return 0
        
        

    def nexts():
        """
        Function for updating points and give the next question/answer
        """
        
        answer_pressed = chosen_answer.get() #index of which answer has been pressed
        points = check_pressed_answer(answer_pressed) #1 if correct answer, 0 otherwise
        
        #Update the points for the current team
        q.score[q.cur_team] +=points
        score_dict[q.cur_team].config(text =q.score[q.cur_team])



        
        #Next question and answer
        q.update_next_question()
        
        #Update answer
        cur_answers = q.cur_answers
        #np.random.shuffle(cur_answers) #Shuffle the question
        for ans,but in zip(cur_answers,radio_buttons_dict.values()):
            but.configure(text = ans)
        
        #Update question
        question_box.configure(text = q.cur_question)
        
    




        

    #Box with the question
    question_box = tkinter.Message(frame_questions,bg = "lightblue",text = q.cur_question,font=("Helvetica",20),justify=tkinter.LEFT,aspect=200,relief=tkinter.SUNKEN) #Initialize with the first question
    question_box.pack()


    #Radio buttons for the different answer-choices
    chosen_answer = tkinter.IntVar()
    radio_buttons_dict =  {"radio_"+str(i):tkinter.Radiobutton(frame_questions,text=ans,variable=chosen_answer,value=i) for i,ans in enumerate(q.cur_answers)} #Create dictionary of buttons - initialize with the first answers


    #Print the radio buttons to the creen
    for but in radio_buttons_dict.values():
        but.pack()



    #Create button for next question and answer
    tkinter.Button(text="Answer",bg="green",command=nexts).pack()


    window.mainloop()
    

if __name__=="__main__":
    #create_gui(2)
    main()
    
    
