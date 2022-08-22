def f(x):
    if x<2 :
        y=-1
    if x>=2 :
        y=3
    return y
def g(x):
    if x==0:
        y=2
    else:
        if x<3:
            y=2*x/3
            #print("y at line 13 =", y)
        else:
            if x==4:
                y='constant g4'
            else:
                y='whatever'
    return y    

def main():
    x=input("Enter your x:")
    print("x=",x)
    y=f(float(x))
    print("y  =", y)
    y=g(float(y)+1)
    print("g(f(x)+1)=", y)
 
				
if __name__ == "__main__":
    main()