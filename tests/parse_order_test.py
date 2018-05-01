import sys
sys.path.append('../')
from dance import *

def test_parse_order_info():
    order, before, after = parse_order_info(" 42 ")
    assert order == '42' and before == None and after == None

    order, before, after = parse_order_info("42")
    assert order == '42' and before == None and after == None

    order, before, after = parse_order_info(">42 ")
    assert order == None and before == None and after == '42'
    
    order, before, after = parse_order_info("<42")
    assert order == None and before == '42' and after == None
    
    order, before, after = parse_order_info(">5 and <42 ")
    assert order == None and before == '42' and after == '5'
    
    order, before, after = parse_order_info("<42 and >5")
    assert order == None and before == '42' and after == '5'

    
    order, before, after = parse_order_info(" 7 ")
    assert order == '7' and before == None and after == None
    
    order, before, after = parse_order_info(" 7 ")
    assert order == '7' and before == None and after == None
    
    order, before, after = parse_order_info(" 7 ")
    assert order == '7' and before == None and after == None
