# 🚗 BASWheels - Problem Statement

## Executive Overview

BASWheels addresses a critical market gap in the automotive purchasing journey. While millions of consumers save money for a car purchase, they face a fundamentally broken information market where sellers have all the leverage and buyers have none.

---

## 🎯 The Problem

### User Profile
**Primary Users:** First-time and inexperienced car buyers in South Asia (Pakistan, with potential expansion to regional markets) who are making a significant financial decision without expert guidance.

### Pain Points

| Pain Point | Impact | Severity |
|-----------|--------|----------|
| **Information Asymmetry** | Sellers exploit buyer naivety; buyers don't know what questions to ask or what's a fair price | 🔴 Critical |
| **No Personalized Guidance** | Existing platforms (PakWheels, OLX) show all cars, not matching buyer's specific needs | 🔴 Critical |
| **Preference Confusion** | Buyers unclear on how to balance price, fuel type, family needs, trunk space, and other factors | 🟠 High |
| **Scattered Data Sources** | Car information spread across multiple sites; buyers spend hours cross-referencing | 🟠 High |
| **No Scoring Transparency** | Even when recommendations exist, buyers don't understand WHY a car is suggested | 🟡 Medium |
| **Impulse Decisions** | Without structured decision-making, buyers often regret purchases post-sale | 🔴 Critical |

### Why It Matters

Car purchases represent **6-12 months of average salary** for most users in our target market. A poor decision results in:
- ✗ Financial loss (overpayment, repairs, poor resale value)
- ✗ Quality of life impact (unreliable vehicle, high fuel costs)
- ✗ Emotional stress (buyer's remorse, vendor disputes)

**The gap:** No affordable, transparent, preference-driven car recommendation system exists in South Asia.

---

## 🎯 MVP Goal

Create a **preference-based car recommendation engine** that:

1. ✅ Collects structured user preferences (budget, fuel type, use case, family needs)
2. ✅ Fetches real-time car data from online marketplaces using Tavily API
3. ✅ Ranks matches based on how well they align with user preferences
4. ✅ Explains scoring breakdowns so users understand recommendations
5. ✅ Provides transparent, unbiased guidance independent of seller incentives

### MVP Accomplishments
- ✅ Built fully functional Streamlit UI with dark/light mode
- ✅ Integrated Tavily API for real-time market data aggregation
- ✅ Implemented intelligent scoring algorithm (7 criteria: price, fuel, condition, purpose, trunk, economy, reliability)
- ✅ Created breakdown explanations showing why each car ranked as it did
- ✅ Deployed preference form with dropdowns, sliders, and multi-select inputs
- ✅ Responsive design optimized for mobile and desktop

---

## 📋 Scope & Out-of-Scope

### ✅ IN SCOPE (MVP + Near Term)
- Preference collection from users
- Real-time car data aggregation from multiple sources (PakWheels, OLX, CarWale)
- Intelligent ranking based on preference alignment
- Transparent scoring explanations
- Mobile-responsive UI
- Dark/Light theme support
- Local testing and deployment

### ❌ OUT-OF-SCOPE (Future Releases)
- **Direct seller connection** - Users cannot contact sellers through the app yet; they must verify details independently
- **Seller verification/ratings** - No seller reputation system in MVP
- **Finance/loan integration** - Payment plans and financing options deferred to v2.0
- **Insurance recommendations** - Will be added in future releases
- **Maintenance tracking** - Post-purchase features dependant
- **Vehicle history reports** - Accident/damage history analysis (compliance considerations)
- **Multilingual support** - Currently English only; Urdu/other languages in v2.0
- **Offline functionality** - Requires live internet connection
- **User accounts/saved preferences** - Stateless MVP; future release will add persistence

---

## 📊 Assumptions

### Technical Assumptions
1. **Tavily API availability** - Assumes Tavily API remains available and responsive (API key valid)
2. **Data quality** - Assumes scraped car data contains sufficient detail for accurate extraction
3. **Regex patterns work** - Assumes price, specs are formatted consistently across source sites
4. **Python 3.8+** - Target environment has Python 3.8 or higher
5. **Streamlit compatibility** - Assumes modern browsers support Streamlit's web interface

### User Assumptions
1. **Basic technical literacy** - Users can navigate a web form and understand English
2. **Honest preferences** - Users provide genuine budget and preference inputs
3. **Internet access** - Users have stable internet for searching/verification
4. **Pakistani market knowledge** - Current MVP assumes familiarity with PKR pricing and local car models
5. **Decision-ready** - Users are actively in market, not just browsing

### Market Assumptions
1. **Data availability** - Car listings available on PakWheels, OLX, CarWale with required details
2. **Market homogeneity** - Top 50-100 cars cover 80% of market demand
3. **Preference stability** - User preferences remain consistent during search session
4. **Cost sensitivity** - Price is significant factor for target users (not luxury market)

### Business Assumptions
1. **Free model viability** - Users willing to use free tool for unbiased recommendations
2. **Trust in algorithm** - Users trust ML-based scoring over salesman recommendations
3. **No legal friction** - Web scraping from listed sources doesn't violate TOS (future: partner with platforms)

---

## 🎓 Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| **Functionality** | All core features operational | ✅ 100% |
| **Performance** | Search response time | < 5 seconds |
| **Accuracy** | Preference match rate | > 80% |
| **Usability** | Form completion rate | > 90% |
| **User Satisfaction** | Would recommend score | > 4/5 stars |

---

## 🚀 Next Steps (Post-MVP)

- [ ] Gather user feedback from beta testers
- [ ] Expand to other South Asian markets
- [ ] Add seller verification system
- [ ] Integrate financing options
- [ ] Build user accounts for saved preferences
- [ ] Implement insurance comparisons

---

**Document Version:** 1.0  
**Last Updated:** December 7, 2025  
**Status:** MVP Complete - Ready for Testing
