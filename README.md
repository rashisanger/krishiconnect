\# KrishiConnect – Farmer Market Price Discovery and Buyer Linkage Platform

## Separate backend and frontend

The Django REST API lives in the repository root. The independent React/Vite
frontend lives in `frontend/`. Each app has its own dependencies and server.

Start the backend in one terminal from the repository root:

```bash
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (usually `http://localhost:5173`).
Vite forwards `/api` and `/admin` requests to Django. Copy
`frontend/.env.example` to `frontend/.env.local`; set `VITE_API_BASE_URL=/api`
to use the development proxy, or provide the full API URL for a deployed
backend. Vite derives its proxy destination from that setting.



KrishiConnect is a Django REST Framework-based backend application designed to help farmers discover agricultural market prices, manage crop listings and connect with potential buyers.



The platform provides market price information sourced from the Government of India's Agmarknet/Open Government Data API, along with farmer and buyer management, enquiries, offers and analytics.



\## Technology Stack



\- \*\*Backend:\*\* Python, Django

\- \*\*API Framework:\*\* Django REST Framework

\- \*\*Authentication:\*\* JWT (SimpleJWT)

\- \*\*Database:\*\* SQLite

\- \*\*External Data Source:\*\* Government of India Open Government Data API (Agmarknet)

\- \*\*API Testing:\*\* Postman

\- \*\*Environment Variables:\*\* python-dotenv



\## Project Modules



| Module | Description |

|---|---|

| Accounts | Registration, login, JWT authentication and role management |

| Farmers | Farmer profiles and profile management |

| Buyers | Buyer profiles and buyer-specific functionality |

| Crops | Admin-managed crop catalog and farmer crop listings |

| Market Prices | Agmarknet data import, price search, comparison and history |

| Enquiries | Buyer-farmer enquiries and offers |

| Analytics | Platform, crop price, mandi and farmer listing statistics |



\## User Roles



The application supports three roles:



\- \*\*Farmer:\*\* Manage profile, create and manage crop listings, view enquiries and respond to offers.

\- \*\*Buyer:\*\* Manage profile, browse available crop listings, create enquiries and submit offers.

\- \*\*Admin:\*\* Access administrative functionality and platform overview analytics.



\## Prerequisites



Install the following before running the backend:



\- Python 3.10 or later (use a Python version compatible with the installed Django release).

\- Git

\- Postman (recommended for API testing)



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd KrishiConnect

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



\*\*Windows PowerShell:\*\*



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\*\*Windows Command Prompt:\*\*



```cmd

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 5. Configure environment variables



Create a `.env` file in the project root.



Copy the contents of `.env.example` and add your own Government Open Data API key:



```env

AGMARKNET\_API\_KEY=your\_data\_gov\_in\_api\_key

```



Do not upload `.env` to GitHub or share your API key publicly.



\### 6. Apply database migrations



```bash

python manage.py migrate

```



\### 7. Create an administrator account



```bash

python manage.py createsuperuser

```



Follow the prompts to create the administrator username, email and password.



\### 8. Start the development server



```bash

python manage.py runserver

```



The backend will be available at:



`http://127.0.0.1:8000/`



Django Admin:



`http://127.0.0.1:8000/admin/`



\## API Base URL



All application APIs use the following base URL:



`http://127.0.0.1:8000/api/`



\## API Modules



| Module | Base URL |

|---|---|

| Accounts | `/api/accounts/` |

| Farmers | `/api/farmers/` |

| Buyers | `/api/buyers/` |

| Crops | `/api/crops/` |

| Market Prices | `/api/market-prices/` |

| Enquiries | `/api/enquiries/` |

| Analytics | `/api/analytics/` |



Refer to the API documentation for endpoint paths, HTTP methods, permissions and request formats.



\## Authentication



KrishiConnect uses JSON Web Token (JWT) authentication.



\### Login



Use the login endpoint to obtain access and refresh tokens.



Include the access token in subsequent authenticated API requests:



```http

Authorization: Bearer YOUR\_ACCESS\_TOKEN

```



For JSON requests, use:



```http

Content-Type: application/json

```



When the access token expires, use the refresh endpoint to obtain a new access token.



Do not hardcode JWT tokens in frontend source code or commit them to GitHub.



\## Frontend Integration



The React/Vite frontend in `frontend/` communicates with Django through HTTP
requests. During local development, Vite proxies `/api` requests to the backend.



\*\*Backend API base URL:\*\*



```text

http://127.0.0.1:8000/api/

```



The frontend should:



1\. Register users using the appropriate farmer or buyer registration endpoint.

2\. Authenticate users through the login endpoint.

3\. Store the access token securely using an appropriate frontend authentication strategy.

4\. Send the JWT access token in the Authorization header for protected APIs.

5\. Use the refresh endpoint when the access token expires.

6\. Handle API validation errors and authorization responses.

7\. Display API data in dashboards, tables, forms and charts.



\### CORS Configuration



The backend is configured to allow selected local frontend origins.



If the frontend runs on a different port, add its exact origin to `CORS\_ALLOWED\_ORIGINS` in Django settings.



Examples:



\- React/Vite: `http://localhost:5173`

\- React: `http://localhost:3000`

\- Angular: `http://localhost:4200`



Do not enable unrestricted CORS in production.



\## Market Price Data



KrishiConnect integrates with the Government of India's Open Government Data API for agricultural market prices.



The backend imports market price records into the local database.



The market price APIs support:



\- Crop-based price search

\- State, district and mandi filters

\- Date filtering

\- Minimum, maximum and modal price information

\- Mandi-wise price comparison

\- Historical records available in the database



\*\*Data limitation:\*\* The currently imported dataset contains records from one reporting date. Historical API functionality can retrieve stored records, but meaningful multi-date historical trends require data from multiple dates.



\## Analytics



The analytics module provides:



\- Total available crop listings

\- Total registered farmers and buyers

\- Crop-wise average modal prices

\- Mandi-wise price comparisons

\- Enquiry and offer statistics

\- Farmer-specific crop listing statistics



Historical price analytics are excluded from the implemented analytics scope because the current dataset does not contain sufficient multi-date records.



\## API Testing



Postman can be used to test the backend APIs.



For authenticated requests:



1\. Log in using a registered account.

2\. Copy the access token from the response.

3\. Open the Authorization tab in Postman.

4\. Select Bearer Token.

5\. Paste the access token.

6\. Send the request.



Use different accounts to test farmer, buyer and administrator permissions.



\## Database



The project currently uses SQLite.



The database is created automatically when migrations are applied:



```bash

python manage.py migrate

```



The local database file (`db.sqlite3`) is excluded from GitHub. Each developer creates their own database by applying migrations.



\## Useful Commands



```bash

\# Activate virtual environment (Windows PowerShell)

.\\venv\\Scripts\\Activate.ps1



\# Install dependencies

pip install -r requirements.txt



\# Apply migrations

python manage.py migrate



\# Check Django configuration

python manage.py check



\# Create administrator

python manage.py createsuperuser



\# Start server

python manage.py runserver



\# Import market price records

python manage.py import\_market\_prices --limit 5

\# Create repeatable local demo data and test accounts

python manage.py seed\_demo\_data

```



The demo accounts are `demo_farmer` and `demo_buyer`, both with password
`KrishiDemo2026!`. They are intended for local preview; change or remove them
before using a shared or deployed database.


\## GitHub Collaboration



To collaborate:



1\. Push the backend repository to GitHub.

2\. Add the frontend teammate as a repository collaborator if private.

3\. Share the repository URL.

4\. Ask the teammate to clone the repository.

5\. The teammate should create their own virtual environment, install dependencies, configure `.env` and run migrations.

6\. Start the backend before integrating frontend API requests.



\## Security Notes



\- Never commit `.env` or API keys.

\- Never share passwords or JWT tokens.

\- Use Django's password hashing and authentication mechanisms.

\- Keep role-based access control enabled.

\- Use environment-specific settings for deployment.

\- Configure production `DEBUG`, `ALLOWED\_HOSTS`, HTTPS and CORS appropriately.



\## Project Status



The main backend modules have been developed and their APIs were tested during development.



The frontend and backend are maintained as separate apps in this repository and integrate through REST APIs.

The crop catalog is available at `GET /api/crops/catalog/`. Crop records are
managed in Django Admin; farmers select an existing crop when creating a
listing.



\*\*Project:\*\* KrishiConnect  

\*\*Backend:\*\* Django REST Framework  

\*\*Database:\*\* SQLite

