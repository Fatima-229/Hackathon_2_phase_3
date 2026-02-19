// utils/fetchClient.ts
export const fetchClient = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('token');

  // Clone the options to avoid mutating the original
  const fetchOptions = { 
    ...options,
    // Add a timeout of 10 seconds
    signal: AbortSignal.timeout ? AbortSignal.timeout(10000) : undefined
  };

  // Handle headers properly - they can be a Headers object or a plain object
  const headers = new Headers(options.headers || {});

  // Set content type if not already set
  if (!headers.get('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  // Add authorization header if token exists
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  // Assign the headers back to fetchOptions
  fetchOptions.headers = headers;

  try {
    const response = await fetch(url, fetchOptions);

    // If the response is 401, redirect to login
    if (response.status === 401) {
      localStorage.removeItem('token');
      // Use router instead of direct redirect for Next.js
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
      return response; // Return the response even though it's an error
    }

    return response;
  } catch (error) {
    console.error('API call error:', error);
    
    // Check if it's a network error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      console.error('Network error - please check if the backend server is running');
      throw new Error('Network error: Unable to connect to the server. Please check that the backend is running.');
    }
    
    throw error;
  }
};