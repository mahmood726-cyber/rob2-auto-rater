
# RoB-2 Auto-Rater Pipeline

An automated Risk of Bias 2 (RoB 2) assessment tool for clinical trials.

## Mechanism
Unlike standard AI readers that hallucinate, this pipeline combines Deterministic Registry Checks (CT.gov) with structured LLM prompts. 

1. **Domain 1 (Randomization):** Checks XML for 'Allocation: Randomized'.
2. **Domain 2 (Deviations):** Checks XML for 'Masking: Quadruple (Blind)'.
3. **Domain 3 (Missing Data):** Compares 'EnrollmentCount' vs 'DenominatorCount' in the API.
4. **Domain 4 (Measurement):** LLM analyzes outcome descriptions.
5. **Domain 5 (Reporting):** Compares primary outcomes between the Protocol phase and the Results phase.

Used inside the E156 Ecosystem to generate provisional RoB-2 Traffic Light plots.

