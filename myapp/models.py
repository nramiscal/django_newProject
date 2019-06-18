from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class OwnerManager(models.Manager):
    def registerValidator(self, request):
        # do our validations
        print("2. inside models.py registerValidator")
        print(request.POST)

        errors = {}

        if not request.POST["fname"]:
            errors["fname"] = "Please provide a first name."
        if not request.POST["lname"]:
            errors["lname"] = "Please provide a last name."

        '''
        import re	# the regex module
        # create a regular expression object that we'll use later
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        @app.route('/process', methods=['POST'])
        def submit():
            if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
                flash("Invalid email address!")
        '''

        if not request.POST["email"]:
            errors["email"] = "Please provide an email."
        elif not EMAIL_REGEX.match(request.POST['email']):
            errors["email"] = "Invalid email format."
        else:
            # check that email not already in database
            users = Owner.objects.filter(email=request.POST["email"])
            if users:
                errors["email"] = "Email already in database. Please log in."

        if not request.POST["password"]:
            errors["password"] = "Please provide a password."
        elif request.POST["password"] != request.POST["confirm_pw"]:
            errors["password"] = "Passwords do not match."


        print("3. returning errors dictionary to views")
        return errors



class Owner(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = models.Manager() <-- default
    objects = OwnerManager() # <-- overwriting default
    # pets

    def __repr__(self):
        return f"<Owner {self.fname} id: {self.id}>"

class Pet(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(Owner, related_name="pets", on_delete = models.CASCADE)

    # objects = models.Manager()


    def __repr__(self):
        return f"<Pet {self.name} id: {self.id}>"
