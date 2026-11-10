It is definitely the right time to update these. Since we’ve rebranded to **`cptn_api`** and introduced more sophisticated GTFS tables like `pathways`, `booking_rules`, and `translations`, the API needs to be more granular.

The biggest shifts here are:

1. **Renaming**: Moving from `stn` to `cptn` branding.
2. **Generalized Routing**: Ensuring endpoints reflect that destinations are no longer hardcoded (DLI).
3. **Booking Logic**: Incorporating the `booking_rules` we discussed to handle the "temporal handshake."
4. **Accessibility**: Adding endpoints to fetch pathway data for those "last meter" directions.

---

## 🔐 1. Authentication & Identity

*Unchanged in logic, but renamed for consistency.*

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/api/v1/auth/register/` | Initializes `CustomUser` and `cptn_user_profile`. |
| **POST** | `/api/v1/auth/login/` | Returns JWT Access + Refresh tokens. |
| **POST** | `/api/v1/auth/logout/` | Blacklists tokens; essential for student safety. |

---

## 👤 2. User Profile (Sidecar Logic)

*Includes vehicle capacity and accessibility preferences.*

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/v1/profile/me/` | Returns role, vehicle info, and **default booking rules**. |
| `PATCH` | `/api/v1/profile/me/` | Update profile (e.g., "Silver Hatchback", "Bike Rack: Yes"). |

---

## 🚗 3. Driver Workflow (The "Offer")

*Now supports generalized destinations and specific booking rules.*

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/journey/offer/` | Creates `Route`, `Trip`, `Shape`, and `Frequencies` (Auto-return). |
| `GET` | `/api/v1/driver/trips/` | List current driver's active GTFS `Trips`. |
| `GET` | `/api/v1/driver/requests/` | View all `PENDING` ride requests from riders. |
| `PATCH` | `/api/v1/driver/requests/{id}/` | **Accept/Reject**: Updates `cptn_ride_request` and capacity. |

---

## 🚲 4. Rider Workflow (The "Find & Book")

*Interfaces with `booking_rules` to ensure valid request windows.*

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/v1/journey/search/` | Search by origin/destination. Filters by `booking_rules` (e.g., notice time). |
| `POST` | `/api/v1/journey/request/` | Create a `cptn_ride_request`. Validates against `booking_type`. |
| `GET` | `/api/v1/rider/requests/` | Status of rider’s current/past requests + **Check-in Codes**. |

---

## 📍 5. Map, Assets, & Accessibility

*Now includes pathways and localized stop information.*

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/v1/map/stops/` | List all GTFS `Stops` with `cptn_stop_meta`. |
| `GET` | `/api/v1/map/stops/{id}/pathways/` | **New**: Returns `pathways` for accessibility guidance. |
| `GET` | `/api/v1/map/shapes/{trip_id}/` | Retrieve the high-fidelity ORS polyline for the map. |
| `GET` | `/api/v1/map/markers/` | Returns the `cptn_marker_assets` (DLI, Sponsor, Lot). |

---

## 🚦 6. System Status & Language

*Supports multi-language feeds and system-wide exceptions.*

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/v1/system/translations/` | **New**: Returns `translations.txt` strings for the UI. |
| `GET` | `/api/v1/journey/seats/{trip_id}/` | Returns current `cptn_trip_capacity`. |
| `POST` | `/api/v1/admin/exception/` | **(Admin)** Create `calendar_dates` for holidays/snow days. |

---

### 🧠 Strategic Changes Noted

* **Search vs. Find**: Renamed `/find/` to `/search/` to imply a more complex query involving time-windows and booking rules.
* **Request vs. Join**: Renamed `/join/` to `/request/` to better reflect that the driver must still approve the "handshake" before the rider is actually on the trip.
* **Pathway Integration**: The new `/stops/{id}/pathways/` endpoint is the key to your accessibility goal, providing the walking instructions from the street to the boarding zone.

**Would you like me to start drafting the Django `serializers.py` to show how we transform these complex GTFS tables into JSON for these endpoints?**