from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12                        # Default – 12 ta
    page_size_query_param = 'page_size'   # ?page_size=6 bilan o'zgartirish mumkin
    max_page_size = 100                   # Eng ko'pi – 100 ta