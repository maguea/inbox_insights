# Nate Katz

class Category:
    def __init__(self, name):
        self.name = name  #name of the category        
        self.target_senders = set()  #set of emails that should be auto added to this category
        self.category_tags = set()   #set of alternative names for this category
        self.emails = []  #list of emails that have been categorized here     

    def add_category_tag(self, cat_tag):
        self.category_tags.add(cat_tag)

    def remove_category_tag(self, cat_tag):
        if cat_tag in self.category_tags:
            self.category_tags.remove(cat_tag)

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
    

    
