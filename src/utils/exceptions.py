class PortfolioError(Exception):
    """Base exception for portfolio-related errors"""
    pass

class CoinNotFoundError(PortfolioError):
    """Raised when a requested coin is not found"""
    pass

class InvalidInputError(PortfolioError):
    """Raised when input validation fails"""
    pass

class APIError(PortfolioError):
    """Raised when API requests fail"""
    pass 