# Frontend Structure (Phase 1)

## Overview

The frontend is a **Next.js 16** React application that runs in the browser.

## What is Next.js?

- React framework for building web applications
- Built-in routing (App Router)
- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes (optional)
- Automatic optimization (images, code splitting)

## Frontend Request Flow

```
User Action (click button)
    ↓
React Component event handler
    ↓
API call using fetch/SWR
    ↓
GET /api/v1/products
    ↓
Backend processes request
    ↓
Backend returns JSON
    ↓
Frontend receives JSON
    ↓
Update React state (SWR/Zustand)
    ↓
Component re-renders
    ↓
User sees updated UI
```

## Folder Structure

### app/
**Next.js App Router pages and layouts**

```
app/
├── layout.tsx                 # Root layout (wraps all pages)
├── page.tsx                   # Home page (/)
├── globals.css                # Global styles
│
├── (auth)/                    # Route group for auth pages
│   ├── login/
│   │   └── page.tsx           # /login
│   ├── register/
│   │   └── page.tsx           # /register
│   └── layout.tsx             # Auth-specific layout
│
├── (store)/                   # Route group for shopping
│   ├── products/
│   │   ├── page.tsx           # /products (list all)
│   │   └── [id]/
│   │       └── page.tsx       # /products/[id] (detail page)
│   ├── cart/
│   │   └── page.tsx           # /cart
│   ├── checkout/
│   │   └── page.tsx           # /checkout
│   └── layout.tsx             # Store-specific layout
│
├── (dashboard)/               # Route group for user dashboard
│   ├── profile/
│   │   └── page.tsx           # /profile
│   ├── orders/
│   │   ├── page.tsx           # /orders (list)
│   │   └── [id]/
│   │       └── page.tsx       # /orders/[id] (detail)
│   ├── wishlist/
│   │   └── page.tsx           # /wishlist
│   └── layout.tsx             # Dashboard layout
│
├── (admin)/                   # Route group for admin
│   ├── products/
│   │   ├── page.tsx           # /admin/products
│   │   └── [id]/
│   │       └── page.tsx       # /admin/products/[id]
│   ├── orders/
│   │   └── page.tsx           # /admin/orders
│   ├── analytics/
│   │   └── page.tsx           # /admin/analytics
│   └── layout.tsx             # Admin layout with auth check
```

**Route Groups Explained:**
- `(auth)` - Pages in parentheses are route groups
- Route groups DON'T appear in URL
- Used to organize related pages with shared layouts
- `/login` is in `(auth)/login`, not `app/login`

### components/
**Reusable React components**

```
components/
├── auth/
│   ├── LoginForm.tsx          # Email + password form
│   └── RegisterForm.tsx       # Registration form
│
├── product/
│   ├── ProductCard.tsx        # Single product card
│   ├── ProductGrid.tsx        # Grid of products
│   └── ProductFilter.tsx      # Filter/search component
│
├── cart/
│   ├── CartItem.tsx           # Single cart item
│   └── CartSummary.tsx        # Total price, checkout button
│
├── layout/
│   ├── Header.tsx             # Navigation bar
│   ├── Footer.tsx             # Footer
│   └── Sidebar.tsx            # Navigation sidebar
│
└── common/
    ├── Button.tsx             # Reusable button
    ├── Input.tsx              # Reusable input field
    └── LoadingSpinner.tsx     # Loading animation
```

### hooks/
**Custom React hooks**

```
hooks/
├── useAuth.ts                 # Authentication state
├── useProducts.ts             # Fetch products
├── useCart.ts                 # Shopping cart state
└── useFetch.ts                # Generic data fetching
```

**What are hooks?**
- Functions that use React state/effects
- Reusable logic
- Called from components

Example:
```typescript
// hook: useProducts.ts
function useProducts() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    fetch('/api/v1/products')
      .then(res => res.json())
      .then(data => setProducts(data))
  }, [])
  
  return { products, loading }
}

// usage in component:
function ProductPage() {
  const { products, loading } = useProducts()
  return <div>{products.map(p => <div>{p.name}</div>)}</div>
}
```

### lib/
**Utility functions and configuration**

```
lib/
├── api-client.ts              # HTTP client for backend
├── constants.ts               # API URLs, app constants
├── types.ts                   # TypeScript type definitions
├── validation.ts              # Zod validation schemas
└── utils.ts                   # Helper functions
```

**api-client.ts:**
- Wraps fetch() to call backend
- Adds Authorization header with JWT token
- Handles errors consistently

Example:
```typescript
async function fetchProducts() {
  const response = await apiClient.get('/api/v1/products')
  return response.data
}
```

### stores/
**Global state management (Zustand)**

```
stores/
├── auth-store.ts              # Login state, user info, tokens
├── cart-store.ts              # Items in cart
└── ui-store.ts                # Theme, sidebar open/close
```

**Why Zustand?**
- Lightweight state management
- Alternative to Redux, Context API
- Easy to use

Example:
```typescript
// auth-store.ts
export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  login: (email, password) => {
    // API call
    set({ user, token })
  },
  logout: () => set({ user: null, token: null })
}))

// Usage in component:
function Header() {
  const { user, logout } = useAuthStore()
  return <div>{user.name} <button onClick={logout}>Logout</button></div>
}
```

### public/
**Static assets (images, icons, fonts)**

```
public/
├── images/
│   ├── logo.png
│   ├── hero.jpg
│   └── products/
│       └── product-1.jpg
│
├── icons/
│   ├── search.svg
│   ├── cart.svg
│   └── user.svg
│
└── fonts/
    └── inter.ttf
```

## Key Frontend Concepts

### Next.js App Router
- File-based routing
- `app/page.tsx` = `/`
- `app/products/page.tsx` = `/products`
- `app/products/[id]/page.tsx` = `/products/123`

### React Components
- Functions that return JSX
- Props = input parameters
- State = component memory
- Effects = side effects (API calls)

### SWR (Data Fetching)
- Fetches data with caching
- Automatic revalidation
- Handles loading/error states

Example:
```typescript
import useSWR from 'swr'

function ProductPage() {
  const { data: products, error, isLoading } = useSWR('/api/v1/products')
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>{products.map(p => <ProductCard product={p} />)}</div>
}
```

### Zustand (State Management)
- Global state accessible from any component
- No props drilling
- Similar to Redux but simpler

### TypeScript
- Adds type safety to JavaScript
- Catches errors at build time
- Better IDE autocomplete

## Frontend Communication with Backend

### 1. User Action
```typescript
function LoginPage() {
  const handleLogin = async (email, password) => {
    // Call backend
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    const data = await response.json()
    // Store token
    localStorage.setItem('token', data.access_token)
  }
}
```

### 2. Every Request Includes Token
```typescript
// lib/api-client.ts
async function get(url) {
  const token = localStorage.getItem('token')
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` }
  })
  return response.json()
}
```

### 3. Backend Verifies Token
```python
# backend/app/api/v1/products.py
@router.get("/products")
def get_products(request: Request):
    # Auth middleware already verified token
    user_id = request.user.id
    # Proceed with business logic
```

## Frontend Dependencies (package.json)

```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "zustand": "^4.4.0",
    "swr": "^2.2.0",
    "zod": "^3.22.0",
    "react-hook-form": "^7.48.0",
    "axios": "^1.6.0",
    "tailwindcss": "^4.3.0"
  }
}
```

## Next Steps

Phase 1 complete! Frontend structure created.

Phase 2: Implement authentication (login/register)
- Create LoginForm component
- Implement useAuth hook
- Connect to backend /api/v1/auth/login
