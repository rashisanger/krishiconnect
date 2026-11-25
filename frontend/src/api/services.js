import { apiRequest } from './client.js';

export const accountApi = {
  login: (credentials) => apiRequest('/accounts/login/', { method: 'POST', body: credentials, auth: false }),
  registerFarmer: (data) => apiRequest('/accounts/register/farmer/', { method: 'POST', body: data, auth: false }),
  registerBuyer: (data) => apiRequest('/accounts/register/buyer/', { method: 'POST', body: data, auth: false }),
  profile: () => apiRequest('/accounts/profile/'),
  logout: (refresh) => apiRequest('/accounts/logout/', { method: 'POST', body: { refresh } }),
};

export const listingApi = {
  crops: () => apiRequest('/crops/catalog/'),
  mine: (query) => apiRequest('/crops/my-listings/', { query }),
  create: (data) => apiRequest('/crops/my-listings/', { method: 'POST', body: data }),
  update: (id, data) => apiRequest(`/crops/my-listings/${id}/`, { method: 'PATCH', body: data }),
  remove: (id) => apiRequest(`/crops/my-listings/${id}/`, { method: 'DELETE' }),
  browse: (query) => apiRequest('/buyers/listings/', { query }),
};

export const profileApi = {
  farmer: () => apiRequest('/farmers/profile/'),
  updateFarmer: (data) => apiRequest('/farmers/profile/', { method: 'PATCH', body: data }),
  buyer: () => apiRequest('/buyers/profile/'),
  updateBuyer: (data) => apiRequest('/buyers/profile/', { method: 'PATCH', body: data }),
};

export const marketApi = {
  prices: (query) => apiRequest('/market-prices/', { query }),
  compare: (query) => apiRequest('/market-prices/compare/', { query }),
};

export const negotiationApi = {
  buyerEnquiries: (query) => apiRequest('/enquiries/buyer/', { query }),
  farmerEnquiries: (query) => apiRequest('/enquiries/farmer/', { query }),
  createEnquiry: (data) => apiRequest('/enquiries/buyer/', { method: 'POST', body: data }),
  respondEnquiry: (id, data) => apiRequest(`/enquiries/farmer/${id}/respond/`, { method: 'PATCH', body: data }),
  buyerOffers: (query) => apiRequest('/enquiries/buyer/offers/', { query }),
  farmerOffers: (query) => apiRequest('/enquiries/farmer/offers/', { query }),
  createOffer: (data) => apiRequest('/enquiries/buyer/offers/', { method: 'POST', body: data }),
  decideOffer: (id, status) => apiRequest(`/enquiries/farmer/offers/${id}/decision/`, { method: 'PATCH', body: { status } }),
};

export const analyticsApi = { farmerListings: () => apiRequest('/analytics/farmer/listing-statistics/') };
