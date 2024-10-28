from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='medications/', blank=True, null=True)
    side_effects = models.ManyToManyField('SideEffect', related_name='medications', blank=True)

    def __str__(self):
        return self.name

class SideEffect(models.Model):
    description = models.CharField(max_length=255)
    # Stores the NLP score (e.g., 0.1 to 1.0)
    severity_score = models.FloatField(null=True, blank=True)  
     # Stores the label (e.g., 'mild', 'moderate', 'severe')
    severity_label = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.description

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medications = models.ManyToManyField(Medication, related_name='treatments', blank=True)

    def __str__(self):
        return self.name



class Feedback(models.Model):
    treatment = models.ForeignKey(Treatment, related_name='feedback', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.treatment.name} - Score: {self.sentiment_score}"
        
