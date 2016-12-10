from chartjs.views.lines import BaseLineChartView

from patients.views import PatientDateMixin
from reports.models import ReportData


class DailyGlucoseLevelJSONView(PatientDateMixin, BaseLineChartView):
    glucose_data = None

    def get_context_data(self):
        self.glucose_data = ReportData.glucose_measurement.filter(
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )
        return super(DailyGlucoseLevelJSONView, self).get_context_data()

    def get_labels(self):
        return [
            data.datetime.strftime("%H:%M")
            for data in self.glucose_data
        ]

    def get_data(self):
        return [[data.value for data in self.glucose_data]]
