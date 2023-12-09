def removeStars(string_with_stars):
  stack = []
  for letter in string_with_stars:
    if letter == '*' and len(stack) > 0:
      stack.pop()
    elif letter != '*':
      stack.append(letter)
      
  return ''.join(stack)

print(removeStars('leet**cod*e'))
print(removeStars('erase*****'))
print(removeStars('*****erase*'))
print(removeStars('*****e*rase*'))
print(removeStars('*****e*ras*e*'))
  