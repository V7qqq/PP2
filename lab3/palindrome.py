def palindrome(a):
    palindrome1 = True
    for i in range(len(a)):
        if a[i] != a[-i-1]:
            palindrome1 = False
        
    
    if palindrome1:
        print("yes")
    else:
        print('no')


