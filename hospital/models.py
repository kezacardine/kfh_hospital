from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"

    def get_latest_risk_level(self):
        """Get the risk level from the most recent vital signs"""
        latest_vital = self.vital_signs.first()
        if latest_vital:
            return latest_vital.get_risk_level_display()
        return "No Data"
    
    def get_latest_risk_color(self):
        """Get color for risk level badge"""
        latest_vital = self.vital_signs.first()
        if latest_vital:
            risk = latest_vital.risk_level
            colors = {'LOW': 'success', 'MEDIUM': 'warning', 'HIGH': 'danger'}
            return colors.get(risk, 'secondary')
        return 'secondary'

    class Meta:
        ordering = ['-created_at']

class VitalSign(models.Model):
    RISK_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    heart_rate = models.FloatField(help_text="Heart rate in bpm")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    systolic_bp = models.FloatField(help_text="Systolic blood pressure in mmHg")
    diastolic_bp = models.FloatField(help_text="Diastolic blood pressure in mmHg")
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, blank=True)
    risk_score = models.IntegerField(default=0, help_text="Calculated risk score")
    recorded_at = models.DateTimeField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.patient.patient_id} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')} - {self.risk_level}"

    def save(self, *args, **kwargs):
        """Auto-calculate risk level before saving"""
        self.risk_score = self.calculate_risk_score()
        self.risk_level = self.determine_risk_level()
        super().save(*args, **kwargs)

    def calculate_risk_score(self):
        """
        Calculate risk score based on vital signs
        Score ranges: 0-100 (higher = more risk)
        """
        score = 0
        
        # Heart Rate Risk (Normal: 60-100 bpm)
        if self.heart_rate < 40:
            score += 30  # Severe bradycardia
        elif self.heart_rate < 60:
            score += 15  # Mild bradycardia
        elif self.heart_rate > 120:
            score += 30  # Severe tachycardia
        elif self.heart_rate > 100:
            score += 15  # Mild tachycardia
        
        # Temperature Risk (Normal: 36.1-37.2°C)
        if self.temperature < 35:
            score += 25  # Severe hypothermia
        elif self.temperature < 36:
            score += 10  # Mild hypothermia
        elif self.temperature > 39:
            score += 25  # High fever
        elif self.temperature > 37.5:
            score += 10  # Mild fever
        
        # Systolic Blood Pressure Risk (Normal: 90-120 mmHg)
        if self.systolic_bp < 90:
            score += 20  # Hypotension
        elif self.systolic_bp > 180:
            score += 30  # Stage 3 Hypertension (Crisis)
        elif self.systolic_bp > 140:
            score += 15  # Stage 1-2 Hypertension
        
        # Diastolic Blood Pressure Risk (Normal: 60-80 mmHg)
        if self.diastolic_bp < 60:
            score += 15  # Low diastolic
        elif self.diastolic_bp > 120:
            score += 25  # Hypertensive crisis
        elif self.diastolic_bp > 90:
            score += 10  # Elevated diastolic
        
        return min(score, 100)  # Cap at 100

    def determine_risk_level(self):
        """
        Determine risk level based on calculated score
        Low: 0-30
        Medium: 31-60
        High: 61-100
        """
        if self.risk_score <= 30:
            return 'LOW'
        elif self.risk_score <= 60:
            return 'MEDIUM'
        else:
            return 'HIGH'

    def get_risk_factors(self):
        """Return list of specific risk factors"""
        factors = []
        
        if self.heart_rate < 60:
            factors.append(f"Low heart rate ({self.heart_rate:.0f} bpm)")
        elif self.heart_rate > 100:
            factors.append(f"High heart rate ({self.heart_rate:.0f} bpm)")
        
        if self.temperature < 36:
            factors.append(f"Low temperature ({self.temperature:.1f}°C)")
        elif self.temperature > 37.5:
            factors.append(f"Fever ({self.temperature:.1f}°C)")
        
        if self.systolic_bp < 90:
            factors.append(f"Low blood pressure ({self.systolic_bp:.0f}/{self.diastolic_bp:.0f} mmHg)")
        elif self.systolic_bp > 140 or self.diastolic_bp > 90:
            factors.append(f"High blood pressure ({self.systolic_bp:.0f}/{self.diastolic_bp:.0f} mmHg)")
        
        if not factors:
            factors.append("All vitals within normal range")
        
        return factors

    @property
    def high_hr(self):
        return self.heart_rate > 100

    @property
    def fever(self):
        return self.temperature > 37.5

    @property
    def hypertension(self):
        return self.systolic_bp > 140 or self.diastolic_bp > 90

    class Meta:
        ordering = ['-recorded_at']
