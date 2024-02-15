from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('workout-plan/<int:workout_plan_id>/customers/', views.customer_view, name='customer_view'),
    path('workout-plan/<int:workout_plan_id>/customers/<int:customer_id>/add-progress-report/', views.add_progress_report, name='add_progress_report'),  # Add URL pattern for adding progress report
    path('progress-reports/', views.view_progress_reports, name='view_progress_reports'),
    path('progress-reports/<int:report_id>/edit/', views.edit_progress_report, name='edit_progress_report'),
    path('progress-reports/<int:report_id>/delete/', views.delete_progress_report, name='delete_progress_report'),
    path('salary-report/', views.salary_report, name='salary_report'),
    path('backup/', views.backup_database, name='backup_database'), 
    path('fee-reports/', views.fee_reports, name='fee_report_list'),
    path('add-fee-report/', views.add_fee_report, name='add_fee_report'),
    path('edit-fee-report/<int:fee_report_id>/', views.edit_fee_report, name='edit_fee_report'),
    path('delete-fee-report/<int:fee_report_id>/', views.delete_fee_report, name='delete_fee_report'),
    path('expenses-reports/', views.expenses_reports, name='expenses_reports'),
    path('expenses-reports/add/', views.add_expenses_report, name='add_expenses_report'),
    path('expenses-reports/<int:expense_report_id>/edit/', views.edit_expenses_report, name='edit_expenses_report'),
    path('expenses-reports/<int:expense_report_id>/delete/', views.delete_expenses_report, name='delete_expenses_report'),
    path('profit-reports/', views.view_profit_reports, name='profit_reports'),
    path('profit-reports/add/', views.add_profit_report, name='add_profit_report'),
    path('profit-reports/<int:profit_report_id>/edit/', views.edit_profit_report, name='edit_profit_report'),
    path('profit-reports/<int:profit_report_id>/delete/', views.delete_profit_report, name='delete_profit_report'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/logout/',views.customer_logout, name='customer_logout'),

]