
from django.core.management.base import BaseCommand
from Medication.models import SideEffect
from Medication.nlp_utils import analyze_side_effect_severity  # We'll create this utility function next

class Command(BaseCommand):
    help = 'Analyze the severity of side effects and update the database'

    def handle(self, *args, **kwargs):
        side_effects = SideEffect.objects.all()
        for side_effect in side_effects:
            result = analyze_side_effect_severity(side_effect.description)
            side_effect.severity_label = result['label']
            side_effect.severity_score = result['score']
            side_effect.save()
            self.stdout.write(f'Updated {side_effect.description} with severity {result["label"]}')
