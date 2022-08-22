fruits = {"apple", "banana", "cherry"}
more_fruits = ["orange", "mango", "grapes"]
fruits.update(more_fruits)
print(fruits)

car =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print("car brand is " +car.get("brand"))
car["brand"]="Toyota"
print("car brand is changed to " +car.get("brand"))

#Add the key/value pair "color" : "red" to the car dictionary.
car["color"]="red"
print("set car color to " +car.get("color"))

#Use the pop method to remove "model" from the car dictionary.
print("car model is " +car.get("model"))
car.pop("model")
# print("car model is " +car.get("model"))  # this line has TypeError: can only concatenate str (not "NoneType") to str
car.clear()  # to clear car dictionary


a = 50
b = 10
if a == b:
  print("1")
elif a > b:
  print("2")
else:
  print("3")
  
i = 1
while i < 6:
  print(i)
  i += 1

i = 1
while i < 6:
  if i == 3:
  	break
  i += 1

#Loop through the items in the fruits list.
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  
print('In the loop, when the item value is "banana", jump directly to the next item.')
fruits = ["apple", "banana", "cherry","orange","kiwi"]
for x in fruits:
	if x == "cherry":    # This one will be be printed out
		continue
	print(x)

print('Use the range function to loop through a code set 6 times.')
for x in range(6):
  print(x)



def my_function():
  print("Hello from a function")

#Create a lambda function that takes one parameter (a) and returns it.
x = lambda a:a
