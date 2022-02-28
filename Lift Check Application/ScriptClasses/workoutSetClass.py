class workout_set():
    def __init__(self):
        #list of all reps on left hand
        self.left_reps = []
        #list of all reps on right hand
        self.right_reps = []
        #total reps
        self.reps = self.left_reps + self.right_reps
        #left arm reps
        self.left_reps_len = len(self.left_reps)
        #right arm reps
        self.right_reps_len = len(self.right_reps)