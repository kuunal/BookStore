responses= {
     'verify_response' : {'status':200, 'message':'Successfully verified'},
     'invalid_product_id' : {'status':400, 'message':'No such product'},
     'added_to_wishlist' : {'status':200, 'message':'Added to wishlist'},
     'invalid_product' : {'status':400, 'message':'invalid product'},
     'deleted_wishlist_item' : {'status':200, 'message':'Deleted from wishlist'},
     'otp_invalid' : {'status':401,'message':'OTP is invalid!'},
     'otp_not_generated' : {'status':401,'message':'You havent requested for OTP!'},
     'otp_sent' : {'status':200, 'message':'Please verify by entering OTP sent to you'},
     'login_failed' : {'status': 401, 'message':'invalid Id or pass'},
     'product_already_in_wishlist' : {'status': 400, 'message':'Product already in wishlist'},
    
    }


def get_response_code(key):
    return responses[key]

