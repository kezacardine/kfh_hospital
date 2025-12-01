# Import Django utilities for rendering templates, redirects, and fetching objects
from django.shortcuts import render, redirect, get_object_or_404
# Authentication utilities for login/logout
from django.contrib.auth import authenticate, login, logout
# Decorator to restrict views to logged-in users
from django.contrib.auth.decorators import login_required
# Django messages framework for user feedback
from django.contrib import messages
# ORM functions for aggregation and complex queries
from django.db.models import Avg, Count, Q
# Import models defined in this app
from .models import Patient, VitalSign
# HttpResponse allows sending plain text responses in Django views
from django.http import HttpResponse
# Import date utility to calculate patient age
from datetime import date

# Data analysis and visualization libraries
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (important for server environments)
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime, timedelta


# ---------------- HOME VIEW ----------------
def home(request):
    # Count total patients and vital records
    context = {
        'total_patients': Patient.objects.count(),
        'total_records': VitalSign.objects.count(),
    }
    # Render home page with counts
    return render(request, 'hospital/home.html', context)

# ---------------- COUNT ELDERLY PATIENTS ----------------
def count_elderly_patients():
    """
    Return the number of elderly patients (60+ years old).
    This function was added by Celine as part of project contribution.
    """
    count = 0
    for patient in Patient.objects.all():
        # Calculate age based on birth year
        age = date.today().year - patient.date_of_birth.year
        if age >= 60:
            count += 1
    return count


# --------------- DEMO ELDERLY COUNT VIEW ---------------
def elderly_count_view(request):
    """
    This view displays the number of elderly patients (60+ years).
    Added by Celine to demonstrate the age-analysis feature.
    """
    count = count_elderly_patients()  # Calling function
    return HttpResponse(f"Number of patients aged 60 and above: {count}")
# --------------------------------------------------------




# ---------------- LOGIN VIEW ----------------
def login_view(request):
    # If already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('hospital:dashboard')
    
    # Handle login form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Successful login
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('hospital:dashboard')
        else:
            # Failed login
            messages.error(request, 'Invalid username or password.')
    
    # Render login page
    return render(request, 'hospital/login.html')


# ---------------- LOGOUT VIEW ----------------
def logout_view(request):
    # Log out user
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hospital:home')


# ---------------- DASHBOARD VIEW ----------------
@login_required
def dashboard(request):
    # Aggregate counts
    total_patients = Patient.objects.count()
    total_vitals = VitalSign.objects.count()
    
    # Get vitals recorded in the last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    recent_vitals = VitalSign.objects.filter(recorded_at__gte=yesterday)
    
    # Count abnormal cases
    high_hr_count = recent_vitals.filter(heart_rate__gt=100).count()
    fever_count = recent_vitals.filter(temperature__gt=37.5).count()
    hypertension_count = recent_vitals.filter(Q(systolic_bp__gt=140) | Q(diastolic_bp__gt=90)).count()
    
    # Count critical patients (your contribution)
    critical_count = recent_vitals.filter(
        heart_rate__gt=100,
        temperature__gt=37.5
    ).filter(Q(systolic_bp__gt=140) | Q(diastolic_bp__gt=90)).count()
    
    # Count elderly patients (your contribution)
    elderly_count = count_elderly_patients()
    
    # Get latest 10 patients
    recent_patients = Patient.objects.all()[:10]
    
    # Calculate average vitals
    avg_vitals = VitalSign.objects.aggregate(
        avg_hr=Avg('heart_rate'),
        avg_temp=Avg('temperature'),
        avg_sys=Avg('systolic_bp'),
        avg_dia=Avg('diastolic_bp')
    )
    
    # Pass data to template
    context = {
        'total_patients': total_patients,
        'total_vitals': total_vitals,
        'high_hr_count': high_hr_count,
        'fever_count': fever_count,
        'hypertension_count': hypertension_count,
        'recent_patients': recent_patients,
        'avg_vitals': avg_vitals,
        # Added your contributions here
        'critical_count': critical_count,
        'elderly_count': elderly_count,
    }
    return render(request, 'hospital/dashboard.html', context)


# ---------------- ANALYTICS VIEW --------------
@login_required
def analytics(request):
    # Fetch all vital signs with related patient info
    vital_signs = VitalSign.objects.select_related('patient').all()
    
    # If no data exists, redirect with warning
    if not vital_signs.exists():
        messages.warning(request, 'No data available. Please add patient vital signs first.')
        return redirect('hospital:dashboard')
    
    # Convert queryset to DataFrame for analysis
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
    
    # Add derived columns for abnormal conditions
    df['high_hr'] = df['heart_rate'] > 100
    df['fever'] = df['temperature'] > 37.5
    df['hypertension'] = (df['systolic_bp'] > 140) | (df['diastolic_bp'] > 90)
    df['day'] = np.arange(len(df))  # Simulated timeline
    
    charts = {}
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    # ---------------- Chart 1: Heart Rate Distribution ----------------
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.histplot(df["heart_rate"], kde=True, color='steelblue', ax=ax1)
    ax1.axvline(df["heart_rate"].mean(), color='red', linestyle='--', label=f'Mean: {df["heart_rate"].mean():.1f}')
    ax1.axvline(100, color='orange', linestyle='--', label='High HR Threshold')
    ax1.set_title("Heart Rate Distribution", fontweight='bold')
    ax1.set_xlabel("Heart Rate (bpm)")
    ax1.set_ylabel("Frequency")
    ax1.legend()
    charts['hr_dist'] = fig_to_base64(fig1)
    plt.close(fig1)
    
    # ---------------- Chart 2: Temperature Distribution ----------------
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.kdeplot(df["temperature"], fill=True, color='coral', ax=ax2)
    ax2.axvline(df["temperature"].mean(), color='red', linestyle='--', label=f'Mean: {df["temperature"].mean():.2f}°C')
    ax2.axvline(37.5, color='darkred', linestyle='--', label='Fever Threshold')
    ax2.set_title("Temperature Density Plot", fontweight='bold')
    ax2.set_xlabel("Temperature (°C)")
    ax2.set_ylabel("Density")
    ax2.legend()
    charts['temp_dist'] = fig_to_base64(fig2)
    plt.close(fig2)
    
    # ---------------- Chart 3: Blood Pressure Violin Plot ----------------
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    bp_data = pd.melt(df, value_vars=["systolic_bp", "diastolic_bp"], var_name="BP Type", value_name="mmHg")
    bp_data["BP Type"] = bp_data["BP Type"].replace({"systolic_bp": "Systolic", "diastolic_bp": "Diastolic"})
    sns.violinplot(data=bp_data, x="BP Type", y="mmHg", palette="Set2", ax=ax3)
    ax3.axhline(140, color='red', linestyle='--', alpha=0.5, label='Systolic Limit')
    ax3.axhline(90, color='orange', linestyle='--', alpha=0.5, label='Diastolic Limit')
    ax3.set_title("Blood Pressure Distribution", fontweight='bold')
    ax3.legend()
    charts['bp_violin'] = fig_to_base64(fig3)
    plt.close(fig3)
    
    # ---------------- Chart 4: HR vs Systolic BP Scatter ----------------
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df["systolic_bp"], y=df["heart_rate"], hue=df["high_hr"], 
                    palette={False: "blue", True: "red"}, s=50, alpha=0.6, ax=ax4)
    ax4.set_title("Heart Rate vs Systolic BP", fontweight='bold')
    ax4.set_xlabel("Systolic BP (mmHg)")
    ax4.set_ylabel("Heart Rate (bpm)")
    ax4.legend(title="High HR", labels=["Normal", "High"])
    charts['hr_bp_scatter'] = fig_to_base64(fig4)
    plt.close(fig4)
    
    # ---------------- Chart 5: Heart Rate Trend ----------------
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    sns.regplot(x="day", y="heart_rate", data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax5)
    ax5.set_title("Heart Rate Trend Over Time", fontweight='bold')
    ax5.set_xlabel("Day")
    ax5.set_ylabel("Heart Rate (bpm)")
    charts['hr_trend'] = fig_to_base64(fig5)
    plt.close(fig5)
    
    # ---------------- Chart 6: Correlation Heatmap ----------------
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    corr_matrix = df[["heart_rate", "temperature", "systolic_bp", "diastolic_bp"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax6)
    ax6.set_title("Correlation Heatmap", fontweight='bold')
    charts['corr_heatmap'] = fig_to_base64(fig6)
    plt.close(fig6)

    # Render template with charts
    return render(request, 'hospital/analytics.html', {
        'charts': charts
    })
