# SoulSkill Development Roadmap Plan

## Overview
This plan converts the proposed SaaS roadmap into an actionable implementation sequence for the existing SoulSkill app while preserving current resume functionality and backend behavior.

## Sprint 1 — Foundation
### Goals
- Deliver the refreshed AI Career Growth Platform experience
- Improve navigation and information architecture
- Introduce dashboard and career readiness placeholders

### Planned work
- Finalize the new landing page experience in the Streamlit app
- Keep the existing resume builder as a module inside Career Toolkit
- Add clear navigation between Overview, Career Journey, Dashboard, Toolkit, Coach, Interview, and EQ Growth
- Introduce a visible Career Readiness Score placeholder and supporting metrics
- Ensure all current functionality remains accessible without breaking changes

### Acceptance criteria
- Modern, responsive UI experience
- No backend rewrites
- Resume builder remains functional
- Navigation feels coherent and product-like

## Sprint 2 — AI Career Coach
### Goals
- Add a conversational coaching experience
- Provide career path suggestions and guidance

### Planned work
- Build a structured coaching panel with guided prompts
- Add placeholder conversation flow and recommendation cards
- Connect coaching suggestions to user profile and career goals

### Acceptance criteria
- Users can access a coaching experience from the main navigation
- Recommendations are contextual and easy to understand
- UI is modular and reusable

## Sprint 3 — Emotional Intelligence
### Goals
- Introduce EQ-based growth experiences
- Support confidence and communication coaching

### Planned work
- Add EQ assessment prompts and reflection modules
- Create communication coaching cards and confidence-building guidance
- Keep the experience lightweight and modular

### Acceptance criteria
- Users can browse EQ-related content and next-step modules
- Coaching insights are clearly presented
- Experience remains consistent with the broader platform style

## Sprint 4 — Career Assessment
### Goals
- Add structured assessment and growth planning
- Improve readiness analysis and skill gap visibility

### Planned work
- Introduce assessment screens for skills, career stage, and growth areas
- Present a more detailed readiness score and growth plan
- Link assessment insights back to the toolkit and coaching modules

### Acceptance criteria
- Users can understand where they stand in their career readiness
- Growth plans are personalized and actionable
- Existing resume features remain unaffected

## Sprint 5 — Monetization
### Goals
- Prepare the product for SaaS growth and subscriptions

### Planned work
- Add authentication flow polish and account state handling
- Introduce free vs. Pro experience and upgrade prompts
- Prepare Razorpay integration points for subscription billing
- Add subscription management placeholders and onboarding flow

### Acceptance criteria
- Product can support free and paid usage paths
- Monetization flow is clearly separated from the core app experience
- Existing functionality remains intact for free users

## Implementation Notes
- Keep UI modular and component-driven
- Separate UI and business logic where possible
- Reuse Streamlit components and shared styling patterns
- Avoid breaking the current resume generation and export flows
- Favor incremental delivery over large rewrites
