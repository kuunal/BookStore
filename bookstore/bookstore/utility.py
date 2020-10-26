from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection
from response_codes import get_response_code
from django.db import DatabaseError, IntegrityError, ProgrammingError
from bookstore.book_store_exception import BookStoreError


class DataBaseOperations:

    """
    Comman database connection with try catch for all uses to avoid try catch everytime
    """

    @staticmethod
    def execute_sql(query=None, params=None, many=None):
        try:
            cursor = connection.cursor()
            res = cursor.execute(query, params)
            if many == True:
                result = cursor.fetchall()
                return result if result else None
            if many == False:
                result = cursor.fetchone()
                return result[0] if result else None
            return res
        except ProgrammingError:
            raise BookStoreError(get_response_code("programming_error"))
        except IntegrityError:
            raise BookStoreError(get_response_code("invalid_product_id"))
        except DatabaseError:
            raise BookStoreError(get_response_code("database_error"))
        except Exception:
            raise BookStoreError("somethong went wrong")
        finally:
            cursor.close()
