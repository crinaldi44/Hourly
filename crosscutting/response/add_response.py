class AddResponse:
    """Represents an instance of a response when a new row
       has been added. Once the row is added to the table,
       returns the "id" of the element within 'data' and,
       additionally, sets the headers containing the location
       of the new resource.

       :cvar domain: The domain the document has been added to.
       :type str

    """

    def __init__(self, uid=None):
        """Instantiates a new instance of the AddResponse.

        :param domain: Represents the domain
        :type str
        """

        if uid is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

    def serve(self):
        return serve_response(message)