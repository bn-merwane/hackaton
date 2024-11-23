from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import TicketsSerializers
from datetime import datetime
from apps.posts.models import Post
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ticket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Ticket
from .serializers import TicketsSerializers
from apps.analytics.models import *
from django.contrib.auth import logout
from apps.analytics.models import Employee_data 


class HomePage(APIView):
    def get(self, request):
        user = request.user
        try:
            ticket = Ticket.objects.get(owner=user)
            serializer = TicketsSerializers(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(
                {"message": "No tickets found for the user."}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        user = request.user
        try:
            ticket = Ticket.objects.get(owner=user)
            ticket.delete()
            return Response(
                {"message": "Ticket successfully deleted."}, 
                status=status.HTTP_200_OK
            )
        except Ticket.DoesNotExist:
            return Response(
                {"message": "No tickets found for the user."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        




class Reserve(APIView):

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "User not authenticated."}, status=401)

        code_postal = request.GET.get("code_postal")

        if not code_postal:
            return Response({"message": "Postal code is required."}, status=400)

        get_poste=Post.objects.get(code_postale=code_postal)
        reserved_tickets = Ticket.objects.filter(related_post=get_poste).values_list("nmr",flat=True)
        nmr_dispo = []
        starting_number = 1

        # Generate 10 available ticket numbers
        while len(nmr_dispo) < 10:
            if starting_number not in reserved_tickets:
                nmr_dispo.append(starting_number)
            starting_number += 1

        # Calculate starting times for tickets
        current_time = datetime.now()  # Get current time as a datetime object
        starting_time = current_time + timedelta(minutes=len(reserved_tickets) * 5 + 5)

        ticket_disponible_liste = []
        for i in range(10):
            ticket_disponible_liste.append({
                "ticket_number": nmr_dispo[i],
                "available_time": starting_time.strftime("%H:%M")  # Format time as HH:MM
            })
            starting_time += timedelta(minutes=5)  # Increment by 5 minutes for each ticket

        return Response({
            "available_tickets": ticket_disponible_liste,
            "user_name": user.first_name
        }, status=200)
    
    def post(self, request):
        user = request.user


        if not user.is_authenticated:
            return Response({"message": "User not authenticated."}, status=401)

    
        nmr_tiquet = request.data.get("nmr")
        type_tiquet = request.data.get("type")
        is_hendicape = request.data.get("handicape")
        code_postale = request.data.get("code_postale")

        if not all([nmr_tiquet, type_tiquet, code_postale]):
            return Response({"message": "Missing required fields."}, status=400)

    
        try:
            related_post = Post.objects.get(code_postale=code_postale)
        except Post.DoesNotExist:
            return Response({"message": "Invalid postal code, no related post found."}, status=404)

        # Create the ticket
        ticket = Ticket.objects.create(
            related_post=related_post,
            ticket_type=type_tiquet,
            handicap=is_hendicape,
            owner=user,
            nmr=nmr_tiquet
        )

        return Response({"message": "Ticket reserved successfully."}, status=201)
 

class CurrentTicketAdmin(APIView):

    def get(self, request):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"message": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            post = Post.objects.get(employees=user)
            first_ticket = post.ticket_set.first()
            print(first_ticket)

            if not first_ticket:
                return Response(
                    {"message": "No tickets available for this post."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer_ticket = TicketsSerializers(first_ticket)
            return Response(serializer_ticket.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                {"message": "No post found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def post(self, request):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"message": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        test_logout = request.data.get("logout")
        if test_logout:
            logout(request)

            employee = Employee_data.objects.get(employee = user)
            employee.todaylogout = datetime.now()
            return Response(
                {"message": "User logged out successfully."},
                status=status.HTTP_200_OK
            )

        try:
            # Retrieve the post associated with the user
            post = Post.objects.get(employees=user)
            analysis_account = Employee_data.objects.get(employee=user)
            analysis_account.TodayNmbrTiquets += 1
            analysis_account.save()
            first_ticket = post.ticket_set.first()
            print(first_ticket)
            if not first_ticket:
                return Response(
                    {"message": "No tickets available for this post."},
                    status=status.HTTP_404_NOT_FOUND
                )

            TicketsTrash.objects.create(
    related_post=first_ticket.related_post,
    ticket_type=first_ticket.ticket_type,
    handicap=first_ticket.handicap,
    nmr=first_ticket.nmr,
)


            ticket_trash = TicketsTrash.objects.last()  


            ticket_trash.owner.add(first_ticket.owner)  

         
            first_ticket.delete()

   
            next_ticket = post.ticket_set.first()
            print(next_ticket)
            if not next_ticket:
                return Response(
                    {"message": "No more tickets available."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize and return the next ticket
            serializer_ticket = TicketsSerializers(next_ticket)
            return Response(serializer_ticket.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                {"message": "No post found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Employee_data.DoesNotExist:
            return Response(
                {"message": "Analysis account not found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




    def put(self, request):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"message": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Fetch the post associated with the user
            post = Post.objects.get(employees=user)

            # Retrieve the last deleted ticket
            last_deleted_ticket = TicketsTrash.objects.filter(related_post=post).last()

            if not last_deleted_ticket:
                return Response(
                    {"message": "No precedent tickets found ."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize and return the last deleted ticket
            serialized_ticket = TicketsSerializers(last_deleted_ticket)
            return Response(serialized_ticket.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                {"message": "No post found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
