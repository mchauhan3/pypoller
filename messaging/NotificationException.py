class NotificationException(Exception):
    """
    Exception class for notification-related errors.

    Attributes:
        message (str): The error message.
        underlying (Exception): The underlying exception causing the error. Defaults to Exception().
    """

    def __init__(self, message: str, underlying: Exception = Exception()):
        """
        Initialize the NotificationException.

        Args:
            message (str): The error message.
            underlying (Exception, optional): The underlying exception causing the error. Defaults to Exception().
        """
        self.message = message
        self.underlying = underlying

    def __str__(self):
        """
        Convert the exception to a string representation.

        Returns:
            str: The string representation of the exception.
        """
        return f"{self.message} \n Underlying exception: {self.underlying}"
