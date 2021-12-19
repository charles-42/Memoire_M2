class Syllogism:
    
    table_de_verite = {"AA1":["Aac", "Iac", "Ica"], "AA2":["Aca", "Iac", "Ica"], "AA3":"NVC", "AA4":["Iac", "Ica"],
                       "AI1":"NVC", "AI2":["Iac", "Ica"], "AI3":"NVC", "AI4":["Iac", "Ica"],
                       "AE1":["Eac", "Eca", "Oac", "Oca"], "AE2":["Oac"], "AE3":["Eac", "Eca", "Oac", "Oca"], "AE4":["Oac"],
                       "AO1":"NVC", "AO2":"NVC", "AO3":["Oca"], "AO4":["Oac"],  
                       "IA1":["Iac", "Oca"], "IA2":"NVC", "IA3":"NVC", "IA4":["Iac", "Oca"],
                       "IE1":["Oac"], "IE2":["Oac"], "IE3":["Oac"], "IE4":["Oac"], 
                       "EA1":["Oca"], "EA2":["Eac", "Eca", "Oac", "Oca"], "EA3":["Eac", "Eca", "Oac", "Oca"], "EA4":["Oca"],
                       "EI1":["Oca"], "EI2":["Oca"], "EI3":["Oca"], "EI4":["Oca"], 
                       "OA1":"NVC", "OA2":"NVC", "OA3":["Oac"], "OA4":["Oca"],
                       "II1":"NVC", "II2":"NVC", "II3":"NVC", "II4":"NVC",
                       "IO1":"NVC", "IO2":"NVC", "IO3":"NVC", "IO4":"NVC",
                       "EE1":"NVC", "EE2":"NVC", "EE3":"NVC", "EE4":"NVC",
                       "EO1":"NVC", "EO2":"NVC", "EO3":"NVC", "EO4":"NVC",
                       "OA1":"NVC", "OA2":"NVC", "OA3":"NVC", "OA4":"NVC",
                       "OE1":"NVC", "OE2":"NVC", "OE3":"NVC", "OE4":"NVC",
                       "OO1":"NVC", "OO2":"NVC", "OO3":"NVC", "OO4":"NVC"
                    }
    table_mood = {"A":"All", "I":"Some", "E":"No", "O":"Some not"}
    
    def __init__(self, syllogism: str):
        self.syllogism = syllogism
        self.listed = self.__rawsyllogism_to_list()
        self.sentenced = self.__syllogism_to_str()
        self.mood = self.__syllogism_mood()
        self.figure = self.__syllogism_figure()[0]
        self.full_form = self.mood + self.figure
        self.abc = self.__syllogism_figure()[1]
        self.conclusion = self.__get_conclusion()
        self.conclusion_str = self.__conclusion_to_str()
        self.has_conclusion = self.__has_conclusion()

    def __rawsyllogism_to_list(self, input_type="Syllogism",input=None):
        if input_type == "Syllogism":
            sentences = self.syllogism.split("/")
        elif input_type == "choices":
            sentences = input.split("|")    

        for i,sentence in enumerate(sentences):
            sentences[i] = sentence.split(";")
        return sentences

    def __syllogism_to_str(self): 
        sentences = self.__rawsyllogism_to_list()
        sentenced=["",""]
        for i, sentence in enumerate(sentences):
            sentenced[i] = self.premisse_to_str(sentence)
        
        if len(sentences)==1:
            return str(sentenced[0])
        else:
            return " and ".join(sentenced)
    
    @staticmethod
    def premisse_to_str(premisse):
        if  isinstance(premisse,str):
            premisse = premisse.split(";") 
        if premisse[0] == "Some":
            premisse.insert(2,"are")
        if premisse[0] == "All":
            premisse.insert(2,"are")
        if premisse[0] == "No":
            premisse.insert(2,"are")
        if premisse[0] == "Some not":
            premisse[0] = "Some"
            premisse.insert(2,"are not")
        return " ".join(premisse)   

    def __str__(self):
        return self.sentenced

    def __syllogism_mood(self):
    
        sentences =   self.__rawsyllogism_to_list()
        mood=["",""]
        for i, sentence in enumerate(sentences):
            if   sentence[0] == "All":
                mood[i] = "A"
            elif sentence[0] == "Some":
                mood[i] = "I"
            elif sentence[0] == "No":
                mood[i] = "E"
            elif sentence[0] == "Some not":
                mood[i] = "O"  
            else:
                mood[i] = "X" 
        return "".join(mood)

    def __syllogism_figure(self):

        sentences =  self.__rawsyllogism_to_list()
        if   sentences[0][2] == sentences[1][1]:
            return ("1", {'a':sentences[0][1], "b": sentences[0][2], "c":sentences[1][2]})
        elif sentences[0][1] == sentences[1][2]:
            return ("2", {'a':sentences[0][2], "b": sentences[0][1], "c":sentences[1][1]})
        elif sentences[0][2] == sentences[1][2]:
            return ("3", {'a':sentences[0][1], "b": sentences[0][2], "c":sentences[1][1]})
        elif sentences[0][1] == sentences[1][1]:
            return ("4", {'a':sentences[0][2], "b": sentences[0][1], "c":sentences[1][2]})  
        else:
            return ("X","X") 

    def __get_conclusion(self):
        conclusion=[]
        full_dictionnaire = {}
        for d in (self.abc, self.__class__.table_mood):
            full_dictionnaire.update(d)
        for form, conclusions_list in self.__class__.table_de_verite.items():
            if self.full_form == form:
                if conclusions_list == "NVC":
                    return "NVC"
                for valid_conclusion in conclusions_list:
                    c = []
                    for character in valid_conclusion:
                        c.append(full_dictionnaire[character])
                    c.append(valid_conclusion)
                    conclusion.append(c)
        return conclusion

    def __has_conclusion(self):
    #Est ce qu'une full form peut ne pas $etre dans le dico? à tester
        for form, conclusions_list in self.__class__.table_de_verite.items():
            if self.full_form == form:
                if conclusions_list == "NVC":
                    return True
                else:
                    return False
    
    def __conclusion_to_str(self): 
        if self.conclusion == "NVC":
            return "NVC"
        conclusion_str=[]
        for concl in self.conclusion:
            conclusion_str.append(self.premisse_to_str(concl[0:3]))
        return conclusion_str

    def evaluate_form(self, premisse):
        form=["X","X","X"]
        for letter, word in self.table_mood.items():
            if word == premisse[0]:
                form[0] = letter
        for i,member in enumerate(premisse[1:],1):
            for letter, word in self.abc.items():
                if word == member:
                    form[i]=letter
        return "".join(form)

    def evaluate_conclusion(self,premisse):
        if premisse == 'NVC':
            return ("NVC",True) if self.conclusion == "NVC" else ("NVC",False)
        if isinstance(premisse,str):
            premisse = premisse.split(";")
        for valid in self.conclusion:
            if valid[0:3] == premisse:
                return (valid[3], True)
        return (self.evaluate_form(premisse),False)

    def choice_to_str(self,choice):
        choice = choice.split("|")
        choice_to_str=[]
        for c in choice:
            choice_to_str.append(self.premisse_to_str(c))
        return choice_to_str

    def choice_to_form(self,choice):
        choice = self.__rawsyllogism_to_list(input=choice, input_type="choices")
        choices_form=[]
        for c in choice:
            choices_form.append(self.evaluate_form(c))
        return choices_form

    def choice_to_choice_list(self,choice):
        #Très moche
        return self.__rawsyllogism_to_list(input=choice, input_type="choices")


if __name__ == "__main__":
    cho = "All;sailors;potters|All;potters;sailors|Some;sailors;potters|Some;potters;sailors|Some not;sailors;potters|Some not;potters;sailors|No;sailors;potters|No;potters;sailors|NVC"
    my_syl = Syllogism("All;sailors;plumbers/All;plumbers;potters")
    # print(f"{my_syl.conclusion=}")
    # print(f"{my_syl.conclusion_str=}")
    # print(f"{my_syl.full_form=}")
    print(f"{my_syl.choice_to_str(cho)=}")
    print(f"{my_syl.choice_to_form(cho)=}")

