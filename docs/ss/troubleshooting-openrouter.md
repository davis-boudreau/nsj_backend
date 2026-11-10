The error **"403 Client Error: Forbidden for URL"** from OpenRouteService suggests one of the following issues:  

### **Possible Causes & Fixes**
#### **1. Invalid API Key**
- The most common reason is that your API key is incorrect or has expired.
- **Fix**: Check your API key by running the following in your Django shell:
  ```python
  from decouple import config
  print(config('OPENROUTESERVICE_API_KEY'))
  ```
  - Ensure it matches the key in your OpenRouteService account.

#### **2. API Key Not Authorized for Routing**
- OpenRouteService keys have **access restrictions** (e.g., only allowing certain services).
- **Fix**: 
  - Log into [OpenRouteService](https://openrouteservice.org/) → Check your API key settings.
  - Ensure that **"Directions Service"** is enabled.

#### **3. Incorrect Request Method**
- OpenRouteService **directions API** expects a **GET request** for route calculations.  
- Your code is using:
  ```python
  response = requests.post(url, headers=headers, json=params)  # Change to GET
  ```
- **Fix**: Change it back to `requests.get(...)`:
  ```python
  response = requests.get(url, headers=headers, params=params)
  ```

#### **4. Incorrect API URL**
- Ensure your API URL is correct:
  ```python
  print(config('OPENROUTESERVICE_DIRECTIONS_URL'))
  ```
- The expected URL for car routing is:
  ```
  https://api.openrouteservice.org/v2/directions/driving-car/geojson
  ```
- **Fix**: If `config('OPENROUTESERVICE_DIRECTIONS_URL')` is wrong, update your `.env` file:
  ```
  OPENROUTESERVICE_DIRECTIONS_URL=https://api.openrouteservice.org/v2/directions/driving-car/geojson
  ```

#### **5. Rate Limit Exceeded**
- Free-tier accounts on OpenRouteService have **daily limits**.
- **Fix**: Log into OpenRouteService → Check your usage statistics.
- If you’ve exceeded limits, either:
  - Wait for the reset.
  - Upgrade your plan.

---

### **Recommended Debugging Steps**
1. **Test API Key Manually**  
   Run this in **Postman** or terminal:
   ```sh
   curl -X GET "https://api.openrouteservice.org/v2/directions/driving-car?api_key=YOUR_API_KEY&start=-61.991581,45.622765&end=-61.3696801,45.6270521"
   ```
   If you get `403 Forbidden`, the issue is with your key.

2. **Enable Debugging in Django**  
   Modify your `get_directions_openrouter` method:
   ```python
   logger.debug(f"API Key: {api_key[:5]}*****")
   logger.debug(f"API URL: {url}")
   ```
   Then check Django logs.

3. **Retry With a New API Key**
   - If the key looks correct, generate a **new one** from OpenRouteService.

Try these steps and let me know if the issue persists! 🚀