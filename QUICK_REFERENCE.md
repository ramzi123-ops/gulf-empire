# 🚀 Quick Reference Guide

> Fast lookup for common patterns and components

---

## 🎨 Color Usage

```tailwind
Primary:      bg-primary, text-primary, border-primary
Hover:        hover:bg-primary-700, hover:text-primary-600
Light BG:     bg-primary-50
White Cards:  bg-white
Borders:      border-gray-200, border-gray-300
Text:         text-gray-900 (dark), text-gray-700 (body), text-gray-600 (secondary)
```

---

## 📐 Common Layouts

### Product Grid (5 per row)
```html
<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
  <!-- Product cards -->
</div>
```

### Sidebar + Content
```html
<div class="flex flex-col lg:flex-row gap-2">
  <aside class="lg:w-50 flex-shrink-0">...</aside>
  <div class="flex-1">...</div>
</div>
```

### Page Container
```html
<div class="container mx-auto px-2 sm:px-4 pb-8 pt-2">
  <!-- Content -->
</div>
```

---

## 🧩 Component Snippets

### Product Card
```html
<div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
  <a href="#" class="block relative overflow-hidden">
    <img class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
  </a>
  <div class="p-3">
    <a href="#" class="block font-medium text-sm text-gray-900 hover:text-primary transition-colors mb-3">Name</a>
    <div class="flex items-center justify-between gap-2">
      <span class="text-base font-bold text-primary">299 ﷼</span>
      <button class="bg-primary hover:bg-primary-700 text-white p-2 rounded-lg transition-colors">
        <svg class="w-5 h-5">...</svg>
      </button>
    </div>
  </div>
</div>
```

### Primary Button
```html
<button class="bg-primary hover:bg-primary-700 text-white font-bold py-4 px-6 rounded-lg transition-colors">
  Text
</button>
```

### Input Field
```html
<input 
  type="text"
  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
```

### Badge
```html
<span class="bg-primary text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">جديد</span>
```

---

## ⚡ HTMX Patterns

### Filter
```html
<input 
  type="checkbox"
  hx-get="{% url 'store:product_list' %}"
  hx-target="#product-grid"
  hx-include="[name='category'],[name='brand'],[name='search'],[name='min_price'],[name='max_price'],[name='rating']">
```

### Add to Cart
```html
<form 
  hx-post="{% url 'orders:add_to_cart' product.id %}"
  hx-target="#mini-cart"
  hx-swap="outerHTML">
  {% csrf_token %}
  <button type="submit">Add</button>
</form>
```

---

## 📱 Responsive Breakpoints

```tailwind
sm:  640px   /* Tablet portrait */
md:  768px   /* Tablet landscape */
lg:  1024px  /* Desktop */
xl:  1280px  /* Large desktop */
```

---

## 🌐 RTL Safe Classes

```tailwind
Use:  space-x-reverse, start-0, end-0, ms-4, me-4, ps-4, pe-4
Avoid: left-0, right-0, ml-4, mr-4, pl-4, pr-4
```

---

## 📏 Spacing Scale

```tailwind
gap-1:  4px    p-2:  8px    mb-2:  8px
gap-2:  8px    p-3:  12px   mb-3:  12px
gap-3:  12px   p-4:  16px   mb-4:  16px
gap-4:  16px   p-6:  24px   mb-6:  24px
gap-6:  24px   p-8:  32px   mb-8:  32px
gap-8:  32px
```

---

## 🔤 Typography Scale

```tailwind
text-[10px]  - Tiny (badges)
text-xs      - Small (12px)
text-sm      - Body (14px)
text-base    - Default (16px)
text-lg      - Large (18px)
text-2xl     - Heading (24px)
text-3xl     - Title (30px)
```

---

## ✅ Quick Checklist

When creating a new page:
- [ ] White background cards with `shadow-sm`
- [ ] Primary color (#00869E) for CTAs
- [ ] Rounded corners `rounded-lg`
- [ ] Hover effects with `transition-colors`
- [ ] RTL-safe positioning (`start`, `end`)
- [ ] Responsive grid breakpoints
- [ ] HTMX with `hx-include` for filters
- [ ] Proper spacing from scale
- [ ] Mobile-first approach

---

**For detailed documentation, see `DESIGN_SYSTEM.md`**
