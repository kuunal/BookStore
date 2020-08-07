TOTAL_NUMBER_OF_OTP_CHARACTER = 6
JWT_EXPIRATION_TIME=300
OTP_EXPIRY_TIME=300
OTP_BLOCK_TIME=3600 
PAGINATOR_PAGE_LIMIT = 5

responses= {
     'no_headers' : {'status' : 401, 'message' : 'No headers found'},
     'invalid_login' :{'status':400, 'message':'Invalid login_id'},
     'login_required' : {'status':401 ,'message' : 'Please login first'},
     'jwt_auth_error' : {'status' : 401, 'message' : 'Invalid Token'},
     'jwt_decode_error' : { 'status' : 400, 'message' : 'JWT decode error'},
     'jwt_signature_expired' : {'status' : 401, 'message':'Token is expired! Please login again.'}, 
     'verify_response' : {'status':200, 'message':'Successfully verified'},
     'invalid_product_id' : {'status':400, 'message':'No such product'},
     'added_to_wishlist' : {'status':200, 'message':'Added to wishlist'},
     'invalid_product' : {'status':400, 'message':'invalid product'},
     'deleted_wishlist_item' : {'status':200, 'message':'Removed from wishlist'},
     'otp_invalid' : {'status':401,'message':'OTP is invalid!'},
     'otp_not_generated' : {'status':401,'message':'You havent requested for OTP!'},
     'otp_sent' : {'status':200, 'message':'Please verify by entering OTP sent to you'},
     'login_failed' : {'status': 401, 'message':'invalid Id or pass'},
     'product_already_in_wishlist' : {'status': 400, 'message':'Product already in wishlist'},
     'wishlist_delete_does_exists':{'status':400, 'message':'No such item in wishlist'},
     'added_to_cart' : {'status':200, 'message':'Added to cart'},
     'updated_quantity': {'status':200, 'message':'Updated quantity successfully'},
     'out_of_stock' : {'status':400, 'message':'Product out of stock for that quantity'},
     'order_placed' : {'status' : 200, 'message' : 'Order Placed'},
     'not_available' : {'status' : 400, 'message' : 'Product not available'},
     'item_not_in_cart':{'status':400, 'message':'No such item in cart'},
     'removed_cart_item' : {'status':200, 'message':'Removed from cart'},
     'database_error' : {"status":500, 'message':'Something went wrong'}, 
     'programming_error' : {"status":500, 'message':'Something went wrong'},
     'integrity_error' : {"status":500, 'message':'Something went wrong'},
     'too_many_otp' : {'status' : 400 , 'message': 'You have tried too many times. Please come back again tommorow'},
     'logout' : {'status' :200, 'message' : 'Logged out successfully!'},
     'invalid_data' : {'status' : 400, 'message':'Invalid Data'}
    }


def get_response_code(key):
    return responses[key]

