from backend.ai_engine.kuramoto import MultiDomainKuramotoEngine

def test_aligned_is_coherent():
    e=MultiDomainKuramotoEngine()
    e.upsert("a",phase=0.0)
    e.upsert("b",phase=0.0)
    assert e.order_parameter()["coherence"] > .999

def test_opposed_is_incoherent():
    e=MultiDomainKuramotoEngine()
    e.upsert("a",phase=0.0)
    e.upsert("b",phase=3.141592653589793)
    assert e.order_parameter()["coherence"] < .001
