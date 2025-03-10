"""
PowerPath API client core.

This module provides the base HTTP client for the PowerPath API with retry mechanism and error handling.
"""

import time
import random
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Type, Callable
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ...logger import configure_logging
from ..models import PowerPathBase

# Set up logging using the logger helper
logger = configure_logging(logger_name="powerpath_helper", log_level=15)  # FINE level

# Type variable for generic response types
T = TypeVar('T', bound=PowerPathBase)
TList = TypeVar('TList', bound=List[PowerPathBase])


class PowerPathClientError(Exception):
    """Base exception for PowerPath API client errors."""
    pass


class PowerPathRequestError(PowerPathClientError):
    """Exception raised for errors in the request."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class PowerPathAuthenticationError(PowerPathRequestError):
    """Exception raised for authentication errors (401)."""
    pass


class PowerPathNotFoundError(PowerPathRequestError):
    """Exception raised for resource not found errors (404)."""
    pass


class PowerPathServerError(PowerPathRequestError):
    """Exception raised for server errors (5xx)."""
    pass


class PowerPathRateLimitError(PowerPathRequestError):
    """Exception raised for rate limit errors (429)."""
    pass


class PowerPathClient:
    """
    Base HTTP client for the PowerPath API.
    
    This client handles:
    - Authentication
    - Retry mechanism with exponential backoff
    - Error handling
    - Request/response logging
    
    Attributes:
        base_url: The base URL for the PowerPath API
        api_key: The API key for authentication (if required)
        timeout: The timeout for requests in seconds
        max_retries: The maximum number of retries for failed requests
        session: The requests session
    """
    
    def __init__(
        self,
        base_url: str = "https://api.alpha1edtech.com",
        api_key: Optional[str] = None,  # Kept for backward compatibility
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize the PowerPath API client.
        
        Args:
            base_url: The base URL for the PowerPath API
            api_key: Not required for PowerPath API (kept for backward compatibility)
            timeout: The timeout for requests in seconds
            max_retries: The maximum number of retries for failed requests
        
        Note:
            As of now, no authentication is required to use the PowerPath API.
            The api_key parameter is kept for backward compatibility but is not used.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key  # Kept for backward compatibility
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Set up session with retry mechanism
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        
        # Note: No authentication is required for the PowerPath API
        # The api_key parameter is kept for backward compatibility but is not used
        
        logger.info(f"PowerPath API client initialized with base URL: {self.base_url}")
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build the full URL for an API endpoint.
        
        Args:
            endpoint: The API endpoint path
            
        Returns:
            str: The full URL
        """
        # Ensure endpoint starts with a slash
        if not endpoint.startswith('/'):
            endpoint = f'/{endpoint}'
        
        return f"{self.base_url}{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle the API response and raise appropriate exceptions.
        
        Args:
            response: The requests Response object
            
        Returns:
            Dict[str, Any]: The JSON response data
            
        Raises:
            PowerPathAuthenticationError: If authentication fails (401)
            PowerPathNotFoundError: If resource is not found (404)
            PowerPathRateLimitError: If rate limit is exceeded (429)
            PowerPathServerError: If server error occurs (5xx)
            PowerPathRequestError: For other request errors
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {e}"
            
            if response.status_code == 401:
                logger.error(f"Authentication error: {error_msg}")
                raise PowerPathAuthenticationError(error_msg, status_code=response.status_code, response=response)
            elif response.status_code == 404:
                logger.error(f"Resource not found: {error_msg}")
                raise PowerPathNotFoundError(error_msg, status_code=response.status_code, response=response)
            elif response.status_code == 429:
                logger.error(f"Rate limit exceeded: {error_msg}")
                raise PowerPathRateLimitError(error_msg, status_code=response.status_code, response=response)
            elif 500 <= response.status_code < 600:
                logger.error(f"Server error: {error_msg}")
                raise PowerPathServerError(error_msg, status_code=response.status_code, response=response)
            else:
                logger.error(f"Request error: {error_msg}")
                raise PowerPathRequestError(error_msg, status_code=response.status_code, response=response)
        except ValueError:
            # Invalid JSON response
            error_msg = "Invalid JSON response"
            logger.error(error_msg)
            raise PowerPathRequestError(error_msg, response=response)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: The HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: The API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
            
        Raises:
            PowerPathClientError: If the request fails
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.timeout
        
        # Log the request
        logger.fine(f"Making {method} request to {url}")
        if params:
            logger.fine(f"Query parameters: {params}")
        if json_data:
            logger.fine(f"JSON data: {json_data}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout,
            )
            
            # Log the response
            logger.fine(f"Response status: {response.status_code}")
            
            # Handle the response
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            # Network-related errors
            error_msg = f"Request failed: {e}"
            logger.error(error_msg)
            raise PowerPathClientError(error_msg) from e
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: The API endpoint path
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
        """
        return self._request("GET", endpoint, params=params, headers=headers, timeout=timeout)
    
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: The API endpoint path
            json_data: JSON data
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
        """
        return self._request("POST", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)
    
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: The API endpoint path
            json_data: JSON data
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
        """
        return self._request("PUT", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)
    
    def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a PATCH request to the API.
        
        Args:
            endpoint: The API endpoint path
            json_data: JSON data
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
        """
        return self._request("PATCH", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)
    
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: The API endpoint path
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Dict[str, Any]: The JSON response data
        """
        return self._request("DELETE", endpoint, params=params, headers=headers, timeout=timeout)
    
    def get_resource(self, endpoint: str, model_class: Type[T], **kwargs) -> T:
        """
        Get a single resource and convert it to a model instance.
        
        Args:
            endpoint: The API endpoint path
            model_class: The model class to convert the response to
            **kwargs: Additional arguments to pass to the get method
            
        Returns:
            T: The model instance
        """
        logger.fine(f"Getting resource from {endpoint} as {model_class.__name__}")
        data = self.get(endpoint, **kwargs)
        return model_class.model_validate(data)
    
    def get_resources(self, endpoint: str, model_class: Type[T], **kwargs) -> List[T]:
        """
        Get a list of resources and convert them to model instances.
        
        Args:
            endpoint: The API endpoint path
            model_class: The model class to convert the response items to
            **kwargs: Additional arguments to pass to the get method
            
        Returns:
            List[T]: The list of model instances
        """
        logger.fine(f"Getting resources from {endpoint} as {model_class.__name__}[]")
        data = self.get(endpoint, **kwargs)
        result = [model_class.model_validate(item) for item in data]
        logger.fine(f"Retrieved {len(result)} {model_class.__name__} items")
        return result
    
    def create_resource(self, endpoint: str, model_class: Type[T], data: Dict[str, Any], **kwargs) -> T:
        """
        Create a resource and convert the response to a model instance.
        
        Args:
            endpoint: The API endpoint path
            model_class: The model class to convert the response to
            data: The data to send in the request
            **kwargs: Additional arguments to pass to the post method
            
        Returns:
            T: The model instance
        """
        logger.fine(f"Creating {model_class.__name__} at {endpoint}")
        response_data = self.post(endpoint, json_data=data, **kwargs)
        result = model_class.model_validate(response_data)
        logger.info(f"Created {model_class.__name__} with ID: {getattr(result, 'id', None)}")
        return result
    
    def update_resource(self, endpoint: str, model_class: Type[T], data: Dict[str, Any], **kwargs) -> T:
        """
        Update a resource and convert the response to a model instance.
        
        Args:
            endpoint: The API endpoint path
            model_class: The model class to convert the response to
            data: The data to send in the request
            **kwargs: Additional arguments to pass to the patch method
            
        Returns:
            T: The model instance
        """
        logger.fine(f"Updating {model_class.__name__} at {endpoint}")
        response_data = self.patch(endpoint, json_data=data, **kwargs)
        result = model_class.model_validate(response_data)
        logger.info(f"Updated {model_class.__name__} with ID: {getattr(result, 'id', None)}")
        return result
    
    def delete_resource(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Delete a resource.
        
        Args:
            endpoint: The API endpoint path
            **kwargs: Additional arguments to pass to the delete method
            
        Returns:
            Dict[str, Any]: The response data
        """
        logger.fine(f"Deleting resource at {endpoint}")
        result = self.delete(endpoint, **kwargs)
        logger.info(f"Deleted resource at {endpoint}")
        return result 