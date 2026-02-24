---
inclusion: auto
name: external-api-oauth2
description: External API OAuth 2.0 integration with Authorization Code Grant and PKCE. Third-party APIs like Lightspeed, Stripe, etc. Use when implementing OAuth2 authentication for external/third-party APIs (NOT for FSM/Landmark APIs - see file 06 for FSM).
---

# External API OAuth 2.0 Integration Guide for IPA

## Table of Contents

- [AI Assistant Instructions](#ai-assistant-instructions)
- [Overview](#overview)
- [OAuth 2.0 Flow Overview](#oauth-20-flow-overview)
- [Prerequisites](#prerequisites)
- [Testing Phase (Postman)](#testing-phase-postman)
  - [Step 1: Generate PKCE Values](#step-1-generate-pkce-values)
  - [Step 2: Build Authorization URL](#step-2-build-authorization-url)
  - [Step 3: Get Authorization Code](#step-3-get-authorization-code)
  - [Step 4: Exchange Code for Tokens](#step-4-exchange-code-for-tokens-postman)
  - [Step 5: Test API Call](#step-5-test-api-call-postman)
  - [Step 6: Test Refresh Token](#step-6-test-refresh-token-postman)
- [IPA Implementation](#ipa-implementation)
  - [FSM Configuration Variables](#fsm-configuration-variables)
  - [IPA Process Flow](#ipa-process-flow)
  - [WEBRN Node Configuration](#webrn-node-configuration-refresh-token)
  - [Error Handling Patterns](#error-handling-patterns)
- [Security Best Practices](#security-best-practices)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Production Deployment Checklist](#production-deployment-checklist)
- [API Provider-Specific Notes](#api-provider-specific-notes)
- [Quick Reference](#quick-reference)
- [Glossary](#glossary)

## AI Assistant Instructions

**When to Load This File:**

- User mentions: "OAuth", "OAuth2" for **external/third-party APIs**
- User asks about: Lightspeed API, Stripe API, external service integration
- User working with: WEBRN nodes calling **external APIs** (NOT FSM/Landmark)

**NOT for FSM APIs:** If user is working with FSM/Landmark/ION APIs, refer to `06_FSM_Business_Classes_and_API.md` instead.

**Your Role:**

- Guide user through OAuth 2.0 implementation in IPA
- Generate PowerShell scripts for PKCE generation
- Provide IPA process flow patterns for token management
- Help troubleshoot OAuth errors (invalid_grant, invalid_client, 401, etc.)
- Ensure security best practices (encryption, no logging of tokens)

**Critical Rules:**

- NEVER log or display actual tokens (access_token, refresh_token, client_secret)
- ALWAYS use ES5 JavaScript syntax for IPA code (no let/const/arrow functions)
- ALWAYS encrypt sensitive credentials in FSM config variables
- ALWAYS implement token expiry checking (refresh 5 minutes before expiry)
- ALWAYS handle 401 errors by clearing token and retrying

**Implementation Approach:**

1. Start with Postman testing to validate OAuth flow before IPA implementation
2. Generate PKCE values using PowerShell (provide script)
3. Walk through authorization URL construction with actual parameters
4. Test token exchange and refresh in Postman first
5. Only after successful Postman testing, implement in IPA
6. Use WEBRN nodes for all HTTP calls (token refresh and API calls)
7. Implement proper error handling for 401, 429, and network errors

## Overview

OAuth 2.0 Authorization Code Grant flow with PKCE for **external third-party API** integrations in IPA.

**Important:** This guide is for **external APIs only** (Lightspeed, Stripe, etc.). For FSM/Landmark/ION APIs, see `06_FSM_Business_Classes_and_API.md`.

**Use Cases:**

- Lightspeed Retail POS API integration
- Any third-party API requiring OAuth 2.0 authentication
- Secure API access without storing user passwords

**Key Concepts:**

- **Authorization Code Grant:** Three-way handshake between your app, user, and API provider
- **PKCE (Proof Key for Code Exchange):** Security extension to prevent authorization code interception
- **Access Token:** Short-lived token (typically 1 hour) for API calls
- **Refresh Token:** Long-lived token to get new access tokens without user re-authorization

## OAuth 2.0 Flow Overview

**Three Main Steps:**

```text
1. Authorization (One-time, User Action)
   User → Authorize App → Get Authorization Code (60 seconds validity)

2. Token Exchange (Automated)
   Authorization Code → Access Token + Refresh Token

3. API Access (Automated, Repeatable)
   Access Token → API Call → Data
   (When expired: Refresh Token → New Access Token)
```

## Prerequisites

**Before starting OAuth integration, obtain from API provider:**

- Client ID (public identifier for your app)
- Client Secret (private key - keep secure!)
- Redirect URI (where authorization code is sent)
- Scopes (permissions your app needs)
- Account ID (if required by API)
- API Documentation (endpoints, data formats)

**Example (Lightspeed):**

```text
Client ID: f7b49b63f8a47a7777aa8c0bc3fe3ba4f275c8ad29b4e85ce3ebf0ba3c379a62
Client Secret: b5dc606d1137eec38ea98cfd9021d141e94396117f9596265c9fb85e477d86fa
Redirect URI: https://mingle-portal.inforcloudsuite.com/TENANT/token
Scope: employee:all
Account ID: 313281
```

## Testing Phase (Postman)

### Step 1: Generate PKCE Values

**PowerShell Script:**

```powershell
# Generate code_verifier (random 64-character string)
$code_verifier = -join ((48..57) + (65..90) + (97..122) + @(45, 95) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# Generate code_challenge (SHA256 hash, base64url encoded)
$bytes = [System.Text.Encoding]::UTF8.GetBytes($code_verifier)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$hash = $sha256.ComputeHash($bytes)
$base64 = [Convert]::ToBase64String($hash)
$code_challenge = $base64.TrimEnd('=').Replace('+', '-').Replace('/', '_')

Write-Host "code_verifier: $code_verifier"
Write-Host "code_challenge: $code_challenge"
```

**Save both values!** You'll need them in subsequent steps.

### Step 2: Build Authorization URL

**URL Format:**

```text
https://PROVIDER_AUTH_URL/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=SCOPE&state=RANDOM_STRING&code_challenge=CODE_CHALLENGE&code_challenge_method=S256
```

**Example (Lightspeed):**

```text
https://cloud.lightspeedapp.com/auth/oauth/authorize?response_type=code&client_id=f7b49b63f8a47a7777aa8c0bc3fe3ba4f275c8ad29b4e85ce3ebf0ba3c379a62&redirect_uri=https%3A%2F%2Fmingle-portal.inforcloudsuite.com%2FROSENUAT_TST%2Ftoken&scope=employee:all&state=test123&code_challenge=uRY_PfDzKQNyBLB6-CZhOgDdgMqy0W8_IYn2ehGQekU&code_challenge_method=S256
```

**Parameters:**

- `response_type=code` - Request authorization code
- `client_id` - Your app's client ID
- `redirect_uri` - URL-encoded redirect URI
- `scope` - Permissions (space-separated if multiple)
- `state` - Random string for security (prevents CSRF attacks)
- `code_challenge` - Generated PKCE challenge
- `code_challenge_method=S256` - SHA256 hashing method

### Step 3: Get Authorization Code

**Process:**

1. **Paste URL in browser**
2. **Log in** with API provider account
3. **Authorize** the application
4. **Browser redirects** to: `https://redirect-uri?code=AUTHORIZATION_CODE&state=test123`
5. **Copy the code** (you have 60 seconds!)

**⏱️ Time Sensitivity:** Authorization codes expire in 60 seconds. Have Postman ready before starting.

### Step 4: Exchange Code for Tokens (Postman)

**Request:**

```http
Method: POST
URL: https://PROVIDER_TOKEN_URL/token
Content-Type: application/x-www-form-urlencoded
```

**Body:**

| Key              | Value                                  |
|------------------|----------------------------------------|
| `client_id`      | Your client ID                         |
| `client_secret`  | Your client secret                     |
| `code`           | Authorization code from Step 3         |
| `grant_type`     | `authorization_code`                   |
| `code_verifier`  | Code verifier from Step 1              |
| `redirect_uri`   | Same redirect URI used in authorization URL |

**Example (Lightspeed):**

```http
POST https://cloud.lightspeedapp.com/auth/oauth/token

Body:
client_id=f7b49b63f8a47a7777aa8c0bc3fe3ba4f275c8ad29b4e85ce3ebf0ba3c379a62
client_secret=b5dc606d1137eec38ea98cfd9021d141e94396117f9596265c9fb85e477d86fa
code=def502007de31470ea99de43b25a9ca42a790f5c...
grant_type=authorization_code
code_verifier=m8iJZxAJMOskabcj47edIUozyNFR5GWPE3Tw...
redirect_uri=https://mingle-portal.inforcloudsuite.com/ROSENUAT_TST/token
```

**Response:**

```json
{
  "token_type": "Bearer",
  "expires_in": 3600,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiI...",
  "refresh_token": "def50200eaa89f99c6b70e6df1fdc37e..."
}
```

**Save the refresh_token!** This is the most important value for IPA automation.

### Step 5: Test API Call (Postman)

**Request:**

```http
Method: GET (or POST/PUT depending on API)
URL: https://API_BASE_URL/endpoint
```

**Headers:**

| Key              | Value                      |
|------------------|----------------------------|
| `Authorization`  | `Bearer ACCESS_TOKEN`      |
| `Content-Type`   | `application/json`         |

**Example (Lightspeed - Get Employees):**

```http
GET https://api.lightspeedapp.com/API/V3/Account/313281/Employee.json

Headers:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiI...
Content-Type: application/json
```

**Response:**

```json
{
  "Employee": {
    "employeeID": "1",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

### Step 6: Test Refresh Token (Postman)

**Request:**

```http
Method: POST
URL: https://PROVIDER_TOKEN_URL/token
Content-Type: application/x-www-form-urlencoded
```

**Body:**

| Key              | Value                      |
|------------------|----------------------------|
| `client_id`      | Your client ID             |
| `client_secret`  | Your client secret         |
| `refresh_token`  | Refresh token from Step 4  |
| `grant_type`     | `refresh_token`            |

**Example (Lightspeed):**

```http
POST https://cloud.lightspeedapp.com/auth/oauth/token

Body:
client_id=f7b49b63f8a47a7777aa8c0bc3fe3ba4f275c8ad29b4e85ce3ebf0ba3c379a62
client_secret=b5dc606d1137eec38ea98cfd9021d141e94396117f9596265c9fb85e477d86fa
refresh_token=def50200eaa89f99c6b70e6df1fdc37e...
grant_type=refresh_token
```

**Response:**

```json
{
  "token_type": "Bearer",
  "expires_in": 3600,
  "access_token": "NEW_ACCESS_TOKEN",
  "refresh_token": "NEW_REFRESH_TOKEN"
}
```

**Note:** Some providers issue a new refresh_token with each refresh. Always update your stored refresh_token.

## IPA Implementation

### FSM Configuration Variables

**Create encrypted config variables in FSM:**

```javascript
// Public credentials (can be stored unencrypted)
var v_OAuth_ClientId = "f7b49b63f8a47a7777aa8c0bc3fe3ba4f275c8ad29b4e85ce3ebf0ba3c379a62";
var v_OAuth_AccountId = "313281";
var v_OAuth_Scope = "employee:all";

// Sensitive credentials (MUST be encrypted in FSM)
var v_OAuth_ClientSecret = "b5dc606d1137eec38ea98cfd9021d141e94396117f9596265c9fb85e477d86fa";
var v_OAuth_RefreshToken = "def50200eaa89f99c6b70e6df1fdc37e...";

// API endpoints
var v_OAuth_TokenURL = "https://cloud.lightspeedapp.com/auth/oauth/token";
var v_OAuth_ApiBaseURL = "https://api.lightspeedapp.com/API/V3/Account/313281/";

// Runtime variables (in process, not config)
var v_OAuth_AccessToken = "";
var v_OAuth_TokenExpiry = "";  // Timestamp when token expires
```

### IPA Process Flow

```text
START
  ↓
ASSGN: Initialize Variables
  - Load config variables
  - Check if access_token exists in process context
  ↓
BRANCH: Token Valid?
  Condition: v_OAuth_AccessToken != "" && v_OAuth_TokenExpiry > Date.now()
  ├─ YES → Skip to API Call
  └─ NO → Get New Token
      ↓
      WEBRN: Refresh Access Token
        URL: {v_OAuth_TokenURL}
        Method: POST
        Headers: Content-Type: application/x-www-form-urlencoded
        Body: 
          client_id={v_OAuth_ClientId}&
          client_secret={v_OAuth_ClientSecret}&
          refresh_token={v_OAuth_RefreshToken}&
          grant_type=refresh_token
        Response Variable: v_TokenResponse
      ↓
      ASSGN: Parse Token Response
        v_OAuth_AccessToken = v_TokenResponse.access_token
        v_OAuth_TokenExpiry = Date.now() + (v_TokenResponse.expires_in * 1000)
        // If new refresh_token provided, update config variable
        if (v_TokenResponse.refresh_token) {
          v_OAuth_RefreshToken = v_TokenResponse.refresh_token
        }
      ↓
      BRANCH: Token Refresh Success?
        Condition: v_OAuth_AccessToken != ""
        ├─ YES → Continue
        └─ NO → Error Handling
            ↓
            EMAIL: Notify Admin
            ↓
            END (Error)
  ↓
WEBRN: Call API
  URL: {v_OAuth_ApiBaseURL}Employee.json
  Method: GET
  Headers: 
    Authorization: Bearer {v_OAuth_AccessToken}
    Content-Type: application/json
  Response Variable: v_ApiResponse
  ↓
BRANCH: API Call Success?
  Condition: HTTP Status = 200
  ├─ YES → Process Data
  └─ NO → Error Handling
      ↓
      BRANCH: Token Expired? (HTTP 401)
        ├─ YES → Clear token, retry from top
        └─ NO → Log error, notify admin
  ↓
ASSGN: Process API Response
  - Parse JSON
  - Transform data
  - Validate data
  ↓
LM: Update FSM
  - Business class operations
  - Update records
  ↓
END (Success)
```

### WEBRN Node Configuration (Refresh Token)

**Activity Type:** WEBRN (Web Run)

**URL:** `{v_OAuth_TokenURL}`

**Method:** POST

**Headers:**

```text
Content-Type: application/x-www-form-urlencoded
```

**Body (URL-encoded):**

```text
client_id={v_OAuth_ClientId}&client_secret={v_OAuth_ClientSecret}&refresh_token={v_OAuth_RefreshToken}&grant_type=refresh_token
```

**Response Mapping:**

```javascript
// Parse JSON response
var response = JSON.parse(webRunResponse);
v_OAuth_AccessToken = response.access_token;
v_OAuth_TokenExpiry = new Date().getTime() + (response.expires_in * 1000);

// Update refresh token if provider issues new one
if (response.refresh_token) {
  v_OAuth_RefreshToken = response.refresh_token;
  // TODO: Update FSM config variable with new refresh token
}
```

### WEBRN Node Configuration (API Call)

**Activity Type:** WEBRN (Web Run)

**URL:** `{v_OAuth_ApiBaseURL}Employee.json`

**Method:** GET (or POST/PUT depending on operation)

**Headers:**

```text
Authorization: Bearer {v_OAuth_AccessToken}
Content-Type: application/json
```

**Body (if POST/PUT):**

```json
{
  "Employee": {
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

**Response Mapping:**

```javascript
// Parse JSON response
var response = JSON.parse(webRunResponse);

// Extract data
var employees = response.Employee;
if (!Array.isArray(employees)) {
  employees = [employees];  // Single employee, convert to array
}

// Process each employee
for (var i = 0; i < employees.length; i++) {
  var emp = employees[i];
  v_EmployeeId = emp.employeeID;
  v_FirstName = emp.firstName;
  v_LastName = emp.lastName;
  // ... map other fields
}
```

### Error Handling Patterns

**Token Refresh Failure:**

```javascript
BRANCH: Token Refresh Failed?
  Condition: v_OAuth_AccessToken == "" || errorCode != 0
  ├─ YES → 
      ASSGN: Log Error
        v_ErrorMessage = "OAuth token refresh failed: " + errorMessage
      ↓
      EMAIL: Notify Admin
        To: admin@company.com
        Subject: OAuth Integration Error
        Body: {v_ErrorMessage}
      ↓
      END (Error)
  └─ NO → Continue
```

**API Call Failure:**

```javascript
BRANCH: API Call Failed?
  Condition: httpStatusCode != 200
  ├─ YES →
      BRANCH: Token Expired? (401 Unauthorized)
        ├─ YES →
            ASSGN: Clear Token
              v_OAuth_AccessToken = ""
              v_OAuth_TokenExpiry = ""
            ↓
            GOTO: Token Refresh (retry)
        └─ NO →
            ASSGN: Log Error
              v_ErrorMessage = "API call failed: HTTP " + httpStatusCode
            ↓
            EMAIL: Notify Admin
            ↓
            END (Error)
  └─ NO → Continue
```

**Rate Limiting (429 Too Many Requests):**

```javascript
BRANCH: Rate Limited?
  Condition: httpStatusCode == 429
  ├─ YES →
      ASSGN: Get Retry-After Header
        v_RetryAfter = responseHeaders["Retry-After"]  // Seconds
      ↓
      WAIT: Delay
        Duration: {v_RetryAfter} seconds
      ↓
      GOTO: API Call (retry)
  └─ NO → Continue
```

## Security Best Practices

### 1. Encrypt Sensitive Data

**CRITICAL:** Always encrypt these values in FSM:

- Client Secret
- Refresh Token
- Access Token (if stored)

**FSM Encryption:**

- Use FSM's built-in encryption for config variables
- Never store plaintext credentials in LPD files
- Never log sensitive values

### 2. Token Storage

**DO:**

- ✅ Store refresh_token in encrypted FSM config variable
- ✅ Store access_token in process context (runtime only)
- ✅ Clear access_token after process completes (if not needed)

**DON'T:**

- ❌ Store access_token in database (short-lived, security risk)
- ❌ Store tokens in plain text
- ❌ Share tokens between processes (each process should manage its own)

### 3. Token Expiry Management

**Best Practice:** Refresh token 5 minutes before expiry

```javascript
// Check if token expires in less than 5 minutes
var expiryBuffer = 5 * 60 * 1000;  // 5 minutes in milliseconds
var needsRefresh = (v_OAuth_TokenExpiry - Date.now()) < expiryBuffer;

if (needsRefresh) {
  // Refresh token proactively
}
```

### 4. Error Logging

**DO:**

- ✅ Log error messages (without sensitive data)
- ✅ Log HTTP status codes
- ✅ Log timestamps for troubleshooting

**DON'T:**

- ❌ Log access tokens
- ❌ Log refresh tokens
- ❌ Log client secrets
- ❌ Log full API responses (may contain sensitive data)

**Example:**

```javascript
// GOOD
v_LogMessage = "API call failed: HTTP 401 at " + new Date().toISOString();

// BAD
v_LogMessage = "API call failed with token: " + v_OAuth_AccessToken;
```

## Common Issues and Solutions

### Issue 1: "invalid_grant" Error

**Symptoms:** Token exchange fails with "invalid_grant"

**Causes:**

- Authorization code expired (> 60 seconds)
- Authorization code already used
- Wrong code_verifier
- Redirect URI mismatch

**Solution:**

- Get fresh authorization code
- Ensure code_verifier matches code_challenge
- Verify redirect_uri exactly matches registered URI

### Issue 2: "invalid_client" Error

**Symptoms:** Token request fails with "invalid_client"

**Causes:**

- Wrong client_id or client_secret
- Client not active/registered
- Client blocked by provider

**Solution:**

- Verify credentials with API provider
- Check client status in provider's developer portal
- Ensure client_id and client_secret are correct

### Issue 3: Redirect URI Triggers SSO Loop

**Symptoms:** After authorization, redirected to another login screen

**Causes:**

- Redirect URI requires authentication
- Redirect URI not publicly accessible
- Redirect URI misconfigured

**Solution:**

- Use public endpoint that doesn't require authentication
- For testing: Use localhost or provider's test callback URL
- For production: Create public IPA endpoint to receive code

### Issue 4: Token Refresh Returns New Refresh Token

**Symptoms:** Refresh token stops working after first use

**Causes:**

- Provider issues new refresh_token with each refresh
- Old refresh_token invalidated after use

**Solution:**

- Always check if response includes new refresh_token
- Update stored refresh_token after each refresh
- Implement logic to update FSM config variable

```javascript
if (response.refresh_token && response.refresh_token != v_OAuth_RefreshToken) {
  v_OAuth_RefreshToken = response.refresh_token;
  // Update FSM config variable (requires LM call or API)
}
```

### Issue 5: 401 Unauthorized on API Call

**Symptoms:** API call fails with HTTP 401

**Causes:**

- Access token expired
- Access token invalid
- Insufficient permissions (scope)

**Solution:**

- Clear access_token and retry (triggers refresh)
- Verify scope includes required permissions
- Check token expiry timestamp

## Production Deployment Checklist

### Pre-Deployment

- [ ] Test complete OAuth flow in Postman
- [ ] Test refresh token flow
- [ ] Test API calls with access token
- [ ] Verify error handling (expired token, rate limiting, network errors)
- [ ] Document API endpoints and data mappings
- [ ] Create encrypted FSM config variables
- [ ] Test IPA process in development environment

### Deployment

- [ ] Store refresh_token in encrypted FSM config variable
- [ ] Configure production API endpoints
- [ ] Set up monitoring/alerting for OAuth failures
- [ ] Document one-time authorization process for users
- [ ] Create runbook for token refresh failures
- [ ] Test end-to-end in production

### Post-Deployment

- [ ] Monitor API call success rates
- [ ] Monitor token refresh success rates
- [ ] Set up alerts for repeated failures
- [ ] Document troubleshooting procedures
- [ ] Schedule periodic token validation tests

## API Provider-Specific Notes

### Lightspeed Retail POS (R-Series)

**Authorization URL:** `https://cloud.lightspeedapp.com/auth/oauth/authorize`

**Token URL:** `https://cloud.lightspeedapp.com/auth/oauth/token`

**API Base URL:** `https://api.lightspeedapp.com/API/V3/Account/{accountID}/`

**Key Points:**

- Requires PKCE (code_challenge)
- Access token expires in 1 hour (3600 seconds)
- Refresh token issues new refresh_token on each use
- Rate limiting: Check API documentation
- Account ID required in API URLs

**Common Endpoints:**

- `GET /Employee.json` - List employees
- `POST /Employee.json` - Create employee
- `PUT /Employee/{id}.json` - Update employee
- `GET /Sale.json` - List sales
- `GET /Item.json` - List inventory items

**Scopes:**

- `employee:all` - Full employee access
- `employee:read` - Read-only employee access
- Check documentation for other scopes

## Additional Resources

**OAuth 2.0 Specification:**

- [RFC 6749: OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749)
- [RFC 7636: PKCE Extension](https://tools.ietf.org/html/rfc7636)

**Testing Tools:**

- [Postman](https://www.postman.com/)
- [OAuth 2.0 Playground](https://www.oauth.com/playground/)
- [PKCE Code Generator](https://developer.pingidentity.com/en/tools/pkce-code-generator.html)

**IPA Documentation:**

- Steering File 01: IPA and IPD Complete Guide
- Steering File 02: Work Unit Analysis
- Steering File 06: FSM Business Classes and API

## Quick Reference

### OAuth 2.0 Flow Summary

| Step | Action | Duration | Output |
|------|--------|----------|--------|
| 1. Generate PKCE | Run PowerShell script | Instant | code_verifier, code_challenge |
| 2. Authorization | User authorizes in browser | Manual | Authorization code (60s validity) |
| 3. Token Exchange | POST to token endpoint | < 1s | access_token, refresh_token |
| 4. API Call | GET/POST with Bearer token | < 1s | API data |
| 5. Token Refresh | POST with refresh_token | < 1s | New access_token |

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 401 | Unauthorized | Clear token, refresh, retry |
| 403 | Forbidden | Check scopes/permissions |
| 429 | Rate Limited | Wait (Retry-After header), retry |
| 500 | Server Error | Log error, notify admin |

### IPA Variable Naming Convention

| Variable Type | Naming Pattern | Example |
|---------------|----------------|---------|
| Config (Public) | `v_OAuth_ClientId` | Client ID, Account ID |
| Config (Encrypted) | `v_OAuth_ClientSecret` | Client Secret, Refresh Token |
| Runtime | `v_OAuth_AccessToken` | Access Token, Token Expiry |
| Response | `v_TokenResponse` | API responses |
| Error | `v_ErrorMessage` | Error messages |

## Glossary

**Access Token:** Short-lived token (typically 1 hour) used to authenticate API requests. Sent in Authorization header as "Bearer {token}".

**Authorization Code:** Temporary code (60 seconds validity) exchanged for access and refresh tokens. Obtained after user authorizes app.

**Client ID:** Public identifier for your application. Safe to expose in URLs and logs.

**Client Secret:** Private key for your application. MUST be kept secure and encrypted.

**Code Challenge:** SHA256 hash of code_verifier, sent in authorization request. Part of PKCE flow.

**Code Verifier:** Random string (43-128 characters) used in PKCE flow. Sent when exchanging authorization code for tokens.

**Grant Type:** OAuth flow type. "authorization_code" for initial token exchange, "refresh_token" for token refresh.

**PKCE (Proof Key for Code Exchange):** Security extension to OAuth 2.0 that prevents authorization code interception attacks.

**Redirect URI:** URL where authorization code is sent after user authorizes app. Must match registered URI exactly.

**Refresh Token:** Long-lived token used to obtain new access tokens without user re-authorization. Store securely.

**Scope:** Permissions your app requests. Space-separated list (e.g., "employee:all sale:read").

**State:** Random string sent in authorization request and returned in redirect. Used to prevent CSRF attacks.

**Last Updated:** 2026-02-08

**Maintained By:** Kiro AI Assistant

**Related Files:** 01_IPA_and_IPD_Complete_Guide.md, 06_FSM_Business_Classes_and_API.md
