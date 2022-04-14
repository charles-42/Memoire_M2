from numpy import true_divide
from utils import table_de_verite, choice_form


class Syllogism:
    """ class used to analyse syllogisms for Ragni2016 and Verser2018
    
    arg: two premisses separated by / : 
        exemple: Some;models;manages/All;models;clerks
    
    """

    table_de_verite = table_de_verite
    table_mood = {"A":"All", "I":"Some", "E":"No", "O":"Some not"}
    
    choice_form = choice_form

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
        """Transform the raw format to list

        Args:
            input_type (str, optional): 
                - if input_type = "Syllogism" (Defaults) take class argument as argument
                - if input_type = "choices", takes a choice list as argument (list of one premisse separated by | ).
            input ([str], optional): argument if input_type = "choices"

        Returns:
            list: Syllogism or choices as list
        """

        if input_type == "Syllogism":
            sentences = self.syllogism.split("/")
        elif input_type == "choices":
            sentences = input.split("|")    

        for i,sentence in enumerate(sentences):
            sentences[i] = sentence.split(";")
        return sentences

    @staticmethod
    def premisse_to_str(premisse):
        """Transform a single premisse to str

        Args:
            premisse (list or str): if str each word is separated by ;
                exemple: "Some;models;manages"

        Returns:
            str: a clean premisse
        """
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
    
    def __syllogism_to_str(self): 
        
        """ Transform the raw format to clean strings: 
            
            Args:
            - syllogism (two premisses separated by / )
            - choices (list of one premisse separated by | )

            Return:
            - for syllogism a string like Some models are managers and All models are clerks
            - for cloices a list of strings
        """
        sentences = self.__rawsyllogism_to_list()
        sentenced=["",""]
        for i, sentence in enumerate(sentences):
            sentenced[i] = self.premisse_to_str(sentence)
        
        if len(sentences)==1:
            return str(sentenced[0])
        else:
            return " and ".join(sentenced)


    def __str__(self):
        return self.sentenced

    def __syllogism_mood(self):
        """ Return the mood of the syllogism

        Returns:
            str: two letter description
            A: All
            I: Some
            E: NO
            O: Some not
            X: Unknown 
        """
    
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
        """Return Syllogisme figure

        Returns:
            tuple: first element: the figure (from 1 to 4) 
                    second element: the value of each composant of the figure
                    return (X,X) if unknown
        """

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
        """From a syllogism, return the list of valid conclusion

        Returns:
            List[List]: each element of the main list is a valid conclusion which includes
                the three elements plus the form of the valid conclusion 
                retrun "NVC" if there is no valid conclusion
        """
        conclusion=[]
        full_dictionnaire = {}
        for d in (self.abc, self.__class__.table_mood):
            full_dictionnaire.update(d)
        for form, conclusions_list in self.__class__.table_de_verite.items():
            if self.full_form == form:
                if conclusions_list == ["NVC"]:
                    return ["NVC"]
                for valid_conclusion in conclusions_list:
                    c = []
                    for character in valid_conclusion:
                        c.append(full_dictionnaire[character])
                    c.append(valid_conclusion)
                    conclusion.append(c)
        return conclusion

    def __has_conclusion(self):
        """Return if the conclusion has valid conclusion or not

        Returns:
            bool: has valid conclusion or not
        """
    #Est ce qu'une full form peut ne pas $etre dans le dico? à tester
        for form, conclusions_list in self.__class__.table_de_verite.items():
            if self.full_form == form:
                return False if conclusions_list == ["NVC"] else True

    
    def __conclusion_to_str(self):
        """
        Transform the valid conclusion list to string format.
        """ 
        if self.conclusion == ["NVC"]:
            return ["NVC"]
        conclusion_str=[]
        for concl in self.conclusion:
            conclusion_str.append(self.premisse_to_str(concl[0:3]))
        return conclusion_str

    def evaluate_form(self, conclusion):
        """for a syllogisme, five the form of a conclusion

        Args:
            conclusion (list): a conclusion on the list format (three elements)

        Returns:
            str: the form of the conclusion
        """
        form=["X","X","X"]
        for letter, word in self.table_mood.items():
            if word == conclusion[0]:
                form[0] = letter
        for i,member in enumerate(conclusion[1:],1):
            for letter, word in self.abc.items():
                if word == member:
                    form[i]=letter
        return "".join(form)

    def evaluate_conclusion(self,ccl):
        """ for a given Syllogism return if a conclusion is valid or not

        Args:
            ccl (list): a conclusion on the list format (three elements)


        Returns:
            tuple: fist element: the form of the conclusion
                    second element: a booleenn, the conclusion is valid or not
        """
        if ccl == 'NVC':
            return ("NVC",True) if self.conclusion == ["NVC"] else ("NVC",False)
        if isinstance(ccl,str):
            ccl = ccl.split(";")
        for valid in self.conclusion:
            if valid[0:3] == ccl:
                return (valid[3], True)
        return (self.evaluate_form(ccl),False)

    def choice_to_str(self,choice):
        choice = choice.split("|")
        choice_to_str=[]
        for c in choice:
            choice_to_str.append(self.premisse_to_str(c))
        return choice_to_str


    def choice_to_choice_list(self,choice):
        #Très moche
        return self.__rawsyllogism_to_list(input=choice, input_type="choices")


if __name__ == "__main__":
    cho = "All;sailors;potters|All;potters;sailors|Some;sailors;potters|Some;potters;sailors|Some not;sailors;potters|Some not;potters;sailors|No;sailors;potters|No;potters;sailors|NVC"
    my_syl = Syllogism("All;sailors;plumbers/All;plumbers;potters")
    print(f"{my_syl.conclusion=}")
    # print(f"{my_syl.conclusion_str=}")
    # print(f"{my_syl.full_form=}")

    #print(f"{my_syl.choice_to_str(cho)=}")
    #print(f"{my_syl.choice_to_form(cho)=}")

