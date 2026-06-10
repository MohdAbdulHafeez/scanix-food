/* Shapes returned by POST /api/v1/scan. Fields are optional and the UI
   reads them defensively — the backend evolves and not every scan
   populates every System. */

export interface ScanProduct {
  product_name?: string | null;
  brand?: string | null;
  category?: string | null;
  barcode?: string | null;
  image_url?: string | null;
  identity_confidence?: number;
  nutriscore?: string | null;
  nova?: number | null;
  matched_by?: string[];
}

export interface Nutrition {
  nutrition_detected?: boolean;
  calories?: number;
  protein?: number;
  fat?: number;
  saturated_fat?: number;
  sugar?: number;
  sodium?: number;
  carbohydrates?: number;
  fiber?: number;
  [k: string]: unknown;
}

export interface Recommendation {
  recommendation?: string; // DAILY | OCCASIONAL | AVOID
  reason?: string;
  best_for?: string[];
}

export interface TrustIntelligence {
  overall_trust_score?: number;
  overall_trust_level?: string;
  is_fssai_valid?: boolean;
  authenticity_score?: number;
  authenticity_grade?: string;
  brand_trust_score?: number;
  adulteration_detected?: boolean;
  adulteration_risk_level?: string;
  counterfeit_risk_level?: string;
  warnings?: string[];
  recommendations?: string[];
  contradictions?: unknown[];
  label_anomalies?: unknown[];
}

export interface SwapCandidate {
  name?: string;
  brand?: string | null;
  overall_score?: number;
  why_better?: string[];
  nova_group?: number;
  sugar?: number | null;
  protein?: number | null;
  sodium?: number | null;
}

export interface SmartSwaps {
  current_health_score?: number;
  current_nova_group?: number;
  current_processing_level?: string;
  recommendation?: string | null;
  ai_reasoning?: string | null;
  top_swaps?: SwapCandidate[];
  comparison_summary?: Record<string, string>;
}

export interface ScanResult {
  success?: boolean;
  metadata?: {
    scan_id?: string;
    timestamp?: string;
    processing_time_ms?: number;
    audit_trail?: { ocr_raw?: string; ocr_corrected?: string };
  };
  product?: ScanProduct;
  nutrition?: Nutrition;
  scan_quality?: {
    coverage_score?: number;
    completeness_score?: number;
    image_quality_score?: number;
    scan_quality_score?: number;
    scan_reliability_score?: number;
  };
  recommendation?: Recommendation;
  badges?: string[];
  positives?: { title?: string; value?: string; reason?: string }[];
  negatives?: { title?: string; reason?: string; severity?: string }[];
  allergens?: { allergen?: string; severity?: string }[];
  risks?: { risks?: string[]; overall_risk?: string; hidden_sugars?: string[] };
  trust?: {
    trust_score?: number;
    source_reliability?: number;
    evidence_strength?: number;
    data_confidence?: number;
  };
  verification?: {
    barcode_verified?: boolean;
    ocr_verified?: boolean;
    source_verified?: boolean;
    verification_level?: string;
  };
  trust_intelligence?: TrustIntelligence;
  ingredients?: {
    ingredient_count?: number;
    additive_count?: number;
    preservative_count?: number;
    artificial_count?: number;
    ingredients?: string[];
    e_numbers?: string[];
    [k: string]: unknown;
  };
  smart_swaps?: SmartSwaps;
  metabolic_intelligence?: Record<string, any>;
  consumer_intelligence?: Record<string, any>;
  digital_twin?: Record<string, any>;
  food_explainer?: Record<string, any>;
  nutritionist?: Record<string, any>;
  claims?: { claims_detected?: string[]; claim_details?: unknown[] };
  ocr?: {
    extracted_text?: string;
    average_confidence?: number;
    ocr_quality_score?: number;
  };
  [k: string]: unknown;
}
