class rep():
    def __init__(self):
        #time it took to complete the rep
        self.timeup = 0
        #list of form issues
        self.form_issues = set()
        self.min_angle = 180
        #which side the rep was completed on
        self.which_side_rep = ""
    
    #returns the form issues    
    def get_form_issues(self):
        return self.form_issues
    
    #adds a form issue to the rep
    def add_form_issue(self, strFormIssue):
        self.form_issues.add(strFormIssue)
    
    #pass in a string of the form "left" or "right"    
    def add_which_side(self, side):
        self.which_side_rep = side
    
    #returns the time a rep took to complete
    def get_time_str(self):
        return self.timeup
    
    def toString(self):
        return 

    def __str__(self):
        return str([self.timeup, self.form_issues, self.which_side_rep])