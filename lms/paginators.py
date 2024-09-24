from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы в запросе
    max_page_size = 100  # Максимальный размер страницы

class LessonPagination(PageNumberPagination):
    page_size = 5  # Меньшее количество элементов на странице для уроков
    page_size_query_param = 'page_size'
    max_page_size = 50
