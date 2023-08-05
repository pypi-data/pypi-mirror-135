from verify_django_serializer.exceptions import TypeSerializerError


def validate_return_response(serializer_class):
    """
        Decorator to valid response format.
    """
    def Inner(function):
        def wrapper(*args, **kwargs):
            response = function(*args, **kwargs)
            if isinstance(serializer_class, list):
                for idx, serializer_template in enumerate(serializer_class):
                    serializer = serializer_template(data=response.data)
                    if serializer.is_valid():
                        break
                    if idx + 1 == len(serializer_class):
                        raise TypeSerializerError(
                            "Errors: {}".format(serializer.errors)
                        )
            else:
                serializer = serializer_class(data=response.data)
                if not serializer.is_valid():
                    raise TypeSerializerError(
                        "Errors: {}".format(serializer.errors)
                    )

            return response
        return wrapper
    return Inner
