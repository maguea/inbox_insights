# Nate Katz

class Category:
    def __init__(self, name):
        self.name = name  #name of the category        
        self.target_senders = set()  #set of emails that should be auto added to this category
        self.alternative_names = set()   #set of alternative names for this category
        self.emails = []  #list of emails that have been categorized here     

    def add_alternative_name(self, alt_name):
        self.alternative_names.add(alt_name)

    def remove_alternative_name(self, alt_name):
        if alt_name in self.alternative_names:
            self.alternative_names.remove(alt_name)

    def add_target_sender(self, email):
        self.target_senders.add(email)

    def remove_target_sender(self, email):
        if email in self.target_senders:
            self.target_senders.remove(email)

    def add_email(self, email):
        self.emails.append(email)

    def remove_email(self, email):
        if email in self.emails:
            self.emails.remove(email)

    def clear_emails(self):
        self.emails = []
    
    def list_target_senders(self):
        return self.target_senders
    
    def count_target_senders(self):
        return len(self.target_senders)
    

    
