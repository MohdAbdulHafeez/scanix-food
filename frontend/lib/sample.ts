import type { ScanResult } from "./types";

/* A representative dossier so the UI can be explored before the OCR
   backend is running. Shaped exactly like a real /api/v1/scan response.
   Product is fictional; the numbers are plausible for an Indian
   ultra-processed snack. */

export const SAMPLE_SCAN: ScanResult = {
  success: true,
  metadata: {
    scan_id: "scan_3f9c1ad7sample",
    timestamp: "2026-06-10T09:42:11Z",
    processing_time_ms: 4180,
    audit_trail: {
      ocr_corrected:
        "CRUNCHWAVE MASALA MAGIC\nNet Qty 52g\nINGREDIENTS: Refined Palm Oil, Potato, Rice Flour, " +
        "Corn Flour, Iodised Salt, Sugar, Spices & Condiments, Maltodextrin, Acidity Regulator (330), " +
        "Flavour Enhancers (627, 631), Anticaking Agent (551), Antioxidant (319), Added Flavours " +
        "(Natural & Artificial). CONTAINS: Wheat, Milk. May contain Soy.\n" +
        "NUTRITIONAL INFORMATION (per 100g): Energy 538 kcal, Protein 6.8 g, Carbohydrate 56.2 g, " +
        "Total Sugars 7.4 g, Total Fat 31.5 g, Saturated Fat 14.8 g, Sodium 712 mg, Fibre 2.1 g.\n" +
        "FSSAI Lic. No. 10012021000123\nNo Added MSG  •  Baked Goodness  •  Real Masala",
    },
  },
  product: {
    product_name: "Crunchwave Masala Magic",
    brand: "Crunchwave",
    category: "chips_and_crisps",
    barcode: "8901234567890",
    image_url: null,
    identity_confidence: 88,
    nutriscore: "e",
    nova: 4,
    matched_by: ["ocr_brand", "ocr_category", "barcode", "openfoodfacts"],
  },
  nutrition: {
    nutrition_detected: true,
    calories: 538,
    protein: 6.8,
    fat: 31.5,
    saturated_fat: 14.8,
    sugar: 7.4,
    sodium: 712,
    carbohydrates: 56.2,
    fiber: 2.1,
  },
  scan_quality: {
    coverage_score: 90,
    completeness_score: 85,
    image_quality_score: 78,
    scan_quality_score: 83,
    scan_reliability_score: 91,
  },
  recommendation: {
    recommendation: "AVOID",
    reason: "Ultra-processed with very high saturated fat and sodium",
    best_for: [],
  },
  badges: ["ULTRA_PROCESSED", "HIDDEN_SUGAR"],
  positives: [{ title: "Some Protein", value: "6.8g", reason: "Protein detected in nutrition facts" }],
  negatives: [
    { title: "Palm Oil", reason: "Detected refined palm oil", severity: "MEDIUM" },
    { title: "Flavour Enhancer (MSG family)", reason: "Detected INS 627 / 631", severity: "MEDIUM" },
    { title: "Synthetic Antioxidant", reason: "Detected INS 319 (TBHQ)", severity: "MEDIUM" },
  ],
  allergens: [
    { allergen: "Wheat (Gluten)", severity: "HIGH" },
    { allergen: "Milk", severity: "HIGH" },
    { allergen: "Soy", severity: "HIGH" },
  ],
  risks: {
    risks: ["High Saturated Fat", "High Sodium Profile", "Hidden Sugar", "Ultra Processed"],
    overall_risk: "HIGH",
    hidden_sugars: ["maltodextrin"],
  },
  trust: { trust_score: 86, source_reliability: 95, evidence_strength: 90, data_confidence: 84 },
  verification: {
    barcode_verified: true,
    ocr_verified: true,
    source_verified: true,
    verification_level: "HIGH",
  },
  trust_intelligence: {
    overall_trust_score: 64,
    overall_trust_level: "MEDIUM",
    is_fssai_valid: true,
    authenticity_score: 81,
    authenticity_grade: "B",
    brand_trust_score: 58,
    adulteration_detected: false,
    adulteration_risk_level: "low",
    counterfeit_risk_level: "low",
    warnings: [
      "Front-of-pack claim “No Added MSG” contradicts flavour enhancers INS 627 & 631 in the ingredient list.",
      "“Baked Goodness” claim is unverified; refined palm oil is the first ingredient.",
    ],
    recommendations: [
      "Treat 'No Added MSG' as misleading — 627/631 act on the same taste pathway.",
      "FSSAI licence verified and valid; manufacturer is registered.",
    ],
    contradictions: [{}, {}],
    label_anomalies: [],
  },
  ingredients: {
    ingredient_count: 14,
    additive_count: 6,
    preservative_count: 1,
    artificial_count: 3,
    ingredients: [
      "Refined Palm Oil",
      "Potato",
      "Rice Flour",
      "Corn Flour",
      "Iodised Salt",
      "Sugar",
      "Spices & Condiments",
      "Maltodextrin",
      "Acidity Regulator (330)",
      "Flavour Enhancer (627)",
      "Flavour Enhancer (631)",
      "Anticaking Agent (551)",
      "Antioxidant (319)",
      "Added Flavours",
    ],
    e_numbers: ["E330", "E627", "E631", "E551", "E319"],
  },
  smart_swaps: {
    current_health_score: 34,
    current_nova_group: 4,
    current_processing_level: "ULTRA_PROCESSED",
    recommendation: "A roasted, lower-sodium snack cuts saturated fat by more than half.",
    ai_reasoning:
      "All three alternatives drop the palm-oil saturated fat and the MSG-family enhancers while keeping the savoury masala profile you're after.",
    comparison_summary: { sugar: "+44%", sodium: "+38%", saturated_fat: "+61%", protein: "+12%" },
    top_swaps: [
      { name: "Roasted Masala Chana", brand: "Tasty Nibbles", overall_score: 78, nova_group: 2, sugar: 1.2, protein: 19, sodium: 410, why_better: ["No palm oil", "3× the protein", "Half the sodium"] },
      { name: "Baked Multigrain Chips", brand: "Greenleaf", overall_score: 66, nova_group: 3, sugar: 2.0, protein: 9, sodium: 480, why_better: ["No MSG-family enhancers", "Lower saturated fat"] },
      { name: "Air-popped Jowar Puffs", brand: "Millet Co", overall_score: 71, nova_group: 2, sugar: 0.8, protein: 8, sodium: 360, why_better: ["Whole grain", "Lowest sodium"] },
    ],
  },
  metabolic_intelligence: {
    verdict: { overall: { score: 38, label: "POOR" } },
    metabolic: { glycemic_load: { value: 18, band: "HIGH" }, insulin_load: { band: "ELEVATED" } },
  },
  consumer_intelligence: {
    summary: {
      consumer_score: 41,
      fssai_score: 88,
      consumer_safety_index: 52,
      deception_score: 63,
      overall_alert: "CAUTION",
      buy_recommendation: "THINK_TWICE",
    },
    compliance: { is_compliant: true, fssai_license: "10012021000123" },
  },
  digital_twin: {
    overall_digital_twin_score: 46,
    overall_verdict: "HIGH_RISK",
    organ_impact: {
      organ_health_score: 46,
      liver_impact_score: 52,
      heart_impact_score: 38,
      pancreas_impact_score: 49,
      kidney_impact_score: 55,
    },
  },
  food_explainer: {
    success: true,
    summary: {
      scientific_consensus: "STRONG",
      evidence_strength: "HIGH",
      final_verdict: {
        verdict:
          "This is a treat food, not an everyday snack. The combination of refined palm oil and 712mg sodium per 100g pushes it into the 'occasional, small portion' bracket. The 'No Added MSG' line is technically true but practically misleading — INS 627 and 631 are MSG's chemical cousins.",
      },
    },
  },
  nutritionist: {
    success: true,
    answer:
      "If you enjoy this, keep the portion to about half a pack and pair it with something fresh — a cucumber-tomato side blunts the sodium spike. On most days, the roasted chana swap below gives you the same crunch with triple the protein and none of the palm oil.",
  },
  claims: {
    claims_detected: ["no added msg", "baked", "real masala"],
    claim_details: [],
  },
  ocr: { extracted_text: "", average_confidence: 0.84, ocr_quality_score: 84 },
};
