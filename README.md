# City Health Department Monitoring Seasonal Infectious Disease — Vaccination Outreach Planner for Mobile & Under-Served Populations

> **Phase 1 Software Prototype (40% Milestone)**  
> *A human-in-the-loop decision support system for planning seasonal vaccination outreach using aggregate non-discriminatory population risk indicators.*

---

## 🌟 Core System Highlights

1. **Surveillance & Area Explorer**: Aggregate demographic and disease risk monitoring across 12 synthetic city zones with interactive Leaflet maps.
2. **Dual-Objective Recommendation Engine**: Compare **Objective A (Maximum Eligible Reach)** vs **Objective B (Emerging Risk Reduction)** against the **Historical Average Baseline**.
3. **Hard & Soft Constraint Engine**: Enforces travel distance boundaries and session capacity limits, flagging infeasible allocations for mandatory human review.
4. **100% Explainable Recommendations**: Visual factor score breakdowns explaining why each zone was selected.
5. **Human Review & Audit Trail Console**: Authorised clinicians/reviewers can Accept, Modify, Reject, or Override recommendations. Overrides mandate documented justification logged permanently for audit compliance.
6. **Empirical Evaluation & Error Analysis**: Benchmark showing +22% reach efficiency gain over historical baselines, alongside 4 detailed algorithmic error/failure mode walkthroughs.
7. **Privacy & Responsible AI**: Uses 100% synthetic aggregate data. Zero personal health information (PHI) or protected characteristics.

---

## 🚀 How to Run the Prototype

### Prerequisites
- Python 3.10+
- Node.js v18+ and npm

### Quick Start (Windows)
Double-click `run_app.bat` or execute in PowerShell:
```powershell
.\run_app.bat
```

### Manual Launch

#### 1. Start FastAPI Backend Server
```powershell
# Set PYTHONPATH to include backend folder
$env:PYTHONPATH="backend"
python backend/main.py
```
*Backend API runs at: `http://127.0.0.1:8000`*  
*Swagger API Docs at: `http://127.0.0.1:8000/docs`*

#### 2. Start React + Vite Frontend Dev Server
```powershell
cd frontend
npm install
npm run dev
```
*Frontend runs at: `http://localhost:3000`*

#### 3. Run Backend Unit Tests
```powershell
$env:PYTHONPATH="backend"
python -m pytest tests/
```

---

## 📁 Repository Structure

```text
c:\city health/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (areas, planner, reviews, eval)
│   │   ├── core/         # Config & database setup
│   │   ├── data/         # Synthetic seed data builder (12 city areas)
│   │   ├── models/       # SQLAlchemy ORM & Pydantic validation models
│   │   └── planner/      # Baseline, Reach Engine, Risk Engine, Constraints, Evaluator
│   ├── main.py           # FastAPI entrypoint
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Navbar, AreaMap, StatCard, RecommendationCard, ReviewModal, etc.
│   │   ├── pages/        # Dashboard, AreaExplorer, OutreachPlanner, ReviewConsole, Eval, Journeys
│   │   ├── services/     # REST API service client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css     # Design system CSS tokens
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── docs/                 # Complete Phase 1 documentation artifacts
│   ├── problem-validation.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── data-schema.md
│   ├── user-journeys.md
│   ├── risk-register.md
│   └── phase-1.md
│
├── tests/                # Pytest unit test suite
│   ├── test_scoring.py
│   ├── test_constraints.py
│   └── test_audit_flow.py
│
├── run_app.bat
└── README.md
```

---

## 🔬 Demonstration Story Walkthrough

To verify the core problem story during demonstration:

1. Open **Dashboard**: Notice the Critical Alert highlighting **Eastside Railway Market (AREA-07)** with a severe emerging risk spike (`0.96`), but low historical attendance (`95 visits`).
2. Go to **Outreach Planner**:
   - Select **Historical Average Baseline** $\rightarrow$ Click *Generate Plan*. Notice Area 07 is ranked low (**#10**), demonstrating how historical averages miss emerging outbreaks!
   - Switch to **Emerging Risk Reduction (Proposed)** $\rightarrow$ Click *Generate Plan*. Notice Area 07 is elevated to **Rank #1 Priority**!
3. Click **Objective Comparison Matrix**: View the side-by-side rank shift table highlighting Area 07's elevation.
4. Go to **Review Console**:
   - Inspect Area 11 or Area 09 recommendation flagged with `HARD_TRAVEL_EXCEEDED`.
   - Click **Override Hard Constraint**. Enter justification reason (e.g., *"Secondary mobile van route authorized"*).
   - Switch to **Public Health Audit Log** tab and verify the audit record logged permanently with timestamp and justification.
5. Go to **Evaluation & Error Analysis**: View the Recharts performance chart showing eligible reach gain per session and inspect the 4 failure mode scenarios.
