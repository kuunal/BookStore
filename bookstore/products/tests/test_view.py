from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

class TestView(APITestCase):

    def test_given_product_url_when_with_no__query_params_returns_product_sortedby_id(self):
        res = self.client.get(reverse('product_list'))
        self.assertEqual(res.status_code,200)


    def test_given_page_one_when_valid_returns_first_id(self):
        res = self.client.get(reverse('product_list'),{'pageno':1})
        self.assertEqual(res.data[0]['id'], 1)

    def test_given_page_when_invalid_returns_first_id(self):
        res = self.client.get(reverse('product_list'),{'pageno':100})
        self.assertEqual(res.data[0]['id'], 1)

    def test_given_page_two_when_invalid_returns_sixth_id(self):
        res = self.client.get(reverse('product_list'),{'pageno':2})
        self.assertEqual(res.data[0]['id'], 6)

        
    def test_given_sortby_field_when_price_returns_result_sorted_by_price(self):
        res = self.client.get(reverse('product_list'),{'sortby':'price'})
        self.assertEqual(res.data[0]['price'],0)

    def test_given_sortby_field_when_author_returns_result_sorted_by_author_name(self):
        res = self.client.get(reverse('product_list'),{'sortby':'author'})
        self.assertEqual(res.data[0]['author'],'Chetan Bhagat\'')

    def test_given_sortby_field_when_title_returns_result_sorted_by_title(self):
        res = self.client.get(reverse('product_list'),{'pageno':1, 'sortby':'title'})
        self.assertEqual(res.data[0]['title'],'11/22/63\'')

    
    def test_given_sortby_field_when_quantity_returns_result_sorted_by_quantity(self):
        res = self.client.get(reverse('product_list'),{'pageno':1, 'sortby':'quantity'})
        self.assertEqual(res.data[0]['quantity'], 0)
    
    def test_given_sortby_field_when_invalid_returns_result_sorted_by_id(self):
        res = self.client.get(reverse('product_list'),{'pageno':1, 'sortby':'wrong_field'})
        self.assertEqual(res.data[0]['id'], 1)

    def test_given_des_field_when_true_returns_result_in_descending_order(self):
        res = self.client.get(reverse('product_list'),{'pageno':1, 'sortby':'price', 'des':'true'})
        self.assertEqual(res.data[0]['price'], 1100)
    
    def test_given_params_when_wrong_returns_response_in_default_order(self):
        res = self.client.get(reverse('product_list'),{'pageno':1000, 'sortby':'wrong', 'des':'asdasdasd'})
        self.assertEqual(res.data[0]['id'], 1)
    
    def test_given_path_param_when_author_name_returns_response_length_of_all_books_by_that_author(self):
        res = self.client.get(reverse('product_list')+'chetan bhagat')
        self.assertEqual(len(res.data), 2)
    
    def test_given_path_param_when_title_returns_response_of_books_with_similar_title(self):
        res = self.client.get(reverse('product_list')+'the mist')
        self.assertEqual(len(res.data), 1)

    def test_given_path_param_when_invalid_returns_custom_response(self):
        res = self.client.get(reverse('product_list')+'wrong_param')
        self.assertEqual(res.data['message'], 'No such product')