# PHASE 5: Next.js Frontend & UI Components - GUIDE

## Frontend Architecture Overview

### Tech Stack
- **Framework**: Next.js 16 (App Router)
- **Styling**: Tailwind CSS
- **State Management**: Zustand (global) + React hooks (local)
- **Forms**: React Hook Form + Zod validation
- **Data Fetching**: SWR for caching and sync
- **HTTP Client**: Axios with auth interceptor
- **Components**: shadcn/ui (Tailwind-based)
- **Icons**: Lucide React

### Project Structure

```
frontend/
├── app/
│   ├── layout.tsx                  # Root layout with providers
│   ├── page.tsx                    # Homepage with recommendations
│   ├── (auth)/                     # Auth route group
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   └── reset-password/page.tsx
│   ├── (shop)/                     # Shopping route group
│   │   ├── products/page.tsx       # Product listing/search
│   │   ├── products/[id]/page.tsx  # Product detail
│   │   ├── cart/page.tsx
│   │   ├── checkout/page.tsx
│   │   └── orders/page.tsx
│   ├── (user)/                     # User route group (protected)
│   │   ├── profile/page.tsx
│   │   ├── wishlist/page.tsx
│   │   └── orders/[id]/page.tsx
│   ├── (admin)/                    # Admin route group (protected)
│   │   ├── dashboard/page.tsx
│   │   ├── products/page.tsx
│   │   └── analytics/page.tsx
│   └── api/auth/                   # Optional: backend calls
├── components/
│   ├── layout/
│   │   ├── Header.tsx              # Navigation header
│   │   ├── Sidebar.tsx             # Sidebar (admin, mobile)
│   │   └── Footer.tsx
│   ├── product/
│   │   ├── ProductCard.tsx         # Product item display
│   │   ├── ProductGrid.tsx         # Grid layout
│   │   ├── ProductDetail.tsx       # Full product page
│   │   ├── ProductFilter.tsx       # Filter sidebar
│   │   └── SearchBar.tsx           # Product search
│   ├── cart/
│   │   ├── CartItem.tsx
│   │   ├── CartSummary.tsx
│   │   └── CartPage.tsx
│   ├── recommendations/
│   │   ├── RecommendationCarousel.tsx  # Horizontal carousel
│   │   ├── SimilarProducts.tsx         # "Similar products" section
│   │   └── TrendingProducts.tsx        # Trending section
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── SignupForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── ui/                         # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── loading-spinner.tsx
│   │   └── ... (other UI components)
│   └── common/
│       ├── Navbar.tsx
│       ├── ErrorBoundary.tsx
│       ├── LoadingState.tsx
│       └── ErrorState.tsx
├── hooks/
│   ├── useAuth.ts                  # Auth context hook
│   ├── useCart.ts                  # Cart state management
│   ├── useProducts.ts              # Products fetching
│   ├── useRecommendations.ts       # Recommendations fetching
│   └── useDebounce.ts              # Debounce hook
├── lib/
│   ├── api-client.ts               # Axios instance with auth
│   ├── auth.ts                     # Auth utilities
│   ├── validators.ts               # Zod schemas
│   └── constants.ts                # Constants
├── store/
│   ├── authStore.ts                # Zustand auth store
│   ├── cartStore.ts                # Zustand cart store
│   └── uiStore.ts                  # UI state (modals, etc.)
├── types/
│   ├── user.ts
│   ├── product.ts
│   ├── order.ts
│   ├── recommendation.ts
│   └── api.ts
├── styles/
│   ├── globals.css                 # Global Tailwind styles
│   └── variables.css               # CSS variables
├── middleware.ts                   # Next.js middleware (auth checks)
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## Key Components to Build

### 1. Authentication Components
**LoginForm.tsx**
- Email input
- Password input
- Remember me checkbox
- Login button
- Link to signup/forgot password
- Error messages
- Integration with /api/auth/login

**SignupForm.tsx**
- Email input with validation
- Password with strength indicator
- Confirm password
- Name fields
- Terms acceptance
- Phone (optional)
- Integration with /api/auth/register

### 2. Product Components
**ProductCard.tsx**
- Image
- Name and description
- Price (with discount if applicable)
- Rating and review count
- "Add to cart" button
- "Add to wishlist" button
- Hover effects

**ProductDetail.tsx**
- Large image gallery
- Product specs
- Price and stock status
- Rating and reviews
- "Add to cart" with quantity selector
- "Add to wishlist"
- Similar products section (recommendations)
- Reviews section

**ProductGrid.tsx**
- Responsive grid (mobile: 1 col, tablet: 2 cols, desktop: 3-4 cols)
- Product cards in grid
- Pagination or infinite scroll
- Loading states

### 3. Recommendation Components
**RecommendationCarousel.tsx**
- Horizontal scrollable list
- Product cards in carousel
- "Previous" / "Next" buttons
- "View all" link
- Used on homepage for "Recommended for You"

**SimilarProducts.tsx**
- Used on product detail page
- Shows 5-10 similar products
- Same carousel style

**TrendingProducts.tsx**
- Top trending items
- Updated daily
- Homepage section

### 4. Cart & Checkout
**CartItem.tsx**
- Product image
- Product name and price
- Quantity selector
- Remove button
- Subtotal

**CartSummary.tsx**
- Items count
- Subtotal
- Shipping (calculated)
- Tax (calculated)
- Total
- "Proceed to checkout" button

**CheckoutForm.tsx**
- Shipping address form
- Billing address same as shipping option
- Payment method selection
- Order review
- Place order button

### 5. Layout Components
**Header.tsx**
- Logo
- Search bar
- Category links
- Cart icon (with item count)
- User menu (login/profile/logout)
- Mobile hamburger menu

**Sidebar.tsx**
- Category filters
- Price range filter
- Rating filter
- Brand filter
- Apply/Clear filters

**Footer.tsx**
- Links (About, Contact, Privacy)
- Newsletter signup
- Social links
- Copyright

## State Management Strategy

### Zustand Stores

**authStore.ts** - User Authentication
```typescript
interface AuthStore {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  setUser: (user: User) => void;
  setTokens: (access: string, refresh: string) => void;
  logout: () => void;
  login: (email: string, password: string) => Promise<void>;
}
```

**cartStore.ts** - Shopping Cart
```typescript
interface CartStore {
  items: CartItem[];
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clear: () => void;
  getTotalPrice: () => number;
  getItemCount: () => number;
}
```

**uiStore.ts** - UI State
```typescript
interface UIStore {
  isMobileMenuOpen: boolean;
  isCartOpen: boolean;
  isFilterOpen: boolean;
  toggleMobileMenu: () => void;
  toggleCart: () => void;
  toggleFilter: () => void;
}
```

## API Integration

### Axios Client (lib/api-client.ts)
```typescript
import axios from 'axios';
import { authStore } from '@/store/authStore';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add auth token
apiClient.interceptors.request.use((config) => {
  const token = authStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Attempt token refresh
      const refreshToken = authStore.getState().refreshToken;
      // Call /api/auth/refresh
      // Update tokens in store
      // Retry original request
    }
    return Promise.reject(error);
  }
);
```

## Data Fetching with SWR

### useProducts Hook
```typescript
import useSWR from 'swr';

export function useProducts(page = 1, search = '') {
  const { data, error, isLoading } = useSWR(
    search ? `/api/products/search?q=${search}&page=${page}` : `/api/products?page=${page}`,
    fetcher,
    { revalidateOnFocus: false }
  );
  
  return {
    products: data?.data || [],
    isLoading,
    error,
    pagination: data?.pagination,
  };
}
```

### useRecommendations Hook
```typescript
export function useRecommendations(type: 'personalized' | 'trending' = 'personalized') {
  const { data, error, isLoading } = useSWR(
    `/api/recommendations?type=${type}`,
    fetcher,
    { revalidateOnFocus: false, dedupingInterval: 60000 }
  );
  
  return {
    recommendations: data?.data?.recommendations || [],
    isLoading,
    error,
  };
}
```

## Form Validation with Zod

### validators.ts
```typescript
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password required'),
});

export const signupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string()
    .min(8, 'Password must be 8+ chars')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain digit')
    .regex(/[!@#$%^&*]/, 'Must contain special char'),
  confirmPassword: z.string(),
  firstName: z.string().min(1, 'First name required'),
  lastName: z.string().min(1, 'Last name required'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type SignupFormData = z.infer<typeof signupSchema>;
```

## Environment Variables

**`.env.local`**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=E-Commerce Platform
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Responsive Design Strategy

Mobile-first approach with Tailwind breakpoints:
- **Mobile** (default): 1 column layouts
- **SM** (640px): Tablet layouts
- **MD** (768px): 2 columns
- **LG** (1024px): 3 columns
- **XL** (1280px): 4 columns

Example grid:
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {products.map(p => <ProductCard key={p.id} product={p} />)}
</div>
```

## Authentication Flow

1. User clicks "Login"
2. Navigates to /login page
3. Fills email/password
4. Calls POST /api/auth/login
5. Receives access_token and refresh_token
6. Store tokens in Zustand + httpOnly cookie
7. Redirect to homepage
8. Navbar updates to show user profile

Logout:
1. Click "Logout"
2. Clear tokens from store
3. Call POST /api/auth/logout (optional)
4. Redirect to /login

## Performance Optimizations

1. **Image Optimization**: Use Next.js Image component
   ```tsx
   import Image from 'next/image';
   <Image src={product.imageUrl} alt={product.name} width={300} height={300} />
   ```

2. **Code Splitting**: Automatic via Next.js App Router

3. **Caching**:
   - SWR for client-side caching with revalidation
   - Next.js server component caching
   - Static generation for frequently accessed pages

4. **Lazy Loading**: 
   - Dynamic imports for heavy components
   - Intersection Observer for images

5. **Bundle Size**:
   - Tree-shaking unused code
   - Analyze with `next/bundle-analyzer`

## Security Considerations

1. **CSRF Protection**: Use SameSite cookies
2. **XSS Prevention**: React auto-escapes JSX
3. **Auth Token Storage**: httpOnly cookies (not localStorage)
4. **Input Validation**: Zod schemas on frontend and backend
5. **API Rate Limiting**: Implement on backend
6. **Sensitive Data**: Never log tokens or passwords

## Build & Run

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Analyze bundle size
npm run analyze
```

## SEO Optimization

1. **Metadata**: Update layout.tsx with proper title, description
   ```tsx
   export const metadata = {
     title: 'E-Commerce Platform - AI Recommendations',
     description: 'Shop with AI-powered personalized recommendations',
     openGraph: { ... }
   };
   ```

2. **Structured Data**: Add schema.org markup for products
3. **Sitemap & Robots**: Add in public/ folder
4. **Canonical URLs**: Prevent duplicate content

## Testing Strategy

- **Unit Tests**: Jest for utilities and hooks
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright for user flows
- **Visual Regression**: Percy or Chromatic

## Summary

Phase 5 builds a production-grade Next.js frontend with:
- Clean component architecture
- Type-safe state management
- Efficient data fetching
- Responsive design
- Authentication integration
- Performance optimization

All components should include:
- TypeScript types
- Tailwind CSS styling
- Error states
- Loading states
- Accessibility (a11y)
- Comprehensive comments

Next: Build components systematically, test with mock data, integrate with backend APIs once Phase 6-8 complete.

