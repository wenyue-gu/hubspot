class Country:

    def __init__(self):
        self.attendees = []
        self.name = None
        self.start_date = None

    def add(self, person):
        self.attendees.append(person.email)

    def get_payload(self):
        payload = dict()
        payload['attendeeCount'] = len(self.attendees)
        payload['attendees'] = sorted(self.attendees)
        payload['name'] = self.name
        payload['startDate'] = self.start_date
        return payload

