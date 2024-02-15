from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Instructor, WorkoutPlan , Customer


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            instructor = Instructor.objects.get(email=email, password=password)
            # Authentication successful
            # You may implement session management or use Django's built-in authentication system here
            # For demonstration, I'm just setting a session variable
            request.session['instructor_id'] = instructor.instructor_id
            return redirect('instructor_dashboard')  # Redirect to instructor dashboard
        except Instructor.DoesNotExist:
            # Instructor with the given email and password does not exist
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')  # Replace 'login.html' with your actual login template

def instructor_dashboard(request):
    # Retrieve instructor from session or authentication system
    instructor_id = request.session.get('instructor_id')
    if instructor_id:
        try:
            instructor = Instructor.objects.get(pk=instructor_id)
            # Retrieve workout plans associated with the instructor
            workout_plans = WorkoutPlan.objects.filter(instructor=instructor)
            # Retrieve customers associated with the instructor
            customers = Customer.objects.filter(workout_plan__in=workout_plans)
            return render(request, 'dashboard.html', {'instructor': instructor, 'workout_plans': workout_plans, 'customers': customers})
        except Instructor.DoesNotExist:
            # Instructor not found, redirect to login
            return redirect('login')
    else:
        # Instructor not authenticated, redirect to login
        return redirect('login')


def logout(request):
    # Clear session variable for instructor ID
    request.session.pop('instructor_id', None)
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Instructor, WorkoutPlan, Customer

def customer_view(request, workout_plan_id):
    # Retrieve instructor from session or authentication system
    instructor_id = request.session.get('instructor_id')
    if instructor_id:
        try:
            instructor = Instructor.objects.get(pk=instructor_id)
            # Retrieve workout plan associated with the instructor
            workout_plan = get_object_or_404(WorkoutPlan, pk=workout_plan_id, instructor=instructor)
            # Retrieve customers associated with the workout plan
            customers = Customer.objects.filter(workout_plan=workout_plan)
            return render(request, 'customer_view.html', {'instructor': instructor, 'workout_plan': workout_plan, 'customers': customers})
        except Instructor.DoesNotExist:
            # Instructor not found, redirect to login
            return redirect('login')
    else:
        # Instructor not authenticated, redirect to login
        return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Instructor, WorkoutPlan, Customer, ProgressReport
from .forms import ProgressReportForm

def add_progress_report(request, workout_plan_id, customer_id):
    workout_plan = get_object_or_404(WorkoutPlan, pk=workout_plan_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    instructor_id = request.session.get('instructor_id')
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    
    if request.method == 'POST':
        form = ProgressReportForm(request.POST)
        if form.is_valid():
            progress_report = form.save(commit=False)
            progress_report.customer = customer
            progress_report.instructor = instructor
            progress_report.save()
            return redirect('customer_view', workout_plan_id=workout_plan_id)
    else:
        form = ProgressReportForm()
    return render(request, 'add_progress_report.html', {'form': form, 'customer': customer, 'workout_plan': workout_plan})


from django.http import HttpResponse
import subprocess

def backup_database(request):
    # Perform backup operation here
    try:
        # Example: Backup using Django's dumpdata command
        backup_file = 'backup.json'
        subprocess.run(['python', 'manage.py', 'dumpdata', '--output', backup_file])
        # Return a response indicating success
        return HttpResponse("Database backup successful. <a href='/'>Go back to homepage</a>")
    except Exception as e:
        # Return a response indicating failure
        return HttpResponse(f"Database backup failed: {str(e)}")


# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import ProgressReport
from .forms import ProgressReportForm

def view_progress_reports(request):
    instructor_id = request.session.get('instructor_id')
    if instructor_id:
        progress_reports = ProgressReport.objects.filter(instructor_id=instructor_id)
        return render(request, 'progress_reports.html', {'progress_reports': progress_reports})
    else:
        return redirect('login')

def edit_progress_report(request, report_id):
    progress_report = get_object_or_404(ProgressReport, pk=report_id)
    if request.method == 'POST':
        form = ProgressReportForm(request.POST, instance=progress_report)
        if form.is_valid():
            form.save()
            return redirect('view_progress_reports')
    else:
        form = ProgressReportForm(instance=progress_report)
    return render(request, 'edit_progress_report.html', {'form': form})

def delete_progress_report(request, report_id):
    progress_report = get_object_or_404(ProgressReport, pk=report_id)
    if request.method == 'POST':
        progress_report.delete()
        return redirect('view_progress_reports')
    return render(request, 'delete_progress_report.html', {'progress_report': progress_report})

# views.py
from django.shortcuts import render
from .models import SalaryReport

def salary_report(request):
    # Retrieve the instructor's salary reports
    instructor_id = request.session.get('instructor_id')
    if instructor_id:
        salary_reports = SalaryReport.objects.filter(instructor_id=instructor_id)
        return render(request, 'salary_report.html', {'salary_reports': salary_reports})
    else:
        # Handle case where instructor is not authenticated
        return redirect('login')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FeeReport
from .forms import FeeReportForm , FeeReportFilterForm

# views.py
import pandas as pd

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeeReportFilterForm
from .models import FeeReport, Customer
import pandas as pd

def fee_reports(request):
    form = FeeReportFilterForm(request.GET)
    fee_reports = FeeReport.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if start_date:
            fee_reports = fee_reports.filter(date_paid__gte=start_date)
        if end_date:
            fee_reports = fee_reports.filter(date_paid__lte=end_date)

        # If the user wants to download the filtered data as Excel
        if 'download_excel' in request.GET:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="fee_reports.xlsx"'
            fee_reports_data = fee_reports.values('fee_report_id', 'customer__name', 'amount', 'date_paid', 'status')
            df = pd.DataFrame(list(fee_reports_data))
            df.to_excel(response, index=False)
            return response

    return render(request, 'fee_report_list.html', {'form': form, 'fee_reports': fee_reports})

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ExpenseReportFilterForm, ExpensesReportForm
from .models import ExpensesReport
import pandas as pd

from django.http import HttpResponse
import pandas as pd

from django.http import HttpResponse
import pandas as pd

def expenses_reports(request):
    form = ExpenseReportFilterForm(request.GET)
    expenses_reports = ExpensesReport.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if start_date:
            expenses_reports = expenses_reports.filter(date_paid__gte=start_date)
        if end_date:
            expenses_reports = expenses_reports.filter(date_paid__lte=end_date)

        # If the user wants to download the filtered data as Excel
        if 'download_excel' in request.GET:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="expenses_reports.xlsx"'
            expenses_reports_data = expenses_reports.values('expense_report_id', 'type', 'amount', 'date_paid')
            df = pd.DataFrame(list(expenses_reports_data))
            df.to_excel(response, index=False)
            return response

    return render(request, 'expenses_reports.html', {'form': form, 'expenses_reports': expenses_reports})

def add_expenses_report(request):
    if request.method == 'POST':
        form = ExpensesReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses_reports')
    else:
        form = ExpensesReportForm()
    return render(request, 'add_expenses_report.html', {'form': form})

def edit_expenses_report(request, expense_report_id):
    expenses_report = ExpensesReport.objects.get(pk=expense_report_id)
    if request.method == 'POST':
        form = ExpensesReportForm(request.POST, instance=expenses_report)
        if form.is_valid():
            form.save()
            return redirect('expenses_reports')
    else:
        form = ExpensesReportForm(instance=expenses_report)
    return render(request, 'edit_expenses_report.html', {'form': form})

def delete_expenses_report(request, expense_report_id):
    expenses_report = ExpensesReport.objects.get(pk=expense_report_id)
    if request.method == 'POST':
        expenses_report.delete()
        return redirect('expenses_reports')
    return render(request, 'delete_expenses_report.html', {'expenses_report': expenses_report})



def add_fee_report(request):
    if request.method == 'POST':
        form = FeeReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_report_list')
    else:
        form = FeeReportForm()
    return render(request, 'add_fee_report.html', {'form': form})

def edit_fee_report(request, fee_report_id):
    fee_report = get_object_or_404(FeeReport, pk=fee_report_id)
    if request.method == 'POST':
        form = FeeReportForm(request.POST, instance=fee_report)
        if form.is_valid():
            form.save()
            return redirect('fee_report_list')
    else:
        form = FeeReportForm(instance=fee_report)
    return render(request, 'edit_fee_report.html', {'form': form})

def delete_fee_report(request, fee_report_id):
    fee_report = get_object_or_404(FeeReport, pk=fee_report_id)
    if request.method == 'POST':
        fee_report.delete()
        return redirect('fee_report_list')
    return render(request, 'delete_fee_report.html', {'fee_report': fee_report})


from django.shortcuts import render, redirect, get_object_or_404
from .models import ProfitReport
from .forms import ProfitReportForm

def add_profit_report(request):
    if request.method == 'POST':
        form = ProfitReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profit_reports')
    else:
        form = ProfitReportForm()
    return render(request, 'add_profit_report.html', {'form': form})

from django.shortcuts import render
from .models import ProfitReport
from .forms import ProfitReportFilterForm
import pandas as pd
from django.http import HttpResponse

def view_profit_reports(request):
    form = ProfitReportFilterForm(request.GET)
    profit_reports = ProfitReport.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if start_date:
            profit_reports = profit_reports.filter(date__gte=start_date)
        if end_date:
            profit_reports = profit_reports.filter(date__lte=end_date)

        # If the user wants to download the filtered data as Excel
        if 'download_excel' in request.GET:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="profit_reports.xlsx"'
            profit_reports_data = profit_reports.values('profit_report_id', 'income', 'expenses', 'profit', 'date')
            df = pd.DataFrame(list(profit_reports_data))
            df.to_excel(response, index=False)
            return response

    return render(request, 'profit_reports.html', {'form': form, 'profit_reports': profit_reports})

def edit_profit_report(request, profit_report_id):
    profit_report = get_object_or_404(ProfitReport, pk=profit_report_id)
    if request.method == 'POST':
        form = ProfitReportForm(request.POST, instance=profit_report)
        if form.is_valid():
            form.save()
            return redirect('profit_reports')
    else:
        form = ProfitReportForm(instance=profit_report)
    return render(request, 'edit_profit_report.html', {'form': form})

def delete_profit_report(request, profit_report_id):
    profit_report = get_object_or_404(ProfitReport, pk=profit_report_id)
    if request.method == 'POST':
        profit_report.delete()
        return redirect('profit_reports')
    return render(request, 'delete_profit_report.html', {'profit_report': profit_report})



from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customer

def customer_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            customer = Customer.objects.get(email=email, password=password)
            # Authentication successful
            # You may implement session management or use Django's built-in authentication system here
            # For demonstration, I'm just setting a session variable
            request.session['customer_id'] = customer.customer_id
            return redirect('customer_dashboard')  # Redirect to customer dashboard
        except Customer.DoesNotExist:
            # Customer with the given email and password does not exist
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'customer_login.html')  # Replace 'customer_login.html' with your actual login template

def customer_dashboard(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
            progress_reports = ProgressReport.objects.filter(customer=customer)
            fee_reports = FeeReport.objects.filter(customer=customer)
            return render(request, 'customer_dashboard.html', {'customer': customer, 'progress_reports': progress_reports, 'fee_reports': fee_reports})
        except Customer.DoesNotExist:
            return redirect('customer_login')
    else:
        return redirect('customer_login')


def customer_logout(request):
    # Clear session variable for customer ID
    request.session.pop('customer_id', None)
    return redirect('customer_login')
