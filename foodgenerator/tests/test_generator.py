"""
Tests foodgenerator.generator
"""

from foodgenerator import generator


def test_generate_products():
    vals = [val for val in generator.generate_products(100)]

    assert vals
    single = vals[50]
    assert single.name
    assert single.category in ['FOOD', 'DRINK', 'OTHER']
    assert int(single.priceInCents)
