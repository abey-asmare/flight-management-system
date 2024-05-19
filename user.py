import csv

class User:
    def __init__(self, id, name, email, profile_image_url, login):
        self.id = id
        self.name = name
        self.email = email
        self.profile_image_url = profile_image_url
        self.login = login

    def save(self):
        with open('assets/.userinfo.csv', mode='w', newline='') as csv_file:
            fieldnames = ['id', 'name', 'email', 'profile_image', 'login']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerow({
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'profile_image': self.profile_image_url,
                'login': self.login
            })

    @classmethod
    def retrieve(cls):
        with open('assets/.userinfo.csv', mode='r', newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            # Read the first row of user data
            row = next(reader, None)
            if row:
                return cls(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    profile_image_url=row['profile_image'],
                    login=row['login']
                )
        return None