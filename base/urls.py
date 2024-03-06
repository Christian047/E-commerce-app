from django.urls import path
from . import views


# create patterns using the function name and url tag
# create urls after creating the views
urlpatterns = [
    path('', views.store, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    # path('login/', views.loginPage, name='login'),
    # path('logout/', views.logoutUser, name='logout'),
    # path('register/', views.RegisterUser.as_view(), name='register'),
    path('like/<int:pk>', views.LikeView, name='like_post'),
    path('incomecreate/', views.IncomeCreateView.as_view(), name='incomecreate'),
    path('update_user_order/', views.update_user_order, name='update_user_order'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('add_vendor_review/<int:vendor_id>/', views.add_vendor_review, name='add_vendor_review'),
    
    path('update_review/<int:pk>/', views.update_review, name='update_review'),
    path('delete_review/<int:pk>/', views.delete_review, name='delete_review'),

    
    path('create-room/', views.create_room, name='create-room'),
    path('activity/', views.activityPage, name='activity'),
    
    path('topics/', views.topicsPage, name='topics'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    
    # remember to pass a pk value if it will have a specific linkage
    
    path('update-room/<str:pk>/', views.updateRoom, name='update-room') ,
    path('update-user/', views.updateUser, name='update-user'),
    
    
    
    path('Category_create/', views.Category_create, name='category_create'),
    path('cat/<slug:category_slug>', views.Category_list.as_view(), name='category'),
    
    #Leave as empty string for base url
	path('', views.store, name="store"),
	path('Vendor_dashboard/', views.Vendor_dashboard, name="Vendor_dashboard"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('Confirm_order/', views.Confirm_order, name="confirm_order"),
	path('Subtract_amount/', views.Subtract_amount, name="Subtract_amount"),
	

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('eachproduct/<str:pk>/', views.Eachproduct, name="eachproduct"),
    path('vendor/<int:vendor_id>/', views.vendor_products, name='vendor_products'),
 
 
    path('create_product/', views.create_product, name="create_product"),
    path('update_product/<str:pk>/', views.update_product, name='update_product') ,
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product') ,
    path('suscribers_list/', views.suscribers_list, name='suscribers_list') ,
    path("penpage/", views.Pendingpage.as_view(), name='penpage'),
    path('penpage/<int:pk>/', views.Pendingpage.as_view(), name='approve_post'),
    path('unapprove/<int:pk>/', views.UnapproveProduct.as_view(), name='unapprove_product'),
]

   