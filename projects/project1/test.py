def my_function(a: int, b: int) -> int:
    """
    Input arg:
      a: int
      b: int
    Return:
      c: int
    """
    c = a+b

    return c


var1 = int(input("Enter integer:"))
var2 = int(input("Enter integer":))
var3 = my_function(var1, var2)
print("answer is", var3)