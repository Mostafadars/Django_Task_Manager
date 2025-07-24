from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task, Category
from .serializer import TaskSerializer, CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = {
        'due_date': ['gte', 'lte', 'exact'],
        'categories': ['exact', 'in'],
    }

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.completed:
            return Response(
                {"error": "Cannot delete a completed task."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Task.objects.all()
        status_param = self.request.query_params.get('status')
        if status_param == 'completed':
            queryset = queryset.filter(completed=True)
        elif status_param == 'pending':
            queryset = queryset.filter(completed=False)
        return queryset

    @action(detail=False, methods=['get'])
    def important(self, request):
        important_tasks = Task.objects.filter(important=True)
        serializer = self.get_serializer(important_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
