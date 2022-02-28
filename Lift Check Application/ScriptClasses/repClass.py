class rep():
    def __init__(self):
        #how much time was the person doing the rep
        self.timeup = 0
        self.form_issues = set()
        self.which_side_rep = ""
        
    def form_issues(self):
        return self.form_issues
    
    def add_form_issue(self, strFormIssue):
        self.form_issues.add(strFormIssue)
        
    def add_which_side(self, side):
        self.which_side_rep = side
    
    def getTimeStr(self):
        return self.timeup

    def __str__(self):
        return str([self.timeup, self.form_issues, self.which_side_rep])