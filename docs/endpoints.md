## 🛠️ Updated API Endpoints (cptn_api)

All endpoints have been migrated to the `cptn_` namespace for consistency and professionalism.

### **1. Authentication & Identity**
* `POST /api/v1/auth/register/`
* `POST /api/v1/auth/token/` (Login)
* `POST /api/v1/auth/token/refresh/`
* `POST /api/v1/auth/token/verify/`
* `POST /api/v1/auth/logout/`

### **2. Profile & Role Management**
* `GET/PATCH /api/v1/profile/me/` (Anonymized vehicle info & seat capacity)
* `POST /api/v1/profile/role/` (Switch between Driver/Rider modes)

### **3. The Carpool Lifecycle (Offers & Acceptances)**
* `POST /api/v1/cptn/offer/` (Driver creates a GTFS Trip/Schedule)
* `GET /api/v1/cptn/find/` (Rider searches for any destination)
* `POST /api/v1/cptn/join/` (Rider creates a `PENDING` booking)
* `PATCH /api/v1/cptn/booking/{id}/` (Driver accepts/rejects the seat request)

### **4. Geospatial & Map Support**
* `GET /api/v1/map/stops/` (Returns all valid destinations/lots)
* `GET /api/v1/map/markers/` (Retrieves `cptn_marker_assets` for icon rendering)
* `GET /api/v1/map/shapes/{trip_id}/` (Retrieves cached ORS polyline)

### **5. Real-Time & Safety**
* `POST /api/v1/cptn/status/` (Check-in: `START`/`END` commute)
* `GET /api/v1/cptn/seats/{trip_id}/` (Dynamic seat availability calculation)

---
