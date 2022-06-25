from django.db import models
from django.contrib.auth.models import User

# These models will be used to store the assignments that operatives will be assigned to.
# Each assignment will have a name, a summary, a detailed description of the task, a due date, and a list of operatives assigned to it, as well as 
# The assignment will also have a list of operatives that have been assigned to it.
# Each operative will be able to be assigned to multiple assignments.
# Operatives can submit text, files (photos, videos or audio) or both.

class Task(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    detail = models.TextField()
    #difficulty = models.IntegerField(default=0)
    location = models.CharField(max_length=200, default="")
    due_date = models.DateField(default=None, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    type = models.CharField(max_length=200, default="Spirit Bomb")
    agents_required = models.IntegerField(default=1)
    max_agents = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    @property
    def time_to_complete(self):
        return self.due_date - self.creation_date

    @property
    def assignment_set(self):
        return Assignment.objects.filter(task=self)

    @property
    def agents(self):
        return [assignment.agents for assignment in self.assignment_set]

class Team(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_lead")

    def __str__(self):
        return self.name

class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=200, default="Not Started")
    assigned_date = models.DateTimeField(default=None, blank=True, null=True)
    completed_date = models.DateTimeField(default=None, blank=True, null=True)

    @property
    def publicity(self):
        return self.task.public

    @property
    def files(self):
        return Attachment.objects.filter(task=self.task)
    
    @property
    def submissions(self):
        this_sumbissions = Submission.objects.filter(assignment=self)
        if this_sumbissions:
            self.status = "Pending Review"
            return this_sumbissions
        else:
            return None

    def __str__(self):
        return self.task.name + " - " + self.agent.username

class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_attachments/')
    file_name = models.CharField(max_length=200)

    def __str__(self):
        return self.task.name + " Attachment: " + self.file_name

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def files(self):
        return SubmitFile.objects.filter(submission=self)

    def __str__(self):
        return self.assignment.name + " - " + self.text[:20]

class SubmitFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_files/')
    file_name = models.CharField(max_length=200)

    def __str__(self):
        return self.submission.assignment.name + " Submission: " + self.file_name