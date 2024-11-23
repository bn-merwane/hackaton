from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from apps.accounts.models import Account

class Reserve(APIView):
    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"message": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        wilaya = request.data.get("wilaya")
        if not wilaya:
            return Response(
                {"message": "Wilaya is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        posts = Post.objects.filter(wilaya=wilaya)
        if not posts.exists():
            return Response(
                {"message": "No posts found for the provided wilaya."},
                status=status.HTTP_404_NOT_FOUND
            )


        paginator = PageNumberPagination()
        paginator.page_size = 1  
        paginated_posts = paginator.paginate_queryset(posts, request)

        
        serialized_posts = PostSerializer(paginated_posts, many=True)

        return paginator.get_paginated_response(serialized_posts.data)


class SettingsPost(APIView):

    def get(self, request):
        user = request.user

        # Ensure the user is authenticated and an admin
        if not user.is_authenticated or not user.is_superuser:
            return Response(
                {"message": "User is not authorized to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            post = Post.objects.get(employees=user)

            employees = post.employees.all()

            # Construct the employee status list
            employee_status = [
                {"user_id": employee.id, "is_active": employee.is_active}
                for employee in employees
            ]

            return Response(
                {
                    "post_id": post.id,
                    "employee_count": employees.count(),
                    "employee_status": employee_status
                },
                status=status.HTTP_200_OK
            )

        except Post.DoesNotExist:
            return Response(
                {"message": "No post found for the current admin user."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"message": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Retrieve the post associated with the authenticated user
            post = Post.objects.filter(employees=user).first()

            if not post:
                return Response(
                    {"message": "No post found for the current user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get the distributor information from the request data
            distributor = request.data.get("distributor")

            post.has_distributor = distributor
            post.save()

            return Response(
                {"message": "Distributor assigned successfully."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )












