# 🏗️ Architecture: cptn_api (Car Pool Transit Network)

The **cptn_api** is a geo-aware Django REST API designed for a generalized peer-to-peer carpooling network. By leveraging the **General Transit Feed Specification (GTFS)**, the system treats individual student commutes as "micro-transit" lines, ensuring industry-standard scalability while maintaining a **Zero-PII** (Personally Identifiable Information) footprint.

---

## 1. Data Layer: The Hybrid GTFS-Sidecar Model

The system utilizes a **Sidecar Pattern**. The core GTFS tables handle spatial and temporal scheduling, while Django-specific "Sidecar" tables manage application logic, user identity, and accessibility assets.

### A. Identity & Governance

| File | cptn_api Interpretation |
| --- | --- |
| **`agency.txt`** | Represents the **Individual Driver**. Each driver is their own "micro-agency." |
| **`feed_info.txt`** | Metadata for the network (Publisher: CPTN Network). |
| **`attributions.txt`** | Credits for **OpenRouteService (ORS)** and campus sponsors. |

### B. Geographic & Spatial Core

| File | cptn_api Interpretation |
| --- | --- |
| **`routes.txt`** | The logical commute path (e.g., "Sydney to Port Hawkesbury"). |
| **`trips.txt`** | A specific occurrence of a ride offered by a driver. |
| **`stop_times.txt`** | Interpolated ETAs at each meeting point along the path. |
| **`stops.txt`** | Official **Safe Zones** (Campuses, Sponsor Shelters, Carpool Lots). |
| **`shapes.txt`** | High-fidelity polylines generated via ORS to map actual road paths. |
| **`pathways.txt`** | **Accessibility Layer:** Walking paths from the curb to the car door. |

### C. Temporal & Application Logic

| File | cptn_api Interpretation |
| --- | --- |
| **`calendar.txt`** | The driver's weekly routine (e.g., Mon/Wed/Fri for the Winter Semester). |
| **`calendar_dates.txt`** | **Exception Engine:** Automated cancellations for holidays and snow days. |
| **`frequencies.txt`** | Logic for the **Mandatory Return Trip** (DLI departure offsets). |
| **`booking_rules.txt`** | The "Handshake" constraints (e.g., 60-minute advance notice). |
| **`translations.txt`** | Multilingual support for UI text and stop names (EN, FR, Mi'kmaw). |

---

## 2. Django Sidecar Extensions (Application Logic)

These tables extend the GTFS standard to support the web application's interactive features.

| Sidecar Table | Linkage | Purpose |
| --- | --- | --- |
| **`CustomUser`** | — | Extends Django Auth for student identities. |
| **`CPTN_User_Profile`** | `Agency` | Bridges `CustomUser` to the GTFS Provider (Driver) role. |
| **`CPTN_Ride_Request`** | `Trip` | Manages the Offer/Accept lifecycle and anonymous check-in codes. |
| **`CPTN_Trip_Capacity`** | `Trip` | Real-time seat inventory and trip status (Scheduled/En Route). |
| **`CPTN_Stop_Meta`** | `Stop` | Stores shelter hours, lighting status, and security features. |
| **`CPTN_Marker_Assets`** | `Stop` | Maps `stop_id` to custom map icons (Graduation Cap, Gold Star). |

---

## 3. The "Journey Engine" Workflow

### Phase 1: The Offer (Driver)

1. **Input:** Driver submits an origin, destination, and seats.
2. **Routing:** Backend calls **ORS** to generate a `Shape`.
3. **Stop Discovery:** PostGIS finds all `Stops` within a 500m buffer of the `Shape`.
4. **Interpolation:** API calculates `Stop_Times` based on ORS distance/duration data.
5. **Return Logic:** A mirror `Trip` is created for the afternoon using `Frequencies`.

### Phase 2: The Booking (Rider)

1. **Search:** Rider searches for a destination. API filters by `Stop` proximity and `Booking_Rules`.
2. **Request:** Rider submits a `CPTN_Ride_Request`.
3. **Acceptance:** Driver accepts; `CPTN_Trip_Capacity` decrements available seats.
4. **Verification:** A 4-digit code is generated in the `CPTN_Ride_Request` for anonymous boarding verification.

---

## 4. Key Architectural Design Principles

* **Zero-PII Compliance:** No home addresses or phone numbers are stored in GTFS files. Meeting points are restricted to `Stops`.
* **Accessibility First:** Using `pathways.txt` and `stop_meta`, the system prioritizes routes that accommodate mobility aids.
* **Industry Compatibility:** The core data remains exportable as a valid GTFS feed for regional transit planning.

Dropping **pathways** makes sense for the **Car Pool Transit Network (CPTN)**. In the GTFS world, `pathways.txt` is primarily used to describe the internal navigation of massive transit hubs (like subway stations or large bus terminals with multiple levels and elevators). For a carpool-based system connecting college campuses and regional stops, those internal "micro-routing" details are unnecessary overhead.

By sticking to the core `Stops`, `Areas`, and `StopAreas` schema, you keep the engine focused on the "macro-routing" (getting from Point A to Point B) while staying fully compatible with standard transit data consumers.

---

### 🛠️ Verification: Your New Endpoint Map

With this setup, your API structure for Phase 1 is now organized as follows:

| Resource | Versioned Endpoint | Purpose |
| --- | --- | --- |
| **Origins** | `/api/v1/journey/areas/` | Driver selects Origin (GeoNames) |
| **Destinations** | `/api/v1/journey/stops/` | Driver selects Destination (NSCC Campus) |
| **Search** | `/api/v1/journey/trips/` | Rider searches for available carpools |
| **Booking** | `/api/v1/journey/requests/` | Rider requests a seat / Driver accepts |
| **Profiles** | `/api/v1/journey/agencies/` | Management of Driver/Agency details |

