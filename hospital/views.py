from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Patient, VitalSign
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime, timedelta

def home(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_records': VitalSign.objects.count(),
    }
    return render(request, 'hospital/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('hospital:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('hospital:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'hospital/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hospital:home')

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_vitals = VitalSign.objects.count()
    
    yesterday = datetime.now() - timedelta(days=1)
    recent_vitals = VitalSign.objects.filter(recorded_at__gte=yesterday)
    
    high_hr_count = recent_vitals.filter(heart_rate__gt=100).count()
    fever_count = recent_vitals.filter(temperature__gt=37.5).count()
    hypertension_count = recent_vitals.filter(Q(systolic_bp__gt=140) | Q(diastolic_bp__gt=90)).count()
    
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
    
    # Chart 1: Heart Rate Distribution
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
    
    # Chart 2: Temperature Distribution
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
    
    # Chart 3: Blood Pressure Violin Plot
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
    
    # Chart 4: HR vs Systolic BP Scatter
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df["systolic_bp"], y=df["heart_rate"], hue=df["high_hr"], palette={False: "blue", True: "red"}, s=50, alpha=0.6, ax=ax4)
    ax4.set_title("Heart Rate vs Systolic BP", fontweight='bold')
    ax4.set_xlabel("Systolic BP (mmHg)")
    ax4.set_ylabel("Heart Rate (bpm)")
    ax4.legend(title="High HR", labels=["Normal", "High"])
    charts['hr_bp_scatter'] = fig_to_base64(fig4)
    plt.close(fig4)
    
    # Chart 5: Heart Rate Trend
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    sns.regplot(x="day", y="heart_rate", data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax5)
    ax5.set_title("Heart Rate Trend Over Time", fontweight='bold')
    ax5.set_xlabel("Day")
    ax5.set_ylabel("Heart Rate (bpm)")
    charts['hr_trend'] = fig_to_base64(fig5)
    plt.close(fig5)
    
    # Chart 6: Correlation Heatmap
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    corr_matrix = df[["heart_rate", "temperature", "systolic_bp", "diastolic_bp"]].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, ax=ax6,
                xticklabels=["HR", "Temp", "Sys BP", "Dia BP"], yticklabels=["HR", "Temp", "Sys BP", "Dia BP"])
    ax6.set_title("Vital Signs Correlation Matrix", fontweight='bold')
    charts['correlation'] = fig_to_base64(fig6)
    plt.close(fig6)
    
    summary_stats = df[["heart_rate", "temperature", "systolic_bp", "diastolic_bp"]].describe()
    alerts = {
        'high_hr': int(df['high_hr'].sum()),
        'fever': int(df['fever'].sum()),
        'hypertension': int(df['hypertension'].sum()),
    }
    
    context = {
        'charts': charts,
        'summary_stats': summary_stats.to_html(classes='table table-striped'),
        'alerts': alerts,
        'total_records': len(df),
    }
    return render(request, 'hospital/analytics.html', context)

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    vital_signs = patient.vital_signs.all()
    context = {'patient': patient, 'vital_signs': vital_signs}
    return render(request, 'hospital/patient_detail.html', context)

@login_required
def generate_sample_data(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can generate sample data.')
        return redirect('hospital:dashboard')
    
    np.random.seed(42)
    num_patients = 50
    
    for i in range(1, num_patients + 1):
        patient_id = f"P{i:04d}"
        if not Patient.objects.filter(patient_id=patient_id).exists():
            patient = Patient.objects.create(
                patient_id=patient_id,
                first_name=f"Patient{i}",
                last_name=f"Test{i}",
                date_of_birth=datetime.now().date() - timedelta(days=np.random.randint(7300, 29200)),
                gender=np.random.choice(['M', 'F']),
                phone=f"+250{np.random.randint(700000000, 799999999)}",
                address=f"Kigali, Rwanda - Address {i}"
            )
            for j in range(np.random.randint(2, 6)):
                VitalSign.objects.create(
                    patient=patient,
                    heart_rate=np.random.normal(75, 10),
                    temperature=np.random.normal(36.8, 0.4),
                    systolic_bp=np.random.normal(120, 15),
                    diastolic_bp=np.random.normal(80, 10),
                    recorded_by=request.user
                )
    
    messages.success(request, f'{num_patients} sample patients with vital signs created successfully!')
    return redirect('hospital:analytics')

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64