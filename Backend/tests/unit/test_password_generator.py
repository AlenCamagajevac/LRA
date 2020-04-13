from core.utils.password_generator import PasswordGenerator


def test_password_generated():
    """
    Generated passwrd should contain only letters, both uppercase
    and lowercase

    Password should be of specified length
    """

    # Given
    password_length = 8

    # When
    password = PasswordGenerator.generate_password(password_length)

    # Then
    assert not any(char.isdigit() for char in password)
    assert len(password) == password_length
