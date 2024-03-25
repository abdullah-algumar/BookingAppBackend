from django.contrib import admin
from django.urls import path
from api import views as api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="This is Room booking API documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_alias = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),

    # <editor-fold desc="Auth">
    path(api_alias + '/register/', api.RegisterView.as_view()),
    path(api_alias + '/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(api_alias + '/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(api_alias + '/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # </editor-fold>

    # <editor-fold desc="User">
    path(api_alias + '/available-rooms/', api.AvailableRooms.as_view(), name='available-rooms'),
    path(api_alias + '/book-room/', api.BookRoom.as_view(), name='reservation'),
    path(api_alias + '/create-reservations/', api.CreateReservations.as_view(), name='create-room'),
    # </editor-fold>
    
    # <editor-fold desc="Admin">
    path(api_alias + '/add-room/', api.AddRoom.as_view(), name='add_room'),
    path(api_alias + '/list-rooms/', api.ListRooms.as_view(), name='list_rooms'),
    path(api_alias + '/get-room/<int:pk>/', api.GetRoom.as_view(), name='get-room'),
    path(api_alias + '/update-room/<int:pk>/', api.UpdateRoom.as_view(), name='update_room'),
    path(api_alias + '/delete-room/<int:pk>/', api.DeleteRoom.as_view(), name='delete_room'),
    # </editor-fold>


    # <editor-fold desc="Swagger">
    path(api_alias + '/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(api_alias + '/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # </editor-fold>
]

