from django import forms
from .models import ProgressReport

from django import forms
from .models import ProgressReport

from django import forms
from .models import ProgressReport

class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        exclude = ['customer', 'instructor']  # Exclude customer and instructor fields from the form
        widgets = {
            'date': forms.SelectDateWidget(attrs={'class': 'form-control'}), 
            'other_metrics': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'date' and field_name != 'other_metrics':
                field.widget.attrs['class'] = 'form-control mb-3' 


# forms.py
from django import forms
from .models import FeeReport

class FeeReportForm(forms.ModelForm):
    class Meta:
        model = FeeReport
        fields = ['customer', 'amount', 'date_paid', 'status']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class FeeReportFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'}))

# forms.py
from django import forms
from .models import ExpensesReport

class ExpenseReportFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


class ExpensesReportForm(forms.ModelForm):
    class Meta:
        model = ExpensesReport
        fields = ['type', 'amount', 'date_paid']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


from .models import ProfitReport
# forms.py
from django import forms
from .models import ProfitReport

class ProfitReportForm(forms.ModelForm):
    class Meta:
        model = ProfitReport
        fields = ['income', 'expenses', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'income': forms.NumberInput(attrs={'class': 'form-control'}),
            'expenses': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProfitReportFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
