# Gulf Emperor Color Guide

## Brand Colors

### Primary Color - Teal (#00869E)
The main brand color used for:
- Primary buttons and CTAs
- Navigation active states
- Product prices
- Important highlights
- Links and interactive elements

**Tailwind Classes:**
```html
<!-- Backgrounds -->
<div class="bg-primary">Primary background</div>
<div class="bg-primary-700">Darker primary</div>

<!-- Text -->
<p class="text-primary">Primary text</p>
<a class="text-primary hover:text-primary-700">Link</a>

<!-- Buttons -->
<button class="bg-primary hover:bg-primary-700 text-white">
  Primary Button
</button>

<!-- Borders -->
<div class="border-primary">Border</div>
```

**Color Palette:**
- primary-50: #E6F7FA (lightest)
- primary-100: #CCEFF5
- primary-200: #99DFEB
- primary-300: #66CFE1
- primary-400: #33BFD7
- **primary-500: #00869E** (base)
- primary-600: #006B7E
- primary-700: #00505F
- primary-800: #00353F
- primary-900: #001A20 (darkest)

---

### Secondary Color - Deep Blue (#065084)
The secondary brand color used for:
- Secondary buttons
- Accent elements
- Headers and titles
- Alternative CTAs
- Badges and labels

**Tailwind Classes:**
```html
<!-- Backgrounds -->
<div class="bg-secondary">Secondary background</div>
<div class="bg-secondary-700">Darker secondary</div>

<!-- Text -->
<p class="text-secondary">Secondary text</p>
<h1 class="text-secondary font-bold">Heading</h1>

<!-- Buttons -->
<button class="bg-secondary hover:bg-secondary-700 text-white">
  Secondary Button
</button>

<!-- Badges -->
<span class="bg-secondary text-white px-3 py-1 rounded">Badge</span>
```

**Color Palette:**
- secondary-50: #E6F0F8 (lightest)
- secondary-100: #CCE1F1
- secondary-200: #99C3E3
- secondary-300: #66A5D5
- secondary-400: #3387C7
- **secondary-500: #065084** (base)
- secondary-600: #05406A
- secondary-700: #04304F
- secondary-800: #032035
- secondary-900: #01101A (darkest)

---

## Usage Examples

### Buttons
```html
<!-- Primary Action -->
<button class="bg-primary hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg">
  إضافة إلى السلة
</button>

<!-- Secondary Action -->
<button class="bg-secondary hover:bg-secondary-700 text-white font-semibold py-3 px-6 rounded-lg">
  المزيد من التفاصيل
</button>

<!-- Outline Button -->
<button class="border-2 border-primary text-primary hover:bg-primary hover:text-white py-3 px-6 rounded-lg">
  عرض الكل
</button>
```

### Cards with Both Colors
```html
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <!-- Header with Secondary -->
  <div class="bg-secondary text-white p-4">
    <h3 class="text-xl font-bold">عنوان البطاقة</h3>
  </div>
  
  <!-- Content -->
  <div class="p-6">
    <p class="text-gray-700 mb-4">محتوى البطاقة</p>
    
    <!-- Price with Primary -->
    <p class="text-2xl font-bold text-primary">250 ر.س</p>
    
    <!-- Button with Primary -->
    <button class="bg-primary hover:bg-primary-700 text-white w-full py-2 rounded">
      شراء الآن
    </button>
  </div>
</div>
```

### Navigation
```html
<nav class="bg-secondary">
  <a href="#" class="text-white hover:text-primary transition">
    الرئيسية
  </a>
  <a href="#" class="text-white hover:text-primary transition">
    المنتجات
  </a>
</nav>
```

### Badges
```html
<!-- Primary Badge -->
<span class="bg-primary text-white text-xs px-3 py-1 rounded-full">
  جديد
</span>

<!-- Secondary Badge -->
<span class="bg-secondary text-white text-xs px-3 py-1 rounded-full">
  مميز
</span>
```

---

## Color Combinations

### Recommended Pairings:
1. **Primary background + White text** - High contrast, good for buttons
2. **Secondary background + White text** - Professional, good for headers
3. **White background + Primary text** - Clean, good for links
4. **Gray background + Secondary text** - Subtle, good for secondary info
5. **Primary + Secondary together** - Use primary for main actions, secondary for supporting elements

### Accessibility:
- Both colors meet WCAG AA standards when used with white text
- Primary (#00869E) contrast ratio with white: 4.5:1
- Secondary (#065084) contrast ratio with white: 8.5:1

---

## Quick Reference

| Element | Recommended Color |
|---------|-------------------|
| Primary CTA Buttons | `bg-primary` |
| Secondary Buttons | `bg-secondary` |
| Product Prices | `text-primary` |
| Headings | `text-secondary` or `text-primary` |
| Links | `text-primary hover:text-primary-700` |
| Active States | `bg-primary` or `text-primary` |
| Badges (New) | `bg-primary` |
| Badges (Featured) | `bg-secondary` |
| Navigation Bar | `bg-secondary` or `bg-white` |
| Footer | `bg-secondary-900` |
