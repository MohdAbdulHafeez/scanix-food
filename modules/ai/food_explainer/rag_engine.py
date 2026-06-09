from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from typing import Dict
from typing import List
from typing import Optional
from typing import Any
from datetime import datetime


# =========================================================
# SOURCE TYPES
# =========================================================

class SourceType(
    str,
    Enum,
):

    PUBMED = "PUBMED"

    WHO = "WHO"

    FDA = "FDA"

    NIH = "NIH"

    USDA = "USDA"

    EFSA = "EFSA"

    OPENFOODFACTS = (
        "OPENFOODFACTS"
    )

    CROSSREF = "CROSSREF"

    WEB = "WEB"

    INTERNAL = "INTERNAL"


# =========================================================
# EVIDENCE STRENGTH
# =========================================================

class EvidenceStrength(
    str,
    Enum,
):

    LOW = "LOW"

    MODERATE = (
        "MODERATE"
    )

    HIGH = "HIGH"

    VERY_HIGH = (
        "VERY_HIGH"
    )


# =========================================================
# SCIENTIFIC CONSENSUS
# =========================================================

class ScientificConsensus(
    str,
    Enum,
):

    MOSTLY_POSITIVE = (
        "MOSTLY_POSITIVE"
    )

    MOSTLY_NEGATIVE = (
        "MOSTLY_NEGATIVE"
    )

    MIXED_EVIDENCE = (
        "MIXED_EVIDENCE"
    )

    INSUFFICIENT_EVIDENCE = (
        "INSUFFICIENT_EVIDENCE"
    )


# =========================================================
# EVIDENCE DOCUMENT
# =========================================================

@dataclass
class EvidenceDocument:

    source: SourceType

    title: str

    summary: str

    url: str

    source_score: float

    evidence_strength: (
        EvidenceStrength
    )

    publication_year: (
        Optional[int]
    ) = None

    authors: List[str] = (
        field(
            default_factory=list
        )
    )

    keywords: List[str] = (
        field(
            default_factory=list
        )
    )


# =========================================================
# CITATION
# =========================================================

@dataclass
class Citation:

    title: str

    source: str

    url: str

    year: Optional[int]


# =========================================================
# RESEARCH CONFIDENCE
# =========================================================

@dataclass
class ResearchConfidence:

    score: float

    level: str

    studies_found: int

    source_diversity: int


# =========================================================
# RETRIEVAL RESULT
# =========================================================

@dataclass
class RetrievalResult:

    evidence: List[
        EvidenceDocument
    ]

    citations: List[
        Citation
    ]

    consensus: (
        ScientificConsensus
    )

    confidence: (
        ResearchConfidence
    )

    contradictions: (
        List[str]
    )


# =========================================================
# SOURCE WEIGHTS
# =========================================================

SOURCE_WEIGHTS = {

    SourceType.PUBMED:
    1.00,

    SourceType.WHO:
    1.00,

    SourceType.FDA:
    1.00,

    SourceType.NIH:
    0.95,

    SourceType.USDA:
    0.90,

    SourceType.EFSA:
    0.90,

    SourceType.OPENFOODFACTS:
    0.75,

    SourceType.CROSSREF:
    0.85,

    SourceType.WEB:
    0.60,

    SourceType.INTERNAL:
    0.95,
}


# =========================================================
# EVIDENCE RANKER
# =========================================================

class EvidenceRanker:

    def rank(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> List[
        EvidenceDocument
    ]:

        def score(

            doc: EvidenceDocument,

        ) -> float:

            source_weight = (

                SOURCE_WEIGHTS.get(
                    doc.source,
                    0.50,
                )

            )

            strength_bonus = {

                EvidenceStrength.LOW:
                0.25,

                EvidenceStrength.MODERATE:
                0.50,

                EvidenceStrength.HIGH:
                0.75,

                EvidenceStrength.VERY_HIGH:
                1.00,

            }.get(

                doc.evidence_strength,
                0.25,
            )

            recency_bonus = 0.0

            if doc.publication_year:

                age = max(

                    0,

                    datetime.now().year
                    -
                    doc.publication_year,

                )

                recency_bonus = max(

                    0,

                    (
                        20 - age
                    )

                    /

                    20,

                )

            return (

                source_weight

                * 0.60

                +

                strength_bonus

                * 0.25

                +

                recency_bonus

                * 0.15

            )

        return sorted(

            evidence,

            key=score,

            reverse=True,

        )


# =========================================================
# CITATION ENGINE
# =========================================================

class CitationEngine:

    def build(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> List[
        Citation
    ]:

        citations = []

        seen = set()

        for doc in evidence:

            key = (

                doc.title,
                doc.url,
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            citations.append(

                Citation(

                    title=
                    doc.title,

                    source=
                    doc.source.value,

                    url=
                    doc.url,

                    year=
                    doc.publication_year,

                )

            )

        return citations


# =========================================================
# RESEARCH CONFIDENCE ENGINE
# =========================================================

class ResearchConfidenceEngine:

    def calculate(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> ResearchConfidence:

        if not evidence:

            return (

                ResearchConfidence(

                    score=0,

                    level="LOW",

                    studies_found=0,

                    source_diversity=0,

                )

            )

        source_diversity = len(

            set(

                doc.source

                for doc

                in evidence

            )

        )

        total_weight = 0.0

        for doc in evidence:

            total_weight += (

                SOURCE_WEIGHTS.get(

                    doc.source,

                    0.5,

                )

            )

        score = min(

            100,

            round(

                (

                    total_weight

                    /

                    len(
                        evidence
                    )

                )

                * 100,

                2,

            )

        )

        if score >= 85:

            level = (
                "VERY_HIGH"
            )

        elif score >= 70:

            level = (
                "HIGH"
            )

        elif score >= 50:

            level = (
                "MODERATE"
            )

        else:

            level = (
                "LOW"
            )

        return (

            ResearchConfidence(

                score=score,

                level=level,

                studies_found=
                len(
                    evidence
                ),

                source_diversity=
                source_diversity,

            )

        )


# =========================================================
# TRUST ENGINE
# =========================================================

class TrustEngine:

    def calculate(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> Dict[
        str,
        Any,
    ]:

        if not evidence:

            return {

                "trust_score":
                0,

                "tier1_sources":
                0,

                "tier2_sources":
                0,

                "tier3_sources":
                0,

            }

        tier1 = {

            SourceType.PUBMED,

            SourceType.WHO,

            SourceType.FDA,

            SourceType.NIH,

        }

        tier2 = {

            SourceType.USDA,

            SourceType.EFSA,

            SourceType.OPENFOODFACTS,

        }

        tier1_count = 0

        tier2_count = 0

        tier3_count = 0

        trust_score = 0.0

        for doc in evidence:

            source = doc.source

            trust_score += (

                SOURCE_WEIGHTS.get(
                    source,
                    0.5,
                )

            )

            if source in tier1:

                tier1_count += 1

            elif source in tier2:

                tier2_count += 1

            else:

                tier3_count += 1

        trust_score = round(

            min(

                100,

                (

                    trust_score

                    /

                    len(
                        evidence
                    )

                )

                * 100,

            ),

            2,

        )

        return {

            "trust_score":
            trust_score,

            "tier1_sources":
            tier1_count,

            "tier2_sources":
            tier2_count,

            "tier3_sources":
            tier3_count,

        }


# =========================================================
# CONTRADICTION DETECTOR
# =========================================================

class ContradictionDetector:

    POSITIVE = {

        "beneficial",

        "protective",

        "safe",

        "recommended",

        "supports",

        "improves",

    }

    NEGATIVE = {

        "harmful",

        "risk",

        "unsafe",

        "concern",

        "adverse",

        "increases",

    }

    def detect(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> List[
        str
    ]:

        contradictions = []

        positive_hits = 0

        negative_hits = 0

        for doc in evidence:

            text = (

                doc.summary
                .lower()
            )

            if any(

                word in text

                for word

                in self.POSITIVE

            ):

                positive_hits += 1

            if any(

                word in text

                for word

                in self.NEGATIVE

            ):

                negative_hits += 1

        if (

            positive_hits > 0

            and

            negative_hits > 0

        ):

            contradictions.append(

                "Evidence contains both positive and negative findings."

            )

        return contradictions


# =========================================================
# CONSENSUS ENGINE
# =========================================================

class ConsensusEngine:

    POSITIVE_TERMS = {

        "beneficial",
        "protective",
        "supports",
        "recommended",
        "safe",
        "improves",
        "healthy",
        "favorable",

    }

    NEGATIVE_TERMS = {

        "harmful",
        "risk",
        "unsafe",
        "concern",
        "adverse",
        "increases",
        "dangerous",
        "negative",

    }

    def determine(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> ScientificConsensus:

        if not evidence:

            return (

                ScientificConsensus
                .INSUFFICIENT_EVIDENCE

            )

        positive_score = 0

        negative_score = 0

        for doc in evidence:

            text = (

                f"{doc.title} "
                f"{doc.summary}"

            ).lower()

            source_weight = (

                SOURCE_WEIGHTS.get(

                    doc.source,

                    0.5,

                )

            )

            for term in self.POSITIVE_TERMS:

                if term in text:

                    positive_score += (
                        source_weight
                    )

            for term in self.NEGATIVE_TERMS:

                if term in text:

                    negative_score += (
                        source_weight
                    )

        total = (

            positive_score

            +

            negative_score

        )

        if total == 0:

            return (

                ScientificConsensus
                .INSUFFICIENT_EVIDENCE

            )

        positive_ratio = (

            positive_score
            /
            total

        )

        if positive_ratio >= 0.70:

            return (

                ScientificConsensus
                .MOSTLY_POSITIVE

            )

        if positive_ratio <= 0.30:

            return (

                ScientificConsensus
                .MOSTLY_NEGATIVE

            )

        return (

            ScientificConsensus
            .MIXED_EVIDENCE

        )


# =========================================================
# INTERNAL KNOWLEDGE RETRIEVER
# =========================================================

class InternalKnowledgeRetriever:

    """
    Retrieves evidence from:

    System 2
    Ingredient Intelligence

    System 3
    Metabolic Intelligence

    System 4
    Consumer Intelligence
    """

    def retrieve(

        self,

        ingredient_intelligence: Dict[
            str,
            Any,
        ],

        metabolic_intelligence: Dict[
            str,
            Any,
        ],

        consumer_intelligence: Dict[
            str,
            Any,
        ],

    ) -> List[
        EvidenceDocument
    ]:

        evidence = []

        evidence.extend(

            self._ingredient_evidence(

                ingredient_intelligence

            )

        )

        evidence.extend(

            self._metabolic_evidence(

                metabolic_intelligence

            )

        )

        evidence.extend(

            self._consumer_evidence(

                consumer_intelligence

            )

        )

        return evidence

    # ============================================
    # INGREDIENT EVIDENCE
    # ============================================

    def _ingredient_evidence(

        self,

        ingredient_intelligence: Dict[
            str,
            Any,
        ],

    ) -> List[
        EvidenceDocument
    ]:

        evidence = []

        ingredient_risks = (

            ingredient_intelligence
            .get(
                "ingredient_risks",
                {},
            )
            .get(
                "ingredient_risks",
                [],
            )

        )

        for item in ingredient_risks:

            evidence.append(

                EvidenceDocument(

                    source=
                    SourceType.INTERNAL,

                    title=
                    item.get(
                        "name",
                        "Ingredient",
                    ),

                    summary=
                    item.get(
                        "explanation",
                        "",
                    ),

                    url=
                    "internal://ingredient-risk",

                    source_score=
                    item.get(
                        "risk_score",
                        50,
                    ),

                    evidence_strength=
                    EvidenceStrength.MODERATE,

                    keywords=
                    item.get(
                        "risk_domains",
                        [],
                    ),

                )

            )

        return evidence

    # ============================================
    # METABOLIC EVIDENCE
    # ============================================

    def _metabolic_evidence(

        self,

        metabolic_intelligence: Dict[
            str,
            Any,
        ],

    ) -> List[
        EvidenceDocument
    ]:

        evidence = []

        metabolic = (

            metabolic_intelligence
            .get(
                "metabolic",
                {},
            )

        )

        glycemic = (

            metabolic
            .get(
                "glycemic_load",
                {},
            )

        )

        evidence.append(

            EvidenceDocument(

                source=
                SourceType.INTERNAL,

                title=
                "Glycemic Impact",

                summary=
                f"Glycemic load score: "
                f"{glycemic.get('score', 0)}",

                url=
                "internal://glycemic",

                source_score=
                glycemic.get(
                    "score",
                    0,
                ),

                evidence_strength=
                EvidenceStrength.HIGH,

            )

        )

        return evidence

    # ============================================
    # CONSUMER EVIDENCE
    # ============================================

    def _consumer_evidence(

        self,

        consumer_intelligence: Dict[
            str,
            Any,
        ],

    ) -> List[
        EvidenceDocument
    ]:

        evidence = []

        consumer = (

            consumer_intelligence
            .get(
                "consumer",
                {},
            )

        )

        evidence.append(

            EvidenceDocument(

                source=
                SourceType.INTERNAL,

                title=
                "Consumer Analysis",

                summary=
                consumer.get(

                    "consumer_category",

                    "UNKNOWN",

                ),

                url=
                "internal://consumer",

                source_score=
                consumer.get(

                    "consumer_score",

                    50,

                ),

                evidence_strength=
                EvidenceStrength.MODERATE,

            )

        )

        return evidence


# =========================================================
# SOURCE DIVERSITY ENGINE
# =========================================================

class SourceDiversityEngine:

    def analyze(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> Dict[
        str,
        Any,
    ]:

        distribution = {}

        for doc in evidence:

            source = (
                doc.source.value
            )

            distribution[source] = (

                distribution.get(
                    source,
                    0,
                )

                + 1

            )

        return {

            "total_sources":
            len(
                distribution
            ),

            "distribution":
            distribution,

            "source_diversity_score":
            min(

                100,

                len(
                    distribution
                )

                * 10,

            ),

        }


# =========================================================
# BASE RETRIEVER
# =========================================================

class BaseRetriever:

    source_type: SourceType

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        raise NotImplementedError


# =========================================================
# PUBMED RETRIEVER
# =========================================================

class PubMedRetriever(
    BaseRetriever
):

    source_type = (
        SourceType.PUBMED
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# WHO RETRIEVER
# =========================================================

class WHORetriever(
    BaseRetriever
):

    source_type = (
        SourceType.WHO
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# FDA RETRIEVER
# =========================================================

class FDARetriever(
    BaseRetriever
):

    source_type = (
        SourceType.FDA
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# NIH RETRIEVER
# =========================================================

class NIHRetriever(
    BaseRetriever
):

    source_type = (
        SourceType.NIH
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# USDA RETRIEVER
# =========================================================

class USDARetriever(
    BaseRetriever
):

    source_type = (
        SourceType.USDA
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# EFSA RETRIEVER
# =========================================================

class EFSARetriever(
    BaseRetriever
):

    source_type = (
        SourceType.EFSA
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# OPEN FOOD FACTS
# =========================================================

class OpenFoodFactsRetriever(
    BaseRetriever
):

    source_type = (
        SourceType.OPENFOODFACTS
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# TAVILY RETRIEVER
# =========================================================

class TavilyRetriever(
    BaseRetriever
):

    source_type = (
        SourceType.WEB
    )

    def retrieve(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        return []


# =========================================================
# EVIDENCE DEDUPLICATION ENGINE
# =========================================================

class EvidenceDeduplicationEngine:

    def deduplicate(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> List[
        EvidenceDocument
    ]:

        unique = {}

        for doc in evidence:

            key = (

                doc.title
                .strip()
                .lower(),

                doc.source.value,

            )

            existing = (
                unique.get(key)
            )

            if not existing:

                unique[key] = doc

                continue

            if (

                doc.source_score
                >
                existing.source_score

            ):

                unique[key] = doc

        return list(
            unique.values()
        )


# =========================================================
# RESEARCH COVERAGE ANALYZER
# =========================================================

class ResearchCoverageAnalyzer:

    def analyze(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> Dict[
        str,
        Any,
    ]:

        total = len(
            evidence
        )

        if total == 0:

            return {

                "coverage":
                "LOW",

                "study_count":
                0,

            }

        if total >= 25:

            coverage = (
                "EXCELLENT"
            )

        elif total >= 15:

            coverage = (
                "GOOD"
            )

        elif total >= 5:

            coverage = (
                "MODERATE"
            )

        else:

            coverage = (
                "LOW"
            )

        return {

            "coverage":
            coverage,

            "study_count":
            total,

        }


# =========================================================
# EVIDENCE QUALITY ENGINE
# =========================================================

class EvidenceQualityEngine:

    def analyze(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> Dict[str, Any]:

        if not evidence:

            return {

                "quality_score": 0,

                "quality_level":
                "LOW",

            }

        score = 0.0

        for doc in evidence:

            source_weight = (

                SOURCE_WEIGHTS.get(
                    doc.source,
                    0.5,
                )

            )

            strength_weight = {

                EvidenceStrength.LOW:
                0.25,

                EvidenceStrength.MODERATE:
                0.50,

                EvidenceStrength.HIGH:
                0.75,

                EvidenceStrength.VERY_HIGH:
                1.00,

            }.get(

                doc.evidence_strength,

                0.25,

            )

            score += (

                source_weight
                *
                strength_weight

            )

        quality_score = round(

            min(

                100,

                (

                    score

                    /

                    len(
                        evidence
                    )

                )

                * 100,

            ),

            2,

        )

        if quality_score >= 85:

            level = (
                "VERY_HIGH"
            )

        elif quality_score >= 70:

            level = (
                "HIGH"
            )

        elif quality_score >= 50:

            level = (
                "MODERATE"
            )

        else:

            level = (
                "LOW"
            )

        return {

            "quality_score":
            quality_score,

            "quality_level":
            level,

        }


# =========================================================
# SOURCE FRESHNESS ENGINE
# =========================================================

class SourceFreshnessEngine:

    CURRENT_YEAR = (
        datetime.now().year
    )

    def analyze(

        self,

        evidence: List[
            EvidenceDocument
        ],

    ) -> Dict[str, Any]:

        years = [

            doc.publication_year

            for doc in evidence

            if doc.publication_year

        ]

        if not years:

            return {

                "freshness_score":
                50,

                "average_age":
                None,

            }

        avg_age = round(

            sum(

                self.CURRENT_YEAR
                -
                year

                for year

                in years

            )

            /

            len(years),

            2,

        )

        freshness_score = max(

            0,

            min(

                100,

                100
                -
                (
                    avg_age
                    * 4
                ),

            ),

        )

        return {

            "freshness_score":
            round(
                freshness_score,
                2,
            ),

            "average_age":
            avg_age,

        }


# =========================================================
# RESEARCH GAP ENGINE
# =========================================================

class ResearchGapEngine:

    def analyze(

        self,

        evidence: List[
            EvidenceDocument
        ],

        contradictions:
        List[str],

    ) -> Dict[str, Any]:

        gaps = []

        if len(
            evidence
        ) < 5:

            gaps.append(

                "LIMITED_RESEARCH_VOLUME"

            )

        if contradictions:

            gaps.append(

                "CONFLICTING_EVIDENCE"

            )

        return {

            "gap_count":
            len(
                gaps
            ),

            "research_gaps":
            gaps,

        }


# =========================================================
# FOOD RAG ENGINE
# =========================================================

class FoodRAGEngine:

    def __init__(self):

        self.ranker = (
            EvidenceRanker()
        )

        self.citation_engine = (
            CitationEngine()
        )

        self.trust_engine = (
            TrustEngine()
        )

        self.consensus_engine = (
            ConsensusEngine()
        )

        self.confidence_engine = (
            ResearchConfidenceEngine()
        )

        self.contradiction_detector = (
            ContradictionDetector()
        )

        self.internal_retriever = (
            InternalKnowledgeRetriever()
        )

        self.diversity_engine = (
            SourceDiversityEngine()
        )

        self.dedup_engine = (
            EvidenceDeduplicationEngine()
        )

        self.coverage_analyzer = (
            ResearchCoverageAnalyzer()
        )

        self.quality_engine = (
            EvidenceQualityEngine()
        )

        self.freshness_engine = (
            SourceFreshnessEngine()
        )

        self.research_gap_engine = (
            ResearchGapEngine()
        )

        self.retrievers = [

            PubMedRetriever(),

            WHORetriever(),

            FDARetriever(),

            NIHRetriever(),

            USDARetriever(),

            EFSARetriever(),

            OpenFoodFactsRetriever(),

            TavilyRetriever(),

        ]

    # =====================================================
    # BUILD QUERY
    # =====================================================

    def _build_query(

        self,

        product_name: str,

        ingredients: List[
            str
        ],

    ) -> str:

        ingredient_text = (
            ", ".join(
                ingredients[:10]
            )
        )

        return (

            f"{product_name} "

            f"{ingredient_text} "

            f"nutrition health effects"

        )

    # =====================================================
    # EXTERNAL RETRIEVAL
    # =====================================================

    def _retrieve_external(

        self,

        query: str,

    ) -> List[
        EvidenceDocument
    ]:

        evidence = []

        for retriever in (

            self.retrievers

        ):

            try:

                results = (

                    retriever.retrieve(
                        query
                    )
                )

                evidence.extend(
                    results
                )

            except Exception:

                continue

        return evidence

    # =====================================================
    # MASTER ANALYSIS
    # =====================================================

    def analyze(

        self,

        product_name: str,

        ingredient_intelligence:
        Dict[str, Any],

        metabolic_intelligence:
        Dict[str, Any],

        consumer_intelligence:
        Dict[str, Any],

    ) -> Dict[
        str,
        Any,
    ]:

        ingredients = [

            item.get(
                "name",
                "",
            )

            for item in

            ingredient_intelligence.get(
                "ingredients",
                [],
            )

        ]

        query = (

            self._build_query(

                product_name=
                product_name,

                ingredients=
                ingredients,

            )

        )

        internal_evidence = (

            self.internal_retriever
            .retrieve(

                ingredient_intelligence=
                ingredient_intelligence,

                metabolic_intelligence=
                metabolic_intelligence,

                consumer_intelligence=
                consumer_intelligence,

            )

        )

        external_evidence = (

            self._retrieve_external(
                query
            )

        )

        evidence = (

            internal_evidence

            +

            external_evidence

        )

        evidence = (

            self.dedup_engine
            .deduplicate(
                evidence
            )

        )

        ranked_evidence = (

            self.ranker.rank(
                evidence
            )
        )

        citations = (

            self.citation_engine
            .build(
                ranked_evidence
            )
        )

        confidence = (

            self.confidence_engine
            .calculate(
                ranked_evidence
            )
        )

        consensus = (

            self.consensus_engine
            .determine(
                ranked_evidence
            )
        )

        contradictions = (

            self.contradiction_detector
            .detect(
                ranked_evidence
            )
        )

        trust = (

            self.trust_engine
            .calculate(
                ranked_evidence
            )
        )

        diversity = (

            self.diversity_engine
            .analyze(
                ranked_evidence
            )
        )
        

        coverage = (

            self.coverage_analyzer
            .analyze(
                ranked_evidence
            )

        )

        quality = (
            self.quality_engine
            .analyze(
                ranked_evidence
            )
        )

        freshness = (
            self.freshness_engine
            .analyze(
                ranked_evidence
            )
        )

        research_gaps = (
            self.research_gap_engine
            .analyze(
                ranked_evidence,
                contradictions,
            )
        )

        return {
            "query": query,
            "evidence": ranked_evidence,
            "citations": citations,
            "research_confidence": confidence,
            "scientific_consensus": consensus,
            "trust": trust,
            "source_diversity": diversity,
            "contradictions": contradictions,
            "research_coverage": coverage,
            "evidence_quality":quality,
            "source_freshness":freshness,
            "research_gaps":research_gaps,
        }


food_rag_engine = (
    FoodRAGEngine()
)