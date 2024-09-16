import django_filters
from users.models import Payment

class PaymentFilter(django_filters.FilterSet):
    course = django_filters.CharFilter(field_name='course__title', lookup_expr='icontains')
    lesson = django_filters.CharFilter(field_name='lesson__title', lookup_expr='icontains')
    payment_method = django_filters.ChoiceFilter(field_name='payment_method', choices=Payment.payment_method)

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
