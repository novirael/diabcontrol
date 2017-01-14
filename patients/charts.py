from chartjs.views import JSONView
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


class DailyHrLevelJSONView(PatientDateMixin, BaseLineChartView):

    @property
    def hr_data(self):
        return ReportData.objects.filter(
            type='heart_rate',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    def get_labels(self):
        return [
            data.datetime.strftime("%H:%M")
            for data in self.hr_data
        ]

    def get_data(self):
        return [[data.value for data in self.hr_data]]


class DailyStepsLevelJSONView(PatientDateMixin, BaseLineChartView):

    @property
    def steps_data(self):
        return ReportData.objects.filter(
            type='steps',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    def get_labels(self):
        return [
            data.datetime.strftime("%H:%M")
            for data in self.steps_data
        ]

    def get_data(self):
        return [[data.value for data in self.steps_data]]


class DailyMacrosLevelJSONView(PatientDateMixin, JSONView):

    @property
    def fat_data(self):
        return ReportData.objects.filter(
            type='fat',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    @property
    def protein_data(self):
        return ReportData.objects.filter(
            type='protein',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    @property
    def carbohydrates_data(self):
        return ReportData.objects.filter(
            type='carbohydrates',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    @staticmethod
    def make_dict(name, val):
        return {'name': name, 'y': val}

    def get_context_data(self):
        context = {}  # super(DailyMacrosLevelJSONView, self).get_context_data(**kwargs)

        fat_data = sum([data.value for data in self.fat_data])
        protein_data = sum([data.value for data in self.protein_data])
        carb_data = sum([data.value for data in self.carbohydrates_data])

        macros = [fat_data] + [protein_data] + [carb_data]
        percentage = [i / (float(sum(macros) or 1) / 100.0) for i in macros]

        context['macros'] = [
            self.make_dict("Fat", percentage[0]),
            self.make_dict("Protein", percentage[1]),
            self.make_dict("Carbohydrates", percentage[2])
        ]
        return context


class MonthlyMacrosLevelJSONView(PatientDateMixin, JSONView):
    @property
    def fat_data(self):
        return ReportData.objects.filter(
            type='fat',
            patient_id=self.patient.id,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    @property
    def protein_data(self):
        return ReportData.objects.filter(
            type='protein',
            patient_id=self.patient.id,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    @property
    def carbohydrates_data(self):
        return ReportData.objects.filter(
            type='carbohydrates',
            patient_id=self.patient.id,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

    def get_context_data(self):
        context = {}  # super(DailyMacrosLevelJSONView, self).get_context_data(**kwargs)

        fat_data = sum([data.value for data in self.fat_data])
        protein_data = sum([data.value for data in self.protein_data])
        carb_data = sum([data.value for data in self.carbohydrates_data])

        macros = [fat_data] + [protein_data] + [carb_data]
        percentage = [i / (float(sum(macros) or 1) / 100.0) for i in macros]

        context['macros'] = [
            DailyMacrosLevelJSONView.make_dict("Fat", percentage[0]),
            DailyMacrosLevelJSONView.make_dict("Protein", percentage[1]),
            DailyMacrosLevelJSONView.make_dict("Carbohydrates", percentage[2])
        ]
        return context


class YearlyMacrosLevelJSONView(PatientDateMixin, JSONView):
    @property
    def fat_data(self):
        return ReportData.objects.filter(
            type='fat',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    @property
    def protein_data(self):
        return ReportData.objects.filter(
            type='protein',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    @property
    def carbohydrates_data(self):
        return ReportData.objects.filter(
            type='carbohydrates',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    def get_context_data(self):
        context = {}

        fat_data = sum([data.value for data in self.fat_data])
        protein_data = sum([data.value for data in self.protein_data])
        carb_data = sum([data.value for data in self.carbohydrates_data])

        macros = [fat_data] + [protein_data] + [carb_data]
        percentage = [i / (float(sum(macros) or 1) / 100.0) for i in macros]

        context['macros'] = [
            DailyMacrosLevelJSONView.make_dict("Fat", percentage[0]),
            DailyMacrosLevelJSONView.make_dict("Protein", percentage[1]),
            DailyMacrosLevelJSONView.make_dict("Carbohydrates", percentage[2])
        ]
        return context


class SummaryHrLevelJSONView(PatientDateMixin, BaseLineChartView):
    hr_data = None

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
                for data in self.hr_data
                if self.contain_chunk(data.datetime, chunk)
            ] or [0]
            data_sets['min'].append(min(results))
            data_sets['max'].append(max(results))
            data_sets['avg'].append(sum(results) / (len(results)))

        return data_sets.values()


class MonthlyHrLevelJSONView(SummaryHrLevelJSONView):

    @property
    def hr_data(self):
        return ReportData.objects.filter(
            type='heart_rate',
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


class YearlyHrLevelJSONView(SummaryHrLevelJSONView):

    @property
    def hr_data(self):
        return ReportData.objects.filter(
            type='heart_rate',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    def get_start_end_chunk(self):
        """Returns month in year range."""
        return 1, 13

    @staticmethod
    def contain_chunk(timestamp, month):
        return timestamp.month == month


class SummaryStepsLevelJSONView(PatientDateMixin, BaseLineChartView):
    steps_data = None

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
                for data in self.steps_data
                if self.contain_chunk(data.datetime, chunk)
            ] or [0]
            data_sets['min'].append(min(results))
            data_sets['max'].append(max(results))
            data_sets['avg'].append(sum(results) / (len(results)))

        return data_sets.values()


class MonthlyStepsLevelJSONView(SummaryStepsLevelJSONView):

    @property
    def steps_data(self):
        return ReportData.objects.filter(
            type='steps',
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


class YearlyStepsLevelJSONView(SummaryStepsLevelJSONView):

    @property
    def steps_data(self):
        return ReportData.objects.filter(
            type='steps',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    def get_start_end_chunk(self):
        """Returns month in year range."""
        return 1, 13

    @staticmethod
    def contain_chunk(timestamp, month):
        return timestamp.month == month


class SummaryClimbedLevelJSONView(PatientDateMixin, BaseLineChartView):
    climbed_data = None

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
                for data in self.climbed_data
                if self.contain_chunk(data.datetime, chunk)
            ] or [0]
            data_sets['min'].append(min(results))
            data_sets['max'].append(max(results))
            data_sets['avg'].append(sum(results) / (len(results)))

        return data_sets.values()


class MonthlyClimbedLevelJSONView(SummaryClimbedLevelJSONView):

    @property
    def climbed_data(self):
        return ReportData.objects.filter(
            type='flights_climbed',
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


class YearlyClimbedLevelJSONView(SummaryClimbedLevelJSONView):

    @property
    def climbed_data(self):
        return ReportData.objects.filter(
            type='flights_climbed',
            patient_id=self.patient.id,
            datetime__year=self.current_date.year,
        )

    def get_start_end_chunk(self):
        """Returns month in year range."""
        return 1, 13

    @staticmethod
    def contain_chunk(timestamp, month):
        return timestamp.month == month
