from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Employee_data as AnalysisModel
from apps.posts.models import Post
from apps.tickets.models import TicketsTrash

class Analysis(APIView):

    def get(self, request):
        user = request.user

        # Ensure the user is authenticated and a superuser
        if not user.is_authenticated or not user.is_superuser:
            return Response(
                {"message": "You do not have access to this page."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Fetch the post associated with the superuser
            post = Post.objects.get(employees=user)

            # Retrieve all employees linked to the post
            employees = post.employees.all()

            # Construct employee details with analysis data
            employee_details = []
            for employee in employees:
                try:
                    # Fetch employee analysis data
                    employee_analysis = AnalysisModel.objects.get(employee=employee)
                    employee_details.append({
                        "employee_id": employee.id,
                        "first_name": employee.first_name,
                        "ticket_number": employee_analysis.TodayNmbrTiquets,
                        "last_login": employee_analysis.todayLogin,
                        "last_logout": employee_analysis.todaylogout,
                    })
                except AnalysisModel.DoesNotExist:
                    # Handle missing analysis data
                    employee_details.append({
                        "employee_id": employee.id,
                        "first_name": employee.first_name,
                        "ticket_number": None,
                        "last_login": None,
                        "last_logout": None,
                        "message": "Analysis data not available for this employee."
                    })

            # Determine the most charged hours of the day
            work_hours_list = range(8, 18)  # Work hours from 8 AM to 5 PM
            most_charged_hours = []
            for hour in work_hours_list:
                ticket_count = TicketsTrash.objects.filter(
                    created_at__hour=hour
                ).count()
                most_charged_hours.append({"hour": hour, "ticket_count": ticket_count})

            # Determine the most active days of the week
            weekdays_map = {
                1: "Sunday", 2: "Monday", 3: "Tuesday",
                4: "Wednesday", 5: "Thursday", 6: "Friday", 7: "Saturday"
            }
            most_active_days = []
            for day_index, day_name in weekdays_map.items():
                ticket_count = TicketsTrash.objects.filter(
                    created_at__week_day=day_index
                ).count()
                most_active_days.append({"day": day_name, "ticket_count": ticket_count})

            # Return the analysis data
            return Response(
                {
                    "post_id": post.id,
                    "employee_count": employees.count(),
                    "employee_details": employee_details,
                    "most_charged_hours": most_charged_hours,
                    "most_active_days": most_active_days,
                },
                status=status.HTTP_200_OK
            )

        except Post.DoesNotExist:
            return Response(
                {"message": "No post found for the current superuser."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
