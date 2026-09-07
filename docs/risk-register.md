# Public Health Risk Register (Phase 1)

| Risk ID | Identified Risk | Probability | Impact | Mitigation Strategy | Risk Owner |
| --- | --- | --- | --- | --- | --- |
| **R-01** | **Historical Data Lag**: Relying on past attendance misses emerging disease outbreaks in transient populations. | High | High | Emerging Risk Reduction Engine incorporates real-time disease velocity and transit mobility indices to override historical lag. | Lead Analytics Officer |
| **R-02** | **Algorithmic Over-Reliance**: Staff treat automated recommendations as uncritical commands. | Medium | Critical | Mandatory Human-in-the-Loop review gate; system explicitly requires clinician approval before status changes to APPROVED. | Public Health Officer |
| **R-03** | **Hard Constraint Bypass**: Mobile units dispatched to remote zones exceeding travel fuel/time range. | Medium | Medium | Automated hard travel constraint validator flags violations and mandates documented justification before override. | Logistics Coordinator |
| **R-04** | **Discriminatory Targeting Risk**: Algorithmic scores unintentionally proxy sensitive demographic traits. | Low | Critical | Strict aggregate operational variables only (population, risk, service gap, accessibility). Zero protected traits in database. | System Architect |
| **R-05** | **Mobility Data Outdated**: Transit inflow/outflow patterns shift rapidly during holiday/weather events. | Medium | Medium | Allow staff to dynamically adjust mobility weights ($v_3$) in planner configuration panel. | Data Engineering Team |
| **R-06** | **Session Capacity Bottleneck**: Single outreach session reaches <10% of high-density settlement demand. | High | Medium | Error Analysis Engine flags capacity bottlenecks and prompts coordinator to schedule recurring pop-up sessions. | Outreach Coordinator |
