from django.urls import path
from .views import DashboardStatsView
from .monthly_report import MonthlyReportView, AvailableMonthsView

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('monthly-report/', MonthlyReportView.as_view(), name='monthly-report'),
    path('available-months/', AvailableMonthsView.as_view(), name='available-months'),
]
