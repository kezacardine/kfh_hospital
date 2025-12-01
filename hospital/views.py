# ---------------- IMPORTS ----------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.http import HttpResponse
from datetime import date, datetime, timedelta

# Models
from .models import Patient, VitalSign

# Data analysis libraries
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # For server compatibility
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import random

# ---------------- HOME VIEW ----------------
def home(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_records': VitalSign.objects.count(),
    }
    return render(request, 'hospital/home.html', context)

# ---------------- COUNT ELDERLY PATIENTS ----------------
def count_elderly_patients():
    count = 0
    for patient in Patient.objects.all():
        age = date.today().year - patient.date_of_birth.year
        if age >= 60:
            count += 1
    return count

# ---------------- ELDERLY COUNT VIEW ----------------
def elderly_count_view(request):
    count = count_elderly_patients()
    return HttpResponse(f"Number of patients aged 60 and above: {count}")

# ---------------- LOGIN ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('hospital:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('hospital:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'hospital/login.html')

# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hospital:home')

# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_vitals = VitalSign.objects.count()

    yesterday = datetime.now() - timedelta(days=1)
    recent_vitals = VitalSign.objects.filter(recorded_at__gte=yesterday)

    high_hr_count = recent_vitals.filter(heart_rate__gt=100).count()
    fever_count = recent_vitals.filter(temperature__gt=37.5).count()
    hypertension_count = recent_vitals.filter(
        Q(systolic_bp__gt=140) | Q(diastolic_bp__gt=90)
    ).count()

    recent_patients = Patient.objects.all()[:10]

    avg_vitals = VitalSign.objects.aggregate(
        avg_hr=Avg('heart_rate'),
        avg_temp=Avg('temperature'),
        avg_sys=Avg('systolic_bp'),
        avg_dia=Avg('diastolic_bp')
    )

    context = {
        'total_patients': total_patients,
        'total_vitals': total_vitals,
        'high_hr_count': high_hr_count,
        'fever_count': fever_count,
        'hypertension_count': hypertension_count,
        'recent_patients': recent_patients,
        'avg_vitals': avg_vitals,
    }
    return render(request, 'hospital/dashboard.html', context)

# ---------------- FIGURE TO BASE64 ----------------
def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

# ---------------- ANALYTICS ----------------
@login_required
def analytics(request):
    vital_signs = VitalSign.objects.select_related('patient').all()
    if not vital_signs.exists():
        messages.warning(request, 'No data available. Please add patient vital signs first.')
        return redirect('hospital:dashboard')

    data = []
    for vs in vital_signs:
        data.append({
            'patient_id': vs.patient.patient_id,
            'heart_rate': vs.heart_rate,
            'temperature': vs.temperature,
            'systolic_bp': vs.systolic_bp,
            'diastolic_bp': vs.diastolic_bp,
        })

    df = pd.DataFrame(data)
    df['high_hr'] = df['heart_rate'] > 100
    df['fever'] = df['temperature'] > 37.5
    df['hypertension'] = (df['systolic_bp'] > 140) | (df['diastolic_bp'] > 90)
    df['day'] = np.arange(len(df))

    charts = {}
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'

    # Heart Rate Distribution
    fig1, ax1 = plt.subplots(figsize=(8,5))
    sns.histplot(df["heart_rate"], kde=True, ax=ax1)
    ax1.set_title("Heart Rate Distribution")
    charts['hr_dist'] = fig_to_base64(fig1)
    plt.close(fig1)

    # Temperature Density
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.kdeplot(df["temperature"], fill=True, ax=ax2)
    ax2.set_title("Temperature Density Plot")
    charts['temp_dist'] = fig_to_base64(fig2)
    plt.close(fig2)

    # Blood Pressure Violin
    fig3, ax3 = plt.subplots(figsize=(8,5))
    bp_data = pd.melt(df, value_vars=["systolic_bp","diastolic_bp"], var_name="BP Type", value_name="mmHg")
    sns.violinplot(data=bp_data, x="BP Type", y="mmHg", ax=ax3)
    ax3.set_title("Blood Pressure Distribution")
    charts['bp_violin'] = fig_to_base64(fig3)
    plt.close(fig3)

    # HR vs BP Scatter
    fig4, ax4 = plt.subplots(figsize=(8,5))
    sns.scatterplot(x=df["systolic_bp"], y=df["heart_rate"], hue=df["high_hr"], ax=ax4)
    ax4.set_title("Heart Rate vs Systolic BP")
    charts['hr_bp_scatter'] = fig_to_base64(fig4)
    plt.close(fig4)

    # HR Trend
    fig5, ax5 = plt.subplots(figsize=(8,5))
    sns.regplot(x="day", y="heart_rate", data=df, ax=ax5)
    ax5.set_title("Heart Rate Trend Over Time")
    charts['hr_trend'] = fig_to_base64(fig5)
    plt.close(fig5)

    # Correlation Heatmap
    fig6, ax6 = plt.subplots(figsize=(8,5))
    corr_matrix = df[["heart_rate","systolic_bp","diastolic_bp","temperature"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax6)
    ax6.set_title("Correlation Heatmap")
    charts['heatmap'] = fig_to_base64(fig6)
    plt.close(fig6)

    return render(request, 'hospital/analytics.html', {"charts": charts})

# ---------------- PATIENT DETAIL ----------------
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    vitals = VitalSign.objects.filter(patient=patient).order_by('-recorded_at')
    return render(request, 'hospital/patient_detail.html', {
        'patient': patient,
        'vitals': vitals
    })

# ---------------- GENERATE SAMPLE DATA ----------------
@login_required
def generate_sample_data(request):
    if Patient.objects.count() < 10:
        for i in range(1, 11):
            Patient.objects.create(
                patient_id=f"P{i:03d}",
                name=f"Patient {i}",
                date_of_birth=datetime(1950 + i, 1, 1).date(),
                gender=random.choice(['Male','Female'])
            )

    patients = Patient.objects.all()
    for _ in range(50):
        patient = random.choice(patients)
        VitalSign.objects.create(
            patient=patient,
            heart_rate=random.randint(60, 120),
            temperature=random.uniform(36.0, 39.0),
            systolic_bp=random.randint(100,160),
            diastolic_bp=random.randint(60,100),
            recorded_at=datetime.now() - timedelta(days=random.randint(0,10))
        )
    return HttpResponse("Sample data generated successfully!")
