# 📋 BASWheels - Use Cases & High-Level Design

## Overview
This document outlines three distinct user personas and their interaction patterns with BASWheels, along with a comprehensive system architecture and data flow diagram.

---

## 🎭 Use Case 1: Budget-Conscious Commuter (Aqsa)

### Actor Profile
**Name:** Aqsa  
**Age:** 28  
**Occupation:** School Teacher  
**Budget:** PKR 1.5 - 2.5 Million  
**Key Need:** Reliable daily commute with excellent fuel economy

### Trigger
Aqsa's motorcycle broke down. After repair quotes of PKR 150,000, she decided to save for a car instead. After 6 months of saving, she now has PKR 2 million and needs to find the right car **within the next 2 weeks** before the new academic year starts.

### Preconditions
- ✓ Aqsa has stable income and confirmed budget
- ✓ She has internet access via smartphone
- ✓ She has done basic research on car models
- ✓ She knows her priorities: fuel efficiency, reliability, lower maintenance

### Main Flow

| Step | Actor | System | UI Element |
|------|-------|--------|-----------|
| 1 | Aqsa opens BASWheels URL | Loads Streamlit interface | Home page with "Find Cars" button |
| 2 | Aqsa enters preferences: <br/> • Budget: 1.5M - 2.5M PKR <br/> • Fuel Type: Petrol (good economy) <br/> • Purpose: Commute <br/> • Seats: 5 (solo + occasional passenger) <br/> • Preferences: Economy | System validates inputs | Multi-step form with sliders & dropdowns |
| 3 | Aqsa clicks "Search" | Tavily API queries: "petrol car pakistan 1.5-2.5 million good fuel economy" | Loading spinner |
| 4 | System aggregates results from PakWheels, OLX, CarWale | Extracts: price, fuel type, seats, trunk space, fuel economy | 8-12 car results returned |
| 5 | System runs scoring algorithm | Computes match scores based on: price fit (40%), fuel type (20%), economy (20%), purpose (10%), reliability (10%) | Results sorted descending |
| 6 | Aqsa reviews results: <br/> 1. Honda Civic 1.5 (2020) - 94/100 ✓ <br/> 2. Toyota Corolla (2019) - 91/100 ✓ <br/> 3. Suzuki Swift (2021) - 85/100 | System shows breakdown: "Civic scores high because price is in range (35/40), good fuel economy (18/20), petrol match (20/20)" | Detailed score cards with explanations |
| 7 | Aqsa clicks on Civic for details | Shows: specs, market price range, similar models, price history | Expandable details panel |
| 8 | Aqsa verifies on OLX/PakWheels | Takes system recommendations as guidance for independent verification | External link to source |
| 9 | Aqsa negotiates and purchases | Makes informed decision backed by data | Transaction complete |

### Alternate Flow - No Matches Found

**Condition:** System finds < 3 cars matching all criteria

| Step | Action |
|------|--------|
| A1 | System suggests relaxing one constraint (e.g., "Expand budget by 200K to see 8 more options") |
| A2 | Aqsa adjusts: increases max budget to 2.7M | 
| A3 | System reruns search with new parameters |
| A4 | System displays 10+ results with breakdown |

### Alternate Flow - User Uncertain About Preferences

**Condition:** Aqsa doesn't know what fuel economy is "good"

| Step | Action |
|------|--------|
| A1 | User hovers over "Fuel Economy" input | Tooltip appears: "Average car gets 12 km/l, good = 14-17 km/l, excellent = 18+ km/l" |
| A2 | Aqsa selects "Good (14-17 km/l)" range | System adjusts scoring weights |
| A3 | Results update in real-time |

### Success Criteria
✅ Aqsa identifies 3-5 suitable cars  
✅ She understands why each car ranked as it did  
✅ She makes confident, data-backed purchase decision  
✅ No buyer's remorse (she has objective reasoning)

---

## 🎭 Use Case 2: Luxury Family Traveler (Ahmed)

### Actor Profile
**Name:** Ahmed  
**Age:** 42  
**Occupation:** Business Owner  
**Budget:** PKR 5 - 8 Million  
**Key Need:** Spacious SUV for family trips, weekend getaways

### Trigger
Ahmed's family is growing (3 kids). His current 5-seater sedan isn't enough for road trips. He wants a 7-seater SUV with good trunk space, comfort, and good resale value. He has 3 weeks to decide before his planned trip to northern areas.

### Preconditions
- ✓ Ahmed has adequate budget and financing pre-approved
- ✓ He knows he wants SUV specifically (researched online)
- ✓ He prioritizes space, comfort, brand reputation
- ✓ He can spend 2-3 hours researching

### Main Flow

| Step | Actor | System | Details |
|------|-------|--------|---------|
| 1 | Ahmed accesses BASWheels on desktop | Loads UI in light mode | Full dashboard view |
| 2 | Ahmed fills form: <br/> • Budget: 5M - 8M PKR <br/> • Fuel Type: Any (flexible) <br/> • Vehicle Type: SUV <br/> • Seats: 7 seater <br/> • Purpose: Family/Roadtrip <br/> • Trunk: Prefer 600L+ | Form accepts multi-select purposes | Sliders for price range, checkboxes for purposes |
| 3 | Ahmed clicks "Find Best SUVs" | Tavily searches: "7 seater SUV pakistan 5-8 million family" | API integration with PakWheels, OLX |
| 4 | System returns 12 SUVs and ranks them | Scoring weights: trunk space (25%), seats (20%), price (20%), fuel economy (15%), brand reliability (20%) | Sorted: Toyota Fortuner (97/100), Mahindra XUV700 (94/100), etc. |
| 5 | Ahmed sees detailed breakdown: <br/> "Fortuner: +25 trunk space, +20 7-seater, +20 price fit, +15 fuel, +17 Toyota reliability = 97/100" | Each scoring dimension explained in plain language | Interactive breakdown chart |
| 6 | Ahmed compares top 3 side-by-side: <br/> - Toyota Fortuner vs <br/> - Mahindra XUV700 vs <br/> - Hyundai Santa Fe | System displays comparison table | Visual comparison of all specifications |
| 7 | Ahmed saves notes: "Check Fortuner's 2020 model on PakWheels, verify mileage" | System suggests verification checklist | Notes panel in sidebar |
| 8 | Ahmed visits source links, test drives, and negotiates | Makes informed decision with confidence | Transaction complete |


### Alternate Flow - Budget Adjustment

**Condition:** Ahmed finds fewer options than expected in 5-8M range

| Step | Action |
|------|--------|
| A1 | System suggests: "3 more options available if you extend to 8.5M" | Suggestion widget |
| A2 | Ahmed adjusts budget slider to 8.5M | Real-time update |
| A3 | 7 additional results appear | Seamless experience |

### Success Criteria
✅ Ahmed sees all viable 7-seater options  
✅ Understands trade-offs (Toyota reliability vs Mahindra features vs Hyundai price)  
✅ Confident in top pick backed by data  
✅ Uses system as reference during dealer negotiations

---

## 🎭 Use Case 3: First-Time Buyer on Tight Budget (Zainab)

### Actor Profile
**Name:** Zainab  
**Age:** 24  
**Occupation:** Graphic Designer (freelance)  
**Budget:** PKR 600K - 1.2 Million  
**Key Need:** Cheapest reliable car, new to car buying

### Trigger
Zainab just got her first stable freelance client contract. She needs transportation to client meetings. A friend recommended BASWheels for unbiased advice (friend didn't want to steer her toward expensive options).

### Preconditions
- ✓ Zainab has confirmed PKR 1M budget (savings)
- ✓ She's a first-time buyer, unsure what to prioritize
- ✓ She prefers automatic transmission (easier to drive)
- ✓ She wants minimal maintenance hassle

### Main Flow

| Step | Actor | System | Details |
|------|-------|--------|---------|
| 1 | Zainab opens BASWheels on mobile | Mobile-responsive Streamlit UI | Touch-friendly interface |
| 2 | Zainab enters: <br/> • Budget: 600K - 1.2M PKR <br/> • Condition: Used (new cars too expensive) <br/> • Fuel: Any <br/> • Purpose: Daily commute <br/> • Transmission: Automatic | Form guides her through questions | Dropdowns, not free text |
| 3 | Zainab unsure about transmission - clicks help icon | Tooltip: "Manual = cheaper, Automatic = easier to drive, more expensive" | Contextual help available |
| 4 | Zainab selects "Automatic" | System adjusts search weight for transmission | Updated preferences accepted |
| 5 | System searches: "used automatic car pakistan 600k-1.2m commute" | Tavily aggregates OLX, PakWheels budget section | 15 results returned |
| 6 | System ranks (weights: price 35%, condition 25%, transmission type 20%, reliability 20%) | Top results: <br/> 1. Suzuki Alto 2018 Automatic - 89/100 <br/> 2. Daihatsu Mira 2017 Auto - 85/100 <br/> 3. Honda Civic 2008 Auto - 80/100 | Ranked results |
| 7 | Zainab reviews Alto recommendation: "Great match: within budget (650K), automatic, reliable brand, low maintenance" | Scoring breakdown: Price ✓, Condition ✓, Auto ✓, Reliability ✓ | Clear explanation |
| 8 | Zainab notices disclaimer: "Verify on original source, check vehicle history, test drive" | System reminds to verify independently | Important disclaimer |
| 9 | Zainab visits PakWheels, verifies seller, test drives Alto | Makes purchase with confidence | Transaction complete |

### Alternate Flow - Feature Overwhelm

**Condition:** Zainab confused by too many options

| Step | Action |
|------|--------|
| A1 | System offers: "Beginner Mode" - simplified form | Toggle in sidebar |
| A2 | Beginner form shows only: Budget, Fuel, Purpose (3 questions) | Simplified UX |
| A3 | System auto-sets weights based on first-time buyer profile | Smart defaults |
| A4 | Results are cleaner, easier to understand | Reduced cognitive load |

### Alternate Flow - Very Low Budget

**Condition:** Zainab realizes 600K budget doesn't yield many matches

| Step | Action |
|------|--------|
| A1 | System proactively suggests: "Popular budget options in your range" | Shows market reality |
| A2 | Suggests popular models in 600-1.2M range | Alto, Cultus, WagonR |
| A3 | Recommends focusing on condition & mileage vs price | Guidance for budget segment |

### Success Criteria
✅ Zainab finds 5+ suitable options  
✅ Understands why Alto is best fit (clear breakdown)  
✅ Feels confident making her first car purchase  
✅ No regrets - data-backed, unbiased recommendation

---

## 🏗️ High-Level System Architecture & Data Flow

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        BASWHEELS SYSTEM                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   USER INTERFACE     │
│   (Streamlit)        │
│ • Preference Form    │
│ • Results Display    │
│ • Score Breakdown    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│         PREFERENCE INPUT LAYER                           │
│ ◆ Budget Range (Min-Max Slider)                         │
│ ◆ Fuel Type (Dropdown: Petrol/Diesel/EV/Hybrid/Any)     │
│ ◆ Condition (Radio: New/Used/Either)                    │
│ ◆ Vehicle Type (Multi-select: Sedan/SUV/Hatchback/etc)  │
│ ◆ Purposes (Checkboxes: Commute/Family/Luxury/Roadtrip) │
│ ◆ Specs (Seats, Trunk Size, Transmission, etc.)         │
└──────────┬───────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│    API INTEGRATION LAYER (api_fetch.py)                 │
│                                                          │
│    ┌────────────────┐                                   │
│    │ Tavily Search  │  Query: "petrol car pakistan      │
│    │     Engine     │  1.5-2.5M commute good fuel"     │
│    └────────┬───────┘                                   │
│             │                                           │
│    ┌────────▼────────────────────────────────────────┐ │
│    │ Search Multiple Sources                        │ │
│    │ • PakWheels.com (top dealer site)              │ │
│    │ • OLX.com.pk (C2C marketplace)                 │ │
│    │ • CarWale.com (South Asia auto data)           │ │
│    └────────┬───────────────────────────────────────┘ │
│             │                                          │
│    ┌────────▼────────────────────────────────────────┐ │
│    │ Tavily API Response: 10 results with:           │ │
│    │ • Title: "2020 Honda Civic 1.5"                │ │
│    │ • URL: source link                              │ │
│    │ • Content: full description                      │ │
│    └────────┬───────────────────────────────────────┘ │
└──────────┬───────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│    DATA EXTRACTION LAYER (api_fetch.py parsing)         │
│                                                          │
│  For each search result, extract:                       │
│  ◆ Price: regex patterns for "lac", "million", "PKR"   │
│  ◆ Fuel Type: keyword match (petrol/diesel/ev/hybrid)  │
│  ◆ Condition: "new" or "used" keyword detection        │
│  ◆ Seats: regex "5 seater", "7 seater"                │
│  ◆ Trunk Space: regex "350L", "400 liters"             │
│  ◆ Fuel Economy: regex "12 km/l", "km/l" patterns      │
│  ◆ Tags: infer from text (family=sedan, luxury, etc)   │
│  ◆ Reliability Rating: brand-based lookup (Toyota=4.5) │
│                                                          │
│  Output: Structured DataFrame                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ Car     │ Price  │ Fuel │ Seats │ Trunk │  │       │
│  │ Civic   │ 2.3M   │ Pet  │ 5     │ 385L  │  │       │
│  │ Corolla │ 2.1M   │ Pet  │ 5     │ 420L  │  │       │
│  │ Swift   │ 1.8M   │ Pet  │ 5     │ 268L  │  │       │
│  └─────────────────────────────────────────────┘       │
└──────────┬───────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│    SCORING & RANKING LAYER (scoring.py)                │
│                                                          │
│  1. NORMALIZATION: Scale all metrics to 0-1            │
│     • Price: Is it in user's budget range?             │
│     • Trunk: Compare across all results               │
│     • Fuel Economy: Compare across all results         │
│                                                          │
│  2. SCORING (7 Criteria):                             │
│     • Price Match (40% weight)                        │
│       └─ If 1.5M-2.5M range: score = 1.0            │
│       └─ If outside range: linear decay               │
│     • Fuel Type (20% weight)                          │
│       └─ Exact match = 1.0, Hybrid = 0.7, EV = 0.6  │
│     • Condition (New/Used) (15% weight)               │
│     • Purpose Alignment (10% weight)                  │
│       └─ "Commute" tag in car = +10%                 │
│     • Trunk Space (8% weight)                         │
│     • Fuel Economy (5% weight)                        │
│     • Reliability Rating (2% weight)                  │
│                                                          │
│  3. WEIGHTED SUM:                                      │
│     TOTAL_SCORE = (price × 0.40) + (fuel × 0.20)      │
│                   + (condition × 0.15) + ...           │
│                                                          │
│  4. RANKING: Sort by TOTAL_SCORE descending           │
│     Top result: Honda Civic - 94/100                  │
│     2nd result: Toyota Corolla - 91/100              │
│     3rd result: Suzuki Swift - 85/100                │
│                                                          │
│  Output: Ranked list with detailed breakdowns         │
└──────────┬───────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│    PRESENTATION LAYER (main.py - Streamlit)            │
│                                                          │
│  Display Results:                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🏆 #1: Honda Civic 2020 - 94/100 ⭐⭐⭐⭐⭐     │   │
│  │                                                 │   │
│  │ Why this match:                                 │   │
│  │  ✓ Price: 2.3M (Your range: 1.5-2.5M)        │   │
│  │    Score: 35/40                                │   │
│  │  ✓ Fuel: Petrol (Your preference: Petrol)     │   │
│  │    Score: 20/20                                │   │
│  │  ✓ Condition: Used (Your choice: Either)      │   │
│  │    Score: 15/15                                │   │
│  │  ✓ Purpose: Good for Commute                  │   │
│  │    Score: 10/10                                │   │
│  │  ✓ Trunk: 385L (Better than 60% of options)   │   │
│  │    Score: 8/8                                  │   │
│  │  ✓ Fuel Economy: 14 km/l (Good)               │   │
│  │    Score: 4/5                                  │   │
│  │  ✓ Reliability: Honda (Excellent brand)       │   │
│  │    Score: 2/2                                  │   │
│  │                                                 │   │
│  │ [View Details] [Visit Source] [Compare]       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Dark/Light Theme Toggle (User Preference)             │
│  Mobile Responsive Layout                              │
│  Navigation: Find Cars | Score Analysis | Settings     │
└──────────────────────────────────────────────────────────┘
```

### Data Flow Sequence (Detailed)

```
1. USER INPUT
   ├─ Submits preference form via Streamlit
   └─ System validates all inputs

2. QUERY CONSTRUCTION
   ├─ Builds search query: "[fuel_type] car [country] 
   │  [min_price]-[max_price] [purposes]"
   └─ Example: "petrol car pakistan 1500000-2500000 commute"

3. TAVILY API CALL
   ├─ Sends query to Tavily Search Engine
   ├─ Specifies: max_results=10, include_domains=[sources]
   └─ Receives: title, content, URL for each result

4. DATA EXTRACTION
   ├─ For each result, run regex patterns
   ├─ Extract: price, fuel, seats, trunk, economy, condition
   ├─ Lookup: reliability rating by car brand
   └─ Output: Structured DataFrame with 10-12 cars

5. SCORING ALGORITHM
   ├─ Normalize price across result set
   ├─ Normalize fuel economy across result set
   ├─ Normalize trunk space across result set
   ├─ Apply user preference weights
   ├─ Calculate individual scores (0-1)
   ├─ Calculate weighted total (0-100)
   └─ Create breakdown explanation for each car

6. RANKING
   ├─ Sort cars by total score (descending)
   └─ Rank: 1st place to 10th place

7. PRESENTATION
   ├─ Render in Streamlit UI
   ├─ Show: Car name, score, breakdown, source link
   ├─ Enable: Dark/light mode, responsive design
   └─ Allow: Click for details, compare cars
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.52.1 | Web UI, forms, visualization |
| **Search API** | Tavily API | Real-time market data aggregation |
| **Data Processing** | Pandas 2.3.3 | Structured data handling |
| **Data Extraction** | Python Regex | Price/spec parsing |
| **Scoring Engine** | NumPy 2.3.5 | Numerical computations |
| **Visualization** | Altair 6.0.0 | Interactive charts |
| **Backend Logic** | Python 3.8+ | Core algorithms |
| **Environment Mgmt** | python-dotenv 1.2.1 | API key management |
| **HTTP Requests** | Requests 2.32.5 | API communication |

---

## 🔄 Example Data Flow: Aqsa's Journey

```
START: Aqsa opens BASWheels
  │
  ├─► Enters form: Budget PKR 1.5-2.5M, Fuel=Petrol, Purpose=Commute
  │
  ├─► Clicks "Find Cars"
  │
  ├─► System constructs: "petrol car pakistan 1500000-2500000 commute"
  │
  ├─► Tavily API queries: PakWheels, OLX, CarWale
  │   └─ Returns 10 results with titles & descriptions
  │
  ├─► Extraction regex runs:
  │   ├─ Honda Civic: 2.3M, petrol, 5 seat, 385L trunk, 14 km/l
  │   ├─ Toyota Corolla: 2.1M, petrol, 5 seat, 420L trunk, 14 km/l
  │   └─ Suzuki Swift: 1.8M, petrol, 5 seat, 268L trunk, 17 km/l
  │
  ├─► Scoring algorithm:
  │   ├─ Civic: 35/40 price + 20/20 fuel + 0/0 seats + 8/8 trunk + 
  │   │          4/5 economy + 2/2 reliability = 94/100 ✅
  │   ├─ Corolla: 40/40 price + 20/20 fuel + 8/8 trunk + 4/5 economy + 2/2 = 91/100
  │   └─ Swift: 40/40 price + 20/20 fuel + 5/8 trunk + 5/5 economy + 2/2 = 85/100
  │
  ├─► Ranking: Civic #1, Corolla #2, Swift #3
  │
  ├─► Display in Streamlit:
  │   ├─ Civic card with: 94/100, price ✓, fuel ✓, economy ✓
  │   ├─ Explanation: "Best match: within budget, petrol as preferred, 
  │   │               good fuel economy (14 km/l)"
  │   └─ Link to source: PakWheels listing
  │
  └─► END: Aqsa makes informed decision
```

---

## 🎯 Design Principles

1. **Transparency** - All scores explained, no black boxes
2. **Simplicity** - 3-5 input fields, clear results
3. **Trust** - No seller bias, data-driven recommendations
4. **Accessibility** - Mobile-responsive, multiple themes
5. **Speed** - < 5 seconds from form to ranked results
6. **Extensibility** - Easy to add new data sources or scoring criteria

---

**Document Version:** 1.0  
**Last Updated:** December 7, 2025  
**Status:** Complete
