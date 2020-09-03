class Partner:
    def __init__(self, data):
        self.firstname = data['firstName']
        self.lastname = data['lastName']
        self.email = data['email']
        self.country = data['country']
        self.availableDates = data['availableDates']
