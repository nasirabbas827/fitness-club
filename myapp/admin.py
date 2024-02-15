from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime
import calendar
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import DateFieldListFilter

from .models import Instructor, Customer, WorkoutPlan
from .models import FeeReport, SalaryReport, ExpensesReport, ProfitReport , ProgressReport

class DateRangeFilter(admin.DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.links += (
            (_('Today'), {
                self.lookup_kwarg_since: str(datetime.date.today()),
                self.lookup_kwarg_until: str(datetime.date.today()),
            }),
            (_('This week'), {
                self.lookup_kwarg_since: str(datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())),
                self.lookup_kwarg_until: str(datetime.date.today() + datetime.timedelta(days=6 - datetime.date.today().weekday())),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: str(datetime.date.today().replace(day=1)),
                self.lookup_kwarg_until: str(datetime.date.today().replace(day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])),
            }),
            (_('This year'), {
                self.lookup_kwarg_since: str(datetime.date.today().replace(month=1, day=1)),
                self.lookup_kwarg_until: str(datetime.date.today().replace(month=12, day=31)),
            }),
        )

class FeeReportAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    list_display = ['fee_report_id', 'customer', 'amount', 'date_paid', 'status']
    list_filter = [('date_paid', DateRangeFilter), 'status']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fee_reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Customer', 'Amount', 'Date Paid', 'Status'])
        for obj in queryset:
            writer.writerow([obj.fee_report_id, obj.customer, obj.amount, obj.date_paid, obj.status])
        return response

    export_as_csv.short_description = "Export selected fee reports as CSV"

class SalaryReportAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    list_display = ['salary_report_id', 'instructor', 'amount', 'date_paid']
    list_filter = [('date_paid', DateRangeFilter)]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="salary_reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Instructor', 'Amount', 'Date Paid'])
        for obj in queryset:
            writer.writerow([obj.salary_report_id, obj.instructor, obj.amount, obj.date_paid])
        return response

    export_as_csv.short_description = "Export selected salary reports as CSV"

class ExpensesReportAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    list_display = ['expense_report_id', 'type', 'amount', 'date_paid']
    list_filter = [('date_paid', DateRangeFilter)]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses_reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Type', 'Amount', 'Date Paid'])
        for obj in queryset:
            writer.writerow([obj.expense_report_id, obj.type, obj.amount, obj.date_paid])
        return response

    export_as_csv.short_description = "Export selected expenses reports as CSV"

class ProfitReportAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    list_display = ['profit_report_id', 'income', 'expenses', 'profit', 'date']
    readonly_fields = ['profit']  # Make the profit field read-only
    list_filter = [('date', DateRangeFilter)]

    def save_model(self, request, obj, form, change):
        obj.profit = obj.income - obj.expenses  # Automatically calculate profit
        super().save_model(request, obj, form, change)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profit_reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Income', 'Expenses', 'Profit', 'Date'])
        for obj in queryset:
            writer.writerow([obj.profit_report_id, obj.income, obj.expenses, obj.profit, obj.date])
        return response

    export_as_csv.short_description = "Export selected profit reports as CSV"

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'qualification', 'timings_from', 'timings_to']

class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'instructor']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'BMI', 'goal', 'workout_plan']

admin.site.register(FeeReport, FeeReportAdmin)
admin.site.register(SalaryReport, SalaryReportAdmin)
admin.site.register(ExpensesReport, ExpensesReportAdmin)
admin.site.register(ProfitReport, ProfitReportAdmin)

admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(WorkoutPlan, WorkoutPlanAdmin)
admin.site.register(ProgressReport)
