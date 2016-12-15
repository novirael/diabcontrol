from chartjs.views.lines import BaseLineChartView
from calendar import monthrange

from patients.views import PatientDateMixin
from reports.models import ReportData


class DailyGlucoseLevelJSONView(PatientDateMixin, BaseLineChartView):

    @property
    def glucose_data(self):
        return ReportData.glucose_measurement.filter(
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    def get_labels(self):
        return [
            data.datetime.strftime("%H:%M")
            for data in self.glucose_data
        ]

    def get_data(self):
        return [[data.value for data in self.glucose_data]]


class SummaryGlucoseLevelJSONView(PatientDateMixin, BaseLineChartView):
    glucose_data = None

    def get_start_end_chunk(self):
        raise NotImplementedError()

    @staticmethod
    def contain_chunk(timestamp, chunk):
        raise NotImplementedError()

    def get_labels(self):
        return list(range(*self.get_start_end_chunk()))

    def get_data(self):
        data_sets = dict(
            min=[],
            max=[],
            avg=[],
        )

        for chunk in range(*self.get_start_end_chunk()):
            results = [
                data.value
                for data in self.glucose_data
                if self.contain_chunk(data.datetime, chunk)
            ] or [0]
            data_sets['min'].append(min(results))
            data_sets['max'].append(max(results))
            data_sets['avg'].append(sum(results) / (len(results)))

        return data_sets.values()


class MonthlyGlucoseLevelJSONView(SummaryGlucoseLevelJSONView):

    @property
    def glucose_data(self):
        return ReportData.glucose_measurement.filter(
            patient_id=self.patient.id,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    def get_start_end_chunk(self):
        """Returns days in month range."""
        days_count = monthrange(self.current_date.year, self.current_date.month)[1]
        return 1, days_count + 1

    @staticmethod
    def contain_chunk(timestamp, day):
        return timestamp.day == day


class YearlyGlucoseLevelJSONView(SummaryGlucoseLevelJSONView):

    @property
    def glucose_data(self):
        return ReportData.glucose_measurement.filter(
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    def get_start_end_chunk(self):
        """Returns month in year range."""
        return 1, 13

    @staticmethod
    def contain_chunk(timestamp, month):
        return timestamp.month == month
