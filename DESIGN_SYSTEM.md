# 🎨 Gulf Emperor Design System Guide

> **Professional, Modern & Minimal Design System for E-commerce**  
> A comprehensive guide for maintaining consistency across all pages

---

## 📋 Table of Contents

1. [Core Principles](#core-principles)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Components Library](#components-library)
6. [HTMX Patterns](#htmx-patterns)
7. [Responsive Design](#responsive-design)
8. [RTL Support](#rtl-support)
9. [Best Practices](#best-practices)

---

## 🎯 Core Principles

### Design Philosophy
- **Minimal & Clean**: Less is more - focus on content, remove clutter
- **Professional**: Business-grade quality with attention to detail
- **Modern**: Contemporary UI patterns and smooth interactions
- **Accessible**: Clear hierarchy, readable text, intuitive navigation
- **Responsive**: Mobile-first approach with seamless scaling

### Key Characteristics
- ✅ White backgrounds with subtle shadows
- ✅ Single primary color (#00869E) - no secondary colors
- ✅ Generous white space
- ✅ Compact, information-dense layouts
- ✅ Smooth transitions and hover effects
- ✅ Consistent rounded corners

---

## 🎨 Color System

### Primary Color Palette
```css
primary: {
  DEFAULT: '#00869E',  /* Main brand color */
  50:  '#E6F7FA',      /* Lightest - backgrounds */
  100: '#CCEFF5',
  200: '#99DFEB',
  300: '#66CFE1',
  400: '#33BFD7',
  500: '#00869E',      /* Base */
  600: '#006B7E',      /* Hover states */
  700: '#00505F',      /* Active states */
  800: '#00353F',
  900: '#001A20',      /* Darkest */
}
```

### Semantic Colors
```tailwind
/* Success */
bg-green-600, text-green-600

/* Warning */
bg-yellow-400, text-yellow-400 (ratings)
bg-yellow-500 (badges)

/* Error / Danger */
bg-red-500, text-red-600

/* Neutral Grays */
gray-50   - Light backgrounds
gray-100  - Hover backgrounds
gray-200  - Borders
gray-300  - Disabled states
gray-400  - Placeholders
gray-500  - Secondary text
gray-600  - Body text
gray-700  - Headings
gray-900  - Primary text
```

### Usage Rules
- **Primary Color**: Use for CTAs, links, active states, brand elements
- **Gray Scale**: Use for text hierarchy, borders, backgrounds
- **Semantic Colors**: Use only for their intended purpose
- **Never**: Mix multiple accent colors on the same element

---

## 📝 Typography

### Font System
```tailwind
/* Base Font */
font-sans  /* Default system font stack */

/* Size Scale */
text-[10px]  - Tiny labels (badges)
text-xs      - Small text (12px)
text-sm      - Body text (14px)
text-base    - Default (16px)
text-lg      - Large text (18px)
text-xl      - Headings (20px)
text-2xl     - Page titles (24px)
text-3xl     - Hero titles (30px)
text-4xl     - Large displays (36px)

/* Weight Scale */
font-normal      - 400 (body text)
font-medium      - 500 (emphasized text)
font-semibold    - 600 (subheadings)
font-bold        - 700 (headings, prices)

/* Line Height */
leading-tight    - Compact headings
leading-normal   - Body text (default)
leading-relaxed  - Comfortable reading
```

### Typography Hierarchy
```html
<!-- Page Title -->
<h1 class="text-3xl font-bold text-gray-900 mb-4">

<!-- Section Title -->
<h2 class="text-2xl font-bold text-gray-900 mb-6">

<!-- Subsection Title -->
<h3 class="text-lg font-semibold text-gray-900 mb-3">

<!-- Body Text -->
<p class="text-sm text-gray-700">

<!-- Small Text -->
<span class="text-xs text-gray-600">

<!-- Price (Large) -->
<span class="text-4xl font-bold text-primary">

<!-- Price (Regular) -->
<span class="text-base font-bold text-primary">
```

---

## 📐 Spacing & Layout

### Spacing Scale
```tailwind
/* Gap Sizes */
gap-1   - 4px  (tight elements)
gap-2   - 8px  (card grids, compact)
gap-3   - 12px (default spacing)
gap-4   - 16px (sections)
gap-6   - 24px (major sections)
gap-8   - 32px (page sections)

/* Padding */
p-2     - 8px  (compact cards)
p-3     - 12px (card content)
p-4     - 16px (normal spacing)
p-6     - 24px (generous padding)
p-8     - 32px (large containers)

/* Margin */
mb-2    - 8px  (tight spacing)
mb-3    - 12px (default)
mb-4    - 16px (elements)
mb-6    - 24px (sections)
mb-8    - 32px (major sections)
```

### Container & Layout
```html
<!-- Page Container -->
<div class="container mx-auto px-2 sm:px-4 pb-8 pt-2">

<!-- Two Column Layout (Sidebar + Content) -->
<div class="flex flex-col lg:flex-row gap-2">
  <aside class="lg:w-50 flex-shrink-0">...</aside>
  <div class="flex-1">...</div>
</div>

<!-- Product Grid -->
<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
  <!-- 5 products per row on large screens -->
</div>
```

### Border Radius
```tailwind
rounded-lg      - 8px  (default for cards, buttons)
rounded-md      - 6px  (smaller elements)
rounded-full    - 9999px (badges, pills)
```

---

## 🧩 Components Library

### 1. Cards

#### Product Card (Grid)
```html
<div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
  <!-- Image with hover zoom -->
  <a href="#" class="block relative overflow-hidden">
    <img class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
    
    <!-- Badges (top-right) -->
    <div class="absolute top-2 end-2 flex flex-col gap-1">
      <span class="bg-primary text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">جديد</span>
      <span class="bg-red-500 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">-20%</span>
    </div>
  </a>
  
  <!-- Content -->
  <div class="p-3">
    <a href="#" class="block font-medium text-sm text-gray-900 hover:text-primary transition-colors mb-3 line-clamp-2">
      Product Name
    </a>
    
    <!-- Category -->
    <div class="text-[10px] text-gray-500 mb-1">Category</div>
    
    <!-- Price & Action -->
    <div class="flex items-center justify-between gap-2">
      <div class="flex-1">
        <div class="flex items-baseline gap-1">
          <span class="text-base font-bold text-primary">299</span>
          <span class="text-xs text-gray-600">﷼</span>
        </div>
      </div>
      
      <!-- Add to Cart Button -->
      <button class="bg-primary hover:bg-primary-700 text-white p-2 rounded-lg transition-colors">
        <svg class="w-5 h-5">...</svg>
      </button>
    </div>
  </div>
</div>
```

**Key Points:**
- White background with subtle shadow
- Hover effect: shadow increase + image scale
- Compact padding: `p-3`
- Image height: `h-48`
- Badges positioned `top-2 end-2` (RTL safe)

#### Content Card
```html
<div class="bg-white rounded-lg shadow-sm p-6 md:p-8 mb-8">
  <!-- Content -->
</div>
```

**Usage:** Product details, forms, content sections

---

### 2. Buttons

#### Primary Button
```html
<button class="bg-primary hover:bg-primary-700 text-white font-bold py-4 px-6 rounded-lg transition-colors text-lg">
  إضافة إلى السلة
</button>
```

#### Icon Button
```html
<button class="bg-primary hover:bg-primary-700 text-white p-2 rounded-lg transition-colors">
  <svg class="w-5 h-5">...</svg>
</button>
```

#### Disabled Button
```html
<button disabled class="bg-gray-400 text-gray-600 font-bold py-4 px-6 rounded-lg cursor-not-allowed">
  غير متوفر
</button>
```

**Button Rules:**
- Always use `transition-colors` for smooth hover
- Primary color for main actions
- Gray for disabled states
- Consistent padding: `py-2 px-4` or `py-4 px-6`

---

### 3. Form Elements

#### Text Input
```html
<input 
  type="text"
  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
```

#### Number Input (Compact)
```html
<input 
  type="number"
  class="w-20 px-2 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-sm">
```

#### Checkbox
```html
<input 
  type="checkbox"
  class="rounded border-gray-300 text-primary focus:ring-primary-500">
```

#### Radio Button
```html
<input 
  type="radio"
  class="text-primary focus:ring-primary-500">
```

#### Select Dropdown
```html
<select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm">
  <option>Option 1</option>
</select>
```

**Form Rules:**
- Always use `focus:ring-2 focus:ring-primary`
- Border: `border-gray-300`
- Rounded: `rounded-lg`
- White background (default)

---

### 4. Badges

```html
<!-- New Badge -->
<span class="bg-primary text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">جديد</span>

<!-- Discount Badge -->
<span class="bg-red-500 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">-20%</span>

<!-- Out of Stock -->
<span class="bg-gray-500 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">نفد</span>

<!-- Featured Badge -->
<span class="bg-yellow-500 text-white text-xs font-semibold px-3 py-1 rounded-full">مميز</span>
```

**Badge Rules:**
- Use `text-[10px]` for small badges (grid)
- Use `text-xs` for larger badges (detail pages)
- Always `rounded-full`
- Font weight: `font-semibold`

---

### 5. Navigation Elements

#### Navbar (Fixed)
```html
<nav class="bg-white shadow-md fixed top-0 left-0 right-0 z-50" dir="rtl">
  <div class="container mx-auto px-4">
    <div class="flex justify-between items-center h-16">
      <!-- Content -->
    </div>
  </div>
</nav>
```

**Navbar Rules:**
- White background
- Fixed position at top
- Height: `h-16` (64px)
- Shadow: `shadow-md`
- Primary color for text/links
- Hover: `hover:text-primary-600`

#### Sidebar Filter
```html
<aside class="lg:w-50 flex-shrink-0">
  <div class="bg-white rounded-lg shadow-sm p-2 sticky top-4">
    <!-- Filter sections -->
  </div>
</aside>
```

#### Breadcrumb
```html
<nav class="flex items-center gap-2 text-sm text-gray-600 mb-8">
  <a href="#" class="hover:text-primary">المنتجات</a>
  <span>‹</span>
  <span class="text-gray-900">Current Page</span>
</nav>
```

---

### 6. Pagination

```html
<div class="mt-8 border-t border-gray-200 bg-white shadow-sm px-4 py-3 rounded-lg">
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
    <!-- Product count -->
    <div>
      <p class="text-sm text-gray-700">
        عرض <span class="font-medium">1</span> إلى <span class="font-medium">15</span> 
        من <span class="font-medium">100</span> منتج
      </p>
    </div>
    
    <!-- Page buttons -->
    <nav class="flex items-center gap-1">
      <!-- First Page -->
      <a href="#" class="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
        <svg class="w-4 h-4">...</svg>
      </a>
      
      <!-- Page Numbers -->
      <span class="inline-flex items-center px-4 py-2 text-sm font-semibold text-white bg-primary rounded-lg">1</span>
      <a href="#" class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">2</a>
      
      <!-- Ellipsis -->
      <span class="inline-flex items-center px-2 py-2 text-sm text-gray-700">...</span>
    </nav>
  </div>
</div>
```

**Pagination Rules:**
- Show first, last, current, and ±2 pages
- Arrows for RTL: `>>` first, `>` previous, `<` next, `<<` last
- Active page: white text on primary background
- Inactive pages: gray text on white with border

---

### 7. Empty States

```html
<div class="bg-white rounded-lg shadow-sm p-12 text-center">
  <svg class="mx-auto h-16 w-16 text-gray-400 mb-4">...</svg>
  <h3 class="text-lg font-semibold text-gray-900 mb-2">لم يتم العثور على منتجات</h3>
  <p class="text-gray-600">جرِّب تعديل معايير البحث أو إزالة الفلاتر</p>
</div>
```

---

## ⚡ HTMX Patterns

### Basic HTMX Attributes
```html
<!-- Standard HTMX request -->
<element
  hx-get="/url"
  hx-target="#target-id"
  hx-swap="outerHTML"
  hx-trigger="click"
>
```

### Filter with HTMX
```html
<input 
  type="checkbox"
  name="brand"
  value="bmw"
  hx-get="{% url 'store:product_list' %}"
  hx-target="#product-grid"
  hx-include="[name='category'],[name='search'],[name='min_price'],[name='max_price'],[name='rating']"
>
```

**Key Points:**
- Always use `hx-include` to preserve other filters
- Target: `#product-grid` for product updates
- Target: `#mini-cart` for cart updates
- Swap: `outerHTML` (default)

### Add to Cart Pattern
```html
<form 
  hx-post="{% url 'orders:add_to_cart' product.id %}"
  hx-target="#mini-cart"
  hx-swap="outerHTML">
  {% csrf_token %}
  <button type="submit" class="bg-primary...">أضف للسلة</button>
</form>
```

### HTMX Rules
1. ✅ Always include CSRF token in forms
2. ✅ Use `hx-include` to preserve filter state
3. ✅ Target specific elements (`#product-grid`, `#mini-cart`)
4. ✅ Use semantic HTTP methods (GET for filters, POST for actions)
5. ✅ Handle loading states with HTMX indicators

---

## 📱 Responsive Design

### Breakpoints
```tailwind
sm:  640px   /* Small tablets */
md:  768px   /* Tablets */
lg:  1024px  /* Desktop */
xl:  1280px  /* Large desktop */
```

### Grid Responsiveness
```html
<!-- Product Grid: 2 cols → 3 cols → 5 cols -->
<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">

<!-- Content Grid: 1 col → 2 cols → 4 cols -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

<!-- Two Column Layout -->
<div class="flex flex-col lg:flex-row gap-2">
  <aside class="lg:w-50">...</aside>
  <div class="flex-1">...</div>
</div>
```

### Mobile-First Approach
```html
<!-- Base: Mobile -->
<div class="px-2 py-2">
  
<!-- Tablet and up -->
<div class="px-2 md:px-4 py-2 md:py-4">

<!-- Hide on mobile -->
<div class="hidden md:block">

<!-- Show only on mobile -->
<div class="md:hidden">
```

### Responsive Typography
```html
<h1 class="text-2xl md:text-3xl lg:text-4xl">
```

---

## 🌐 RTL Support

### RTL Setup
```html
<!-- Always set dir attribute -->
<div dir="rtl">
  <!-- Content -->
</div>
```

### RTL-Safe Spacing
```tailwind
/* ❌ DON'T USE */
ml-4, mr-4, pl-4, pr-4

/* ✅ USE INSTEAD */
space-x-reverse  /* For RTL horizontal spacing */
space-x-4 space-x-reverse

/* OR use logical properties */
ms-4  /* margin-inline-start */
me-4  /* margin-inline-end */
ps-4  /* padding-inline-start */
pe-4  /* padding-inline-end */
```

### RTL-Safe Positioning
```tailwind
/* ❌ DON'T USE */
left-0, right-0

/* ✅ USE INSTEAD */
start-0  /* inline-start */
end-0    /* inline-end */

/* Example: Badge positioning */
<div class="absolute top-2 end-2">  <!-- RTL safe -->
```

### Text Direction
```html
<!-- Arabic/RTL content -->
<p class="text-right">النص العربي</p>

<!-- Mixed content -->
<div class="flex items-center space-x-reverse space-x-2">
  <span>العربي</span>
  <span>123</span>
</div>
```

---

## ✨ Best Practices

### 1. Component Structure
```html
<!-- ✅ Good: Clear hierarchy -->
<div class="card">
  <div class="card-image">...</div>
  <div class="card-content">
    <div class="card-title">...</div>
    <div class="card-meta">...</div>
    <div class="card-actions">...</div>
  </div>
</div>

<!-- ❌ Bad: Flat structure -->
<div class="card">
  <img>
  <h3>...</h3>
  <span>...</span>
  <button>...</button>
</div>
```

### 2. Hover States
```html
<!-- ✅ Always add transitions -->
<a class="text-gray-700 hover:text-primary transition-colors">

<!-- ✅ Card hover effects -->
<div class="shadow-sm hover:shadow-md transition-shadow">

<!-- ✅ Image zoom on hover -->
<img class="group-hover:scale-105 transition-transform duration-300">
```

### 3. Accessibility
```html
<!-- ✅ Use semantic HTML -->
<nav>...</nav>
<main>...</main>
<article>...</article>

<!-- ✅ Add ARIA labels -->
<button aria-label="أضف إلى السلة">...</button>

<!-- ✅ Use proper alt text -->
<img src="..." alt="Product name">
```

### 4. Performance
```html
<!-- ✅ Optimize images -->
<img class="w-full h-48 object-cover" loading="lazy">

<!-- ✅ Limit shadow complexity -->
<!-- Use shadow-sm, shadow-md, shadow-lg -->

<!-- ✅ Use CSS transitions instead of animations -->
<div class="transition-all duration-300">
```

### 5. Consistency Checklist
- [ ] White backgrounds for cards
- [ ] Primary color for CTAs and links
- [ ] Rounded corners: `rounded-lg`
- [ ] Subtle shadows: `shadow-sm`
- [ ] Hover effects on interactive elements
- [ ] Consistent spacing: `gap-2`, `p-3`, `mb-4`
- [ ] Font sizes from predefined scale
- [ ] RTL-safe positioning
- [ ] HTMX includes all filters
- [ ] Responsive grid breakpoints

---

## 📦 Component Checklist

When creating a new component, ensure:

### Visual Design
- [ ] Uses primary color (#00869E) only
- [ ] White background with `shadow-sm`
- [ ] Rounded corners `rounded-lg`
- [ ] Proper spacing (gap-2, p-3, etc.)
- [ ] Hover effects with transitions
- [ ] Consistent typography scale

### Functionality
- [ ] HTMX attributes if dynamic
- [ ] Proper form handling (CSRF)
- [ ] Loading states
- [ ] Error states
- [ ] Empty states

### Responsiveness
- [ ] Mobile-first design
- [ ] Breakpoint scaling
- [ ] Touch-friendly (min 44px touch targets)
- [ ] Flexible layouts

### RTL Support
- [ ] `dir="rtl"` where needed
- [ ] RTL-safe spacing (`space-x-reverse`)
- [ ] Logical positioning (`start`, `end`)
- [ ] Arabic text alignment

### Accessibility
- [ ] Semantic HTML
- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Color contrast (WCAG AA)
- [ ] Focus states

---

## 🎯 Quick Reference

### Most Common Classes
```tailwind
/* Cards */
bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-3

/* Buttons */
bg-primary hover:bg-primary-700 text-white font-bold py-2 px-4 rounded-lg transition-colors

/* Text */
text-sm text-gray-700
text-base font-bold text-primary
text-[10px] text-gray-500

/* Layout */
grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2
flex items-center justify-between gap-2

/* Spacing */
mb-2 mb-3 mb-4 mb-6 mb-8
p-2 p-3 p-4 p-6 p-8
gap-1 gap-2 gap-3 gap-4
```

---

## 📚 Resources

- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **HTMX Docs**: https://htmx.org/docs
- **Color Palette**: `#00869E` (Primary)
- **Font**: System font stack (font-sans)

---

## 🔄 Updates

**Version**: 1.0  
**Last Updated**: November 2025  
**Status**: Active

### Recent Changes
- Removed secondary color scheme
- Implemented white navbar with primary text
- Added pagination with smart ellipsis
- Compact product grid (5 per row)
- Inline price filter inputs
- Enhanced rating filter (1-5 stars)

---

**Remember**: Consistency is key. When in doubt, refer to existing product pages as the golden standard. Keep it clean, minimal, and professional! 🚀
