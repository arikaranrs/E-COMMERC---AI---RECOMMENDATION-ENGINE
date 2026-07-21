'use client'

import React, { useState, useEffect } from 'react'
import {
  Sparkles,
  ShoppingCart,
  User as UserIcon,
  Search,
  Filter,
  CheckCircle,
  Trash2,
  History,
  Info,
  ChevronRight,
  TrendingUp,
  Cpu,
  BookOpen,
  ShoppingBag,
  Moon,
  Sun,
  Layers,
  ArrowRight,
  Plus,
  Minus
} from 'lucide-react'

// Define Frontend types matching backend schemas
interface Brand {
  id: number
  name: string
  description?: string
}

interface Category {
  id: number
  name: string
  description?: string
  icon_url?: string
}

interface Product {
  id: number
  name: string
  description: string
  price: number
  discount_price?: number
  category_id: number
  brand_id?: number
  stock_quantity: number
  image_url?: string
  sku?: string
  rating: number
  review_count: number
  category?: Category
  brand?: Brand
}

interface CartItem {
  id: number
  cart_id: number
  product_id: number
  quantity: number
  product: Product
}

interface Cart {
  id: number
  user_id: number
  items: CartItem[]
  total: number
  items_count: number
}

interface OrderItem {
  id: number
  order_id: number
  product_id: number
  quantity: number
  price_per_unit: number
  subtotal: number
  product: Product
}

interface Order {
  id: number
  user_id: number
  total_amount: number
  status: string
  shipping_address: string
  billing_address: string
  payment_method: string
  created_at: string
  items: OrderItem[]
}

// User Mock Profiles matching backend seed
const SIMULATED_USERS = [
  {
    id: 1,
    name: 'Sarah Readings',
    email: 'sarah.bookworm@example.com',
    role: 'Tech & Books Enthusiast',
    bio: 'Avid reader, tech-hobbyist, and professional software engineer. Prefers developer guidebooks and technical references.',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=60',
    preferredCategory: 'Books'
  },
  {
    id: 2,
    name: 'David Gates',
    email: 'david.techie@example.com',
    role: 'Gadget Geek & Smart Home Reviewer',
    bio: 'Smart home builder, tech early-adopter. I love mechanical keyboards, wireless audio, and clean OLED displays.',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=60',
    preferredCategory: 'Electronics'
  },
  {
    id: 3,
    name: 'Emily Vogue',
    email: 'emily.stylist@example.com',
    role: 'Fashion Designer & Lifestyle Blogger',
    bio: 'Focuses on elegant design, vintage leather apparel, daily streetwear, and high-performance cooking gear.',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&auto=format&fit=crop&q=60',
    preferredCategory: 'Fashion'
  },
  {
    id: 4,
    name: 'Guest User',
    email: 'admin@example.com',
    role: 'Global Default Profile',
    bio: 'Default visitor dashboard profile. Receives general recommendation listings.',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=60',
    preferredCategory: 'All Categories'
  }
]

const RECOMMENDATION_ALGORITHMS = [
  {
    type: 'personalized',
    name: 'Personalized Matrix Match',
    description: 'Hybrid profile mapping aligning user preference histories and implicit activity signals.',
    badge: '98% Accuracy',
    icon: Sparkles
  },
  {
    type: 'collaborative',
    name: 'Collaborative Filtering (CF)',
    description: 'User-Item matrix comparison finding other users with similar purchasing and rating habits.',
    badge: 'Similar Users',
    icon: Cpu
  },
  {
    type: 'content_based',
    name: 'Content-Based (TF-IDF)',
    description: 'Text mining model indexing tags, brands, categories, and review text for semantic similarity.',
    badge: 'Item Similarity',
    icon: Layers
  },
  {
    type: 'hybrid',
    name: 'Hybrid Recommendation',
    description: 'Ensemble algorithm combining content descriptors and Collaborative User vectors.',
    badge: 'Balanced Match',
    icon: ShoppingBag
  },
  {
    type: 'trending',
    name: 'Trending & Popularity',
    description: 'Aggregates highest average rating counts and transaction volume over the past 48 hours.',
    badge: 'Hot Seller',
    icon: TrendingUp
  }
]

export default function Home() {
  const [currentUser, setCurrentUser] = useState(SIMULATED_USERS[0])
  const [selectedAlgo, setSelectedAlgo] = useState(RECOMMENDATION_ALGORITHMS[0])
  const [isDarkMode, setIsDarkMode] = useState(true)
  
  // Data State
  const [recommendedProducts, setRecommendedProducts] = useState<Product[]>([])
  const [catalogProducts, setCatalogProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [brands, setBrands] = useState<Brand[]>([])
  const [cart, setCart] = useState<Cart | null>(null)
  const [orderHistory, setOrderHistory] = useState<Order[]>([])
  
  // Filtering & UI State
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState<number | null>(null)
  const [selectedBrandFilter, setSelectedBrandFilter] = useState<number | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [isHistoryOpen, setIsHistoryOpen] = useState(false)
  const [checkoutSuccess, setCheckoutSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

  // Fetch Recommended Products
  const fetchRecommendations = async (userId: number, algoType: string) => {
    try {
      const res = await fetch(`${API_BASE}/recommendations?user_id=${userId}&type=${algoType}`)
      if (res.ok) {
        const data = await res.json()
        setRecommendedProducts(data)
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err)
    }
  }

  // Fetch Catalog Products
  const fetchCatalog = async () => {
    try {
      let url = `${API_BASE}/products`
      const params = []
      if (selectedCategoryFilter !== null) params.push(`category_id=${selectedCategoryFilter}`)
      if (selectedBrandFilter !== null) params.push(`brand_id=${selectedBrandFilter}`)
      if (searchQuery) params.push(`search=${encodeURIComponent(searchQuery)}`)
      
      if (params.length > 0) {
        url += `?${params.join('&')}`
      }
      
      const res = await fetch(url)
      if (res.ok) {
        const data = await res.json()
        setCatalogProducts(data)
      }
    } catch (err) {
      console.error('Error fetching catalog:', err)
    }
  }

  // Fetch Categories & Brands
  const fetchMetadata = async () => {
    try {
      const [resCat, resBrand] = await Promise.all([
        fetch(`${API_BASE}/products/categories`),
        fetch(`${API_BASE}/products/brands`)
      ])
      if (resCat.ok) setCategories(await resCat.json())
      if (resBrand.ok) setBrands(await resBrand.json())
    } catch (err) {
      console.error('Error fetching metadata:', err)
    }
  }

  // Fetch Shopping Cart
  const fetchCart = async (userId: number) => {
    try {
      const res = await fetch(`${API_BASE}/cart?user_id=${userId}`)
      if (res.ok) {
        const data = await res.json()
        setCart(data)
      }
    } catch (err) {
      console.error('Error fetching cart:', err)
    }
  }

  // Fetch Order History
  const fetchOrders = async (userId: number) => {
    try {
      const res = await fetch(`${API_BASE}/orders?user_id=${userId}`)
      if (res.ok) {
        const data = await res.json()
        setOrderHistory(data)
      }
    } catch (err) {
      console.error('Error fetching orders:', err)
    }
  }

  // Init Data on User or Algo change
  useEffect(() => {
    fetchMetadata()
  }, [])

  useEffect(() => {
    fetchRecommendations(currentUser.id, selectedAlgo.type)
    fetchCart(currentUser.id)
    fetchOrders(currentUser.id)
  }, [currentUser, selectedAlgo])

  useEffect(() => {
    fetchCatalog()
  }, [selectedCategoryFilter, selectedBrandFilter, searchQuery])

  // Cart Operations
  const handleAddToCart = async (productId: number) => {
    try {
      const res = await fetch(`${API_BASE}/cart?user_id=${currentUser.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
      })
      if (res.ok) {
        const updatedCart = await res.json()
        setCart(updatedCart)
        // Auto open cart drawer for feedback
        setIsCartOpen(true)
      }
    } catch (err) {
      console.error('Error adding to cart:', err)
    }
  }

  const handleUpdateQuantity = async (itemId: number, newQty: number) => {
    try {
      const res = await fetch(`${API_BASE}/cart/${itemId}?user_id=${currentUser.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: newQty })
      })
      if (res.ok) {
        const updatedCart = await res.json()
        setCart(updatedCart)
      }
    } catch (err) {
      console.error('Error updating quantity:', err)
    }
  }

  const handleRemoveFromCart = async (itemId: number) => {
    try {
      const res = await fetch(`${API_BASE}/cart/${itemId}?user_id=${currentUser.id}`, {
        method: 'DELETE'
      })
      if (res.ok) {
        const updatedCart = await res.json()
        setCart(updatedCart)
      }
    } catch (err) {
      console.error('Error removing item:', err)
    }
  }

  // Checkout
  const handleCheckout = async () => {
    if (!cart || cart.items.length === 0) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/orders?user_id=${currentUser.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          shipping_address: '123 Enterprise Way, Tech District, CA 94016',
          billing_address: '123 Enterprise Way, Tech District, CA 94016',
          payment_method: 'Simulated Visa Card Ending in 8899'
        })
      })
      if (res.ok) {
        setCheckoutSuccess(true)
        setCart(null)
        // Refresh orders and recommendations (since order acts as a collaborative filtering feedback signal)
        fetchOrders(currentUser.id)
        fetchRecommendations(currentUser.id, selectedAlgo.type)
        setTimeout(() => {
          setCheckoutSuccess(false)
          setIsCartOpen(false)
        }, 3000)
      }
    } catch (err) {
      console.error('Error during checkout:', err)
    } finally {
      setLoading(false)
    }
  }

  // Helper to generate simulated recommendation match scores
  const getMatchScore = (product: Product, algoType: string) => {
    let base = 85
    // Add variations based on product properties and user choices
    if (algoType === 'personalized' && product.category?.name === currentUser.preferredCategory) {
      base = 96
    } else if (algoType === 'content_based' && product.rating > 4.5) {
      base = 92
    } else if (algoType === 'trending') {
      base = 94
    }
    // seed stability based on id
    return base + (product.id % 5)
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 font-sans ${isDarkMode ? 'bg-[#0f172a] text-slate-100' : 'bg-slate-50 text-slate-900'}`}>
      {/* BACKGROUND GRADIENTS (DARK MODE GLOWS) */}
      {isDarkMode && (
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] rounded-full bg-violet-600/10 blur-[120px]" />
          <div className="absolute top-[20%] right-[-10%] w-[600px] h-[600px] rounded-full bg-blue-600/10 blur-[130px]" />
          <div className="absolute bottom-[-10%] left-[20%] w-[500px] h-[500px] rounded-full bg-indigo-600/5 blur-[120px]" />
        </div>
      )}

      {/* TOP HEADER */}
      <header className={`sticky top-0 z-40 backdrop-blur-md border-b transition-colors duration-300 ${isDarkMode ? 'bg-[#0f172a]/80 border-slate-800/80' : 'bg-white/80 border-slate-200'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-violet-600 to-blue-500 flex items-center justify-center text-white shadow-md shadow-violet-600/20">
              <Sparkles className="h-5 w-5 animate-pulse" />
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-violet-400 via-indigo-300 to-blue-400 bg-clip-text text-transparent">
                Antigravity Recs
              </span>
              <span className="block text-[10px] text-slate-400 font-semibold tracking-wider uppercase">AI recommendation engine</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Dark Mode Switch */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className={`p-2.5 rounded-xl border transition-all ${isDarkMode ? 'bg-slate-800/50 border-slate-700 hover:bg-slate-700/50 text-amber-400' : 'bg-slate-100 border-slate-200 hover:bg-slate-200 text-slate-600'}`}
              title="Toggle Theme"
            >
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>

            {/* View Order History Button */}
            <button
              onClick={() => setIsHistoryOpen(true)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium transition-all ${isDarkMode ? 'bg-slate-800/50 border-slate-700 hover:bg-slate-700 text-slate-300' : 'bg-slate-100 border-slate-200 hover:bg-slate-200 text-slate-700'}`}
            >
              <History className="h-4 w-4" />
              <span className="hidden md:inline">Order History</span>
            </button>

            {/* Cart Button */}
            <button
              onClick={() => setIsCartOpen(true)}
              className="relative flex items-center gap-2.5 px-4.5 py-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white rounded-xl font-semibold text-sm shadow-lg shadow-violet-600/20 hover:scale-[1.02] transition-all"
            >
              <ShoppingCart className="h-4 w-4" />
              <span>Cart</span>
              {cart && cart.items_count > 0 && (
                <span className="absolute -top-1.5 -right-1.5 h-5.5 min-w-5.5 px-1 flex items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white border-2 border-[#0f172a] animate-bounce">
                  {cart.items_count}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10 space-y-8">
        
        {/* INTERACTIVE PLAYGROUND HERO PANEL */}
        <section className={`rounded-3xl border p-6 md:p-8 transition-all ${isDarkMode ? 'bg-slate-900/60 border-slate-800/80 backdrop-blur-sm' : 'bg-white border-slate-200/80 shadow-sm'}`}>
          <div className="flex flex-col lg:flex-row gap-8 items-start">
            
            {/* User Switcher Column */}
            <div className="w-full lg:w-2/5 space-y-4">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 text-[10px] uppercase tracking-wider font-extrabold rounded-md bg-violet-600/10 text-violet-400">Step 1</span>
                <h2 className="text-sm font-extrabold tracking-wide uppercase text-slate-400">Simulate Target User</h2>
              </div>
              <p className="text-xs text-slate-400">Choose a user profile to load their historical purchases, reviews, and personalized recommendation list.</p>
              
              <div className="grid grid-cols-2 gap-3">
                {SIMULATED_USERS.map((user) => {
                  const isSelected = currentUser.id === user.id
                  return (
                    <button
                      key={user.id}
                      onClick={() => setCurrentUser(user)}
                      className={`flex flex-col items-start p-3 rounded-2xl border text-left transition-all hover:scale-[1.01] ${
                        isSelected 
                          ? 'border-violet-500/80 bg-violet-500/10 ring-1 ring-violet-500/30' 
                          : isDarkMode ? 'border-slate-800 bg-slate-800/20 hover:bg-slate-850' : 'border-slate-200 bg-slate-50 hover:bg-slate-100'
                      }`}
                    >
                      <div className="flex items-center gap-2.5 mb-2">
                        <img src={user.avatar} alt={user.name} className="h-8.5 w-8.5 rounded-full object-cover border border-violet-500/30" />
                        <div>
                          <h4 className="text-xs font-bold leading-tight">{user.name.split(' ')[0]}</h4>
                          <span className="text-[9px] text-slate-400 font-semibold">{user.preferredCategory}</span>
                        </div>
                      </div>
                      <p className="text-[10px] leading-relaxed text-slate-400 line-clamp-2">{user.bio}</p>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Split Divider */}
            <div className="hidden lg:block self-stretch w-px bg-slate-800/80" />

            {/* Algorithm Selector Column */}
            <div className="w-full lg:w-3/5 space-y-4">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 text-[10px] uppercase tracking-wider font-extrabold rounded-md bg-indigo-600/10 text-indigo-400">Step 2</span>
                <h2 className="text-sm font-extrabold tracking-wide uppercase text-slate-400">Choose Recommendation Model</h2>
              </div>
              <p className="text-xs text-slate-400">Select which algorithm drives recommendations. Observe how matches change based on user profile preferences.</p>

              <div className="flex flex-col gap-2.5">
                {RECOMMENDATION_ALGORITHMS.map((algo) => {
                  const isSelected = selectedAlgo.type === algo.type
                  const Icon = algo.icon
                  return (
                    <button
                      key={algo.type}
                      onClick={() => setSelectedAlgo(algo)}
                      className={`w-full flex items-center justify-between p-3.5 rounded-2xl border text-left transition-all ${
                        isSelected 
                          ? 'border-indigo-500/85 bg-indigo-500/10 ring-1 ring-indigo-500/30' 
                          : isDarkMode ? 'border-slate-800 bg-slate-800/20 hover:bg-slate-850' : 'border-slate-200 bg-slate-50 hover:bg-slate-100'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`p-2 rounded-xl ${isSelected ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-700/20 text-slate-400'}`}>
                          <Icon className="h-5 w-5" />
                        </div>
                        <div>
                          <h4 className="text-xs font-bold">{algo.name}</h4>
                          <p className="text-[10px] text-slate-400 line-clamp-1 mt-0.5">{algo.description}</p>
                        </div>
                      </div>
                      <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full ${isSelected ? 'bg-indigo-500/20 text-indigo-300' : 'bg-slate-850 text-slate-400'}`}>
                        {algo.badge}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>

          </div>
        </section>

        {/* SECTION A: RECOMMENDATIONS CAROUSEL */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-indigo-400" />
              <h2 className="text-lg font-bold tracking-tight">
                Recommended for <span className="text-indigo-400">{currentUser.name}</span>
              </h2>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 font-semibold capitalize border border-indigo-500/20">
                {selectedAlgo.name}
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Computed in real-time</p>
          </div>

          {recommendedProducts.length === 0 ? (
            <div className={`text-center py-12 rounded-2xl border ${isDarkMode ? 'border-slate-800' : 'border-slate-200'}`}>
              <Info className="h-8 w-8 text-slate-500 mx-auto mb-2" />
              <p className="text-sm text-slate-400">No cached recommendations found for this model.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {recommendedProducts.map((prod) => {
                const matchScore = getMatchScore(prod, selectedAlgo.type)
                return (
                  <div
                    key={`rec-${prod.id}`}
                    className={`group relative rounded-2xl border p-4.5 transition-all flex flex-col justify-between hover:translate-y-[-2px] ${
                      isDarkMode 
                        ? 'bg-slate-900/40 border-slate-800 hover:border-slate-700/80 shadow-md shadow-black/10' 
                        : 'bg-white border-slate-200/80 hover:border-slate-300 shadow-sm'
                    }`}
                  >
                    {/* Match Score Badge */}
                    <div className="absolute top-3 left-3 z-10 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#0f172a]/80 backdrop-blur-sm border border-violet-500/30 text-violet-300 text-[10px] font-bold">
                      <Sparkles className="h-3 w-3 animate-spin-slow" />
                      <span>{matchScore}% Match</span>
                    </div>

                    <div className="space-y-4">
                      {/* Product Image */}
                      <div className="relative aspect-video rounded-xl overflow-hidden bg-slate-800/50">
                        <img 
                          src={prod.image_url} 
                          alt={prod.name} 
                          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
                        />
                      </div>

                      {/* Info */}
                      <div className="space-y-1.5">
                        <div className="flex justify-between items-center text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                          <span>{prod.category?.name}</span>
                          <span>{prod.brand?.name}</span>
                        </div>
                        <h3 className="text-sm font-bold line-clamp-1 group-hover:text-violet-400 transition-colors">{prod.name}</h3>
                        <p className="text-[11px] leading-normal text-slate-400 line-clamp-2">{prod.description}</p>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-800/80 flex items-center justify-between gap-4">
                      <div>
                        <span className="text-lg font-extrabold">${prod.price}</span>
                        <span className="block text-[9px] text-emerald-400 font-bold">In Stock</span>
                      </div>
                      <button
                        onClick={() => handleAddToCart(prod.id)}
                        className="p-2.5 rounded-xl bg-violet-600 hover:bg-violet-500 text-white shadow-md shadow-violet-600/10 transition-all hover:scale-[1.03]"
                        title="Add to Cart"
                      >
                        <ShoppingCart className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </section>

        {/* SECTION B: CATALOG BROWSER */}
        <section className="space-y-6">
          <div className="border-t border-slate-850 pt-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold tracking-tight">Product Catalog Explorer</h2>
              <p className="text-xs text-slate-400">Browse all inventory, filter by tags, and log click patterns</p>
            </div>
            
            {/* Search Box */}
            <div className="relative w-full md:w-80">
              <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className={`w-full pl-10 pr-4 py-2.5 rounded-xl text-sm border focus:outline-none focus:ring-1 transition-all ${
                  isDarkMode 
                    ? 'bg-slate-900/60 border-slate-800 focus:border-violet-500 focus:ring-violet-500' 
                    : 'bg-white border-slate-200 focus:border-violet-500 focus:ring-violet-500'
                }`}
              />
            </div>
          </div>

          <div className="flex flex-col lg:flex-row gap-8 items-start">
            {/* Filters Sidebar */}
            <aside className="w-full lg:w-64 space-y-6 shrink-0">
              {/* Category Filter */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-slate-400">
                  <Filter className="h-3.5 w-3.5 text-violet-400" />
                  <span>Filter by Category</span>
                </div>
                <div className="flex flex-wrap lg:flex-col gap-1.5">
                  <button
                    onClick={() => setSelectedCategoryFilter(null)}
                    className={`px-3.5 py-2 rounded-xl text-left text-xs font-semibold border transition-all ${
                      selectedCategoryFilter === null 
                        ? 'border-violet-500 bg-violet-500/10 text-violet-300' 
                        : isDarkMode ? 'border-slate-800 hover:bg-slate-850' : 'border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    All Categories
                  </button>
                  {categories.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategoryFilter(cat.id)}
                      className={`px-3.5 py-2 rounded-xl text-left text-xs font-semibold border transition-all ${
                        selectedCategoryFilter === cat.id 
                          ? 'border-violet-500 bg-violet-500/10 text-violet-300' 
                          : isDarkMode ? 'border-slate-800 hover:bg-slate-850' : 'border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {cat.name}
                    </button>
                  ))}
                </div>
              </div>

              {/* Brand Filter */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-slate-400">
                  <Layers className="h-3.5 w-3.5 text-indigo-400" />
                  <span>Filter by Brand</span>
                </div>
                <div className="flex flex-wrap lg:flex-col gap-1.5">
                  <button
                    onClick={() => setSelectedBrandFilter(null)}
                    className={`px-3.5 py-2 rounded-xl text-left text-xs font-semibold border transition-all ${
                      selectedBrandFilter === null 
                        ? 'border-indigo-500 bg-indigo-500/10 text-indigo-300' 
                        : isDarkMode ? 'border-slate-800 hover:bg-slate-850' : 'border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    All Brands
                  </button>
                  {brands.map((br) => (
                    <button
                      key={br.id}
                      onClick={() => setSelectedBrandFilter(br.id)}
                      className={`px-3.5 py-2 rounded-xl text-left text-xs font-semibold border transition-all ${
                        selectedBrandFilter === br.id 
                          ? 'border-indigo-500 bg-indigo-500/10 text-indigo-300' 
                          : isDarkMode ? 'border-slate-800 hover:bg-slate-850' : 'border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {br.name}
                    </button>
                  ))}
                </div>
              </div>
            </aside>

            {/* Catalog Grid */}
            <div className="flex-1 w-full">
              {catalogProducts.length === 0 ? (
                <div className={`text-center py-20 rounded-2xl border ${isDarkMode ? 'border-slate-800' : 'border-slate-200'}`}>
                  <Search className="h-8 w-8 text-slate-500 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-slate-400">No matching products found.</p>
                  <p className="text-xs text-slate-500 mt-1">Try resetting your filter parameters or search term.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {catalogProducts.map((prod) => (
                    <div
                      key={`cat-${prod.id}`}
                      className={`group rounded-2xl border p-4.5 transition-all flex flex-col justify-between hover:translate-y-[-2px] ${
                        isDarkMode 
                          ? 'bg-slate-900/40 border-slate-800 hover:border-slate-700/80 shadow-md shadow-black/10' 
                          : 'bg-white border-slate-200/80 hover:border-slate-300 shadow-sm'
                      }`}
                    >
                      <div className="space-y-4">
                        {/* Image */}
                        <div className="relative aspect-video rounded-xl overflow-hidden bg-slate-800/50">
                          <img 
                            src={prod.image_url} 
                            alt={prod.name} 
                            className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>

                        {/* Details */}
                        <div className="space-y-1.5">
                          <div className="flex justify-between items-center text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                            <span>{prod.category?.name}</span>
                            <span>{prod.brand?.name}</span>
                          </div>
                          <h3 className="text-sm font-bold line-clamp-1 group-hover:text-violet-400 transition-colors">{prod.name}</h3>
                          <p className="text-[11px] leading-normal text-slate-400 line-clamp-2">{prod.description}</p>
                        </div>
                      </div>

                      <div className="mt-4 pt-4 border-t border-slate-800/80 flex items-center justify-between gap-4">
                        <div>
                          <span className="text-lg font-extrabold">${prod.price}</span>
                          <span className="block text-[9px] text-emerald-400 font-bold">Qty: {prod.stock_quantity} left</span>
                        </div>
                        <button
                          onClick={() => handleAddToCart(prod.id)}
                          className="p-2.5 rounded-xl bg-violet-600 hover:bg-violet-500 text-white shadow-md shadow-violet-600/10 transition-all hover:scale-[1.03]"
                          title="Add to Cart"
                        >
                          <ShoppingCart className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>

      </main>

      {/* SHOPPING CART DRAWER */}
      {isCartOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden flex justify-end">
          {/* Backdrop */}
          <div 
            onClick={() => setIsCartOpen(false)}
            className="absolute inset-0 bg-[#020617]/70 backdrop-blur-xs transition-opacity" 
          />
          
          {/* Drawer Body */}
          <div className={`w-full max-w-md h-full relative z-10 flex flex-col justify-between border-l shadow-2xl transition-transform ${isDarkMode ? 'bg-[#0f172a] border-slate-850' : 'bg-white border-slate-200'}`}>
            {/* Header */}
            <div className="p-6 border-b border-slate-850 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <ShoppingCart className="h-5 w-5 text-violet-400" />
                <h3 className="font-extrabold text-base">Shopping Cart</h3>
              </div>
              <button 
                onClick={() => setIsCartOpen(false)}
                className="text-xs font-bold text-slate-400 hover:text-slate-200 uppercase tracking-wider"
              >
                Close
              </button>
            </div>

            {/* Checkout Success Banner */}
            {checkoutSuccess && (
              <div className="mx-6 mt-4 p-4.5 rounded-2xl bg-emerald-500/15 border border-emerald-500/35 text-center space-y-2">
                <CheckCircle className="h-8 w-8 text-emerald-400 mx-auto" />
                <h4 className="text-xs font-bold text-emerald-300">Order Placed Successfully!</h4>
                <p className="text-[10px] text-slate-300">Implicit transaction feedback registered. Recommendations updating.</p>
              </div>
            )}

            {/* Cart Items List */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {!cart || cart.items.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center space-y-2">
                  <ShoppingBag className="h-10 w-10 text-slate-600" />
                  <h4 className="text-sm font-bold text-slate-400">Cart is empty</h4>
                  <p className="text-xs text-slate-500">Add products from the catalog to get started.</p>
                </div>
              ) : (
                cart.items.map((item) => (
                  <div 
                    key={item.id}
                    className={`flex gap-4 p-3 rounded-2xl border ${isDarkMode ? 'border-slate-850 bg-slate-900/30' : 'border-slate-100 bg-slate-50'}`}
                  >
                    <img 
                      src={item.product.image_url} 
                      alt={item.product.name} 
                      className="h-16 w-16 rounded-xl object-cover border border-slate-800/80 shrink-0" 
                    />
                    <div className="flex-1 space-y-1.5 flex flex-col justify-between">
                      <div>
                        <h4 className="text-xs font-bold line-clamp-1">{item.product.name}</h4>
                        <span className="text-[10px] text-slate-400">${item.product.price} each</span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        {/* Quantity Counter */}
                        <div className="flex items-center gap-1.5 bg-slate-850 rounded-lg p-0.5 border border-slate-800/80">
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                            className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-white"
                          >
                            <Minus className="h-3 w-3" />
                          </button>
                          <span className="text-[10px] font-bold px-1.5 min-w-[16px] text-center">{item.quantity}</span>
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                            className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-white"
                          >
                            <Plus className="h-3 w-3" />
                          </button>
                        </div>

                        {/* Remove */}
                        <button
                          onClick={() => handleRemoveFromCart(item.id)}
                          className="text-slate-500 hover:text-rose-400 p-1 transition-colors"
                          title="Delete item"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Footer Summary / Checkout */}
            {cart && cart.items.length > 0 && (
              <div className="p-6 border-t border-slate-850 space-y-4">
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-slate-400 font-semibold">
                    <span>Subtotal</span>
                    <span>${cart.total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-xs text-slate-400 font-semibold">
                    <span>Shipping</span>
                    <span className="text-emerald-400">FREE</span>
                  </div>
                  <div className="flex justify-between font-extrabold text-sm border-t border-slate-850 pt-2">
                    <span>Total Amount</span>
                    <span className="text-violet-400">${cart.total.toFixed(2)}</span>
                  </div>
                </div>

                <button
                  onClick={handleCheckout}
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-2.5 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-extrabold text-xs shadow-lg shadow-violet-600/10 hover:scale-[1.01] transition-all disabled:opacity-50"
                >
                  {loading ? 'Processing Checkout...' : 'Simulate Order Checkout'}
                  <ArrowRight className="h-4.5 w-4.5" />
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ORDER HISTORY DRAWER/MODAL */}
      {isHistoryOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden flex justify-center items-center">
          {/* Backdrop */}
          <div 
            onClick={() => setIsHistoryOpen(false)}
            className="absolute inset-0 bg-[#020617]/75 backdrop-blur-xs transition-opacity" 
          />
          
          {/* Modal Content */}
          <div className={`w-full max-w-2xl max-h-[80vh] relative z-10 rounded-3xl border shadow-2xl flex flex-col justify-between ${isDarkMode ? 'bg-[#0f172a] border-slate-800' : 'bg-white border-slate-200'}`}>
            {/* Header */}
            <div className="p-6 border-b border-slate-850 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <History className="h-5 w-5 text-indigo-400" />
                <h3 className="font-extrabold text-base">Purchase History for {currentUser.name}</h3>
              </div>
              <button 
                onClick={() => setIsHistoryOpen(false)}
                className="text-xs font-bold text-slate-400 hover:text-slate-200 uppercase tracking-wider"
              >
                Close
              </button>
            </div>

            {/* List */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {orderHistory.length === 0 ? (
                <div className="text-center py-12 space-y-2">
                  <History className="h-8 w-8 text-slate-600 mx-auto" />
                  <p className="text-sm font-semibold text-slate-400">No orders found.</p>
                  <p className="text-xs text-slate-500">Checkout a cart to see order logs populate here.</p>
                </div>
              ) : (
                orderHistory.map((order) => (
                  <div 
                    key={order.id}
                    className={`rounded-2xl border p-4.5 space-y-4 ${isDarkMode ? 'border-slate-850 bg-slate-900/20' : 'border-slate-100 bg-slate-50'}`}
                  >
                    <div className="flex items-center justify-between text-xs flex-wrap gap-2">
                      <div>
                        <span className="text-slate-400 font-semibold">Order ID: </span>
                        <span className="font-bold">#ORD-000{order.id}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 font-semibold">Placed on: </span>
                        <span className="font-bold">{new Date(order.created_at).toLocaleDateString()}</span>
                      </div>
                      <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] uppercase font-extrabold">
                        {order.status}
                      </span>
                    </div>

                    <div className="border-t border-slate-850/80 pt-3 space-y-2">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex justify-between items-center text-xs">
                          <span className="font-bold text-slate-300 line-clamp-1">{item.product.name}</span>
                          <span className="text-slate-400 text-[11px] shrink-0">{item.quantity}x @ ${item.price_per_unit}</span>
                        </div>
                      ))}
                    </div>

                    <div className="border-t border-slate-850/80 pt-3 flex justify-between items-center">
                      <div className="text-[10px] text-slate-400">
                        <span className="block">Paid via: {order.payment_method}</span>
                      </div>
                      <span className="text-sm font-extrabold text-violet-400">Total: ${order.total_amount}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className={`border-t transition-colors duration-300 py-6 mt-12 text-center text-xs text-slate-400 ${isDarkMode ? 'bg-[#0f172a] border-slate-850' : 'bg-white border-slate-200'}`}>
        <p>© 2026 Antigravity Enterprise Recommendation Engine Playground. All rights reserved.</p>
      </footer>
    </div>
  )
}
