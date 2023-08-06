from testingpackageuploadingtobydrama import say_hello

def test_helloworld_no_params():
    assert say_hello() == "hello, World!"

def test_helloworld_with_param():
    assert say_hello("everyone") == "Hello, everyone!"
