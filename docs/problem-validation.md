# Problem Validation & Stakeholder Discovery Plan

**Project:** Vaccination Outreach Planner for Mobile & Under-Served Populations  
**Phase:** Phase 1 Deliverable  

---

## 1. Problem Validation Hypothesis

> **Hypothesis:** "City health department vaccination outreach resource allocation relies too heavily on historical averages instead of emerging local risk, leading to delayed outbreak detection, misallocated mobile clinics, and missed under-served populations."

---

## 2. Targeted Stakeholder Discovery Questions

### A. Public Health Officers & Program Managers
1. How are mobile vaccination clinic routes currently decided prior to seasonal disease peaks?
2. How far in advance are outreach budgets committed based on past attendance metrics?
3. What data sources are currently combined manually when evaluating an outbreak risk signal?

### B. Outreach Coordinators & Field Logistics Staff
1. How frequently do mobile outreach sessions suffer from either unused excess capacity or severe overcrowding?
2. What physical travel boundaries (e.g. road access, travel distance from health base) limit your mobile team deployment?
3. What notice is required to redirect a scheduled mobile clinic to an emerging high-risk zone?

### C. Clinicians & Authorised Reviewers
1. What level of algorithmic explainability do you require before approving an automated location recommendation?
2. What operational constraints (e.g. cold-chain storage capacity, staffing limits) must NEVER be bypassed without recorded justification?

### D. Under-Served & Mobile Population Representatives
1. What are the primary access barriers preventing attendance at central health clinics (e.g. travel distance, transit cost, working hours)?
2. How do mobile market vendors or seasonal workers receive information about local pop-up vaccination points?

---

## 3. Pain Confirmation vs. Invalidation Evidence Criteria

| Evidence Type | Confirms Hypothesis (Pain Exists) | Invalidates Hypothesis (Pain Resolved) |
| --- | --- | --- |
| **Resource Allocation** | >60% of mobile clinics are sent to historical locations despite zero emerging disease signals. | Outreach routes dynamically shift weekly based on surveillance data. |
| **Outbreak Response** | High-risk outbreaks in under-served zones take >14 days to receive outreach support. | Outbreak zones receive mobile pop-up support within <48 hours. |
| **Session Capacity** | Session capacity utilization fluctuates wildly (<40% or >150% overflow). | Session utilization remains consistent at 80–95%. |
| **Data Combination** | Staff spend >10 hours/week manually combining spreadsheets. | Integrated dashboard displays combined risk and service history automatically. |

---

## 4. Simulated Stakeholder Validation Feedback (Phase 1 Prototype)

> [!NOTE]
> *The feedback below is synthetic/simulated for Phase 1 college project evaluation purposes.*

```json
[
  {
    "stakeholder": "Dr. Aris Thorne (Public Health Officer)",
    "feedback": "Historical average planning repeatedly sent our mobile team to Suburb North because past attendance was high, while Eastside Market had zero coverage during a flu spike. The dual-objective planner highlighting emerging risk spikes solves this directly.",
    "status": "PAIN_CONFIRMED"
  },
  {
    "stakeholder": "Elena Rostova (Outreach Field Coordinator)",
    "feedback": "The hard travel distance constraint check is critical. Automated suggestions often select remote locations without considering our 12 km mobile bus range. Being able to record a mandatory override reason keeps our operations accountable.",
    "status": "PAIN_CONFIRMED"
  }
]
```
