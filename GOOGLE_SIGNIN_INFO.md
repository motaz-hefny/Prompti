# Google Sign-In Information

## Current Status: MOCK/PLACEHOLDER ONLY

The "Sign In with Google" button in Prompti is currently **non-functional** and serves as a **visual placeholder** for future implementation.

### What It Does Now:
- ✅ Displays a button with Google branding
- ✅ Shows proper styling and positioning
- ❌ Does NOT authenticate users
- ❌ Does NOT connect to Google OAuth
- ❌ Does NOT save data to Google Drive

### Why It's a Placeholder:
This was intentional based on the original requirements document, which specified:
> "Mock 'Sign In with Google' button (placeholder for future Google OAuth integration)"

### Current App Functionality:
The app works perfectly **without** authentication:
- All data is stored in browser sessionStorage
- No user accounts needed
- No cloud storage
- Works offline after initial load
- Privacy-friendly (no data leaves your browser except AI API calls)

---

## How to Implement Real Google Sign-In

If you want to add real Google authentication, here's what you need to do:

### Step 1: Set Up Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure OAuth consent screen:
   - App name: Prompti
   - User support email: your email
   - Developer contact: your email
6. Create OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized JavaScript origins: 
     - `http://localhost:5173` (for development)
     - `https://your-domain.com` (for production)
   - Authorized redirect URIs:
     - `http://localhost:5173`
     - `https://your-domain.com`
7. Copy the Client ID

### Step 2: Install Required Package

```bash
npm install @react-oauth/google
```

### Step 3: Add Client ID to Environment

Update `.env`:
```env
VITE_GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
```

### Step 4: Wrap App with GoogleOAuthProvider

Update `src/main.tsx`:
```tsx
import { GoogleOAuthProvider } from '@react-oauth/google';

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={clientId}>
      <App />
    </GoogleOAuthProvider>
  </React.StrictMode>
);
```

### Step 5: Update PromptiSidebar Component

Replace the mock button in `src/components/prompti/PromptiSidebar.tsx`:

```tsx
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';

// Replace the current button with:
<GoogleLogin
  onSuccess={(credentialResponse) => {
    const decoded = jwtDecode(credentialResponse.credential);
    console.log('User info:', decoded);
    // Store user info in state
    // Update UI to show logged-in state
  }}
  onError={() => {
    console.log('Login Failed');
  }}
  useOneTap
/>
```

### Step 6: Add User State Management

Create a user context or use existing state:
```tsx
interface User {
  name: string;
  email: string;
  picture: string;
}

const [user, setUser] = useState<User | null>(null);
```

### Step 7: Implement Sign Out

```tsx
import { googleLogout } from '@react-oauth/google';

const handleSignOut = () => {
  googleLogout();
  setUser(null);
  // Clear user data
};
```

---

## Google Drive Integration (Future Feature)

To implement "Save to Drive" functionality:

### Step 1: Enable Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Google Drive API"
3. Add Drive scope to OAuth consent screen

### Step 2: Install Google API Client

```bash
npm install gapi-script
```

### Step 3: Request Drive Permissions

Update OAuth scopes:
```tsx
<GoogleLogin
  scope="https://www.googleapis.com/auth/drive.file"
  // ... other props
/>
```

### Step 4: Implement Save to Drive

```tsx
const saveToGoogleDrive = async (content: string, filename: string) => {
  const accessToken = // get from OAuth response
  
  const file = new Blob([content], { type: 'text/plain' });
  const metadata = {
    name: filename,
    mimeType: 'text/plain',
  };

  const form = new FormData();
  form.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
  form.append('file', file);

  const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: form,
  });

  return response.json();
};
```

---

## Alternative: Backend Authentication

For production apps, consider implementing authentication with a backend:

### Option 1: Supabase Auth
- Built-in Google OAuth
- User management
- Database integration
- Free tier available

### Option 2: Firebase Auth
- Google's authentication service
- Easy Google Sign-In integration
- Firestore for data storage
- Free tier available

### Option 3: Auth0
- Enterprise-grade authentication
- Multiple providers
- Easy integration
- Free tier available

---

## Current Recommendation

**For now, keep the mock button** because:
1. The app works perfectly without authentication
2. Adding real auth requires backend infrastructure
3. It's clearly marked as a placeholder
4. Users understand it's a future feature

**When to implement real auth:**
1. When you need to save user data in the cloud
2. When you want to sync across devices
3. When you need to share prompts with others
4. When you want to track usage per user

---

## Privacy Considerations

### Current (No Auth):
- ✅ No user data collected
- ✅ No tracking
- ✅ Works offline
- ✅ Privacy-friendly
- ❌ No cross-device sync
- ❌ Data lost if browser cache cleared

### With Google Auth:
- ✅ Cross-device sync
- ✅ Data backup
- ✅ Persistent storage
- ❌ User data sent to Google
- ❌ Requires privacy policy
- ❌ GDPR compliance needed

---

## Summary

**Current Status**: Mock button only, no real authentication

**To Implement**: Follow steps above or use authentication service

**Recommendation**: Keep as-is unless you need cloud features

**Timeline**: 2-4 hours to implement basic Google Sign-In

**Cost**: Free (Google OAuth is free)

---

For questions or help implementing authentication, refer to:
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [@react-oauth/google Documentation](https://www.npmjs.com/package/@react-oauth/google)
- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
