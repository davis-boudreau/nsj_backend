The updated **Authentication & Identity** section now reflects the full token lifecycle required for a seamless mobile and web experience. By including `refresh` and `verify` endpoints, you ensure that students stay logged in during their commute without the friction of constant re-authentication.

---

## 🔐 1. Authentication & Identity

*Managed via Django REST Framework + SimpleJWT.*

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/api/v1/auth/register/` | **User Creation**: Initializes a `User` and a blank `stn_user_profile`. |
| **POST** | `/api/v1/auth/login/` | **Token Issue**: Validates credentials and returns Access + Refresh tokens. |
| **POST** | `/api/v1/auth/token/refresh/` | **Token Rotation**: Provides a new Access token using a valid Refresh token. |
| **POST** | `/api/v1/auth/token/verify/` | **Session Check**: Confirms if a token is still active (used on app startup). |
| **POST** | `/api/v1/auth/logout/` | **Revocation**: Blacklists the Refresh token to prevent further access. |

---

### **Why Full Token lifestyle matter for stn_api:**

* **Continuous UX:** In a transit app, you don't want a session to expire while a rider is waiting at a stop (like **CBOUN**) looking for their driver. The `/refresh/` endpoint allows the app to stay active in the background.
* **Security & Safety:** If a student loses their phone, the `/logout/` (blacklist) endpoint ensures their account can be immediately secured, protecting their "Driver" or "Rider" status from unauthorized use.
* **Efficiency:** The `/verify/` endpoint is a "lightweight" call. The frontend can check if the user is still logged in without having to pull full profile data, making the app feel faster and more responsive.
